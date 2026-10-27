"""Tu inflación personal: tu presupuesto por rubros, convertido en un índice con los genéricos.

El presupuesto (TOML) dice cuánto gastas al mes en cada rubro de lenguaje común (súper, renta,
gasolina…). Cada rubro se reparte entre sus genéricos con los ponderadores oficiales llevados al
mes de tu gasto (nivel B del reporte: **imputado**), y con esos pesos se calcula tu índice:

``P(t) = 100 · Σ_k s_k · I_k(t) / I_k(e)``, con ``e`` el mes de tu gasto (``P(e) = 100``).

``I_k`` es el índice de tu ciudad para lo que tiene precio local y el nacional para lo que tiene
precio casi único (columna ``indice`` de ``catalogos/rubros.csv``), o cuando tu ciudad ya no
cotiza ese genérico. Reglas especiales:

- **Vivienda propia:** en modo ``gasto_efectivo`` (por omisión) no entra; en modo ``consumo``
  entra con la renta que estimas que pagarías. La hipoteca nunca va aquí: el pago de deuda no
  está en el INPC; va en ``no_cubierto``.
- **Aumento propio:** para un rubro puedes poner el aumento anual que tú viste (tu renta, tu
  colegiatura) y se usa en lugar de los índices del INEGI.
- **No cubierto:** lo que el INPC no mide (seguro de gastos médicos, intereses, impuestos) se
  reporta aparte y no mueve el índice.
"""

from __future__ import annotations

import csv
import difflib
import textwrap
import tomllib
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from .ciudades import DatosCiudades
from .datos import COLUMNA_GENERAL, DatosINPC
from .indices import Serie, incidencias, indice_ponderado, valores_en, variacion
from .periodos import Periodo
from .reconstruccion import BASE_PONDERADORES

CATALOGO = Path(__file__).parent / "catalogos" / "rubros.csv"
NACIONAL = "nacional"
MODOS_VIVIENDA = ("gasto_efectivo", "consumo")
RUBRO_VIVIENDA_PROPIA = "vivienda_propia"
# Desde ago-2024 rige la canasta 2024: antes no existen 16 de sus genéricos.
PRIMER_MES_GASTO = Periodo(2024, 8)
CLAVES_PRESUPUESTO = {
    "ciudad",
    "periodo_gasto",
    "vivienda_propia",
    "gasto",
    "aumento_propio",
    "no_cubierto",
}


class ErrorPresupuesto(ValueError):
    """El presupuesto no se puede leer o no es consistente con los datos."""


@dataclass(frozen=True)
class Rubro:
    clave: str
    nombre: str
    genericos: tuple[str, ...]
    nacionales: frozenset[str]  # genéricos que siempre usan el índice nacional


def cargar_rubros(ruta: Path = CATALOGO) -> dict[str, Rubro]:
    """Catálogo de rubros → genéricos, en el orden del archivo."""
    filas: dict[str, list[dict[str, str]]] = defaultdict(list)
    with ruta.open(encoding="utf-8", newline="") as archivo:
        for fila in csv.DictReader(archivo):
            filas[fila["rubro"]].append(fila)
    return {
        clave: Rubro(
            clave,
            propias[0]["nombre"],
            tuple(f["codigo"] for f in propias),
            frozenset(f["codigo"] for f in propias if f["indice"] == NACIONAL),
        )
        for clave, propias in filas.items()
    }


# --- presupuesto -----------------------------------------------------------------------------


@dataclass
class Presupuesto:
    ciudad: str
    periodo_gasto: Periodo
    vivienda_propia: str
    gasto: dict[str, float]
    aumento_propio: dict[str, float] = field(default_factory=dict)
    no_cubierto: dict[str, float] = field(default_factory=dict)


def _numero(seccion: str, clave: str, valor: object, minimo: float = 0) -> float:
    if isinstance(valor, bool) or not isinstance(valor, int | float):
        raise ErrorPresupuesto(f"[{seccion}] {clave}: debe ser un número, no {valor!r}")
    if valor < minimo:
        raise ErrorPresupuesto(f"[{seccion}] {clave}: debe ser al menos {minimo}")
    return float(valor)


