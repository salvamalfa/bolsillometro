"""Cetes a 28 días y UDI del SIE de Banxico (sin token), para el rendimiento real.

Se descargan de la misma exportación CSV que usa la consulta de series del SIE
(``consultarDirectorioInternetAction.do?accion=consultarSeries``), que no pide token. Como el
INEGI, no es una API documentada, así que todo se valida antes de escribir ``data/banxico/``:

- **UDI contra INPC.** La UDI se deriva del INPC quincenal: del día 10 al 25 de cada mes crece
  lo que subió el INPC en la 2ª quincena del mes anterior, y del 25 al 10 del mes siguiente lo
  de la 1ª quincena del mes, a tasa diaria constante. Con los datos de ``data/`` debe cuadrar
  hasta el redondeo (±1e-6), tramo por tramo y día por día. Es una prueba cruzada: Banxico
  confirma al INEGI y viceversa.
- **Cetes.** Tasas entre 0 y 30%, sin huecos de más de 14 días entre subastas.
- **Sin revisiones.** Una descarga nueva no puede cambiar ni quitar fechas ya guardadas.

Se guardan las series tal como se publican (UDI diaria y Cetes por subasta). Lo mensual se
calcula al usarlas, de fin de mes a fin de mes: ``variacion_udi`` y ``rendimiento_cetes``.
"""

from __future__ import annotations

import csv
import datetime as dt
import io
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path

from . import datos as disco
from .datos import COLUMNA_GENERAL, DatosINPC
from .periodos import Periodo
from .red import ClienteHTTP, ErrorFuente

URL_SERIES = (
    "https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do"
    "?accion=consultarSeries"
)
SERIE_UDI = "SP68257"  # Valor de UDIS, diaria
SERIE_CETES28 = "SF43936"  # Cetes a 28 días, tasa de rendimiento de la subasta semanal

ANIO_INICIAL = 2018

DIRECTORIO = "banxico"
ARCHIVO_UDI = "udi_diaria.csv"
ARCHIVO_CETES28 = "cetes28_subasta.csv"
ARCHIVO_METADATOS = "metadatos.json"

TOLERANCIA_UDI = 1e-6  # en el factor de crecimiento de cada media quincena
TASA_MAXIMA = 30.0
HUECO_MAXIMO_CETES = 14  # días entre subastas
PLAZO_CETES = 28  # días
BASE_DIAS = 360  # convención de tasas de Cetes

Serie = dict[dt.date, float]


class ErrorBanxico(ErrorFuente):
    """Banxico respondió algo distinto de lo esperado o los datos no pasan las validaciones."""


class ClienteBanxico(ClienteHTTP):
    Error = ErrorBanxico

    def exportar(self, series: Iterable[str], anio_inicial: int, anio_final: int) -> str:
        """Niveles de ``series`` entre dos años, como CSV ya decodificado."""
        formulario = [
            ("locale", "es"),
            ("version", "3"),
            ("anoInicial", str(anio_inicial)),
            ("anoFinal", str(anio_final)),
            ("tipoInformacion", ""),
            ("metadatosWeb", "true"),
            ("formatoCSV.x", "1"),
            ("formatoCSV.y", "1"),
            *(("series", serie) for serie in series),
        ]
        respuesta = self._pedir("POST", URL_SERIES, data=formulario)
        if "text/csv" not in respuesta.headers.get("Content-Type", ""):
            raise ErrorBanxico("La exportación del SIE no devolvió un CSV")
        return respuesta.content.decode("latin-1")


def leer_exportacion(texto: str) -> dict[str, dict[dt.date, float | None]]:
    """Lee el CSV del SIE y devuelve ``{serie: {fecha: valor}}``.

    Los metadatos van antes de la fila ``Fecha``, que trae las claves de las series; cada fila
    siguiente es un día (``dd/mm/aaaa``). ``N/E`` y celdas vacías se leen como ``None``.
    """
    filas = list(csv.reader(io.StringIO(texto)))
    try:
        inicio = next(i for i, fila in enumerate(filas) if fila and fila[0] == "Fecha")
    except StopIteration:
        raise ErrorBanxico("La exportación del SIE no trae la fila 'Fecha'") from None
    claves = [celda.strip() for celda in filas[inicio][1:] if celda.strip()]
    series: dict[str, dict[dt.date, float | None]] = {clave: {} for clave in claves}
    for fila in filas[inicio + 1 :]:
        if not fila or not fila[0].strip():
            continue
        fecha = dt.datetime.strptime(fila[0].strip(), "%d/%m/%Y").date()
        valores = fila[1 : len(claves) + 1]
        if len(valores) != len(claves):
            raise ErrorBanxico(f"La fila {fila[0]!r} no trae un valor por serie")
        for clave, valor in zip(claves, valores, strict=True):
            valor = valor.strip()
            series[clave][fecha] = None if valor in ("", "N/E") else float(valor)
    return series


