"""Pipeline de la fase 0: descargar del INEGI, validar y escribir ``data/``.

Nada se escribe si la validación falla: si el INEGI cambia algo (estructura, ids, formato),
el pipeline se rompe de forma visible en lugar de guardar datos corruptos.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from . import datos as disco
from .datos import COLUMNA_GENERAL, DatosINPC, EntradaCatalogo
from .inegi import (
    ESTRUCTURA_MENSUAL,
    ESTRUCTURA_QUINCENAL,
    URL_EXPORTACION,
    URL_PONDERADORES,
    ClienteINEGI,
)
from .lectura import (
    Generico,
    genericos_del_arbol,
    leer_arbol,
    leer_exportacion,
    leer_ponderadores,
)
from .periodos import Periodo
from .reconstruccion import (
    BASE_PONDERADORES,
    Comparacion,
    error_maximo,
    factor_encadenamiento,
    reconstruir_inpc,
)

ANIO_INICIAL = 2018
GENERICOS_ESPERADOS = 292


class ErrorValidacion(RuntimeError):
    """Los datos descargados no pasan las validaciones."""


@dataclass(frozen=True)
class Reconstruccion:
    mensual: list[Comparacion]
    quincenal: list[Comparacion]

    @property
    def cumple(self) -> bool:
        return all(c.cumple for c in self.mensual + self.quincenal)


@dataclass(frozen=True)
class Resumen:
    reconstruccion: Reconstruccion
    nuevos_mensual: list[Periodo]
    nuevos_quincenal: list[Periodo]


def _validar_genericos(nombre: str, genericos: Mapping[str, Generico]) -> None:
    if len(genericos) != GENERICOS_ESPERADOS:
        raise ErrorValidacion(
            f"El árbol {nombre} trae {len(genericos)} genéricos; se esperaban {GENERICOS_ESPERADOS}"
        )


def _series_por_codigo(
    texto_csv: str, id_general: str, genericos: Mapping[str, Generico]
) -> dict[str, dict[Periodo, float | None]]:
    por_id = leer_exportacion(texto_csv)
    ids = {COLUMNA_GENERAL: id_general} | {c: g.id_serie for c, g in genericos.items()}
    faltantes = [codigo for codigo, id_serie in ids.items() if id_serie not in por_id]
    if faltantes:
        raise ErrorValidacion(f"La exportación no trajo las series: {', '.join(faltantes)}")
    return {codigo: por_id[id_serie] for codigo, id_serie in ids.items()}


def descargar(
    cliente: ClienteINEGI | None = None, anio_final: int | None = None
) -> tuple[DatosINPC, bytes]:
    """Descarga genéricos nacionales (mensual y quincenal) y ponderadores 2024."""
    cliente = cliente or ClienteINEGI()
    anio_final = anio_final or dt.date.today().year

    general_m, genericos_m = genericos_del_arbol(
        leer_arbol(cliente.obtener_arbol(ESTRUCTURA_MENSUAL))
    )
    general_q, genericos_q = genericos_del_arbol(
        leer_arbol(cliente.obtener_arbol(ESTRUCTURA_QUINCENAL))
    )
    _validar_genericos("mensual", genericos_m)
    _validar_genericos("quincenal", genericos_q)
    if genericos_m.keys() != genericos_q.keys():
        raise ErrorValidacion("Los árboles mensual y quincenal no traen los mismos genéricos")

    xlsx = cliente.descargar_ponderadores()
    ponderadores = leer_ponderadores(xlsx)
    codigos_ponderadores = {p.codigo for p in ponderadores}
    if len(ponderadores) != GENERICOS_ESPERADOS or codigos_ponderadores != genericos_m.keys():
        raise ErrorValidacion("Los genéricos del XLSX de ponderadores no coinciden con el árbol")
    suma = sum(p.ponderador for p in ponderadores)
    if abs(suma - 100) > 0.01:
        raise ErrorValidacion(f"Los ponderadores suman {suma}, no 100")

    def exportar(estructura: str, id_general: str, genericos: Mapping[str, Generico]):
        ids = [id_general, *(g.id_serie for g in genericos.values())]
        texto = cliente.exportar(estructura, ids, ANIO_INICIAL, anio_final)
        return _series_por_codigo(texto, id_general, genericos)

    catalogo = [
        EntradaCatalogo(COLUMNA_GENERAL, "Índice general", "", general_m, general_q),
        *(
            EntradaCatalogo(c, g.nombre, g.concepto, g.id_serie, genericos_q[c].id_serie)
            for c, g in sorted(genericos_m.items())
        ),
    ]
    datos = DatosINPC(
        mensual=exportar(ESTRUCTURA_MENSUAL, general_m, genericos_m),
        quincenal=exportar(ESTRUCTURA_QUINCENAL, general_q, genericos_q),
        ponderadores=ponderadores,
        catalogo=catalogo,
    )
    return datos, xlsx


def reconstruir(datos: DatosINPC) -> Reconstruccion:
    return Reconstruccion(
        mensual=reconstruir_inpc(datos.mensual, datos.quincenal, datos.ponderadores),
        quincenal=reconstruir_inpc(datos.quincenal, datos.quincenal, datos.ponderadores),
    )


def validar(datos: DatosINPC) -> Reconstruccion:
    """Reconstruye el INPC y falla si algún periodo difiere más de una milésima."""
    resultado = reconstruir(datos)
    if not resultado.mensual or not resultado.quincenal:
        raise ErrorValidacion("No hay periodos que reconstruir desde agosto de 2024")
    fallas = [c for c in resultado.mensual + resultado.quincenal if not c.cumple]
    if fallas:
        detalle = ", ".join(f"{c.periodo} ({c.diferencia:+.3f})" for c in fallas[:5])
        raise ErrorValidacion(f"La reconstrucción del INPC no cuadra en: {detalle}")
    return resultado


def _ultimo(serie: Mapping[Periodo, float | None]) -> Periodo:
    return max(p for p, v in serie.items() if v is not None)


def metadatos(datos: DatosINPC, resultado: Reconstruccion) -> dict:
    """Metadatos sin fechas de descarga: solo cambian cuando cambian los datos."""
    return {
        "fuente": "INEGI, Índice Nacional de Precios al Consumidor (INPC)",
        "deslinde": "Cálculos propios con datos del INPC. No es un producto oficial del "
        "INEGI ni de Banco de México.",
        "ultimo_mensual": str(_ultimo(datos.mensual[COLUMNA_GENERAL])),
        "ultimo_quincenal": str(_ultimo(datos.quincenal[COLUMNA_GENERAL])),
        "base_ponderadores": str(BASE_PONDERADORES),
        "inpc_base_ponderadores": datos.quincenal[COLUMNA_GENERAL][BASE_PONDERADORES],
        "factor_encadenamiento": round(factor_encadenamiento(datos.quincenal), 8),
        "reconstruccion": {
            "mensual": {
                "periodos": len(resultado.mensual),
                "error_maximo": error_maximo(resultado.mensual),
            },
            "quincenal": {
                "periodos": len(resultado.quincenal),
                "error_maximo": error_maximo(resultado.quincenal),
            },
        },
        "origen": {
            "exportacion": URL_EXPORTACION,
            "estructura_mensual": ESTRUCTURA_MENSUAL,
            "estructura_quincenal": ESTRUCTURA_QUINCENAL,
            "ponderadores": URL_PONDERADORES,
        },
    }


def _periodos(serie: Mapping[Periodo, float | None]) -> set[Periodo]:
    return {p for p, v in serie.items() if v is not None}


def actualizar(directorio: Path, cliente: ClienteINEGI | None = None) -> Resumen:
    """Descarga, valida y escribe ``directorio``. Devuelve los periodos nuevos."""
    datos, xlsx = descargar(cliente)
    resultado = validar(datos)

    previos_m: set[Periodo] = set()
    previos_q: set[Periodo] = set()
    ruta_xlsx = directorio / disco.ARCHIVO_XLSX
    ponderadores_previos = None
    if (directorio / disco.ARCHIVO_MENSUAL).exists():
        anteriores = disco.cargar(directorio)
        previos_m = _periodos(anteriores.mensual.get(COLUMNA_GENERAL, {}))
        previos_q = _periodos(anteriores.quincenal.get(COLUMNA_GENERAL, {}))
        ponderadores_previos = anteriores.ponderadores

    disco.guardar(directorio, datos)
    disco.escribir_metadatos(directorio / disco.ARCHIVO_METADATOS, metadatos(datos, resultado))
    # El XLSX se reescribe solo si cambió su contenido, para no generar diffs binarios vacíos.
    if not ruta_xlsx.exists() or ponderadores_previos != datos.ponderadores:
        ruta_xlsx.parent.mkdir(parents=True, exist_ok=True)
        ruta_xlsx.write_bytes(xlsx)

    return Resumen(
        reconstruccion=resultado,
        nuevos_mensual=sorted(_periodos(datos.mensual[COLUMNA_GENERAL]) - previos_m),
        nuevos_quincenal=sorted(_periodos(datos.quincenal[COLUMNA_GENERAL]) - previos_q),
    )


def verificar(directorio: Path) -> Reconstruccion:
    """Reconstruye el INPC con los datos locales, sin red."""
    return reconstruir(disco.cargar(directorio))