def _rubro_conocido(seccion: str, clave: str, rubros: Mapping[str, Rubro]) -> None:
    if clave not in rubros:
        parecidos = difflib.get_close_matches(clave, rubros, n=1)
        sugerencia = f"; ¿quisiste decir {parecidos[0]!r}?" if parecidos else ""
        raise ErrorPresupuesto(f"[{seccion}] rubro desconocido: {clave!r}{sugerencia}")


def leer_presupuesto(texto: str, rubros: Mapping[str, Rubro]) -> Presupuesto:
    """Lee y valida un presupuesto en TOML (ver ``plantilla``)."""
    try:
        datos = tomllib.loads(texto)
    except tomllib.TOMLDecodeError as error:
        raise ErrorPresupuesto(f"El presupuesto no es TOML válido: {error}") from None
    desconocidas = sorted(set(datos) - CLAVES_PRESUPUESTO)
    if desconocidas:
        raise ErrorPresupuesto(f"Claves desconocidas: {', '.join(desconocidas)}")

    ciudad = datos.get("ciudad", NACIONAL)
    if not isinstance(ciudad, str):
        raise ErrorPresupuesto('ciudad: debe ser texto, p. ej. "pachuca" o "nacional"')
    try:
        periodo = Periodo.desde_texto(str(datos.get("periodo_gasto", "")))
    except ValueError:
        raise ErrorPresupuesto('periodo_gasto: debe ser un mes como "2026-09"') from None
    if periodo.es_quincenal:
        raise ErrorPresupuesto("periodo_gasto: debe ser un mes, no una quincena")
    modo = datos.get("vivienda_propia", MODOS_VIVIENDA[0])
    if modo not in MODOS_VIVIENDA:
        raise ErrorPresupuesto(f"vivienda_propia: debe ser {' o '.join(MODOS_VIVIENDA)}")

    gasto = {}
    for clave, valor in dict(datos.get("gasto", {})).items():
        _rubro_conocido("gasto", clave, rubros)
        gasto[clave] = _numero("gasto", clave, valor)
    aumento = {}
    for clave, valor in dict(datos.get("aumento_propio", {})).items():
        _rubro_conocido("aumento_propio", clave, rubros)
        if not gasto.get(clave):
            raise ErrorPresupuesto(f"[aumento_propio] {clave}: no tiene gasto en [gasto]")
        aumento[clave] = _numero("aumento_propio", clave, valor, minimo=-99)
    no_cubierto = {
        clave: _numero("no_cubierto", clave, valor)
        for clave, valor in dict(datos.get("no_cubierto", {})).items()
    }
    presupuesto = Presupuesto(ciudad, periodo, modo, gasto, aumento, no_cubierto)
    if not any(gasto.get(r) for r in rubros_que_cuentan(presupuesto)):
        raise ErrorPresupuesto("[gasto]: pon al menos un rubro con gasto mayor que cero")
    return presupuesto


def rubros_que_cuentan(presupuesto: Presupuesto) -> list[str]:
    """Rubros con gasto que entran al índice (vivienda propia solo en modo consumo)."""
    return [
        r
        for r, monto in presupuesto.gasto.items()
        if monto > 0 and (r != RUBRO_VIVIENDA_PROPIA or presupuesto.vivienda_propia == "consumo")
    ]


def plantilla(rubros: Mapping[str, Rubro], ciudades: list[str] | None = None) -> str:
    """Texto de un ``presupuesto.toml`` comentado, con todos los rubros en cero."""
    lineas = [
        "# Bolsillómetro: tu presupuesto. Pon cuánto gastas AL MES en cada rubro, en pesos.",
        "# Deja en 0 lo que no gastas. Tus datos no salen de tu computadora.",
        "",
        '# Tu ciudad (la más cercana del INPC) o "nacional".',
        *textwrap.wrap(
            "Ciudades: " + (", ".join(ciudades) if ciudades else "ver data/ciudades/catalogo.csv"),
            width=92,
            initial_indent="# ",
            subsequent_indent="#   ",
        ),
        'ciudad = "nacional"',
        "",
        "# Mes al que corresponden los montos (tu gasto típico de ese mes). Desde 2024-08.",
        'periodo_gasto = "2026-09"',
        "",
        '# Si eres dueño de tu casa: "gasto_efectivo" la deja fuera; "consumo" la incluye',
        "# con la renta que estimas que pagarías (ponla en gasto.vivienda_propia).",
        'vivienda_propia = "gasto_efectivo"',
        "",
        "[gasto]",
    ]
    ancho = max(len(clave) for clave in rubros)
    for rubro in rubros.values():
        lineas.append(f"{rubro.clave:<{ancho}} = 0  # {rubro.nombre}")
    lineas += [
        "",
        "# Opcional: el aumento anual (%) que tú viste en un rubro grande, en lugar del índice.",
        "[aumento_propio]",
        "# renta = 8.0",
        "# colegiaturas = 6.5",
        "",
        "# Lo que el INPC no mide: se reporta aparte y no mueve tu inflación (pesos al mes).",
        "[no_cubierto]",
        "# hipoteca = 0",
        "# seguro_gastos_medicos = 0",
        "# intereses_y_comisiones = 0",
        "",
    ]
    return "\n".join(lineas)


