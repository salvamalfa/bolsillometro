"""La web estática: sus datos están al día y su cálculo (JavaScript) es idéntico al de Python."""

import filecmp
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from bolsillometro import banxico, ciudades, reporte, web
from bolsillometro import datos as disco
from bolsillometro.cuestionario import (
    cargar_cuestionario,
    mes_del_gasto,
    presupuesto_desde_respuestas,
)
from bolsillometro.indices import rendimiento_real
from bolsillometro.periodos import Periodo
from bolsillometro.personal import calcular, cargar_rubros

RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "data"
WEB = RAIZ / "web"

# Perfiles distintos: renta con aumento propio, casa propia con auto, sin ciudad, etc.
PERFILES = {
    "renta_pachuca": {
        "ciudad": "pachuca",
        "vivienda": "rentada",
        "renta": "$5,000 a $12,000",
        "aumento_renta": "4% a 8%",
        "super": "$4,000 a $8,000",
        "comer_fuera": "Menos de $1,500",
        "luz": {"monto": 900, "cada": "bimestre"},
        "auto": "no",
        "transporte_publico": "$500 a $1,500",
        "colegiaturas": 4500,
        "aumento_colegiatura": "No sé",
        "ropa_calzado": "$3,000 a $10,000",
        "seguros": "Menos de $1,000",
    },
    "propia_cdmx_auto": {
        "ciudad": "cdmx",
        "vivienda": "propia",
        "hipoteca": "Nada",
        "super": "Menos de $4,000",
        "comer_fuera": "Menos de $1,500",
        "luz": "Menos de $300",
        "gas": "Menos de $300",
        "celular": "$300 a $700",
        "internet_tv": "Menos de $500",
        "auto": "si",
        "gasolina": "$1,000 a $2,500",
        "auto_gastos": "Menos de $10,000",
        "diversion": "$500 a $1,500",
        "mascotas": "Menos de $500",
    },
    "nacional_minimo": {"ciudad": "nacional", "super": 3000, "gasolina": 1200},
    "ciudad_sin_metro": {
        "ciudad": "tulancingo",
        "vivienda": "prestada",
        "super": "$8,000 a $12,000",
        "gas": "$300 a $700",
        "transporte_publico": "Más de $1,500",
        "auto": "no",
        "viajes": "$10,000 a $30,000",
    },
    # Quedó la gasolina de antes de decir que no hay auto: se ignora en vez de fallar.
    "ya_no_aplica": {"super": 1000, "auto": "no", "gasolina": "No sé"},
}


def test_los_datos_de_la_web_estan_al_dia(tmp_path):
    """web/datos/ es exactamente lo que `bolsillometro web` exporta de data/."""
    web.exportar(DATOS, tmp_path)
    nuevos = tmp_path / web.DIRECTORIO_DATOS
    guardados = WEB / web.DIRECTORIO_DATOS
    comparacion = filecmp.dircmp(nuevos, guardados)
    assert comparacion.left_only == comparacion.right_only == []
    for sub in (Path("."), Path(web.DIRECTORIO_CIUDADES)):
        archivos = sorted(p.name for p in (nuevos / sub).glob("*.js"))
        _, distintos, errores = filecmp.cmpfiles(nuevos / sub, guardados / sub, archivos, False)
        assert distintos == errores == [], "corre `python -m bolsillometro web`"


def test_la_base_trae_lo_necesario():
    datos = web.base(DATOS)
    assert len(datos["periodos"]) == web.MESES
    assert datos["periodos"][-1] == disco.leer_metadatos(DATOS / "metadatos.json")["ultimo_mensual"]
    assert len(datos["rubros"]) == 32 and len(datos["ciudades"]) == 55
    assert {"pregunta", "escalas"} <= set(datos["cuestionario"])
    assert datos["cetes"]


