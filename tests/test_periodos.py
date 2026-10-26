import pytest

from bolsillometro.periodos import Periodo


@pytest.mark.parametrize(
    ("etiqueta", "esperado"),
    [
        ("Ene 2024", Periodo(2024, 1)),
        ("Sep 2026", Periodo(2026, 9)),
        ("1Q Ago 2024", Periodo(2024, 8, 1)),
        ("2Q Jul 2024", Periodo(2024, 7, 2)),
        (" Dic 2018 ", Periodo(2018, 12)),
    ],
)
def test_etiqueta_inegi(etiqueta, esperado):
    assert Periodo.desde_etiqueta_inegi(etiqueta) == esperado


@pytest.mark.parametrize("periodo", [Periodo(2024, 1), Periodo(2024, 7, 2), Periodo(2026, 10, 1)])
def test_texto_y_etiqueta_ida_y_vuelta(periodo):
    assert Periodo.desde_texto(str(periodo)) == periodo
    assert Periodo.desde_etiqueta_inegi(periodo.etiqueta_inegi()) == periodo


def test_formato_texto():
    assert str(Periodo(2024, 8)) == "2024-08"
    assert str(Periodo(2024, 8, 1)) == "2024-08-1Q"


def test_orden():
    assert Periodo(2024, 7, 2) < Periodo(2024, 8, 1) < Periodo(2024, 8, 2)
    assert sorted([Periodo(2025, 1), Periodo(2024, 12)]) == [Periodo(2024, 12), Periodo(2025, 1)]


def test_desplazar_mensual():
    assert Periodo(2024, 1).anterior() == Periodo(2023, 12)
    assert Periodo(2024, 9).anterior(12) == Periodo(2023, 9)
    assert Periodo(2024, 12).desplazar(1) == Periodo(2025, 1)


def test_desplazar_quincenal():
    assert Periodo(2024, 1, 1).anterior() == Periodo(2023, 12, 2)
    assert Periodo(2024, 1, 2).anterior() == Periodo(2024, 1, 1)
    assert Periodo(2024, 12, 2).desplazar(1) == Periodo(2025, 1, 1)
    assert Periodo(2026, 10, 1).anterior(24) == Periodo(2025, 10, 1)


@pytest.mark.parametrize("texto", ["2024-13", "2024-01-3Q", "Ene-2024", ""])
def test_texto_invalido(texto):
    with pytest.raises(ValueError):
        Periodo.desde_texto(texto)


@pytest.mark.parametrize("etiqueta", ["Enero 2024", "3Q Ene 2024", "Xyz 2024"])
def test_etiqueta_invalida(etiqueta):
    with pytest.raises(ValueError):
        Periodo.desde_etiqueta_inegi(etiqueta)