# --- cálculo -------------------------------------------------------------------------------


@dataclass(frozen=True)
class Resultado:
    presupuesto: Presupuesto
    indice: dict[Periodo, float]  # P(t), con P(periodo_gasto) = 100
    pesos: dict[str, float]  # código (o "propio:<rubro>") → peso, suman 1
    rubro_de: dict[str, str]  # código → rubro
    fuente: dict[str, str]  # código → "ciudad", "nacional" o "propio"
    series: dict[str, Serie]
    inpc: Serie
    inpc_ciudad: Serie | None

    @property
    def ultimo(self) -> Periodo:
        return max(self.indice)

    def _peso_de(self, condicion) -> float:
        return 100 * sum(peso for codigo, peso in self.pesos.items() if condicion(codigo))

    @property
    def porcentaje_directo(self) -> float:
        """Gasto de rubros con un solo genérico: se asigna directo, sin repartir."""
        conteo = defaultdict(int)
        for rubro in self.rubro_de.values():
            conteo[rubro] += 1
        return self._peso_de(lambda c: self.fuente[c] != "propio" and conteo[self.rubro_de[c]] == 1)

    @property
    def porcentaje_propio(self) -> float:
        return self._peso_de(lambda c: self.fuente[c] == "propio")

    @property
    def porcentaje_imputado(self) -> float:
        return 100 - self.porcentaje_directo - self.porcentaje_propio

    @property
    def porcentaje_ciudad(self) -> float:
        return self._peso_de(lambda c: self.fuente[c] == "ciudad")

    def inflacion(self, rezago: int, periodo: Periodo | None = None) -> float | None:
        return _variacion_o_nada(self.indice, periodo or self.ultimo, rezago)

    def inflacion_inpc(self, rezago: int, periodo: Periodo | None = None) -> float | None:
        return _variacion_o_nada(self.inpc, periodo or self.ultimo, rezago)

    def inflacion_ciudad(self, rezago: int, periodo: Periodo | None = None) -> float | None:
        if self.inpc_ciudad is None:
            return None
        return _variacion_o_nada(self.inpc_ciudad, periodo or self.ultimo, rezago)

    def incidencias_por_rubro(self, rezago: int = 12) -> dict[str, float]:
        """Puntos porcentuales que aporta cada rubro a tu inflación de ``rezago`` meses."""
        hasta = self.ultimo
        desde = hasta.anterior(rezago)
        base = valores_en(self.series, self.presupuesto.periodo_gasto)
        por_codigo = incidencias(self.series, self.pesos, base, desde, hasta)
        por_rubro: dict[str, float] = defaultdict(float)
        for codigo, valor in por_codigo.items():
            por_rubro[self.rubro_de[codigo]] += valor
        return dict(sorted(por_rubro.items(), key=lambda par: -abs(par[1])))

    @property
    def total_cubierto(self) -> float:
        return sum(self.presupuesto.gasto[r] for r in rubros_que_cuentan(self.presupuesto))

    @property
    def total_no_cubierto(self) -> float:
        return sum(self.presupuesto.no_cubierto.values())


def _variacion_o_nada(serie: Serie, periodo: Periodo, rezago: int) -> float | None:
    try:
        return variacion(serie, periodo, rezago)
    except KeyError:
        return None


