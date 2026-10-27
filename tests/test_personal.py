"""Tu inflación personal: catálogo de rubros, presupuesto en TOML, cálculo y CLI."""

from pathlib import Path

import pytest

from bolsillometro import ciudades
from bolsillometro import datos as disco
from bolsillometro.cli import main
from bolsillometro.indices import valores_en
from bolsillometro.periodos import Periodo
from bolsillometro.personal import (
    ErrorPresupuesto,
    Presupuesto,
    calcular,
    cargar_rubros,
    leer_presupuesto,
    plantilla,
)
from bolsillometro.reconstruccion import BASE_PONDERADORES

DATOS = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture(scope="module")
def rubros():
    return cargar_rubros()


@pytest.fixture(scope="module")
def nacional():
    return disco.cargar(DATOS)


@pytest.fixture(scope="module")
def por_ciudad():
    return ciudades.cargar(DATOS)


# --- catálogo ------------------------------------------------------------------------------


def test_cada_generico_esta_en_un_solo_rubro(rubros, nacional):
    codigos = [codigo for rubro in rubros.values() for codigo in rubro.genericos]
    assert len(codigos) == len(set(codigos)) == 292
    assert set(codigos) == {p.codigo for p in nacional.ponderadores}
    assert len(rubros) == 32


def test_lo_de_precio_casi_unico_usa_el_indice_nacional(rubros):
    assert rubros["gasolina"].nacionales == {"212", "213", "214"}
    assert "206" in rubros["auto_compra"].nacionales  # automóviles
    assert not rubros["renta"].nacionales and not rubros["luz"].nacionales


def test_vivienda_propia_es_solo_la_renta_imputada(rubros):
    assert rubros["vivienda_propia"].genericos == ("139",)
    assert rubros["agua"].genericos == ("142",)


# --- presupuesto -----------------------------------------------------------------------------

MINIMO = 'periodo_gasto = "2026-09"\n[gasto]\nsuper = 1000\n'


def test_leer_presupuesto_minimo(rubros):
    presupuesto = leer_presupuesto(MINIMO, rubros)
    assert presupuesto.ciudad == "nacional"
    assert presupuesto.periodo_gasto == Periodo(2026, 9)
    assert presupuesto.vivienda_propia == "gasto_efectivo"
    assert presupuesto.gasto == {"super": 1000.0}


def test_la_plantilla_se_lee_de_vuelta(rubros):
    texto = plantilla(rubros, ["cdmx", "pachuca"])
    assert "cdmx, pachuca" in texto
    with pytest.raises(ErrorPresupuesto, match="al menos un rubro"):
        leer_presupuesto(texto, rubros)
    presupuesto = leer_presupuesto(texto.replace("super              = 0", "super = 900"), rubros)
    assert presupuesto.gasto["super"] == 900
    assert set(presupuesto.gasto) == set(rubros)


@pytest.mark.parametrize(
    ("texto", "mensaje"),
    [
        ("periodo_gasto = 2026", "periodo_gasto"),
        ('periodo_gasto = "2026-09-1Q"\n[gasto]\nsuper = 1', "quincena"),
        (MINIMO + "[otros]\nx = 1", "Claves desconocidas"),
        (MINIMO.replace("super", "supper"), "quisiste decir 'super'"),
        (MINIMO.replace("1000", "-5"), "al menos 0"),
        (MINIMO.replace("1000", '"mil"'), "número"),
        ('vivienda_propia = "rentada"\n' + MINIMO, "vivienda_propia"),
        (MINIMO + "[aumento_propio]\nrenta = 8", "no tiene gasto"),
        ("esto no es toml = = =", "TOML"),
    ],
)
def test_errores_del_presupuesto(rubros, texto, mensaje):
    with pytest.raises(ErrorPresupuesto, match=mensaje):
        leer_presupuesto(texto, rubros)


# --- cálculo -------------------------------------------------------------------------------


def _gasto_promedio(rubros, nacional, e):
    """Lo que gasta el hogar promedio del INPC en cada rubro, a precios del mes ``e``."""
    oficiales = {p.codigo: p.ponderador for p in nacional.ponderadores}
    base = valores_en({c: nacional.quincenal[c] for c in oficiales}, BASE_PONDERADORES)
    en_e = valores_en({c: nacional.mensual[c] for c in oficiales}, e)
    return {
        r.clave: sum(oficiales[c] * en_e[c] / base[c] for c in r.genericos) for r in rubros.values()
    }


@pytest.mark.parametrize("e", [Periodo(2024, 8), Periodo(2025, 9), Periodo(2026, 9)])
def test_el_hogar_promedio_tiene_la_inflacion_del_inpc(rubros, nacional, e):
    presupuesto = Presupuesto("nacional", e, "consumo", _gasto_promedio(rubros, nacional, e))
    resultado = calcular(presupuesto, rubros, nacional)
    assert resultado.indice[e] == pytest.approx(100)
    for t in (Periodo(2025, 9), Periodo(2026, 3), Periodo(2026, 9)):
        assert resultado.inflacion(12, t) == pytest.approx(
            resultado.inflacion_inpc(12, t), abs=0.002
        )
        assert resultado.inflacion(1, t) == pytest.approx(resultado.inflacion_inpc(1, t), abs=0.002)


def test_gasto_efectivo_deja_fuera_la_vivienda_propia(rubros, nacional):
    gasto = {"super": 1000.0, "vivienda_propia": 5000.0}
    efectivo = calcular(
        Presupuesto("nacional", Periodo(2026, 9), "gasto_efectivo", gasto), rubros, nacional
    )
    assert set(efectivo.rubro_de.values()) == {"super"}
    assert efectivo.total_cubierto == 1000
    consumo = calcular(
        Presupuesto("nacional", Periodo(2026, 9), "consumo", gasto), rubros, nacional
    )
    assert consumo.pesos["139"] == pytest.approx(5 / 6)


