"""INPC por ciudad: los 292 genéricos en cada una de las 55 ciudades, mensual.

Se descargan de la estructura "Por ciudad" del INEGI, una ciudad por petición (las
exportaciones de muchas ciudades juntas tardan más o fallan con HTTP 500), y se guardan en
``data/ciudades/`` con la misma forma que el nacional: un CSV ancho por ciudad.

El INEGI no publica los pesos genérico × ciudad, así que el INPC de una ciudad no se puede
reconstruir exacto como el nacional. La validación usa dos pruebas que sí se pueden hacer:

- **Acotamiento.** El índice nacional de cada genérico es un promedio ponderado de sus índices
  por ciudad, así que antes del eslabón de 2024 debe quedar entre el mínimo y el máximo de las
  ciudades. Si un id quedó mal asignado (un genérico o una ciudad por otro), esto falla.
- **Plausibilidad.** El índice general de cada ciudad contra el que se obtiene con sus 292
  genéricos y los ponderadores nacionales. No es exacto porque los pesos de cada ciudad
  difieren, pero la variación anual debe quedar cerca.
"""

from __future__ import annotations

import re
import unicodedata
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import asdict, dataclass, fields
from pathlib import Path

from . import datos as disco
from .datos import COLUMNA_GENERAL, DatosINPC
from .indices import indice_ponderado, valores_en, variacion
from .inegi import ESTRUCTURA_CIUDADES, ClienteINEGI
from .lectura import Generico, Nodo, genericos_del_arbol, leer_arbol, leer_exportacion, leer_temas
from .periodos import Periodo

DIRECTORIO = "ciudades"
ARCHIVO_CATALOGO = "catalogo.csv"
ARCHIVO_METADATOS = "metadatos.json"
SUFIJO_SERIES = "_mensual.csv"

ANIO_INICIAL = 2018
CIUDADES_ESPERADAS = 55
GENERICOS_ESPERADOS = 292
TIMEOUT_ARBOL = 900
SUBTEMA_OBJETO_DEL_GASTO = "por objeto del gasto"

# Claves cortas para nombres que de otro modo serían incómodos de escribir.
ALIAS = {"area-metropolitana-de-la-cd-de-mexico": "cdmx"}


class ErrorCiudades(RuntimeError):
    """Los datos por ciudad no pasan las validaciones."""


@dataclass(frozen=True)
class Ciudad:
    clave: str
    nombre: str
    id_nodo: str
    id_general: str


@dataclass
class DatosCiudades:
    ciudades: list[Ciudad]
    series: dict[str, dict[str, dict[Periodo, float | None]]]  # clave → código → serie


def clave_ciudad(nombre: str) -> str:
    """``"Pachuca, Hgo."`` → ``"pachuca"``; ``"Cd. Juárez, Chih."`` → ``"cd-juarez"``."""
    sin_acentos = unicodedata.normalize("NFKD", nombre).encode("ascii", "ignore").decode()
    base = re.sub(r"^\d+\.\s*", "", sin_acentos).split(",")[0]
    clave = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")
    return ALIAS.get(clave, clave)


def _nombre(titulo: str) -> str:
    return re.sub(r"^\d+\.\s*", "", titulo).strip()