def _serie_propia(
    aumento: float, base: Periodo, periodos: list[Periodo]
) -> dict[Periodo, float | None]:
    """Serie sintética que crece ``aumento`` % al año, parejo cada mes, con 100 en ``base``."""
    mensual = (1 + aumento / 100) ** (1 / 12)
    indice_base = base.anio * 12 + base.mes
    return {p: 100 * mensual ** (p.anio * 12 + p.mes - indice_base) for p in periodos}


def _ultimo(serie: Serie) -> Periodo:
    return max(p for p, v in serie.items() if v is not None)


def calcular(
    presupuesto: Presupuesto,
    rubros: Mapping[str, Rubro],
    nacional: DatosINPC,
    ciudades: DatosCiudades | None = None,
) -> Resultado:
    """Tu índice personal con el presupuesto, los datos nacionales y, si eliges, tu ciudad."""
    e = presupuesto.periodo_gasto
    mensual = nacional.mensual
    ultimo_nacional = _ultimo(mensual[COLUMNA_GENERAL])
    if not PRIMER_MES_GASTO <= e <= ultimo_nacional:
        raise ErrorPresupuesto(
            f"periodo_gasto: debe estar entre {PRIMER_MES_GASTO} y {ultimo_nacional}"
        )

    locales: Mapping[str, Serie] = {}
    inpc_ciudad = None
    if presupuesto.ciudad != NACIONAL:
        if ciudades is None or presupuesto.ciudad not in ciudades.series:
            disponibles = sorted(ciudades.series) if ciudades else []
            parecidas = difflib.get_close_matches(presupuesto.ciudad, disponibles, n=1)
            sugerencia = f"; ¿quisiste decir {parecidas[0]!r}?" if parecidas else ""
            raise ErrorPresupuesto(f"ciudad desconocida: {presupuesto.ciudad!r}{sugerencia}")
        locales = ciudades.series[presupuesto.ciudad]
        inpc_ciudad = locales[COLUMNA_GENERAL]
        if inpc_ciudad.get(e) is None:
            raise ErrorPresupuesto(f"Tu ciudad todavía no tiene datos de {e}")
    ultimo_local = _ultimo(inpc_ciudad) if inpc_ciudad else None

    # Ponderadores oficiales llevados al mes del gasto: w_k · I_k(e) / I_k(2Q jul-2024).
    oficiales = {p.codigo: p.ponderador for p in nacional.ponderadores}
    base_oficial = valores_en({c: nacional.quincenal[c] for c in oficiales}, BASE_PONDERADORES)
    en_e = valores_en({c: mensual[c] for c in oficiales}, e)
    periodos = sorted(mensual[COLUMNA_GENERAL])

    pesos: dict[str, float] = {}
    rubro_de: dict[str, str] = {}
    fuente: dict[str, str] = {}
    series: dict[str, Serie] = {}
    for clave in rubros_que_cuentan(presupuesto):
        rubro, monto = rubros[clave], presupuesto.gasto[clave]
        if clave in presupuesto.aumento_propio:
            codigo = f"propio:{clave}"
            series[codigo] = _serie_propia(presupuesto.aumento_propio[clave], e, periodos)
            pesos[codigo], rubro_de[codigo], fuente[codigo] = monto, clave, "propio"
            continue
        reparto = {c: oficiales[c] * en_e[c] / base_oficial[c] for c in rubro.genericos}
        total = sum(reparto.values())
        for codigo, valor in reparto.items():
            local = locales.get(codigo, {})
            usa_local = (
                codigo not in rubro.nacionales
                and local.get(e) is not None
                and ultimo_local is not None
                and local.get(ultimo_local) is not None
            )
            series[codigo] = local if usa_local else mensual[codigo]
            pesos[codigo] = monto * valor / total
            rubro_de[codigo] = clave
            fuente[codigo] = "ciudad" if usa_local else "nacional"

    total = sum(pesos.values())
    pesos = {codigo: peso / total for codigo, peso in pesos.items()}
    indice = indice_ponderado(series, pesos, valores_en(series, e))
    return Resultado(
        presupuesto,
        indice,
        pesos,
        rubro_de,
        fuente,
        series,
        mensual[COLUMNA_GENERAL],
        inpc_ciudad,
    )
