"""La prueba de fuego: con los datos de ``data/`` se reconstruye el INPC publicado."""

from pathlib import Path

import pytest

from bolsillometro import datos as disco
from bolsillometro.indices import (
    encadenar,
    incidencias,
    indice_ponderado,
    pesos_lowe,
    valores_en,
    variacion,
)
from bolsillometro.periodos import Periodo
from bolsillometro.pipeline import reconstruir
from bolsillometro.reconstruccion import (
    BASE_PONDERADORES,
    INICIO_MENSUAL,
    INICIO_QUINCENAL,
    factor_encadenamiento,
)

DATOS = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture(scope="module")
def datos():
    return disco.cargar(DATOS)


@pytest.fixture(scope="module")
def resultado(datos):
    return reconstruir(datos)


def _ultimo(serie):
    return max(p for p, v in serie.items() if v is not None)


def _periodos_desde(inicio, fin):
    periodos = [inicio]
    while periodos[-1] < fin:
        periodos.append(periodos[-1].desplazar(1))
    return periodos


def test_ponderadores_oficiales(datos):
    assert len(datos.ponderadores) == 292
    assert sum(p.ponderador for p in datos.ponderadores) == pytest.approx(100, abs=0.01)
    assert {p.codigo for p in datos.ponderadores} == set(datos.mensual) - {"general"}


def test_factor_de_encadenamiento(datos):
    assert datos.quincenal["general"][BASE_PONDERADORES] == 136.095
    assert factor_encadenamiento(datos.quincenal) == pytest.approx(1.36095)


def test_reconstruye_cada_mes_desde_agosto_2024(datos, resultado):
    esperados = _periodos_desde(INICIO_MENSUAL, _ultimo(datos.mensual["general"]))
    assert [c.periodo for c in resultado.mensual] == esperados
    fallas = [(str(c.periodo), c.diferencia) for c in resultado.mensual if not c.cumple]
    assert fallas == []


def test_reconstruye_cada_quincena_desde_agosto_2024(datos, resultado):
    esperados = _periodos_desde(INICIO_QUINCENAL, _ultimo(datos.quincenal["general"]))
    assert [c.periodo for c in resultado.quincenal] == esperados
    fallas = [(str(c.periodo), c.diferencia) for c in resultado.quincenal if not c.cumple]
    assert fallas == []


def test_valores_publicados_conocidos(datos):
    assert datos.mensual["general"][Periodo(2024, 8)] == 136.013
    assert datos.mensual["general"][Periodo(2026, 9)] == 146.075
    assert datos.mensual["014"][Periodo(2026, 9)] == 163.374
    assert datos.quincenal["general"][Periodo(2026, 10, 1)] == 146.739


def test_mensual_es_promedio_de_sus_quincenas(datos):
    for codigo, serie in datos.mensual.items():
        for periodo, valor in serie.items():
            q1 = datos.quincenal[codigo].get(Periodo(periodo.anio, periodo.mes, 1))
            q2 = datos.quincenal[codigo].get(Periodo(periodo.anio, periodo.mes, 2))
            if periodo < Periodo(2018, 8) or None in (valor, q1, q2):
                continue
            assert abs(round((q1 + q2) / 2, 3) - valor) <= 0.001 + 1e-9, (codigo, str(periodo))


def test_incidencias_oficiales_suman_la_inflacion_anual(datos):
    pesos = {p.codigo: p.ponderador for p in datos.ponderadores}
    genericos = {codigo: datos.mensual[codigo] for codigo in pesos}
    base = valores_en({c: datos.quincenal[c] for c in pesos}, BASE_PONDERADORES)
    hasta = _ultimo(datos.mensual["general"])
    desde = hasta.anterior(12)
    if desde < INICIO_MENSUAL:
        pytest.skip("Todavía no hay doce meses con la canasta 2024")
    indice = indice_ponderado(genericos, pesos, base)
    contribuciones = incidencias(genericos, pesos, base, desde, hasta)
    assert sum(contribuciones.values()) == pytest.approx(variacion(indice, hasta, rezago=12))
    # El índice reconstruido da la inflación anual publicada (con redondeo de las series).
    publicada = variacion(datos.mensual["general"], hasta, rezago=12)
    assert variacion(indice, hasta, rezago=12) == pytest.approx(publicada, abs=0.002)


def test_encadenar_los_pesos_oficiales_sigue_reconstruyendo_el_inpc(datos):
    pesos = {p.codigo: p.ponderador for p in datos.ponderadores}
    genericos = {codigo: datos.mensual[codigo] for codigo in pesos}
    base = valores_en({c: datos.quincenal[c] for c in pesos}, BASE_PONDERADORES)
    indice = indice_ponderado(genericos, pesos, base, factor_encadenamiento(datos.quincenal))
    # Los ponderadores oficiales llevados a jul-2025 por precios relativos: encadenar con
    # ellos en ese mes no debe mover el INPC reconstruido.
    eslabon = Periodo(2025, 7)
    pesos_eslabon = pesos_lowe(pesos, base, valores_en(genericos, eslabon))
    encadenado = encadenar(indice, genericos, pesos_eslabon, eslabon)
    publicado = datos.mensual["general"]
    fallas = [
        (str(p), round(v, 3) - publicado[p])
        for p, v in encadenado.items()
        if p > eslabon and abs(round(v, 3) - publicado[p]) > 0.001 + 1e-9
    ]
    assert fallas == []
    assert max(encadenado) == _ultimo(publicado)


def test_metadatos_coinciden_con_los_datos(datos, resultado):
    metadatos = disco.leer_metadatos(DATOS / disco.ARCHIVO_METADATOS)
    assert metadatos["ultimo_mensual"] == str(_ultimo(datos.mensual["general"]))
    assert metadatos["ultimo_quincenal"] == str(_ultimo(datos.quincenal["general"]))
    assert metadatos["reconstruccion"]["mensual"]["periodos"] == len(resultado.mensual)
    assert metadatos["reconstruccion"]["quincenal"]["periodos"] == len(resultado.quincenal)
