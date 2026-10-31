"""Lectura de lo que devuelve el INEGI: árbol de series, exportación CSV y XLSX de ponderadores."""

from __future__ import annotations

import csv
import html
import io
import json
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass

import openpyxl

from .periodos import Periodo

_SERIE_EN_ARBOL = re.compile(r"ShowMoreInformation\('(\d+)','(\d+)','([^']*)'")
# Los temas (ciudades, subtemas) no son series: solo traen la clave y el título.
_TEMA_EN_ARBOL = re.compile(r'id="PT(\d+)"[^>]*>([^<]*)<')
_GENERICO = re.compile(r"^(\d{3})\s+(.+)$")
# Dos dígitos: un concepto en el árbol por objeto del gasto o una división en la CCIF.
_DOS_DIGITOS = re.compile(r"^\d{2}\s")
_GRUPO = re.compile(r"^\d{2}\.\d\s")
_CLASE = re.compile(r"^\d{2}\.\d\.\d\s")
_SIN_DATO = {"", "NA", "N/E", "ND"}

TITULO_GENERAL = "Índice general"


@dataclass(frozen=True)
class Nodo:
    """Una serie del árbol de la app "Índices de Precios" del INEGI."""

    id_serie: str
    clave: str
    titulo: str


@dataclass(frozen=True)
class Generico:
    """Un genérico del INPC tal como aparece en el árbol por objeto del gasto."""

    codigo: str
    nombre: str
    id_serie: str
    concepto: str


@dataclass(frozen=True)
class Ponderador:
    """Un renglón del XLSX oficial de ponderadores, con su ubicación en la CCIF 2018."""

    codigo: str
    generico: str
    division: str
    grupo: str
    clase: str
    durabilidad: str
    ponderador: float


def leer_arbol(respuesta: str | Mapping) -> list[Nodo]:
    """Extrae las series de la respuesta de ``ObtieneNodos`` (JSON con HTML en ``d``)."""
    datos = json.loads(respuesta) if isinstance(respuesta, str) else respuesta
    return [
        Nodo(id_serie, clave, html.unescape(titulo).strip())
        for id_serie, clave, titulo in _SERIE_EN_ARBOL.findall(datos["d"])
    ]


def leer_temas(respuesta: str | Mapping) -> dict[str, str]:
    """Temas del árbol (p. ej. las ciudades de "Por ciudad"), como ``{clave: titulo}``."""
    datos = json.loads(respuesta) if isinstance(respuesta, str) else respuesta
    return {
        clave: html.unescape(titulo).strip() for clave, titulo in _TEMA_EN_ARBOL.findall(datos["d"])
    }


def genericos_del_arbol(nodos: Iterable[Nodo]) -> tuple[str, dict[str, Generico]]:
    """Devuelve el id del índice general y los genéricos del árbol, indexados por código.

    El concepto de cada genérico es su nodo padre en el árbol (p. ej. ``01 Tortillas y
    derivados del maíz``); la clave jerárquica del padre es la del genérico sin los
    últimos cuatro dígitos.
    """
    nodos = list(nodos)
    por_clave = {nodo.clave: nodo for nodo in nodos}
    generales = [nodo for nodo in nodos if nodo.titulo == TITULO_GENERAL]
    if not generales:
        raise ValueError("El árbol no trae el índice general")

    genericos: dict[str, Generico] = {}
    for nodo in nodos:
        coincidencia = _GENERICO.match(nodo.titulo)
        if not coincidencia:
            continue
        codigo, nombre = coincidencia.groups()
        if codigo in genericos:
            raise ValueError(f"Genérico repetido en el árbol: {codigo}")
        padre = por_clave.get(nodo.clave[:-4])
        concepto = padre.titulo if padre and _DOS_DIGITOS.match(padre.titulo) else ""
        genericos[codigo] = Generico(codigo, nombre.strip(), nodo.id_serie, concepto)
    return generales[0].id_serie, genericos


def leer_exportacion(texto: str) -> dict[str, dict[Periodo, float | None]]:
    """Lee el CSV de ``Exportacion.aspx`` y devuelve ``{id_serie: {periodo: valor}}``.

    Las filas de metadatos se ignoran; la fila ``Fecha`` trae los ids de las series y las
    siguientes, una por periodo. ``NA``, ``N/E`` y ``ND`` se leen como ``None``.
    """
    filas = list(csv.reader(io.StringIO(texto)))
    try:
        inicio = next(i for i, fila in enumerate(filas) if fila and fila[0] == "Fecha")
    except StopIteration:
        raise ValueError("La exportación no trae la fila 'Fecha'") from None

    ids = [celda.strip() for celda in filas[inicio][1:] if celda.strip()]
    series: dict[str, dict[Periodo, float | None]] = {id_serie: {} for id_serie in ids}
    for fila in filas[inicio + 1 :]:
        if not fila or not fila[0].strip():
            continue
        periodo = Periodo.desde_etiqueta_inegi(fila[0])
        valores = fila[1 : len(ids) + 1]
        if len(valores) != len(ids):
            raise ValueError(f"La fila {fila[0]!r} no trae un valor por serie")
        for id_serie, valor in zip(ids, valores, strict=True):
            valor = valor.strip()
            series[id_serie][periodo] = None if valor in _SIN_DATO else float(valor)
    return series


def leer_ponderadores(contenido: bytes) -> list[Ponderador]:
    """Lee el XLSX "Ponderadores INPC segunda quincena de julio de 2024".

    La columna A trae división (``01``), grupo (``01.1``), clase (``01.1.1``) y genérico
    (``001 Arroz``); la B, la durabilidad; la C, el ponderador.
    """
    libro = openpyxl.load_workbook(io.BytesIO(contenido), read_only=True, data_only=True)
    try:
        hoja = libro.worksheets[0]
        division = grupo = clase = ""
        ponderadores = []
        for fila in hoja.iter_rows(values_only=True):
            texto = str(fila[0] or "").strip()
            if generico := _GENERICO.match(texto):
                codigo, nombre = generico.groups()
                ponderadores.append(
                    Ponderador(
                        codigo=codigo,
                        generico=nombre.strip(),
                        division=division,
                        grupo=grupo,
                        clase=clase,
                        durabilidad=str(fila[1] or "").strip(),
                        ponderador=float(fila[2]),
                    )
                )
            elif _CLASE.match(texto):
                clase = texto
            elif _GRUPO.match(texto):
                grupo, clase = texto, ""
            elif _DOS_DIGITOS.match(texto):
                division, grupo, clase = texto, "", ""
    finally:
        libro.close()
    if not ponderadores:
        raise ValueError("El XLSX no trae ponderadores por genérico")
    return ponderadores