def ciudades_del_arbol(respuesta: Mapping) -> list[tuple[Ciudad, dict[str, Generico]]]:
    """Ciudades del árbol "Por ciudad", cada una con sus genéricos por objeto del gasto.

    Algunas ciudades traen además un subtema por origen de los bienes (SCIAN); solo se usa
    el de objeto del gasto.
    """
    temas = leer_temas(respuesta)
    largo = len(ESTRUCTURA_CIUDADES) + 4
    # Subtema por objeto del gasto de cada ciudad: clave de la ciudad + 4 dígitos.
    subtemas = {
        clave[:largo]: clave
        for clave, titulo in temas.items()
        if len(clave) == largo + 4 and SUBTEMA_OBJETO_DEL_GASTO in titulo
    }
    nodos_por_subtema: dict[str, list[Nodo]] = defaultdict(list)
    for nodo in leer_arbol(respuesta):
        nodos_por_subtema[nodo.clave[: largo + 4]].append(nodo)

    resultado = []
    for clave_tema, titulo in temas.items():
        if len(clave_tema) != largo:
            continue
        if clave_tema not in subtemas:
            raise ErrorCiudades(f"{titulo}: no se encontró el subtema por objeto del gasto")
        id_general, genericos = genericos_del_arbol(nodos_por_subtema[subtemas[clave_tema]])
        ciudad = Ciudad(clave_ciudad(titulo), _nombre(titulo), clave_tema, id_general)
        resultado.append((ciudad, genericos))
    return sorted(resultado, key=lambda par: par[0].clave)


def _recortar(series: dict[str, dict[Periodo, float | None]]) -> None:
    """Quita los periodos en que ninguna serie tiene dato (antes de jul-2018 en ciudades)."""
    con_dato = {p for serie in series.values() for p, v in serie.items() if v is not None}
    for serie in series.values():
        for periodo in [p for p in serie if p not in con_dato]:
            del serie[periodo]


def descargar(cliente: ClienteINEGI, anio_final: int) -> DatosCiudades:
    arbol = cliente.obtener_arbol(ESTRUCTURA_CIUDADES, timeout=TIMEOUT_ARBOL)
    ciudades = ciudades_del_arbol(arbol)
    _validar_estructura(ciudades)
    series = {}
    for ciudad, genericos in ciudades:
        ids = {COLUMNA_GENERAL: ciudad.id_general} | {c: g.id_serie for c, g in genericos.items()}
        texto = cliente.exportar(ESTRUCTURA_CIUDADES, ids.values(), ANIO_INICIAL, anio_final)
        _validar_titulo(ciudad, texto)
        por_id = leer_exportacion(texto)
        faltantes = [codigo for codigo, id_serie in ids.items() if id_serie not in por_id]
        if faltantes:
            raise ErrorCiudades(f"{ciudad.nombre}: la exportación no trajo {', '.join(faltantes)}")
        propias = {codigo: por_id[id_serie] for codigo, id_serie in ids.items()}
        _recortar(propias)
        series[ciudad.clave] = propias
    return DatosCiudades([ciudad for ciudad, _ in ciudades], series)


def _validar_titulo(ciudad: Ciudad, texto: str) -> None:
    """La fila "Título" de la exportación nombra la ciudad: así no se cruzan dos ciudades."""
    fila = next((linea for linea in texto.splitlines() if linea.startswith('"Título"')), "")
    patron = rf"Por ciudad, (\d+\.\s*)?{re.escape(ciudad.nombre)},"
    if not re.search(patron, fila.split('","')[1] if '","' in fila else ""):
        raise ErrorCiudades(f"La exportación de {ciudad.nombre} no trae su nombre en el título")


def _validar_estructura(ciudades: list[tuple[Ciudad, dict[str, Generico]]]) -> None:
    if len(ciudades) != CIUDADES_ESPERADAS:
        raise ErrorCiudades(
            f"El árbol trae {len(ciudades)} ciudades; se esperaban {CIUDADES_ESPERADAS}"
        )
    claves = [ciudad.clave for ciudad, _ in ciudades]
    if len(set(claves)) != len(claves):
        raise ErrorCiudades("Hay claves de ciudad repetidas")
    for ciudad, genericos in ciudades:
        if len(genericos) != GENERICOS_ESPERADOS:
            raise ErrorCiudades(
                f"{ciudad.nombre} trae {len(genericos)} genéricos; "
                f"se esperaban {GENERICOS_ESPERADOS}"
            )


# --- disco ---------------------------------------------------------------------------------


def _ruta_series(directorio: Path, clave: str) -> Path:
    return directorio / DIRECTORIO / f"{clave}{SUFIJO_SERIES}"


