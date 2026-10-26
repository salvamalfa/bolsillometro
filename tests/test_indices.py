import pytest

from bolsillometro.indices import (
    incidencias,
    indice_ponderado,
    normalizar,
    pesos_lowe,
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
