"""Del cuestionario estandarizado (``catalogos/cuestionario.toml``) a un presupuesto.

Quien entrevista hace las preguntas en orden, guarda las respuestas como JSON ``{id: valor}``
y ``presupuesto_desde_respuestas`` las convierte en un ``Presupuesto``:

- Los montos anuales (o los que vienen con ``{"monto": x, "cada": "bimestre"}``) se pasan a
  pesos al mes.
- Un monto que llena varios rubros (p. ej. "súper y mercado") se reparte entre ellos con los
  ponderadores oficiales del INPC llevados al mes del gasto.
- Las preguntas cuya condición ``si`` no se cumple no cuentan, aunque traigan respuesta.
- Una respuesta puede ser el texto de una opción de su ``escala`` ("$300 a $700"); se usa el
  valor que la escala le da. "No sé" en un aumento se omite.
- El mes del gasto es el último con datos: las respuestas describen un mes típico de hoy.
"""

from __future__ import annotations

import math
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from .datos import COLUMNA_GENERAL, DatosINPC
from .personal import NACIONAL, ErrorPresupuesto, Presupuesto, Rubro, gasto_oficial_por_rubro

CUESTIONARIO = Path(__file__).parent / "catalogos" / "cuestionario.toml"
TIPOS = ("ciudad", "opcion", "monto", "porcentaje")
MESES_POR = {"mes": 1, "bimestre": 2, "trimestre": 3, "semestre": 6, "año": 12}


@dataclass(frozen=True)
class Pregunta:
    id: str
    tipo: str
    texto: str
    cada: str = "mes"
    rubros: tuple[str, ...] = ()
    no_cubierto: str | None = None
    aumento_propio: str | None = None
    opciones: tuple[str, ...] = ()
    si: Mapping | None = None
    opcional: bool = False
    escala: str | None = None


@dataclass(frozen=True)
class Opcion:
    texto: str
    valor: float | None  # None: la respuesta se omite (p. ej. "No sé")


@dataclass(frozen=True)
class Cuestionario:
    version: int
    preguntas: tuple[Pregunta, ...] = field(default_factory=tuple)
    escalas: Mapping[str, tuple[Opcion, ...]] = field(default_factory=dict)

    def por_id(self) -> dict[str, Pregunta]:
        return {p.id: p for p in self.preguntas}


def cargar_cuestionario(ruta: Path = CUESTIONARIO) -> Cuestionario:
    datos = tomllib.loads(ruta.read_text(encoding="utf-8"))
    preguntas = []
    for cruda in datos["pregunta"]:
        cruda = dict(cruda)
        cruda["rubros"] = tuple(cruda.get("rubros", ()))
        cruda["opciones"] = tuple(o["valor"] for o in cruda.get("opciones", ()))
        preguntas.append(Pregunta(**cruda))
    escalas = {
        nombre: tuple(
            Opcion(o["texto"], None if o.get("omitir") else float(o["valor"])) for o in opciones
        )
        for nombre, opciones in datos.get("escalas", {}).items()
    }
    return Cuestionario(datos["version"], tuple(preguntas), escalas)


_OMITIDA = object()


def resolver(pregunta: Pregunta, valor: object, cuestionario: Cuestionario) -> object:
    """Traduce el texto de una opción de la escala a su valor; lo demás queda igual."""
    if isinstance(valor, str) and pregunta.escala:
        for opcion in cuestionario.escalas[pregunta.escala]:
            if opcion.texto == valor:
                return _OMITIDA if opcion.valor is None else opcion.valor
        textos = ", ".join(o.texto for o in cuestionario.escalas[pregunta.escala])
        raise ErrorPresupuesto(f"{pregunta.id}: {valor!r} no es una opción ({textos})")
    return valor


def aplica(pregunta: Pregunta, respuestas: Mapping[str, object]) -> bool:
    """Si la pregunta se hace, según su condición ``si`` y las respuestas anteriores."""
    if not pregunta.si:
        return True
    otra = respuestas.get(pregunta.si["pregunta"])
    if "es" in pregunta.si:
        return otra == pregunta.si["es"]
    return _monto_mensual(otra, "mes") > pregunta.si["mayor_que"] if otra is not None else False