def guardar(directorio: Path, datos: DatosCiudades) -> None:
    carpeta = directorio / DIRECTORIO
    for ciudad in datos.ciudades:
        disco.escribir_series(_ruta_series(directorio, ciudad.clave), datos.series[ciudad.clave])
    disco.escribir_csv(
        carpeta / ARCHIVO_CATALOGO,
        [campo.name for campo in fields(Ciudad)],
        (list(asdict(ciudad).values()) for ciudad in datos.ciudades),
    )


def leer_catalogo(directorio: Path) -> list[Ciudad]:
    return [Ciudad(**fila) for fila in disco.leer_csv(directorio / DIRECTORIO / ARCHIVO_CATALOGO)]


def cargar(directorio: Path) -> DatosCiudades:
    ciudades = leer_catalogo(directorio)
    return DatosCiudades(
        ciudades,
        {c.clave: disco.leer_series(_ruta_series(directorio, c.clave)) for c in ciudades},
    )


def escribir_metadatos(directorio: Path, metadatos: Mapping) -> None:
    disco.escribir_metadatos(directorio / DIRECTORIO / ARCHIVO_METADATOS, metadatos)


def leer_metadatos(directorio: Path) -> dict:
    return disco.leer_metadatos(directorio / DIRECTORIO / ARCHIVO_METADATOS)


# --- validación ----------------------------------------------------------------------------

# Antes del eslabón de la 2Q jul-2024 los índices (base 2Q jul-2018 = 100) son aditivos: el
# nacional de cada genérico es un promedio ponderado de sus ciudades, mes por mes.
INICIO_ACOTAMIENTO = Periodo(2018, 8)
FIN_ACOTAMIENTO = Periodo(2024, 7)
HOLGURA_REDONDEO = 0.001 + 1e-9

# Primer mes con la canasta 2024 en todos los genéricos; la variación anual se compara desde
# doce meses después.
BASE_PLAUSIBILIDAD = Periodo(2024, 8)
TOLERANCIA_PLAUSIBILIDAD = 2.0  # puntos porcentuales de inflación anual


@dataclass(frozen=True)
class Plausibilidad:
    ciudad: str
    periodo: Periodo
    publicada: float
    reconstruida: float

    @property
    def diferencia(self) -> float:
        return self.reconstruida - self.publicada


@dataclass(frozen=True)
class Validacion:
    revisiones_acotamiento: int
    fuera_de_rango: list[tuple[str, Periodo]]  # (genérico, periodo)
    plausibilidad: list[Plausibilidad]

    @property
    def peor(self) -> Plausibilidad | None:
        return max(self.plausibilidad, key=lambda p: abs(p.diferencia), default=None)

    @property
    def cumple(self) -> bool:
        peor = self.peor
        return not self.fuera_de_rango and (
            peor is None or abs(peor.diferencia) <= TOLERANCIA_PLAUSIBILIDAD
        )


def acotamiento(datos: DatosCiudades, nacional: DatosINPC) -> tuple[int, list[tuple[str, Periodo]]]:
    """Revisa que cada genérico nacional quede entre el mínimo y el máximo de sus ciudades."""
    revisiones, fuera = 0, []
    for codigo, serie in nacional.mensual.items():
        if codigo == COLUMNA_GENERAL:
            continue
        for periodo, valor in serie.items():
            if valor is None or not INICIO_ACOTAMIENTO <= periodo <= FIN_ACOTAMIENTO:
                continue
            locales = [
                v
                for series in datos.series.values()
                if (v := series.get(codigo, {}).get(periodo)) is not None
            ]
            if not locales:
                continue
            revisiones += 1
            if not min(locales) - HOLGURA_REDONDEO <= valor <= max(locales) + HOLGURA_REDONDEO:
                fuera.append((codigo, periodo))
    return revisiones, fuera


