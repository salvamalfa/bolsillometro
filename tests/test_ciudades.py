"""INPC por ciudad: lectura del árbol, validaciones y pipeline sin red."""

import filecmp
from pathlib import Path

import pytest

from bolsillometro import ciudades
from bolsillometro import datos as disco
from bolsillometro.ciudades import (
    Ciudad,
    DatosCiudades,
    ErrorCiudades,
    acotamiento,
    ciudades_del_arbol,
    clave_ciudad,
)
from bolsillometro.inegi import ESTRUCTURA_CIUDADES
from bolsillometro.periodos import Periodo

DATOS = Path(__file__).resolve().parents[1] / "data"


def _tema(clave, titulo):
    return f'<td id="PT{clave}">{titulo}</a></td>'


def _serie(id_serie, clave, titulo):
    return (
        f'<td>{titulo}</td><button onclick="ShowMoreInformation('
        f"'{id_serie}','{clave}','{titulo}','');\">"
    )


def _arbol_ciudad(clave_tema, titulo, id_general, genericos, con_scian=False):
    """HTML de una ciudad: tema, subtema por objeto del gasto y sus genéricos."""
    og = clave_tema + "0010"
    partes = [
        _tema(clave_tema, titulo),
        _tema(og, "Índice de precios al consumidor, por objeto del gasto"),
        _tema(og + "0010", "Índice general"),
        _serie(id_general, og + "0010", "Índice general"),
        _serie(f"{id_general}0", og + "00100010", "01 Concepto"),
    ]
    for i, (codigo, nombre, id_serie) in enumerate(genericos, start=1):
        partes.append(_serie(id_serie, f"{og}00100010{i:04d}", f"{codigo} {nombre}"))
    if con_scian:
        scian = clave_tema + "0020"
        partes += [
            _tema(scian, "Índice de precios al consumidor, por origen de los bienes (SCIAN 2018)"),
            _serie(f"{id_general}9", scian + "0010", "Índice general"),
            _serie(f"{id_general}8", scian + "00100010", "111 Agricultura"),
        ]
    return "".join(partes)


def test_clave_ciudad():
    assert clave_ciudad("Pachuca, Hgo.") == "pachuca"
    assert clave_ciudad("Cd. Juárez, Chih.") == "cd-juarez"
    assert clave_ciudad("Veracruz,Ver.") == "veracruz"
    assert clave_ciudad("San Andrés Tuxtla, Ver.") == "san-andres-tuxtla"
    assert clave_ciudad("7. Area Metropolitana de la Cd. de México") == "cdmx"


def test_ciudades_del_arbol_usa_solo_el_subtema_por_objeto_del_gasto():
    genericos = [("014", "Tortilla de maíz", "2"), ("138", "Renta de vivienda", "3")]
    arbol = {
        "d": _arbol_ciudad(ESTRUCTURA_CIUDADES + "0360", "Pachuca, Hgo.", "886350", genericos)
        + _arbol_ciudad(
            ESTRUCTURA_CIUDADES + "0330",
            "Monterrey, N.L.",
            "884954",
            [("014", "Tortilla de maíz", "5"), ("138", "Renta de vivienda", "6")],
            con_scian=True,
        )
    }
    resultado = ciudades_del_arbol(arbol)
    assert [ciudad for ciudad, _ in resultado] == [
        Ciudad("monterrey", "Monterrey, N.L.", ESTRUCTURA_CIUDADES + "0330", "884954"),
        Ciudad("pachuca", "Pachuca, Hgo.", ESTRUCTURA_CIUDADES + "0360", "886350"),
    ]
    assert {c: g.id_serie for c, g in resultado[0][1].items()} == {"014": "5", "138": "6"}


def test_nombre_comun():
    assert (
        ciudades.nombre_comun(Ciudad("cdmx", "Area Metropolitana de la Cd. de México", "", ""))
        == "la Ciudad de México"
    )
    assert ciudades.nombre_comun(Ciudad("pachuca", "Pachuca, Hgo.", "", "")) == "Pachuca, Hgo."