def _python(respuestas, periodo=None):
    nacional = disco.cargar(DATOS)
    rubros = cargar_rubros()
    por_ciudad = (
        ciudades.cargar(DATOS) if respuestas.get("ciudad", "nacional") != "nacional" else None
    )
    general = por_ciudad.series[respuestas["ciudad"]]["general"] if por_ciudad else None
    periodo = periodo or mes_del_gasto(nacional, general)
    presupuesto = presupuesto_desde_respuestas(
        respuestas, cargar_cuestionario(), rubros, nacional, periodo=periodo
    )
    resultado = calcular(presupuesto, rubros, nacional, por_ciudad)
    anual = resultado.inflacion(12)
    hasta = resultado.ultimo
    desde = hasta.anterior(12)
    cetes = reporte.rendimiento_cetes(banxico.cargar(DATOS).cetes28, desde, hasta)
    incidencias = resultado.incidencias_por_rubro(12)
    return {
        "gasto": presupuesto.gasto,
        "inflacion": anual,
        "hasta": str(hasta),
        "suben": [(rubros[r].nombre, p) for r, p in incidencias.items() if p > 0][:4],
        "cetes": cetes,
        "real": rendimiento_real(cetes, anual),
    }


GUION = """
const path = require("path"), vm = require("vm"), fs = require("fs");
const web = process.argv[1], perfiles = JSON.parse(fs.readFileSync(0, "utf8"));
const ctx = { window: {} }; vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(web, "datos/base.js"), "utf8"), ctx);
const B = require(path.join(web, "calculo.js"));
const datos = new B.Datos(ctx.window.BOLSILLOMETRO_BASE);
const salida = {};
for (const [nombre, { respuestas, periodo }] of Object.entries(perfiles)) {
  let ciudad = null;
  if ((respuestas.ciudad || "nacional") !== "nacional") {
    const archivo = path.join(web, "datos/ciudades", respuestas.ciudad + ".js");
    vm.runInContext(fs.readFileSync(archivo, "utf8"), ctx);
    ciudad = ctx.window.BOLSILLOMETRO_CIUDADES[respuestas.ciudad];
  }
  const mes = periodo || B.mesDelGasto(datos, ciudad);
  const p = B.presupuestoDesdeRespuestas(datos, respuestas, mes);
  const r = B.resumen(datos, B.calcular(datos, p, ciudad));
  salida[nombre] = { gasto: p.gasto, inflacion: r.inflacion, hasta: r.hasta, cetes: r.cetes,
                     real: r.real, suben: r.suben.map((s) => [s.rubro, s.puntos]) };
}
console.log(JSON.stringify(salida));
"""


@pytest.fixture(scope="module")
def javascript():
    if shutil.which("node") is None:
        pytest.skip("se necesita Node para correr el cálculo de la web")
    salida = subprocess.run(
        ["node", "-e", GUION, "--", str(WEB)],
        input=json.dumps(
            {n: {"respuestas": r, "periodo": None} for n, r in PERFILES.items()}
            | {"rezago": {"respuestas": PERFILES["renta_pachuca"], "periodo": str(_ANTERIOR)}}
        ),
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(salida.stdout)


# Como cuando la ciudad todavía no tiene el último mes: el gasto es del mes anterior.
_ANTERIOR = Periodo.desde_texto(web.base(DATOS)["periodos"][-1]).anterior()


@pytest.mark.parametrize("perfil", [*sorted(PERFILES), "rezago"])
def test_la_web_calcula_igual_que_python(javascript, perfil):
    if perfil == "rezago":
        esperado = _python(PERFILES["renta_pachuca"], _ANTERIOR)
    else:
        esperado = _python(PERFILES[perfil])
    obtenido = javascript[perfil]
    assert obtenido["gasto"] == pytest.approx(esperado["gasto"], abs=0.005)
    assert obtenido["hasta"] == esperado["hasta"]
    assert obtenido["inflacion"] == pytest.approx(esperado["inflacion"], abs=1e-9)
    assert obtenido["cetes"] == pytest.approx(esperado["cetes"], abs=1e-9)
    assert obtenido["real"] == pytest.approx(esperado["real"], abs=1e-9)
    assert [r for r, _ in obtenido["suben"]] == [r for r, _ in esperado["suben"]]
    for (_, js), (_, py) in zip(obtenido["suben"], esperado["suben"], strict=True):
        assert js == pytest.approx(py, abs=1e-9)
