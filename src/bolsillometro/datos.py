"""Formato en disco de ``data/``: CSV versionados, legibles en Excel y con diffs limpios."""

from __future__ import annotations

import csv
import json
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass, fields
from pathlib import Path

from .indices import Serie
from .lectura import Ponderador
from .periodos import Periodo

ARCHIVO_MENSUAL = "inpc_mensual.csv"
ARCHIVO_QUINCENAL = "inpc_quincenal.csv"
ARCHIVO_PONDERADORES = "ponderadores_2024.csv"
ARCHIVO_CATALOGO = "catalogo.csv"
ARCHIVO_METADATOS = "metadatos.json"
ARCHIVO_XLSX = Path("fuente") / "ponderadores_inpc_2q_jul_2024.xlsx"

COLUMNA_GENERAL = "general"


@dataclass(frozen=True)
class EntradaCatalogo:
    codigo: str
    generico: str
    concepto: str
    id_mensual: str
    id_quincenal: str


@dataclass
class DatosINPC:
    """Todo lo que el pipeline guarda: series, ponderadores y catálogo de ids del INEGI."""

    mensual: dict[str, dict[Periodo, float | None]]
    quincenal: dict[str, dict[Periodo, float | None]]
    ponderadores: list[Ponderador]
    catalogo: list[EntradaCatalogo]


def escribir_csv(ruta: Path, encabezado: list[str], filas: Iterable[list[str]]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo, lineterminator="\n")
        escritor.writerow(encabezado)
        escritor.writerows(filas)


def leer_csv(ruta: Path) -> list[dict[str, str]]:
    with ruta.open(encoding="utf-8", newline="") as archivo:
        return list(csv.DictReader(archivo))


def _formato(valor: float | None) -> str:
    # repr da la representación más corta que reproduce el float: 146.075, no 146.075000.
    return "" if valor is None else repr(valor)


def escribir_series(ruta: Path, series: Mapping[str, Serie]) -> None:
    """Formato ancho: una fila por periodo y una columna por serie (``general`` primero)."""
    columnas = [COLUMNA_GENERAL] + sorted(c for c in series if c != COLUMNA_GENERAL)
    periodos = sorted({p for serie in series.values() for p in serie})
    escribir_csv(
        ruta,
        ["periodo", *columnas],
        ([str(p), *(_formato(series[c].get(p)) for c in columnas)] for p in periodos),
    )


def leer_series(ruta: Path) -> dict[str, dict[Periodo, float | None]]:
    filas = leer_csv(ruta)
    if not filas:
        return {}
    series: dict[str, dict[Periodo, float | None]] = {c: {} for c in filas[0] if c != "periodo"}
    for fila in filas:
        periodo = Periodo.desde_texto(fila["periodo"])
        for columna, serie in series.items():
            serie[periodo] = float(fila[columna]) if fila[columna] else None
    return series


def escribir_ponderadores(ruta: Path, ponderadores: Iterable[Ponderador]) -> None:
    nombres = [campo.name for campo in fields(Ponderador)]
    escribir_csv(
        ruta,
        nombres,
        (
            [_formato(v) if isinstance(v, float) else v for v in asdict(p).values()]
            for p in ponderadores
        ),
    )


def leer_ponderadores(ruta: Path) -> list[Ponderador]:
    return [
        Ponderador(**{**fila, "ponderador": float(fila["ponderador"])}) for fila in leer_csv(ruta)
    ]


def escribir_catalogo(ruta: Path, catalogo: Iterable[EntradaCatalogo]) -> None:
    escribir_csv(
        ruta,
        [campo.name for campo in fields(EntradaCatalogo)],
        (list(asdict(entrada).values()) for entrada in catalogo),
    )


def leer_catalogo(ruta: Path) -> list[EntradaCatalogo]:
    return [EntradaCatalogo(**fila) for fila in leer_csv(ruta)]


def escribir_metadatos(ruta: Path, metadatos: Mapping) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    texto = json.dumps(metadatos, ensure_ascii=False, indent=2, sort_keys=True)
    ruta.write_text(texto + "\n", encoding="utf-8")


def leer_metadatos(ruta: Path) -> dict:
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}


def guardar(directorio: Path, datos: DatosINPC) -> None:
    escribir_series(directorio / ARCHIVO_MENSUAL, datos.mensual)
    escribir_series(directorio / ARCHIVO_QUINCENAL, datos.quincenal)
    escribir_ponderadores(directorio / ARCHIVO_PONDERADORES, datos.ponderadores)
    escribir_catalogo(directorio / ARCHIVO_CATALOGO, datos.catalogo)


def cargar(directorio: Path) -> DatosINPC:
    return DatosINPC(
        mensual=leer_series(directorio / ARCHIVO_MENSUAL),
        quincenal=leer_series(directorio / ARCHIVO_QUINCENAL),
        ponderadores=leer_ponderadores(directorio / ARCHIVO_PONDERADORES),
        catalogo=leer_catalogo(directorio / ARCHIVO_CATALOGO),
    )