@dataclass
class DatosBanxico:
    udi: Serie
    cetes28: Serie


# --- disco ---------------------------------------------------------------------------------


def _escribir_serie(ruta: Path, columna: str, serie: Mapping[dt.date, float]) -> None:
    disco.escribir_csv(
        ruta, ["fecha", columna], ([f.isoformat(), repr(v)] for f, v in sorted(serie.items()))
    )


def _leer_serie(ruta: Path, columna: str) -> Serie:
    return {dt.date.fromisoformat(f["fecha"]): float(f[columna]) for f in disco.leer_csv(ruta)}


def guardar(directorio: Path, datos: DatosBanxico) -> None:
    carpeta = directorio / DIRECTORIO
    _escribir_serie(carpeta / ARCHIVO_UDI, "udi", datos.udi)
    _escribir_serie(carpeta / ARCHIVO_CETES28, "tasa", datos.cetes28)


def cargar(directorio: Path) -> DatosBanxico:
    carpeta = directorio / DIRECTORIO
    return DatosBanxico(
        udi=_leer_serie(carpeta / ARCHIVO_UDI, "udi"),
        cetes28=_leer_serie(carpeta / ARCHIVO_CETES28, "tasa"),
    )


def existe(directorio: Path) -> bool:
    return (directorio / DIRECTORIO / ARCHIVO_UDI).exists()


def leer_metadatos(directorio: Path) -> dict:
    return disco.leer_metadatos(directorio / DIRECTORIO / ARCHIVO_METADATOS)


# --- validación ----------------------------------------------------------------------------


@dataclass(frozen=True)
class ComparacionUDI:
    """Crecimiento de la UDI en media quincena contra el del INPC de la quincena que la rige."""

    quincena: Periodo
    desde: dt.date
    hasta: dt.date
    udi: float
    inpc: float

    @property
    def diferencia(self) -> float:
        return self.udi - self.inpc

    @property
    def cumple(self) -> bool:
        return abs(self.diferencia) <= TOLERANCIA_UDI


