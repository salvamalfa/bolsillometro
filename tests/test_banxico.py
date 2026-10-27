"""UDI y Cetes de Banxico: lectura, validación contra el INPC, rendimientos y pipeline sin red."""

import datetime as dt
import filecmp
from pathlib import Path

import pytest

from bolsillometro import banxico
from bolsillometro import datos as disco
from bolsillometro.banxico import (
    ClienteBanxico,
    DatosBanxico,
    ErrorBanxico,
    consistencia_udi,
    leer_exportacion,
    rendimiento_cetes,
    tramo_udi,
    variacion_udi,
)
from bolsillometro.periodos import Periodo

DATOS = Path(__file__).resolve().parents[1] / "data"
D = dt.date

EXPORTACION = (
    "\n"
    '"Banco de México"\n'
    "\n"
    '"Fecha de consulta: 27/10/2026 08:22:04"\n'
    '"Título","Valor de UDIS","Tasa de rendimiento Cetes a 28 días"\n'
    '"Periodicidad","Diaria","Diaria"\n'
    '"Fecha","SP68257","SF43936"\n'
    "21/10/2026,8.871234,N/E\n"
    "22/10/2026,8.872000,6.23\n"
    "23/10/2026,8.872766,\n"
)


def test_leer_exportacion():
    series = leer_exportacion(EXPORTACION)
    assert series["SP68257"] == {
        D(2026, 10, 21): 8.871234,
        D(2026, 10, 22): 8.872,
        D(2026, 10, 23): 8.872766,
    }
    assert series["SF43936"] == {
        D(2026, 10, 21): None,
        D(2026, 10, 22): 6.23,
        D(2026, 10, 23): None,
    }


def test_leer_exportacion_sin_fila_fecha():
    with pytest.raises(ErrorBanxico, match="Fecha"):
        leer_exportacion('"Banco de México"\n')


class _Respuesta:
    def __init__(self, contenido, tipo, estado=200):
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


def test_cliente_exportar_pide_las_series_y_decodifica_latin1():
    sesion = _Sesion(_Respuesta(EXPORTACION.encode("latin-1"), "text/csv;charset=ISO-8859-1"))
    texto = ClienteBanxico(sesion).exportar(["SP68257", "SF43936"], 2018, 2026)
    assert "Banco de México" in texto
    metodo, url, kwargs = sesion.peticiones[0]
    assert metodo == "POST" and "accion=consultarSeries" in url
    formulario = kwargs["data"]
    assert ("series", "SP68257") in formulario and ("series", "SF43936") in formulario
    assert ("anoInicial", "2018") in formulario and ("formatoCSV.x", "1") in formulario


def test_cliente_exportar_rechaza_html():
    sesion = _Sesion(_Respuesta(b"<html></html>", "text/html"))
    with pytest.raises(ErrorBanxico, match="CSV"):
        ClienteBanxico(sesion).exportar(["SP68257"], 2018, 2026)


def test_tramo_udi():
    # La 2Q de septiembre rige del 10 al 25 de octubre; la 1Q de octubre, del 25-oct al 10-nov.
    assert tramo_udi(Periodo(2026, 9, 2)) == (D(2026, 10, 10), D(2026, 10, 25))
    assert tramo_udi(Periodo(2026, 10, 1)) == (D(2026, 10, 25), D(2026, 11, 10))
    assert tramo_udi(Periodo(2026, 12, 2)) == (D(2027, 1, 10), D(2027, 1, 25))
    assert tramo_udi(Periodo(2026, 12, 1)) == (D(2026, 12, 25), D(2027, 1, 10))


def test_consistencia_udi():
    inpc = {Periodo(2026, 9, 1): 100.0, Periodo(2026, 9, 2): 101.0, Periodo(2026, 10, 1): None}
    udi = {D(2026, 10, 10): 8.0, D(2026, 10, 25): 8.08}
    [comparacion] = consistencia_udi(udi, inpc)
    assert comparacion.quincena == Periodo(2026, 9, 2)
    assert comparacion.udi == pytest.approx(1.01) and comparacion.cumple


