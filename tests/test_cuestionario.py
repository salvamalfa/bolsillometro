"""Cuestionario estandarizado, conversión de respuestas a presupuesto, reporte y CLI."""

import json
from pathlib import Path

import pytest

from bolsillometro import banxico, ciudades, reporte
from bolsillometro import datos as disco
from bolsillometro.cli import main
from bolsillometro.cuestionario import aplica, cargar_cuestionario, presupuesto_desde_respuestas
from bolsillometro.periodos import Periodo
from bolsillometro.personal import (
    ErrorPresupuesto,
    a_toml,
    calcular,
    cargar_rubros,
    gasto_oficial_por_rubro,
    leer_presupuesto,
)

DATOS = Path(__file__).resolve().parents[1] / "data"
ULTIMO = Periodo(2026, 9)


@pytest.fixture(scope="module")
def rubros():
    return cargar_rubros()


@pytest.fixture(scope="module")
def nacional():
    return disco.cargar(DATOS)


@pytest.fixture(scope="module")
def cuestionario():
    return cargar_cuestionario()


def _convertir(respuestas, cuestionario, rubros, nacional):
    return presupuesto_desde_respuestas(respuestas, cuestionario, rubros, nacional)


# --- el cuestionario ---------------------------------------------------------------------------


def test_el_cuestionario_es_consistente(cuestionario, rubros):
    ids = [p.id for p in cuestionario.preguntas]
    assert len(ids) == len(set(ids))
    vistos: set[str] = set()
    llenados: set[str] = set()
    for pregunta in cuestionario.preguntas:
        assert pregunta.tipo in ("ciudad", "opcion", "monto", "porcentaje"), pregunta.id
        assert pregunta.cada in ("mes", "año"), pregunta.id
        assert set(pregunta.rubros) <= set(rubros), pregunta.id
        if pregunta.tipo == "opcion":
            assert pregunta.opciones, pregunta.id
        if pregunta.tipo == "monto":
            assert bool(pregunta.rubros) != bool(pregunta.no_cubierto), pregunta.id
        if pregunta.aumento_propio:
            assert pregunta.aumento_propio in llenados, pregunta.id
        if pregunta.si:
            # Las condiciones solo miran preguntas anteriores.
            assert pregunta.si["pregunta"] in vistos, pregunta.id
        vistos.add(pregunta.id)
        llenados |= set(pregunta.rubros)
    # La compra de auto es irregular y la vivienda propia queda fuera por omisión.
    assert set(rubros) - llenados == {"auto_compra", "vivienda_propia"}


def test_cada_monto_tiene_una_escala_de_a_lo_mas_cuatro_opciones(cuestionario):
    for pregunta in cuestionario.preguntas:
        if pregunta.tipo in ("monto", "porcentaje"):
            assert pregunta.escala in cuestionario.escalas, pregunta.id
    for nombre, opciones in cuestionario.escalas.items():
        assert 2 <= len(opciones) <= 4, nombre  # caben en una pregunta de opción múltiple
        valores = [o.valor for o in opciones if o.valor is not None]
        assert valores == sorted(valores) and min(valores) >= 0, nombre


def test_las_respuestas_pueden_ser_opciones_de_la_escala(cuestionario, rubros, nacional):
    respuestas = {
        "vivienda": "rentada",
        "renta": "$5,000 a $12,000",
        "aumento_renta": "No sé",
        "luz": "$300 a $700",
        "ropa_calzado": "Menos de $3,000",  # anual: 2000 / 12
    }
    presupuesto = _convertir(respuestas, cuestionario, rubros, nacional)
    assert presupuesto.gasto == {"renta": 8500, "luz": 500, "ropa_calzado": pytest.approx(166.67)}
    assert presupuesto.aumento_propio == {}
    respuestas["aumento_renta"] = "4% a 8%"
    assert _convertir(respuestas, cuestionario, rubros, nacional).aumento_propio == {"renta": 6}


def test_una_respuesta_que_ya_no_aplica_no_se_valida(cuestionario, rubros, nacional):
    respuestas = {"super": 1000, "auto": "no", "gasolina": "No sé"}
    presupuesto = _convertir(respuestas, cuestionario, rubros, nacional)
    assert "gasolina" not in presupuesto.gasto


def test_aplica(cuestionario):
    preguntas = cuestionario.por_id()
    assert aplica(preguntas["gasolina"], {"auto": "si"})
    assert not aplica(preguntas["gasolina"], {"auto": "no"})
    assert not aplica(preguntas["gasolina"], {})
    assert aplica(preguntas["aumento_renta"], {"renta": 5000})
    assert not aplica(preguntas["aumento_renta"], {"renta": 0})
    assert aplica(preguntas["super"], {})


# --- de respuestas a presupuesto --------------------------------------------------------------


def test_un_monto_de_varios_rubros_se_reparte_con_los_ponderadores(cuestionario, rubros, nacional):
    presupuesto = _convertir({"super": 6000}, cuestionario, rubros, nacional)
    assert presupuesto.periodo_gasto == ULTIMO
    assert sum(presupuesto.gasto.values()) == pytest.approx(6000, abs=0.05)
    oficial = gasto_oficial_por_rubro(rubros, nacional, ULTIMO)
    assert presupuesto.gasto["carne"] / presupuesto.gasto["super"] == pytest.approx(
        oficial["carne"] / oficial["super"], rel=1e-4
    )
    assert set(presupuesto.gasto) == {"super", "carne", "lacteos", "frutas_verduras", "refrescos"}


