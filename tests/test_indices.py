import pytest

from bolsillometro.indices import (
    encadenar,
    incidencias,
    incidencias_encadenadas,
    indice_ponderado,
    normalizar,
    pesos_lowe,
    rendimiento_real,
    valores_en,
    variacion,
)
from bolsillometro.periodos import Periodo

B = Periodo(2025, 1)  # base
T1 = Periodo(2025, 2)
T2 = Periodo(2025, 3)

SERIES = {
    "A": {B: 100.0, T1: 110.0, T2: 121.0},
    "B": {B: 200.0, T1: 200.0, T2: 190.0},
    "C": {B: 50.0, T1: 55.0, T2: None},
}


def test_normalizar():
    assert normalizar({"A": 1, "B": 3, "C": 0}) == {"A": 0.25, "B": 0.75}
    with pytest.raises(ValueError):
        normalizar({"A": 0})


def test_valores_en():
    assert valores_en({"A": SERIES["A"]}, T1) == {"A": 110.0}
    with pytest.raises(KeyError):
        valores_en(SERIES, T2)


def test_indice_ponderado():
    base = valores_en(SERIES, B)
    indice = indice_ponderado(SERIES, {"A": 1, "B": 1}, base)
    # 100 · (0.5 · 110/100 + 0.5 · 200/200) = 105
    assert indice[B] == pytest.approx(100)
    assert indice[T1] == pytest.approx(105)
    assert indice[T2] == pytest.approx(100 * (0.5 * 1.21 + 0.5 * 0.95))


def test_indice_ponderado_omite_periodos_sin_dato_y_aplica_factor():
    base = valores_en(SERIES, B)
    indice = indice_ponderado(SERIES, {"A": 1, "C": 1}, base, factor=1.5)
    assert list(indice) == [B, T1]
    assert indice[T1] == pytest.approx(1.5 * 100 * 1.1)


def test_indice_ponderado_falla_sin_series():
    with pytest.raises(KeyError, match="Z"):
        indice_ponderado(SERIES, {"A": 1, "Z": 1}, {"A": 100.0})


def test_pesos_lowe():
    # Gastaste igual en A y B en T1; A ya estaba 10% más cara que en la base.
    pesos = pesos_lowe({"A": 50, "B": 50}, valores_en(SERIES, T1), valores_en(SERIES, B))
    esperado_a = 0.5 * 100 / 110
    esperado_b = 0.5 * 200 / 200
    total = esperado_a + esperado_b
    assert pesos["A"] == pytest.approx(esperado_a / total)
    assert pesos["B"] == pytest.approx(esperado_b / total)
    assert sum(pesos.values()) == pytest.approx(1)


def test_pesos_lowe_sin_cambio_de_periodo():
    base = valores_en(SERIES, B)
    assert pesos_lowe({"A": 30, "B": 70}, base, base) == pytest.approx({"A": 0.3, "B": 0.7})


def test_variacion():
    serie = {Periodo(2025, 9): 100.0, Periodo(2026, 8): 103.0, Periodo(2026, 9): 104.0}
    assert variacion(serie, Periodo(2026, 9)) == pytest.approx((104 / 103 - 1) * 100)
    assert variacion(serie, Periodo(2026, 9), rezago=12) == pytest.approx(4.0)
    with pytest.raises(KeyError):
        variacion(serie, Periodo(2026, 8))


def test_incidencias_suman_la_variacion():
    base = valores_en(SERIES, B)
    pesos = {"A": 2, "B": 3}
    indice = indice_ponderado(SERIES, pesos, base)
    contribuciones = incidencias(SERIES, pesos, base, T1, T2)
    assert sum(contribuciones.values()) == pytest.approx(variacion(indice, T2))
    assert contribuciones["A"] > 0 > contribuciones["B"]


def test_encadenar_aplica_los_pesos_nuevos_desde_el_eslabon():
    base = valores_en(SERIES, B)
    anterior = indice_ponderado(SERIES, {"A": 1, "B": 1}, base)
    encadenado = encadenar(anterior, SERIES, {"B": 1}, T1)
    assert encadenado[B] == anterior[B]
    assert encadenado[T1] == anterior[T1]
    # Desde T1 solo pesa B: P(T2) = P(T1) · I_B(T2) / I_B(T1).
    assert encadenado[T2] == pytest.approx(anterior[T1] * 190 / 200)


def test_encadenar_con_los_pesos_efectivos_no_cambia_el_indice():
    base = valores_en(SERIES, B)
    pesos = {"A": 2, "B": 3}
    anterior = indice_ponderado(SERIES, pesos, base)
    # Los pesos viejos llevados a T1 por precios relativos describen la misma canasta.
    pesos_t1 = pesos_lowe(pesos, base, valores_en({c: SERIES[c] for c in pesos}, T1))
    assert encadenar(anterior, SERIES, pesos_t1, T1) == pytest.approx(anterior)


def test_encadenar_falla_sin_eslabon_o_sin_series():
    anterior = {B: 100.0}
    with pytest.raises(KeyError, match="eslabón"):
        encadenar(anterior, SERIES, {"A": 1}, T1)
    with pytest.raises(KeyError, match="Z"):
        encadenar(anterior, SERIES, {"Z": 1}, B)


def test_incidencias_encadenadas_suman_la_variacion_total():
    base = valores_en(SERIES, B)
    pesos_viejos = {"A": 2, "B": 3}
    pesos_nuevos = {"A": 1, "B": 4}
    anterior = indice_ponderado(SERIES, pesos_viejos, base)
    encadenado = encadenar(anterior, SERIES, pesos_nuevos, T1)

    antes = incidencias(SERIES, pesos_viejos, base, B, T1)
    despues = incidencias(SERIES, pesos_nuevos, valores_en(SERIES, T1), T1, T2)
    total = incidencias_encadenadas(antes, despues)
    assert sum(total.values()) == pytest.approx((encadenado[T2] / encadenado[B] - 1) * 100)


def test_incidencias_encadenadas_con_genericos_de_un_solo_tramo():
    total = incidencias_encadenadas({"A": 1.0}, {"B": 2.0})
    assert total == pytest.approx({"A": 1.02, "B": 2.0})


def test_rendimiento_real():
    # 10% nominal con 4% de inflación: 1.10 / 1.04 − 1.
    assert rendimiento_real(10, 4) == pytest.approx((1.10 / 1.04 - 1) * 100)
    assert rendimiento_real(5, 5) == pytest.approx(0)
    assert rendimiento_real(3, 6) < 0
    with pytest.raises(ValueError):
        rendimiento_real(5, -100)
