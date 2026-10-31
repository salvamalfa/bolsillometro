import io

import openpyxl
import pytest

from bolsillometro.inegi import ClienteINEGI, ErrorINEGI
from bolsillometro.lectura import (
    genericos_del_arbol,
    leer_arbol,
    leer_exportacion,
    leer_ponderadores,
    leer_temas,
)
from bolsillometro.periodos import Periodo

EXPORTACION = (
    '"Instituto Nacional de Estadística y Geografía",\n'
    '"",\n'
    '"",\n'
    '"Fecha de consulta: 26/10/2026 13:44:16",\n'
    "\n"
    '"Título","Índice general","014 Tortilla de maíz","002 Botanas"\n'
    '"Cifra","","",""\n'
    '"Fecha","865586","865594","865591"\n'
    '"Jun 2018","99.375","98.5","N/E"\n'
    '"Ago 2024","136.013000000000","150.100000000000","NA"\n'
    '"Sep 2026","146.075000000000","163.374000000000","186.169000000000"\n'
)


def _nodo(id_serie, clave, titulo):
    return (
        f'<td>{titulo}</td><button onclick="javascript:ShowMoreInformation('
        f"'{id_serie}','{clave}','{titulo}','');\"></button>"
    )


ARBOL = {
    "d": "".join(
        [
            _nodo("865586", "11200170003000100010", "Índice general"),
            _nodo("865587", "112001700030001000100010", "1. Alimentos, bebidas y tabaco"),
            _nodo("865590", "1120017000300010001000100010", "01 Tortillas y derivados del maíz"),
            _nodo(
                "865591", "11200170003000100010001000100010", "002 Botanas elaboradas con cereales"
            ),
            _nodo("865594", "11200170003000100010001000100020", "014 Tortilla de maíz"),
            _nodo(
                "865602", "1120017000300010001000100020", "03 Galletas, pastas y harinas de trigo"
            ),
            _nodo("865603", "11200170003000100010001000200010", "004 Galletas"),
            _nodo("865604", "112001700030001000100010002000100010", "Galletas dulces */"),
            _nodo("866154", "11200170003000300010", "No duradero"),
        ]
    )
}


def test_leer_exportacion():
    series = leer_exportacion(EXPORTACION)
    assert set(series) == {"865586", "865594", "865591"}
    assert series["865586"][Periodo(2026, 9)] == 146.075
    assert series["865594"][Periodo(2018, 6)] == 98.5
    assert series["865591"][Periodo(2018, 6)] is None
    assert series["865591"][Periodo(2024, 8)] is None
    assert list(series["865586"]) == [Periodo(2018, 6), Periodo(2024, 8), Periodo(2026, 9)]


def test_leer_exportacion_quincenal():
    texto = '"Fecha","821908"\n"2Q Jul 2024","136.095"\n"1Q Ago 2024","135.997"\n'
    serie = leer_exportacion(texto)["821908"]
    assert serie == {Periodo(2024, 7, 2): 136.095, Periodo(2024, 8, 1): 135.997}


def test_leer_exportacion_por_ciudad_trae_nd():
    texto = '"Fecha","886350","886573"\n"Jun 2024","140.1","ND"\n"Ago 2024","141.2","N/E"\n'
    series = leer_exportacion(texto)
    assert series["886350"] == {Periodo(2024, 6): 140.1, Periodo(2024, 8): 141.2}
    assert set(series["886573"].values()) == {None}


def test_leer_exportacion_sin_fila_fecha():
    with pytest.raises(ValueError, match="Fecha"):
        leer_exportacion('"Instituto Nacional de Estadística y Geografía",\n')


def test_arbol_genericos_y_conceptos():
    id_general, genericos = genericos_del_arbol(leer_arbol(ARBOL))
    assert id_general == "865586"
    # Los subgenéricos ("*/") y los agregados no son genéricos.
    assert sorted(genericos) == ["002", "004", "014"]
    tortilla = genericos["014"]
    assert tortilla.nombre == "Tortilla de maíz"
    assert tortilla.id_serie == "865594"
    assert tortilla.concepto == "01 Tortillas y derivados del maíz"
    assert genericos["004"].concepto == "03 Galletas, pastas y harinas de trigo"