def test_ciudades_del_arbol_falla_sin_subtema():
    arbol = {"d": _tema(ESTRUCTURA_CIUDADES + "0360", "Pachuca, Hgo.")}
    with pytest.raises(ErrorCiudades, match="objeto del gasto"):
        ciudades_del_arbol(arbol)


A = Periodo(2020, 1)
B = Periodo(2020, 2)


def _nacional(series):
    return disco.DatosINPC(mensual=series, quincenal={}, ponderadores=[], catalogo=[])


def _ciudades(por_ciudad):
    lista = [Ciudad(clave, clave, "", "") for clave in por_ciudad]
    return DatosCiudades(lista, por_ciudad)


def test_acotamiento_detecta_un_nacional_fuera_del_rango():
    locales = _ciudades(
        {
            "x": {"general": {A: 100.0}, "001": {A: 100.0, B: 102.0}},
            "y": {"general": {A: 100.0}, "001": {A: 104.0, B: 106.0}},
        }
    )
    dentro = _nacional({"general": {A: 1.0}, "001": {A: 103.0, B: 106.0005}})
    assert acotamiento(locales, dentro) == (2, [])
    fuera = _nacional({"general": {A: 1.0}, "001": {A: 103.0, B: 106.1}})
    assert acotamiento(locales, fuera) == (2, [("001", B)])


# --- con los datos reales de data/ -----------------------------------------------------------


@pytest.fixture(scope="module")
def reales():
    return ciudades.cargar(DATOS)


@pytest.fixture(scope="module")
def nacional():
    return disco.cargar(DATOS)


def test_hay_55_ciudades_con_292_genericos(reales, nacional):
    assert len(reales.ciudades) == 55
    for ciudad in reales.ciudades:
        assert set(reales.series[ciudad.clave]) == set(nacional.mensual), ciudad.clave


def _primero(serie):
    return min(p for p, v in serie.items() if v is not None)


def test_valores_publicados_conocidos(reales):
    pachuca = reales.series["pachuca"]
    assert pachuca["general"][Periodo(2026, 9)] == 146.636
    # Pachuca entró al INPC con la base 2018; las ciudades anteriores traen desde enero.
    assert _primero(pachuca["general"]) == Periodo(2018, 7)
    assert _primero(reales.series["cdmx"]["general"]) == Periodo(2018, 1)


def test_los_datos_por_ciudad_pasan_la_validacion(reales, nacional):
    validacion = ciudades.validar(reales, nacional)
    assert validacion.cumple
    assert validacion.fuera_de_rango == []
    assert validacion.revisiones_acotamiento > 800_000 // 55


def test_genericos_que_ya_no_se_cotizan_en_pachuca(reales):
    # Desde la canasta 2024 Pachuca ya no tiene gas natural ni metro: se usa el nacional.
    faltan = ciudades.sin_dato_reciente(reales)
    assert {"146", "221"} <= set(faltan["pachuca"])


def test_un_id_cruzado_rompe_el_acotamiento(reales, nacional):
    # Si la tortilla de Pachuca se leyera como su renta, el nacional quedaría fuera de rango.
    series = {clave: dict(s) for clave, s in reales.series.items()}
    for clave in series:
        series[clave]["014"], series[clave]["138"] = series[clave]["138"], series[clave]["014"]
    cruzados = DatosCiudades(reales.ciudades, series)
    with pytest.raises(ErrorCiudades, match="fuera del rango"):
        ciudades.validar(cruzados, nacional)