def _monto_mensual(valor: object, cada: str) -> float:
    if isinstance(valor, Mapping):
        cada = str(valor.get("cada", cada))
        valor = valor.get("monto")
    if isinstance(valor, bool) or not isinstance(valor, int | float) or not math.isfinite(valor):
        raise ErrorPresupuesto(f"monto inválido: {valor!r}")
    if valor < 0:
        raise ErrorPresupuesto(f"monto negativo: {valor!r}")
    if cada not in MESES_POR:
        raise ErrorPresupuesto(f"frecuencia desconocida: {cada!r} (usa {', '.join(MESES_POR)})")
    return float(valor) / MESES_POR[cada]


def presupuesto_desde_respuestas(
    respuestas: Mapping[str, object],
    cuestionario: Cuestionario,
    rubros: Mapping[str, Rubro],
    nacional: DatosINPC,
    ciudades_validas: list[str] | None = None,
) -> Presupuesto:
    """Convierte las respuestas del cuestionario en un presupuesto listo para ``calcular``."""
    preguntas = cuestionario.por_id()
    desconocidas = sorted(set(respuestas) - set(preguntas))
    if desconocidas:
        raise ErrorPresupuesto(f"Respuestas a preguntas que no existen: {', '.join(desconocidas)}")

    periodo = max(p for p, v in nacional.mensual[COLUMNA_GENERAL].items() if v is not None)
    oficial = gasto_oficial_por_rubro(rubros, nacional, periodo)
    ciudad = NACIONAL
    gasto: dict[str, float] = {}
    aumento: dict[str, float] = {}
    no_cubierto: dict[str, float] = {}

    # En orden, y solo las que aplican según las anteriores: una respuesta guardada para una
    # pregunta que ya no aplica (p. ej. gasolina tras decir que no hay auto) no se valida.
    resueltas = {}
    for pregunta in cuestionario.preguntas:
        if pregunta.id in respuestas and aplica(pregunta, resueltas):
            valor = resolver(pregunta, respuestas[pregunta.id], cuestionario)
            if valor is not _OMITIDA:
                resueltas[pregunta.id] = valor

    for pregunta in cuestionario.preguntas:
        if pregunta.id not in resueltas or not aplica(pregunta, resueltas):
            continue
        valor = resueltas[pregunta.id]
        try:
            if pregunta.tipo == "ciudad":
                ciudad = str(valor)
                if ciudades_validas is not None and ciudad not in [*ciudades_validas, NACIONAL]:
                    raise ErrorPresupuesto(f"ciudad desconocida: {ciudad!r}")
            elif pregunta.tipo == "opcion":
                if valor not in pregunta.opciones:
                    raise ErrorPresupuesto(f"debe ser una de: {', '.join(pregunta.opciones)}")
            elif pregunta.tipo == "porcentaje":
                if valor is None:
                    continue
                if isinstance(valor, bool) or not isinstance(valor, int | float):
                    raise ErrorPresupuesto(f"debe ser un número, no {valor!r}")
                if not -99 <= valor <= 1000:
                    raise ErrorPresupuesto("debe estar entre -99 y 1000")
                aumento[pregunta.aumento_propio] = float(valor)
            else:
                mensual = _monto_mensual(valor, pregunta.cada)
                if pregunta.no_cubierto:
                    if mensual:
                        no_cubierto[pregunta.no_cubierto] = mensual
                    continue
                total = sum(oficial[r] for r in pregunta.rubros)
                for rubro in pregunta.rubros:
                    gasto[rubro] = gasto.get(rubro, 0.0) + mensual * oficial[rubro] / total
        except ErrorPresupuesto as error:
            raise ErrorPresupuesto(f"{pregunta.id}: {error}") from None

    gasto = {r: round(v, 2) for r, v in gasto.items() if v > 0}
    aumento = {r: a for r, a in aumento.items() if gasto.get(r)}
    if not gasto:
        raise ErrorPresupuesto("Las respuestas no traen ningún gasto mayor que cero")
    no_cubierto = {c: round(v, 2) for c, v in no_cubierto.items()}
    return Presupuesto(ciudad, periodo, "gasto_efectivo", gasto, aumento, no_cubierto)
