"""Datos para la web estática (``web/``): solo lo necesario para calcular en el navegador.

La web hace la misma entrevista y el mismo cálculo que ``bolsillometro entrevista``, con el mes
del gasto igual al último mes con datos. Para eso le bastan los últimos ``MESES`` meses de cada
serie (la inflación anual compara el último contra 12 antes, con margen por si las ciudades
van atrás del nacional), los ponderadores y su base, los rubros, el cuestionario y los Cetes.

Se escriben como scripts (``window.BOLSILLOMETRO_… = {...}``) y no como JSON para que la página
funcione también abierta directo desde el disco (``file://``), donde ``fetch`` no se permite.
Una ciudad se carga solo cuando la persona la elige.
"""

from __future__ import annotations

import json
import tomllib
from pathlib import Path

from . import banxico, ciudades
from . import datos as disco
from .cuestionario import CUESTIONARIO
from .datos import COLUMNA_GENERAL
from .indices import valores_en
from .periodos import Periodo
from .personal import cargar_rubros
from .reconstruccion import BASE_PONDERADORES

MESES = 15
DIRECTORIO_DATOS = "datos"
ARCHIVO_BASE = "base.js"
DIRECTORIO_CIUDADES = "ciudades"


def _js(variable: str, valor: object) -> str:
    texto = json.dumps(valor, ensure_ascii=False, separators=(",", ":"))
    return f"{variable}={texto};\n"


def _ultimo(serie) -> Periodo:
    return max(p for p, v in serie.items() if v is not None)


def periodos_web(nacional: disco.DatosINPC) -> list[Periodo]:
    ultimo = _ultimo(nacional.mensual[COLUMNA_GENERAL])
    return [ultimo.anterior(n) for n in range(MESES - 1, -1, -1)]


def base(directorio: Path) -> dict:
    """Todo lo que la web necesita salvo las ciudades."""
    nacional = disco.cargar(directorio)
    periodos = periodos_web(nacional)
    oficiales = {p.codigo: p.ponderador for p in nacional.ponderadores}
    base_oficial = valores_en({c: nacional.quincenal[c] for c in oficiales}, BASE_PONDERADORES)
    lista_ciudades = (
        [
            {"clave": c.clave, "nombre": ciudades.nombre_comun(c)}
            for c in ciudades.leer_catalogo(directorio)
        ]
        if (directorio / ciudades.DIRECTORIO).exists()
        else []
    )
    cetes = []
    if banxico.existe(directorio):
        desde = periodos[0].anterior(1)
        inicio = banxico.fin_de_mes(desde)
        cetes = [
            [fecha.isoformat(), tasa]
            for fecha, tasa in sorted(banxico.cargar(directorio).cetes28.items())
            if fecha >= inicio.replace(day=1)
        ]
    return {
        "version": 1,
        "fuente": "Cálculos propios con datos del INPC (Fuente: INEGI) y de Banxico.",
        "deslinde": "No es un producto oficial del INEGI ni de Banco de México.",
        "periodos": [str(p) for p in periodos],
        "nacional": {
            codigo: [serie.get(p) for p in periodos]
            for codigo, serie in sorted(nacional.mensual.items())
        },
        "ponderadores": oficiales,
        "base_oficial": base_oficial,
        "rubros": [
            {
                "clave": r.clave,
                "nombre": r.nombre,
                "genericos": list(r.genericos),
                "nacionales": sorted(r.nacionales),
            }
            for r in cargar_rubros().values()
        ],
        "cuestionario": tomllib.loads(CUESTIONARIO.read_text(encoding="utf-8")),
        "ciudades": lista_ciudades,
        "cetes": cetes,
    }


def exportar(directorio: Path, salida: Path) -> list[Path]:
    """Escribe ``salida/datos/``; devuelve los archivos escritos."""
    datos = base(directorio)
    periodos = [Periodo.desde_texto(p) for p in datos["periodos"]]
    carpeta = salida / DIRECTORIO_DATOS
    (carpeta / DIRECTORIO_CIUDADES).mkdir(parents=True, exist_ok=True)
    escritos = [carpeta / ARCHIVO_BASE]
    escritos[0].write_text(_js("window.BOLSILLOMETRO_BASE", datos), encoding="utf-8")
    if datos["ciudades"]:
        todas = ciudades.cargar(directorio)
        for entrada in datos["ciudades"]:
            clave = entrada["clave"]
            series = todas.series[clave]
            contenido = {
                codigo: [serie.get(p) for p in periodos] for codigo, serie in sorted(series.items())
            }
            ruta = carpeta / DIRECTORIO_CIUDADES / f"{clave}.js"
            ruta.write_text(
                "window.BOLSILLOMETRO_CIUDADES=window.BOLSILLOMETRO_CIUDADES||{};\n"
                + _js(f"window.BOLSILLOMETRO_CIUDADES[{json.dumps(clave)}]", contenido),
                encoding="utf-8",
            )
            escritos.append(ruta)
    return escritos