def _sin_ultimo_mes(reales, claves=None):
    """Copia de las ciudades sin su último mes (todas, o solo las de ``claves``)."""
    ultimo = ciudades.ultimo_mes(reales)
    series = {}
    for clave, propias in reales.series.items():
        if claves is None or clave in claves:
            propias = {
                codigo: {p: v for p, v in serie.items() if p != ultimo}
                for codigo, serie in propias.items()
            }
        series[clave] = propias
    return DatosCiudades(reales.ciudades, series)


def _nacional_hasta(nacional, hasta):
    """Copia del nacional sin los meses (ni sus quincenas) posteriores a ``hasta``."""
    limite = Periodo(hasta.anio, hasta.mes, 2)
    return disco.DatosINPC(
        mensual={
            c: {p: v for p, v in s.items() if p <= hasta} for c, s in nacional.mensual.items()
        },
        quincenal={
            c: {p: v for p, v in s.items() if p <= limite} for c, s in nacional.quincenal.items()
        },
        ponderadores=nacional.ponderadores,
        catalogo=nacional.catalogo,
    )


def test_falla_si_una_ciudad_no_llega_al_ultimo_mes(reales, nacional):
    with pytest.raises(ErrorCiudades, match="Pachuca"):
        ciudades.validar(_sin_ultimo_mes(reales, {"pachuca"}), nacional)


def test_las_ciudades_pueden_ir_atras_del_nacional(reales, nacional):
    # Así queda data/ entre el paso nacional del workflow y el de ciudades.
    atrasadas = _sin_ultimo_mes(reales)
    assert ciudades.ultimo_mes(atrasadas) < max(nacional.mensual["general"])
    assert ciudades.validar(atrasadas, nacional).cumple


def test_falla_si_las_ciudades_van_adelante_del_nacional(reales, nacional):
    ultimo = ciudades.ultimo_mes(reales)
    with pytest.raises(ErrorCiudades, match="después que el nacional"):
        ciudades.validar(reales, _nacional_hasta(nacional, ultimo.anterior()))


def test_metadatos_coinciden_con_los_datos(reales):
    metadatos = ciudades.leer_metadatos(DATOS)
    assert metadatos["ciudades"] == len(reales.ciudades)
    general = reales.series["pachuca"]["general"]
    assert metadatos["ultimo_mensual"] == str(max(p for p, v in general.items() if v is not None))
    assert metadatos["acotamiento"]["fuera_de_rango"] == 0


# --- pipeline sin red ----------------------------------------------------------------------


def _titulo(ciudad):
    """Título de la ciudad en el árbol del INEGI (la CDMX lleva número)."""
    return "7. " + ciudad.nombre if ciudad.clave == "cdmx" else ciudad.nombre


class ClienteFalso:
    """Sirve el árbol "Por ciudad" y sus exportaciones a partir de ``data/ciudades/``."""

    def __init__(self, reales, nacional, cruzar=False, otra_ciudad=False):
        self.reales = reales
        self.nacional = nacional
        self.cruzar = cruzar  # sirve los valores de cada genérico con el id de otro
        self.otra_ciudad = otra_ciudad  # el título de la exportación nombra otra ciudad
        self.ids = {}  # id de serie → (clave de ciudad, código)

    def obtener_arbol(self, estructura, timeout=None):
        assert estructura == ESTRUCTURA_CIUDADES
        partes = []
        nombres = {e.codigo: e.generico for e in self.nacional.catalogo}
        for ciudad in self.reales.ciudades:
            self.ids[ciudad.id_general] = (ciudad.clave, "general")
            genericos = []
            for codigo in sorted(self.reales.series[ciudad.clave]):
                if codigo == "general":
                    continue
                id_serie = f"{ciudad.id_general}{codigo}"
                self.ids[id_serie] = (ciudad.clave, codigo)
                genericos.append((codigo, nombres[codigo], id_serie))
            partes.append(
                _arbol_ciudad(ciudad.id_nodo, _titulo(ciudad), ciudad.id_general, genericos)
            )
        return {"d": "".join(partes)}

    def exportar(self, estructura, ids, anio_inicial, anio_final):
        ids = list(ids)
        clave = self.ids[ids[0]][0]
        series = self.reales.series[clave]
        periodos = [Periodo(2018, mes) for mes in range(1, 7)] + sorted(series["general"])
        fuente = [ids[0], *reversed(ids[1:])] if self.cruzar else ids
        ciudad = next(c for c in self.reales.ciudades if c.clave == clave)
        if self.otra_ciudad:
            ciudad = next(c for c in self.reales.ciudades if c.clave != clave)
        titulo = f"INPC (mensual), Por ciudad, {_titulo(ciudad)}, Índice general"
        lineas = [
            '"Instituto Nacional de Estadística y Geografía",',
            "",
            f'"Título","{titulo}"' + ',"…"' * (len(ids) - 1),
            '"Fecha","' + '","'.join(ids) + '"',
        ]
        for periodo in periodos:
            valores = []
            for id_serie in fuente:
                valor = series[self.ids[id_serie][1]].get(periodo)
                valores.append("N/E" if valor is None else repr(valor))
            lineas.append(f'"{periodo.etiqueta_inegi()}","' + '","'.join(valores) + '"')
        return "\n".join(lineas) + "\n"