def _dia(anio: int, mes: int, dia: int) -> dt.date:
    """Fecha con ``mes`` posiblemente igual a 13 (enero del año siguiente)."""
    return dt.date(anio + (mes - 1) // 12, (mes - 1) % 12 + 1, dia)


def tramo_udi(quincena: Periodo) -> tuple[dt.date, dt.date]:
    """Días entre los que la UDI crece con el INPC de ``quincena``.

    La 2ª quincena del mes ``m`` rige del 10 al 25 del mes ``m+1``; la 1ª quincena del mes
    ``m``, del 25 de ``m`` al 10 de ``m+1``.
    """
    if quincena.quincena == 2:
        return _dia(quincena.anio, quincena.mes + 1, 10), _dia(quincena.anio, quincena.mes + 1, 25)
    return _dia(quincena.anio, quincena.mes, 25), _dia(quincena.anio, quincena.mes + 1, 10)


def consistencia_udi(
    udi: Mapping[dt.date, float], inpc_quincenal: Mapping[Periodo, float | None]
) -> list[ComparacionUDI]:
    """Compara cada tramo de la UDI con la variación del INPC que lo rige, donde hay datos."""
    comparaciones = []
    for quincena in sorted(inpc_quincenal):
        actual = inpc_quincenal.get(quincena)
        previo = inpc_quincenal.get(quincena.anterior())
        desde, hasta = tramo_udi(quincena)
        if None in (actual, previo) or desde not in udi or hasta not in udi:
            continue
        comparaciones.append(
            ComparacionUDI(quincena, desde, hasta, udi[hasta] / udi[desde], actual / previo)
        )
    return comparaciones


def desviacion_diaria(udi: Mapping[dt.date, float], tramo: ComparacionUDI) -> list[float]:
    """Dentro de un tramo la UDI crece a tasa diaria constante: ``g^(1/n)`` cada día."""
    dias = (tramo.hasta - tramo.desde).days
    diaria = tramo.udi ** (1 / dias)
    fechas = [tramo.desde + dt.timedelta(days=i) for i in range(dias + 1)]
    return [udi[b] / udi[a] - diaria for a, b in zip(fechas, fechas[1:], strict=False)]


@dataclass(frozen=True)
class Validacion:
    udi: list[ComparacionUDI]
    dias_revisados: int = 0
    error_maximo_diario: float = 0.0

    @property
    def error_maximo_udi(self) -> float:
        return max((abs(c.diferencia) for c in self.udi), default=0.0)


def _huecos(fechas: list[dt.date]) -> list[tuple[dt.date, int]]:
    return [(b, (b - a).days) for a, b in zip(fechas, fechas[1:], strict=False)]


def validar(datos: DatosBanxico, nacional: DatosINPC) -> Validacion:
    """Falla con ``ErrorBanxico`` si la UDI no cuadra con el INPC o los Cetes no son plausibles."""
    if not datos.udi or not datos.cetes28:
        raise ErrorBanxico("Faltan datos de UDI o de Cetes")
    saltos = [(f, d) for f, d in _huecos(sorted(datos.udi)) if d != 1]
    if saltos:
        raise ErrorBanxico(f"La UDI tiene huecos: {saltos[0][0]} (tras {saltos[0][1]} días)")
    if min(datos.udi.values()) <= 0:
        raise ErrorBanxico("La UDI tiene valores no positivos")

    fuera = [(f, v) for f, v in sorted(datos.cetes28.items()) if not 0 < v <= TASA_MAXIMA]
    if fuera:
        raise ErrorBanxico(f"Tasa de Cetes fuera de rango: {fuera[0][1]} el {fuera[0][0]}")
    saltos = [(f, d) for f, d in _huecos(sorted(datos.cetes28)) if d > HUECO_MAXIMO_CETES]
    if saltos:
        raise ErrorBanxico(
            f"Faltan subastas de Cetes antes del {saltos[0][0]} ({saltos[0][1]} días)"
        )

    comparaciones = consistencia_udi(datos.udi, nacional.quincenal[COLUMNA_GENERAL])
    if not comparaciones:
        raise ErrorBanxico("No hay tramos de UDI que comparar con el INPC")
    fallas = [c for c in comparaciones if not c.cumple]
    if fallas:
        detalle = ", ".join(f"{c.quincena} ({c.diferencia:+.2e})" for c in fallas[:5])
        raise ErrorBanxico(f"La UDI no cuadra con el INPC en: {detalle}")

    dias, peor = 0, 0.0
    for tramo in comparaciones:
        desviaciones = desviacion_diaria(datos.udi, tramo)
        dias += len(desviaciones)
        peor = max(peor, *(abs(d) for d in desviaciones))
        if peor > TOLERANCIA_UDI:
            raise ErrorBanxico(f"La UDI no crece parejo entre el {tramo.desde} y el {tramo.hasta}")
    return Validacion(comparaciones, dias, peor)


def _sin_revisiones(nombre: str, previa: Mapping, nueva: Mapping) -> None:
    """Lo ya publicado no cambia: cada fecha guardada sigue en la descarga, con el mismo valor."""
    cambios = [f for f, v in previa.items() if nueva.get(f) != v]
    if cambios:
        raise ErrorBanxico(
            f"{nombre}: la descarga cambia o quita {len(cambios)} fechas ya guardadas "
            f"(la primera, {min(cambios)})"
        )


# --- rendimientos --------------------------------------------------------------------------


def fin_de_mes(periodo: Periodo) -> dt.date:
    return _dia(periodo.anio, periodo.mes + 1, 1) - dt.timedelta(days=1)


def variacion_udi(udi: Mapping[dt.date, float], desde: Periodo, hasta: Periodo) -> float:
    """Variación porcentual de la UDI del último día de ``desde`` al último de ``hasta``."""
    inicio, fin = fin_de_mes(desde), fin_de_mes(hasta)
    if inicio not in udi or fin not in udi:
        raise KeyError(f"Falta la UDI del {inicio} o del {fin}")
    return (udi[fin] / udi[inicio] - 1) * 100


def rendimiento_cetes(cetes: Mapping[dt.date, float], desde: Periodo, hasta: Periodo) -> float:
    """Rendimiento porcentual de reinvertir en Cetes a 28 días, de fin de ``desde`` a ``hasta``.

    Cada 28 días se reinvierte a la tasa de la última subasta publicada; el último tramo, más
    corto, se prorratea. Cada tramo rinde ``tasa · días / 360``, la convención de los Cetes.
    """
    inicio, fin = fin_de_mes(desde), fin_de_mes(hasta)
    subastas = sorted(cetes)
    if (
        not subastas
        or subastas[0] > inicio
        or subastas[-1] < fin - dt.timedelta(days=HUECO_MAXIMO_CETES)
    ):
        raise KeyError(f"No hay subastas de Cetes que cubran del {inicio} al {fin}")
    factor, fecha = 1.0, inicio
    while fecha < fin:
        tasa = cetes[max(s for s in subastas if s <= fecha)]
        dias = min(PLAZO_CETES, (fin - fecha).days)
        factor *= 1 + tasa / 100 * dias / BASE_DIAS
        fecha += dt.timedelta(days=dias)
    return (factor - 1) * 100


# --- pipeline ------------------------------------------------------------------------------


def descargar(cliente: ClienteBanxico, anio_final: int) -> DatosBanxico:
    series = leer_exportacion(
        cliente.exportar([SERIE_UDI, SERIE_CETES28], ANIO_INICIAL, anio_final)
    )
    faltantes = [s for s in (SERIE_UDI, SERIE_CETES28) if s not in series]
    if faltantes:
        raise ErrorBanxico(f"La exportación no trajo las series: {', '.join(faltantes)}")
    # Cada serie viene con su propio calendario; las fechas sin dato de una son de la otra.
    return DatosBanxico(
        udi={f: v for f, v in series[SERIE_UDI].items() if v is not None},
        cetes28={f: v for f, v in series[SERIE_CETES28].items() if v is not None},
    )


def metadatos(datos: DatosBanxico, validacion: Validacion) -> dict:
    return {
        "fuente": "Banco de México, Sistema de Información Económica (SIE)",
        "deslinde": "Cálculos propios con datos de Banxico y del INPC. No es un producto oficial "
        "del INEGI ni de Banco de México.",
        "series": {"udi": SERIE_UDI, "cetes28": SERIE_CETES28},
        "ultima_udi": max(datos.udi).isoformat(),
        "ultima_subasta_cetes28": max(datos.cetes28).isoformat(),
        "udi_contra_inpc": {
            "tramos": len(validacion.udi),
            "error_maximo": float(f"{validacion.error_maximo_udi:.2e}"),
            "dias_revisados": validacion.dias_revisados,
            "error_maximo_diario": float(f"{validacion.error_maximo_diario:.2e}"),
            "tolerancia": TOLERANCIA_UDI,
        },
        "origen": URL_SERIES,
    }


@dataclass(frozen=True)
class Resumen:
    validacion: Validacion
    ultima_udi: dt.date
    ultima_subasta: dt.date
    nuevas_udi: int
    nuevas_subastas: int


def actualizar(directorio: Path, cliente: ClienteBanxico | None = None) -> Resumen:
    """Descarga UDI y Cetes, los valida contra el INPC de ``directorio`` y los escribe."""
    if not (directorio / disco.ARCHIVO_MENSUAL).exists():
        raise ErrorBanxico(f"No hay datos nacionales en {directorio}; corre antes `actualizar`")
    nacional = disco.cargar(directorio)
    # La UDI se publica hasta el día 10 del mes siguiente: puede cruzar de año.
    anio_final = max(nacional.quincenal[COLUMNA_GENERAL]).anio + 1
    datos = descargar(cliente or ClienteBanxico(), anio_final)
    resultado = validar(datos, nacional)

    previos = cargar(directorio) if existe(directorio) else DatosBanxico({}, {})
    _sin_revisiones("UDI", previos.udi, datos.udi)
    _sin_revisiones("Cetes", previos.cetes28, datos.cetes28)

    guardar(directorio, datos)
    disco.escribir_metadatos(
        directorio / DIRECTORIO / ARCHIVO_METADATOS, metadatos(datos, resultado)
    )
    return Resumen(
        resultado,
        max(datos.udi),
        max(datos.cetes28),
        len(datos.udi) - len(previos.udi),
        len(datos.cetes28) - len(previos.cetes28),
    )


def verificar(directorio: Path) -> Validacion:
    """Valida ``data/banxico/`` contra el INPC de ``directorio``, sin red."""
    return validar(cargar(directorio), disco.cargar(directorio))