def test_leer_temas():
    arbol = {
        "d": '<td class="EstiloTexto" id="PT1120017000600360">Pachuca, Hgo.</a></td>'
        '<td id="PT11200170006003600010">Índice de precios al consumidor, '
        "por objeto del gasto</a></td>"
    }
    assert leer_temas(arbol) == {
        "1120017000600360": "Pachuca, Hgo.",
        "11200170006003600010": "Índice de precios al consumidor, por objeto del gasto",
    }
    assert leer_temas(ARBOL) == {}


def test_arbol_genericos_repetidos():
    nodos = leer_arbol(ARBOL)
    with pytest.raises(ValueError, match="repetido"):
        genericos_del_arbol(nodos + nodos[-5:-4])


def _xlsx_ponderadores() -> bytes:
    libro = openpyxl.Workbook()
    hoja = libro.active
    for fila in [
        ("Canasta del INPC clasificada por la CCIF 2018", None, None),
        ("Canasta del INPC clasificada de acuerdo con la CCIF", "Durabilidad", "Ponderador"),
        ("01 Alimentos y bebidas no alcohólicas", None, 60.0),
        ("01.1 Alimentos", None, 60.0),
        ("01.1.1 Cereales y productos a base de cereales", None, 60.0),
        ("001 Arroz", "No duradero", 0.1891),
        ("014 Tortilla de maíz", "No duradero", 59.8109),
        ("04 Vivienda, agua, electricidad, gas y otros combustibles", None, 40.0),
        ("04.1 Alquileres efectivos de la vivienda", None, 40.0),
        ("04.1.1 Alquileres efectivos pagados por los inquilinos", None, 40.0),
        ("138 Renta de vivienda", "Servicio", 40.0),
        (None, "Total general", 100),
    ]:
        hoja.append(fila)
    salida = io.BytesIO()
    libro.save(salida)
    return salida.getvalue()


def test_leer_ponderadores():
    ponderadores = leer_ponderadores(_xlsx_ponderadores())
    assert [p.codigo for p in ponderadores] == ["001", "014", "138"]
    arroz, _, renta = ponderadores
    assert arroz.generico == "Arroz"
    assert arroz.division == "01 Alimentos y bebidas no alcohólicas"
    assert arroz.grupo == "01.1 Alimentos"
    assert arroz.clase == "01.1.1 Cereales y productos a base de cereales"
    assert arroz.durabilidad == "No duradero"
    assert arroz.ponderador == 0.1891
    assert renta.division.startswith("04 ")
    assert renta.clase.startswith("04.1.1 ")
    assert sum(p.ponderador for p in ponderadores) == pytest.approx(100)


class _Respuesta:
    def __init__(self, contenido: bytes, tipo: str, estado: int = 200):
        self.content = contenido
        self.headers = {"Content-Type": tipo}
        self.status_code = estado

    def raise_for_status(self):
        pass


class _Sesion:
    def __init__(self, respuesta):
        self.headers = {}
        self.respuesta = respuesta
        self.peticiones = []

    def request(self, metodo, url, **kwargs):
        self.peticiones.append((metodo, url, kwargs))
        return self.respuesta


def test_cliente_exportar_decodifica_cp1252():
    sesion = _Sesion(_Respuesta(EXPORTACION.encode("cp1252"), "text/csv; charset=Windows-1252"))
    texto = ClienteINEGI(sesion).exportar("112001700030", ["865586", "865594"], 2018, 2026)
    assert "Estadística" in texto
    metodo, _, kwargs = sesion.peticiones[0]
    assert metodo == "POST"
    assert kwargs["params"] == {"INPtipoExporta": "CSV"}
    assert kwargs["data"]["_series"] == "c|865586,865594,"
    assert kwargs["data"]["_anioI"] == "2018"


def test_cliente_exportar_rechaza_html():
    sesion = _Sesion(_Respuesta(b"<html></html>", "text/html; charset=utf-8"))
    with pytest.raises(ErrorINEGI):
        ClienteINEGI(sesion).exportar("112001700030", ["865586"], 2018, 2026)


def test_cliente_reintenta_errores_del_servidor():
    sesion = _Sesion(_Respuesta(b"", "text/html", estado=500))
    with pytest.raises(ErrorINEGI, match="3 intentos"):
        ClienteINEGI(sesion, espera=0).descargar_ponderadores()
    assert len(sesion.peticiones) == 3