def plausibilidad(
    clave: str, series: Mapping[str, Mapping[Periodo, float | None]], pesos: Mapping[str, float]
) -> list[Plausibilidad]:
    """Inflación anual publicada de la ciudad contra la de sus genéricos con pesos nacionales.

    Solo entran los genéricos con dato en la base y en el último mes; los pesos se
    renormalizan entre ellos.
    """
    general = series[COLUMNA_GENERAL]
    ultimo = max(p for p, v in general.items() if v is not None)
    disponibles = {
        codigo: peso
        for codigo, peso in pesos.items()
        if series[codigo].get(BASE_PLAUSIBILIDAD) is not None
        and series[codigo].get(ultimo) is not None
    }
    propias = {codigo: series[codigo] for codigo in disponibles}
    indice = indice_ponderado(propias, disponibles, valores_en(propias, BASE_PLAUSIBILIDAD))
    resultado = []
    periodo = BASE_PLAUSIBILIDAD.desplazar(12)
    while periodo <= ultimo:
        if periodo in indice:
            resultado.append(
                Plausibilidad(
                    clave,
                    periodo,
                    variacion(general, periodo, rezago=12),
                    variacion(indice, periodo, rezago=12),
                )
            )
        periodo = periodo.desplazar(1)
    return resultado


def _ultimo(serie: Mapping[Periodo, float | None]) -> Periodo:
    return max(p for p, v in serie.items() if v is not None)


def ultimo_mes(datos: DatosCiudades) -> Periodo:
    """Último mes con dato; ``validar`` garantiza que es el mismo en todas las ciudades."""
    return _ultimo(datos.series[datos.ciudades[0].clave][COLUMNA_GENERAL])


def validar(datos: DatosCiudades, nacional: DatosINPC) -> Validacion:
    """Falla con ``ErrorCiudades`` si los datos por ciudad no son consistentes con el nacional.

    Las ciudades pueden ir atrás del nacional: el workflow las baja después, en su propio paso.
    Lo que no puede pasar es que vayan adelante o que unas lleguen más lejos que otras.
    """
    ultimo_nacional = _ultimo(nacional.mensual[COLUMNA_GENERAL])
    ultimo_ciudades = ultimo_mes(datos)
    if ultimo_ciudades > ultimo_nacional:
        raise ErrorCiudades(
            f"Las ciudades llegan a {ultimo_ciudades}, después que el nacional ({ultimo_nacional})"
        )
    for ciudad in datos.ciudades:
        series = datos.series[ciudad.clave]
        if set(series) != set(nacional.mensual):
            raise ErrorCiudades(f"{ciudad.nombre}: los genéricos no coinciden con el nacional")
        if _ultimo(series[COLUMNA_GENERAL]) != ultimo_ciudades:
            raise ErrorCiudades(
                f"{ciudad.nombre}: el último mes es {_ultimo(series[COLUMNA_GENERAL])}; "
                f"las demás ciudades llegan a {ultimo_ciudades}"
            )

    revisiones, fuera = acotamiento(datos, nacional)
    pesos = {p.codigo: p.ponderador for p in nacional.ponderadores}
    resultado = Validacion(
        revisiones,
        fuera,
        [
            fila
            for ciudad in datos.ciudades
            for fila in plausibilidad(ciudad.clave, datos.series[ciudad.clave], pesos)
        ],
    )
    if fuera:
        detalle = ", ".join(f"{codigo} en {periodo}" for codigo, periodo in fuera[:5])
        raise ErrorCiudades(f"El nacional queda fuera del rango de sus ciudades: {detalle}")
    if not resultado.cumple:
        peor = resultado.peor
        raise ErrorCiudades(
            f"{peor.ciudad} en {peor.periodo}: la inflación anual con pesos nacionales difiere "
            f"{peor.diferencia:+.2f} pp de la publicada (tolerancia ±{TOLERANCIA_PLAUSIBILIDAD})"
        )
    return resultado