def _diaria(desde, valores):
    return {desde + dt.timedelta(days=i): v for i, v in enumerate(valores)}


def test_rendimiento_cetes_con_tasa_constante():
    # 10% anual: 28 días rinden 10 · 28/360 %, y el último tramo se prorratea.
    cetes = {D(2025, 12, 25) + dt.timedelta(days=7 * i): 10.0 for i in range(10)}
    enero = rendimiento_cetes(cetes, Periodo(2025, 12), Periodo(2026, 1))
    assert enero == pytest.approx(((1 + 0.1 * 28 / 360) * (1 + 0.1 * 3 / 360) - 1) * 100)


def test_rendimiento_cetes_usa_la_ultima_subasta_de_cada_reinversion():
    cetes = {D(2025, 12, 25): 10.0, D(2026, 1, 20): 20.0, D(2026, 1, 27): 20.0}
    # Se invierte el 31-dic a 10% (28 días, al 28-ene) y el 28-ene a 20% (3 días).
    enero = rendimiento_cetes(cetes, Periodo(2025, 12), Periodo(2026, 1))
    assert enero == pytest.approx(((1 + 0.1 * 28 / 360) * (1 + 0.2 * 3 / 360) - 1) * 100)


def test_rendimiento_cetes_falla_sin_subastas_que_cubran():
    with pytest.raises(KeyError):
        rendimiento_cetes({D(2026, 1, 15): 10.0}, Periodo(2025, 12), Periodo(2026, 6))


def test_variacion_udi_de_fin_de_mes_a_fin_de_mes():
    udi = {D(2025, 12, 31): 8.0, D(2026, 1, 31): 8.04}
    assert variacion_udi(udi, Periodo(2025, 12), Periodo(2026, 1)) == pytest.approx(0.5)
    with pytest.raises(KeyError):
        variacion_udi(udi, Periodo(2026, 1), Periodo(2026, 2))


# --- con los datos reales de data/ -----------------------------------------------------------


@pytest.fixture(scope="module")
def reales():
    return banxico.cargar(DATOS)


@pytest.fixture(scope="module")
def nacional():
    return disco.cargar(DATOS)


def test_valores_publicados_conocidos(reales):
    assert reales.udi[D(2026, 11, 10)] == 8.897671
    assert reales.cetes28[D(2026, 10, 22)] == 6.23
    assert min(reales.udi) == D(2018, 1, 1)


def test_la_udi_cuadra_con_el_inpc(reales, nacional):
    validacion = banxico.validar(reales, nacional)
    # Una comparación por quincena desde 2018: el INPC de una y la UDI de Banxico se confirman.
    assert len(validacion.udi) >= 200
    assert validacion.error_maximo_udi < banxico.TOLERANCIA_UDI
    assert validacion.dias_revisados >= 3000
    assert validacion.error_maximo_diario < banxico.TOLERANCIA_UDI


def test_una_udi_alterada_no_cuadra_con_el_inpc(reales, nacional):
    udi = dict(reales.udi)
    udi[D(2026, 3, 25)] *= 1.00001
    with pytest.raises(ErrorBanxico, match="no cuadra con el INPC"):
        banxico.validar(DatosBanxico(udi, reales.cetes28), nacional)


def test_un_dia_intermedio_alterado_no_crece_parejo(reales, nacional):
    # El 15 de marzo no es extremo de ningún tramo: solo lo detecta la revisión diaria.
    udi = dict(reales.udi)
    udi[D(2026, 3, 15)] *= 1.00001
    with pytest.raises(ErrorBanxico, match="parejo"):
        banxico.validar(DatosBanxico(udi, reales.cetes28), nacional)


def test_falla_con_un_hueco_en_la_udi(reales, nacional):
    udi = {f: v for f, v in reales.udi.items() if f != D(2026, 3, 1)}
    with pytest.raises(ErrorBanxico, match="huecos"):
        banxico.validar(DatosBanxico(udi, reales.cetes28), nacional)


