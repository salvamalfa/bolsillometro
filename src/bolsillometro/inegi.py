"""Cliente HTTP para la app "Índices de Precios" del INEGI (sin token).

Es la misma exportación que usan los archivos .IQY de Excel: ``GeneraIQY.aspx`` produce una
consulta web que hace un POST a ``Exportacion.aspx`` con estos mismos campos. No es una API
documentada, por eso el pipeline valida todo lo que descarga antes de escribirlo.
"""

from __future__ import annotations

from collections.abc import Iterable

from .red import ClienteHTTP, ErrorFuente

URL_APP = "https://www.inegi.org.mx/app/indicesdeprecios"
URL_ARBOL = f"{URL_APP}/servicios/ArbolAjaxInteraccion.asmx/ObtieneNodos"
URL_EXPORTACION = f"{URL_APP}/Exportacion.aspx"
URL_PONDERADORES = "https://www.inegi.org.mx/rnm/index.php/catalog/1015/download/32034"

ESTRUCTURA_MENSUAL = "112001700030"  # INPC nacional (mensual), por objeto del gasto
ESTRUCTURA_QUINCENAL = "112001600030"  # INPC nacional (quincenal), por objeto del gasto
ESTRUCTURA_CIUDADES = "112001700060"  # INPC por ciudad (mensual): 55 ciudades × 292 genéricos


class ErrorINEGI(ErrorFuente):
    """El INEGI respondió algo distinto de lo esperado."""


class ClienteINEGI(ClienteHTTP):
    Error = ErrorINEGI

    def obtener_arbol(self, estructura: str, timeout: float | None = None) -> dict:
        """Árbol de series de una estructura (ids, claves jerárquicas y títulos).

        El de "Por ciudad" pesa ~63 MB y el INEGI tarda unos 3 minutos en armarlo; para ese
        conviene un ``timeout`` mayor que el del cliente.
        """
        cuerpo = {
            "idNodo": estructura,
            "tituloPrincipal": "",
            "subTitulo": "",
            "esquemaBD": "",
            "paramfuente": "",
            "paramEstructura": estructura,
            "notas": [],
        }
        return self._pedir("POST", URL_ARBOL, timeout=timeout, json=cuerpo).json()

    def exportar(
        self, estructura: str, ids: Iterable[str], anio_inicial: int, anio_final: int
    ) -> str:
        """Niveles de las series ``ids`` entre dos años, como CSV ya decodificado."""
        formulario = {
            "idEstructura": estructura,
            "cuadro": estructura,
            "cvEstructura": estructura,
            "_formato": "CSV",
            "_anioI": str(anio_inicial),
            "_anioF": str(anio_final),
            "_meta": "0",
            "_tipo": "Niveles",
            "_info": "Índices",
            "_orient": "vertical",
            "pf": "inp",
            "st": "",
            "esquema": "",
            "_series": "c|" + "".join(f"{id_serie}," for id_serie in ids),
        }
        respuesta = self._pedir(
            "POST", URL_EXPORTACION, params={"INPtipoExporta": "CSV"}, data=formulario
        )
        if "text/csv" not in respuesta.headers.get("Content-Type", ""):
            raise ErrorINEGI("La exportación no devolvió un CSV")
        return respuesta.content.decode("cp1252")

    def descargar_ponderadores(self) -> bytes:
        """XLSX oficial "Ponderadores INPC segunda quincena de julio de 2024"."""
        contenido = self._pedir("GET", URL_PONDERADORES).content
        if not contenido.startswith(b"PK"):
            raise ErrorINEGI("La descarga de ponderadores no es un XLSX")
        return contenido