def sin_dato_reciente(datos: DatosCiudades) -> dict[str, list[str]]:
    """Genéricos sin dato en el último mes, por ciudad (para esos se usa el nacional)."""
    resultado = {}
    for ciudad in datos.ciudades:
        series = datos.series[ciudad.clave]
        ultimo = _ultimo(series[COLUMNA_GENERAL])
        faltan = sorted(c for c, s in series.items() if s.get(ultimo) is None)
        if faltan:
            resultado[ciudad.clave] = faltan
    return resultado


def metadatos(datos: DatosCiudades, validacion: Validacion) -> dict:
    peor = validacion.peor
    return {
        "fuente": "INEGI, Índice Nacional de Precios al Consumidor (INPC), por ciudad",
        "deslinde": "Cálculos propios con datos del INPC. No es un producto oficial del "
        "INEGI ni de Banco de México.",
        "estructura": ESTRUCTURA_CIUDADES,
        "ciudades": len(datos.ciudades),
        "ultimo_mensual": str(ultimo_mes(datos)),
        "acotamiento": {
            "desde": str(INICIO_ACOTAMIENTO),
            "hasta": str(FIN_ACOTAMIENTO),
            "revisiones": validacion.revisiones_acotamiento,
            "fuera_de_rango": len(validacion.fuera_de_rango),
        },
        "plausibilidad": {
            "base": str(BASE_PLAUSIBILIDAD),
            "tolerancia_pp": TOLERANCIA_PLAUSIBILIDAD,
            "comparaciones": len(validacion.plausibilidad),
            "diferencia_maxima_pp": round(abs(peor.diferencia), 3) if peor else 0.0,
            "peor": f"{peor.ciudad} {peor.periodo}" if peor else "",
        },
        "sin_dato_reciente": sin_dato_reciente(datos),
    }


# --- pipeline ------------------------------------------------------------------------------


@dataclass(frozen=True)
class Resumen:
    validacion: Validacion
    nuevos: list[Periodo]


def actualizar(directorio: Path, cliente: ClienteINEGI | None = None) -> Resumen:
    """Descarga las 55 ciudades, las valida contra el nacional de ``directorio`` y las escribe.

    Necesita los datos nacionales ya actualizados en ``directorio``. No escribe nada si la
    validación falla.
    """
    if not (directorio / disco.ARCHIVO_MENSUAL).exists():
        raise ErrorCiudades(f"No hay datos nacionales en {directorio}; corre antes `actualizar`")
    nacional = disco.cargar(directorio)
    anio_final = _ultimo(nacional.mensual[COLUMNA_GENERAL]).anio
    datos = descargar(cliente or ClienteINEGI(), anio_final)
    resultado = validar(datos, nacional)
    # El INEGI publica nacional y ciudades el mismo día: una descarga atrasada no se guarda.
    ultimo_nacional = _ultimo(nacional.mensual[COLUMNA_GENERAL])
    if ultimo_mes(datos) != ultimo_nacional:
        raise ErrorCiudades(
            f"La descarga por ciudad llega a {ultimo_mes(datos)}; el nacional, a {ultimo_nacional}"
        )

    previos: set[Periodo] = set()
    if (directorio / DIRECTORIO / ARCHIVO_CATALOGO).exists():
        anteriores = cargar(directorio)
        if anteriores.ciudades:
            general = anteriores.series[anteriores.ciudades[0].clave][COLUMNA_GENERAL]
            previos = {p for p, v in general.items() if v is not None}

    guardar(directorio, datos)
    escribir_metadatos(directorio, metadatos(datos, resultado))
    general = datos.series[datos.ciudades[0].clave][COLUMNA_GENERAL]
    nuevos = sorted({p for p, v in general.items() if v is not None} - previos)
    return Resumen(resultado, nuevos)


def verificar(directorio: Path) -> Validacion:
    """Valida los datos por ciudad de ``directorio`` contra el nacional, sin red."""
    return validar(cargar(directorio), disco.cargar(directorio))