def test_falla_con_cetes_fuera_de_rango_o_sin_subastas(reales, nacional):
    cetes = dict(reales.cetes28)
    cetes[D(2026, 10, 22)] = 62.3
    with pytest.raises(ErrorBanxico, match="fuera de rango"):
        banxico.validar(DatosBanxico(reales.udi, cetes), nacional)
    cetes = {f: v for f, v in reales.cetes28.items() if not D(2026, 3, 1) <= f <= D(2026, 4, 1)}
    with pytest.raises(ErrorBanxico, match="Faltan subastas"):
        banxico.validar(DatosBanxico(reales.udi, cetes), nacional)


def test_rendimientos_reales_plausibles(reales, nacional):
    desde, hasta = Periodo(2025, 9), Periodo(2026, 9)
    cetes = rendimiento_cetes(reales.cetes28, desde, hasta)
    udi = variacion_udi(reales.udi, desde, hasta)
    assert 4 < cetes < 12
    # La UDI sigue al INPC con medio mes de rezago: su variación anual queda cerca.
    inpc = (nacional.mensual["general"][hasta] / nacional.mensual["general"][desde] - 1) * 100
    assert udi == pytest.approx(inpc, abs=0.5)


def test_metadatos_coinciden_con_los_datos(reales):
    metadatos = banxico.leer_metadatos(DATOS)
    assert metadatos["ultima_udi"] == max(reales.udi).isoformat()
    assert metadatos["ultima_subasta_cetes28"] == max(reales.cetes28).isoformat()


# --- pipeline sin red ----------------------------------------------------------------------


class ClienteFalso:
    """Sirve la exportación del SIE a partir de ``data/banxico/``."""

    def __init__(self, reales, cambiar=None):
        self.reales = reales
        self.cambiar = cambiar or {}

    def exportar(self, series, anio_inicial, anio_final):
        assert list(series) == [banxico.SERIE_UDI, banxico.SERIE_CETES28]
        udi = self.reales.udi | self.cambiar
        lineas = ['"Banco de México"', '"Fecha","SP68257","SF43936"']
        for fecha in sorted(udi.keys() | self.reales.cetes28.keys()):
            valores = [udi.get(fecha), self.reales.cetes28.get(fecha)]
            celdas = ["N/E" if v is None else f"{v}" for v in valores]
            lineas.append(f"{fecha:%d/%m/%Y}," + ",".join(celdas))
        return "\n".join(lineas) + "\n"


def _copiar_nacional(destino):
    for archivo in (
        disco.ARCHIVO_MENSUAL,
        disco.ARCHIVO_QUINCENAL,
        disco.ARCHIVO_PONDERADORES,
        disco.ARCHIVO_CATALOGO,
    ):
        (destino / archivo).write_bytes((DATOS / archivo).read_bytes())


def test_actualizar_regenera_data_banxico_byte_por_byte(tmp_path, reales):
    _copiar_nacional(tmp_path)
    resumen = banxico.actualizar(tmp_path, ClienteFalso(reales))
    assert resumen.nuevas_udi == len(reales.udi)
    for archivo in (banxico.ARCHIVO_UDI, banxico.ARCHIVO_CETES28, banxico.ARCHIVO_METADATOS):
        assert filecmp.cmp(
            tmp_path / banxico.DIRECTORIO / archivo, DATOS / banxico.DIRECTORIO / archivo, False
        ), archivo
    assert banxico.actualizar(tmp_path, ClienteFalso(reales)).nuevas_udi == 0


def test_actualizar_no_acepta_revisiones_de_lo_ya_guardado(tmp_path, reales):
    _copiar_nacional(tmp_path)
    banxico.actualizar(tmp_path, ClienteFalso(reales))
    # Un valor fuera del periodo que se compara con el INPC, para que falle por la revisión.
    revisado = ClienteFalso(reales, {D(2018, 1, 2): reales.udi[D(2018, 1, 2)] + 0.000001})
    with pytest.raises(ErrorBanxico, match="cambia o quita"):
        banxico.actualizar(tmp_path, revisado)


def test_actualizar_pide_los_datos_nacionales(tmp_path, reales):
    with pytest.raises(ErrorBanxico, match="nacionales"):
        banxico.actualizar(tmp_path, ClienteFalso(reales))