def test_aumento_propio(rubros, nacional):
    presupuesto = Presupuesto(
        "nacional", Periodo(2026, 3), "gasto_efectivo", {"renta": 8000.0}, {"renta": 12.0}
    )
    resultado = calcular(presupuesto, rubros, nacional)
    assert resultado.inflacion(12) == pytest.approx(12)
    assert resultado.inflacion(1) == pytest.approx((1.12 ** (1 / 12) - 1) * 100)
    assert resultado.porcentaje_propio == pytest.approx(100)


def test_directo_imputado_y_no_cubierto(rubros, nacional):
    presupuesto = Presupuesto(
        "nacional",
        Periodo(2026, 9),
        "gasto_efectivo",
        {"luz": 500.0, "super": 1500.0},
        no_cubierto={"seguro_gastos_medicos": 1000.0},
    )
    resultado = calcular(presupuesto, rubros, nacional)
    assert resultado.porcentaje_directo == pytest.approx(25)
    assert resultado.porcentaje_imputado == pytest.approx(75)
    assert resultado.total_no_cubierto == 1000
    # El gasto no cubierto no mueve el índice.
    sin = calcular(
        Presupuesto("nacional", Periodo(2026, 9), "gasto_efectivo", presupuesto.gasto),
        rubros,
        nacional,
    )
    assert resultado.inflacion(12) == sin.inflacion(12)


def test_incidencias_por_rubro_suman_la_inflacion(rubros, nacional):
    gasto = {"super": 3000.0, "renta": 6000.0, "gasolina": 2000.0, "colegiaturas": 3000.0}
    resultado = calcular(
        Presupuesto("nacional", Periodo(2026, 9), "gasto_efectivo", gasto), rubros, nacional
    )
    incidencias = resultado.incidencias_por_rubro(12)
    assert set(incidencias) == set(gasto)
    assert sum(incidencias.values()) == pytest.approx(resultado.inflacion(12))


def test_ciudad_usa_sus_precios_y_el_nacional_cuando_no_hay(rubros, nacional, por_ciudad):
    gasto = {"gas": 600.0, "gasolina": 2000.0, "renta": 5000.0}
    presupuesto = Presupuesto("pachuca", Periodo(2026, 9), "gasto_efectivo", gasto)
    resultado = calcular(presupuesto, rubros, nacional, por_ciudad)
    pachuca = por_ciudad.series["pachuca"]
    assert resultado.fuente["138"] == "ciudad" and resultado.series["138"] is pachuca["138"]
    assert resultado.fuente["145"] == "ciudad"  # gas LP
    # Pachuca ya no cotiza gas natural, y la gasolina tiene precio casi único: nacional.
    assert resultado.fuente["146"] == "nacional"
    assert resultado.fuente["214"] == "nacional"
    assert resultado.inflacion_ciudad(12) == pytest.approx(
        (pachuca["general"][Periodo(2026, 9)] / pachuca["general"][Periodo(2025, 9)] - 1) * 100
    )


def test_ciudad_desconocida_o_periodo_fuera_de_rango(rubros, nacional, por_ciudad):
    gasto = {"super": 1000.0}
    with pytest.raises(ErrorPresupuesto, match="quisiste decir 'pachuca'"):
        calcular(
            Presupuesto("pachuka", Periodo(2026, 9), "gasto_efectivo", gasto),
            rubros,
            nacional,
            por_ciudad,
        )
    with pytest.raises(ErrorPresupuesto, match="periodo_gasto"):
        calcular(
            Presupuesto("nacional", Periodo(2024, 7), "gasto_efectivo", gasto), rubros, nacional
        )
    with pytest.raises(ErrorPresupuesto, match="periodo_gasto"):
        calcular(
            Presupuesto("nacional", Periodo(2030, 1), "gasto_efectivo", gasto), rubros, nacional
        )


# --- CLI -------------------------------------------------------------------------------------


def test_cli_plantilla_no_sobrescribe(tmp_path, capsys):
    destino = tmp_path / "presupuesto.toml"
    assert main(["plantilla", str(destino), "--datos", str(DATOS)]) == 0
    assert "pachuca" in destino.read_text("utf-8")
    assert main(["plantilla", str(destino), "--datos", str(DATOS)]) == 1
    assert "ya existe" in capsys.readouterr().err


def test_cli_mi_inflacion(tmp_path, capsys):
    destino = tmp_path / "presupuesto.toml"
    destino.write_text(
        'ciudad = "pachuca"\nperiodo_gasto = "2026-09"\n'
        "[gasto]\nsuper = 3000\nrenta = 6000\ngasolina = 2000\n"
        "[aumento_propio]\nrenta = 8\n[no_cubierto]\nseguro_gastos_medicos = 1500\n",
        "utf-8",
    )
    assert main(["mi-inflacion", str(destino), "--datos", str(DATOS)]) == 0
    salida = capsys.readouterr().out
    assert "Pachuca, Hgo." in salida and "INPC nacional" in salida and "INPC Pachuca" in salida
    assert "Renta de vivienda" in salida and "seguro_gastos_medicos" in salida


def test_cli_mi_inflacion_con_error(tmp_path, capsys):
    destino = tmp_path / "presupuesto.toml"
    destino.write_text(MINIMO.replace("super", "supper"), "utf-8")
    assert main(["mi-inflacion", str(destino), "--datos", str(DATOS)]) == 1
    assert "quisiste decir 'super'" in capsys.readouterr().err