def test_frecuencias_condiciones_y_no_cubierto(cuestionario, rubros, nacional):
    respuestas = {
        "ciudad": "pachuca",
        "vivienda": "rentada",
        "renta": 7000,
        "aumento_renta": 8,
        "hipoteca": 9000,  # no aplica: la casa es rentada
        "luz": {"monto": 900, "cada": "bimestre"},
        "ropa_calzado": 6000,  # se pregunta al año
        "auto": "no",
        "gasolina": 2000,  # no aplica: no tienen auto
        "seguros": 1500,
    }
    presupuesto = _convertir(respuestas, cuestionario, rubros, nacional)
    assert presupuesto.ciudad == "pachuca"
    assert presupuesto.gasto == {"renta": 7000, "luz": 450, "ropa_calzado": 500}
    assert presupuesto.aumento_propio == {"renta": 8}
    assert presupuesto.no_cubierto == {"seguros": 1500}
    assert presupuesto.vivienda_propia == "gasto_efectivo"


@pytest.mark.parametrize(
    ("respuestas", "mensaje"),
    [
        ({"super": 1000, "lotería": 50}, "no existen"),
        ({"super": 1000, "vivienda": "en un barco"}, "vivienda: debe ser una de"),
        ({"super": -5}, "super: monto negativo"),
        ({"super": "mucho"}, "super: 'mucho' no es una opción"),
        ({"super": True}, "super: monto inválido"),
        ({"super": {"monto": 900, "cada": "quincena"}}, "frecuencia desconocida"),
        ({"vivienda": "rentada", "renta": 5000, "aumento_renta": "poco"}, "aumento_renta"),
        ({"super": 0}, "ningún gasto"),
    ],
)
def test_errores_de_respuestas(cuestionario, rubros, nacional, respuestas, mensaje):
    with pytest.raises(ErrorPresupuesto, match=mensaje):
        _convertir(respuestas, cuestionario, rubros, nacional)


def test_ciudad_desconocida(cuestionario, rubros, nacional):
    with pytest.raises(ErrorPresupuesto, match="ciudad desconocida"):
        presupuesto_desde_respuestas(
            {"ciudad": "gotham", "super": 100}, cuestionario, rubros, nacional, ["pachuca"]
        )


def test_el_toml_se_lee_de_vuelta(cuestionario, rubros, nacional):
    respuestas = {
        "vivienda": "rentada",
        "renta": 1234567.5,  # sin notación científica en el TOML
        "aumento_renta": 8,
        "super": 5000,
        "intereses": 300,
    }
    presupuesto = _convertir(respuestas, cuestionario, rubros, nacional)
    leido = leer_presupuesto(a_toml(presupuesto, rubros), rubros)
    assert leido == presupuesto


# --- reporte -----------------------------------------------------------------------------------


def _resultado(rubros, nacional, ciudad="nacional"):
    gasto = {"super": 4000.0, "renta": 7000.0, "gasolina": 2000.0, "colegiaturas": 3000.0}
    from bolsillometro.personal import Presupuesto

    por_ciudad = ciudades.cargar(DATOS) if ciudad != "nacional" else None
    return calcular(
        Presupuesto(ciudad, ULTIMO, "gasto_efectivo", gasto), rubros, nacional, por_ciudad
    )


def test_el_reporte_empieza_con_una_sola_cifra(rubros, nacional):
    resultado = _resultado(rubros, nacional)
    texto = reporte.texto(resultado, rubros)
    primera = texto.splitlines()[0]
    assert primera == f"Tu inflación: {resultado.inflacion(12):.2f}%"
    assert "INPC" not in texto
    assert "Lo que más la subió" in texto


def test_el_reporte_compara_con_cetes_y_el_detalle_con_el_inpc(rubros, nacional):
    resultado = _resultado(rubros, nacional, "pachuca")
    cetes = banxico.cargar(DATOS).cetes28
    texto = reporte.texto(resultado, rubros, "Pachuca, Hgo.", cetes, detalle=True)
    assert "¿Tus ahorros le ganan?" in texto and "Cetes a 28 días" in texto
    assert "el INPC de Pachuca, Hgo." in texto and "hogar promedio del país" in texto


def test_variacion_por_rubro_con_un_solo_rubro_es_tu_inflacion(rubros, nacional):
    from bolsillometro.personal import Presupuesto

    presupuesto = Presupuesto("nacional", ULTIMO, "gasto_efectivo", {"super": 1000.0})
    resultado = calcular(presupuesto, rubros, nacional)
    assert resultado.variacion_por_rubro(12)["super"] == pytest.approx(resultado.inflacion(12))


# --- CLI ---------------------------------------------------------------------------------------


def test_cli_entrevista(tmp_path, capsys):
    respuestas = tmp_path / "yo.json"
    respuestas.write_text(
        json.dumps(
            {
                "ciudad": "pachuca",
                "vivienda": "rentada",
                "renta": 6500,
                "super": 5000,
                "auto": "si",
                "gasolina": 1800,
                "auto_gastos": 12000,
            }
        ),
        "utf-8",
    )
    assert main(["entrevista", str(respuestas), "--datos", str(DATOS)]) == 0
    salida = capsys.readouterr().out
    assert "Tu inflación:" in salida and "Pachuca, Hgo." in salida
    presupuesto = leer_presupuesto((tmp_path / "yo.toml").read_text("utf-8"), cargar_rubros())
    assert presupuesto.gasto["auto_gastos"] == 1000


def test_cli_entrevista_con_error(tmp_path, capsys):
    respuestas = tmp_path / "yo.json"
    respuestas.write_text(json.dumps({"super": "mucho"}), "utf-8")
    assert main(["entrevista", str(respuestas), "--datos", str(DATOS)]) == 1
    assert "super: 'mucho' no es una opción" in capsys.readouterr().err
