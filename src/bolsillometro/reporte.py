"""El reporte de tu inflación, en lenguaje claro: una cifra, qué la movió y si tus ahorros le ganan.

Por omisión muestra solo lo que una persona necesita: su inflación de los últimos 12 meses, los
rubros que más la subieron (cuánto subió cada uno y cuántos puntos aporta) y, si hay datos de
Banxico, si los Cetes a 28 días le ganaron. Con ``detalle`` agrega la comparación con el INPC,
la inflación del mes y de dónde sale la cifra (directo, imputado, aumento propio, precios de la
ciudad o nacionales y gasto que el INPC no mide).
"""

from __future__ import annotations

from collections.abc import Mapping

from . import banxico
from .indices import rendimiento_real
from .periodos import MESES, Periodo
from .personal import Resultado, Rubro, rubros_que_cuentan

RUBROS_EN_RESUMEN = 4


def mes(periodo: Periodo) -> str:
    return f"{MESES[periodo.mes - 1].lower()}-{periodo.anio}"


def _pesos(valor: float) -> str:
    return f"${valor:,.0f}"


def _porcentaje(valor: float | None) -> str:
    return "—" if valor is None else f"{valor:.2f}%"


def rendimiento_cetes(cetes: Mapping | None, desde: Periodo, hasta: Periodo) -> float | None:
    if not cetes:
        return None
    try:
        return banxico.rendimiento_cetes(cetes, desde, hasta)
    except KeyError:
        return None


def texto(
    resultado: Resultado,
    rubros: Mapping[str, Rubro],
    nombre_ciudad: str | None = None,
    cetes: Mapping | None = None,
    detalle: bool = False,
) -> str:
    hasta = resultado.ultimo
    desde = hasta.anterior(12)
    anual = resultado.inflacion(12)
    if anual is None:
        return "Todavía no hay 12 meses de datos para calcular tu inflación anual.\n"
    lugar = f"los precios de {nombre_ciudad}" if nombre_ciudad else "los precios nacionales"
    lineas = [
        f"Tu inflación: {anual:.2f}%",
        f"de {mes(desde)} a {mes(hasta)}, con tu gasto y {lugar.rstrip('.')}.",
    ]

    incidencias = resultado.incidencias_por_rubro(12)
    variaciones = resultado.variacion_por_rubro(12)
    suben = [(r, p) for r, p in incidencias.items() if p > 0][:RUBROS_EN_RESUMEN]
    if suben:
        lineas += ["", f"Lo que más la subió (de tus {anual:.2f} puntos):"]
        ancho = max(len(rubros[r].nombre) for r, _ in suben)
        for clave, puntos in suben:
            lineas.append(
                f"  {rubros[clave].nombre + ':':<{ancho + 1}}  subió {variaciones[clave]:4.1f}% "
                f"y aporta {puntos:.2f} puntos"
            )
    bajan = [(r, p) for r, p in incidencias.items() if p < 0]
    if bajan:
        clave, puntos = min(bajan, key=lambda par: par[1])
        lineas.append(
            f"  Lo que más la bajó: {rubros[clave].nombre}, "
            f"{variaciones[clave]:.1f}% ({puntos:.2f} puntos)"
        )

    cetes_anual = rendimiento_cetes(cetes, desde, hasta)
    if cetes_anual is not None:
        real = rendimiento_real(cetes_anual, anual)
        veredicto = "le ganó a tu inflación" if real >= 0 else "perdió contra tu inflación"
        lineas += [
            "",
            "¿Tus ahorros le ganan?",
            f"  En Cetes a 28 días, tu dinero ganó {cetes_anual:.2f}%: "
            f"{veredicto} por {abs(real):.2f}%.",
        ]

    if detalle:
        lineas += _detalle(resultado, nombre_ciudad)
    return "\n".join(lineas) + "\n"


def _detalle(resultado: Resultado, nombre_ciudad: str | None) -> list[str]:
    presupuesto = resultado.presupuesto
    lineas = ["", "Detalle:"]
    lineas.append(
        f"  Tu inflación del último mes: {_porcentaje(resultado.inflacion(1))} "
        f"(mes del gasto: {mes(presupuesto.periodo_gasto)})"
    )
    lineas.append(
        f"  Como referencia, el INPC (hogar promedio del país): "
        f"{_porcentaje(resultado.inflacion_inpc(12))} anual"
    )
    if nombre_ciudad:
        lineas.append(
            f"  y el INPC de {nombre_ciudad}: {_porcentaje(resultado.inflacion_ciudad(12))} anual"
        )
    contados = rubros_que_cuentan(presupuesto)
    lineas.append(
        f"  Tu gasto: {_pesos(resultado.total_cubierto)} al mes en {len(contados)} rubros que mide "
        "el INPC"
    )
    lineas.append(f"    {resultado.porcentaje_directo:5.1f}% asignado directo a un genérico")
    lineas.append(
        f"    {resultado.porcentaje_imputado:5.1f}% repartido con ponderadores oficiales (imputado)"
    )
    if resultado.porcentaje_propio:
        lineas.append(f"    {resultado.porcentaje_propio:5.1f}% con el aumento que tú diste")
    if nombre_ciudad:
        nacionales = 100 - resultado.porcentaje_ciudad - resultado.porcentaje_propio
        lineas.append(
            f"  Precios: {resultado.porcentaje_ciudad:.1f}% de tu ciudad y {nacionales:.1f}% "
            "nacionales (lo de precio casi único o que tu ciudad no cotiza)"
        )
    if presupuesto.vivienda_propia == "gasto_efectivo":
        lineas.append("  Vivienda propia: fuera (modo gasto_efectivo)")
    if resultado.total_no_cubierto:
        total = resultado.total_cubierto + resultado.total_no_cubierto
        conceptos = ", ".join(c for c, monto in presupuesto.no_cubierto.items() if monto)
        lineas.append(
            f"  Además: {_pesos(resultado.total_no_cubierto)} al mes que el INPC no mide "
            f"({100 * resultado.total_no_cubierto / total:.1f}% de tu gasto): {conceptos}"
        )
    return lineas