def _copiar_nacional(destino, reales, nacional):
    """Escribe el nacional hasta el último mes de las ciudades, como cuando se publican juntos.

    Así las pruebas del pipeline también pasan cuando ``data/`` ya trae un mes nacional que
    las ciudades todavía no (entre los dos pasos del workflow).
    """
    disco.guardar(destino, _nacional_hasta(nacional, ciudades.ultimo_mes(reales)))


def test_actualizar_regenera_data_ciudades_byte_por_byte(tmp_path, reales, nacional):
    _copiar_nacional(tmp_path, reales, nacional)
    resumen = ciudades.actualizar(tmp_path, ClienteFalso(reales, nacional))
    assert resumen.validacion.cumple
    assert resumen.nuevos[0] == Periodo(2018, 1)
    comparar = filecmp.dircmp(tmp_path / ciudades.DIRECTORIO, DATOS / ciudades.DIRECTORIO)
    assert comparar.left_only == comparar.right_only == []
    _, distintos, errores = filecmp.cmpfiles(
        tmp_path / ciudades.DIRECTORIO,
        DATOS / ciudades.DIRECTORIO,
        comparar.common_files,
        shallow=False,
    )
    assert distintos == errores == []


def test_actualizar_no_escribe_nada_si_falla(tmp_path, reales, nacional):
    _copiar_nacional(tmp_path, reales, nacional)
    with pytest.raises(ErrorCiudades):
        ciudades.actualizar(tmp_path, ClienteFalso(reales, nacional, cruzar=True))
    assert not (tmp_path / ciudades.DIRECTORIO).exists()


def test_actualizar_falla_si_la_exportacion_es_de_otra_ciudad(tmp_path, reales, nacional):
    _copiar_nacional(tmp_path, reales, nacional)
    with pytest.raises(ErrorCiudades, match="título"):
        ciudades.actualizar(tmp_path, ClienteFalso(reales, nacional, otra_ciudad=True))
    assert not (tmp_path / ciudades.DIRECTORIO).exists()


def test_actualizar_no_guarda_una_descarga_atrasada(tmp_path, reales, nacional):
    _copiar_nacional(tmp_path, reales, nacional)
    with pytest.raises(ErrorCiudades, match="descarga por ciudad"):
        ciudades.actualizar(tmp_path, ClienteFalso(_sin_ultimo_mes(reales), nacional))
    assert not (tmp_path / ciudades.DIRECTORIO).exists()


def test_actualizar_pide_los_datos_nacionales(tmp_path, reales, nacional):
    with pytest.raises(ErrorCiudades, match="nacionales"):
        ciudades.actualizar(tmp_path, ClienteFalso(reales, nacional))
