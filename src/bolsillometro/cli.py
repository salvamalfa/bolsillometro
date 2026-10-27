"""Línea de comandos: los datos (``actualizar``, ``actualizar-ciudades``, ``actualizar-banxico``,
``verificar``) y tu inflación (``plantilla``, ``mi-inflacion``)."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from . import banxico, ciudades, personal
from . import datos as disco
from .pipeline import ErrorValidacion, Reconstruccion, actualizar, verificar
from .reconstruccion import Comparacion, error_maximo


def _imprimir_reconstruccion(resultado: Reconstruccion, detalle: bool) -> None:
    for nombre, comparaciones in (
        ("mensual", resultado.mensual),
        ("quincenal", resultado.quincenal),
    ):
        print(f"\nINPC {nombre}: reconstruido con 292 genéricos y ponderadores 2024")
        filas: list[Comparacion] = comparaciones if detalle else comparaciones[-3:]
        print(f"  {'periodo':<12}{'reconstruido':>14}{'publicado':>12}{'dif':>9}")
        for c in filas:
            marca = "" if c.cumple else "  <-- no cuadra"
            print(
                f"  {str(c.periodo):<12}{c.reconstruido:>14.3f}{c.publicado:>12.3f}"
                f"{c.diferencia:>+9.3f}{marca}"
            )
        if not detalle and len(comparaciones) > len(filas):
            print(f"  … {len(comparaciones) - len(filas)} periodos más (usa --detalle)")
        primero = comparaciones[0].periodo if comparaciones else "—"
        ultimo = comparaciones[-1].periodo if comparaciones else "—"
        print(
            f"  {len(comparaciones)} periodos ({primero} a {ultimo}), "
            f"error máximo {error_maximo(comparaciones):.3f}"
        )


def _imprimir_ciudades(validacion: ciudades.Validacion) -> None:
    print("\nINPC por ciudad: 55 ciudades × 292 genéricos (mensual)")
    print(
        f"  acotamiento {ciudades.INICIO_ACOTAMIENTO} a {ciudades.FIN_ACOTAMIENTO}: "
        f"{validacion.revisiones_acotamiento} revisiones, "
        f"{len(validacion.fuera_de_rango)} fuera del rango de sus ciudades"
    )
    peor = validacion.peor
    if peor:
        print(
            f"  plausibilidad: {len(validacion.plausibilidad)} comparaciones de inflación anual; "
            f"la mayor diferencia es {peor.diferencia:+.2f} pp ({peor.ciudad}, {peor.periodo}; "
            f"tolerancia ±{ciudades.TOLERANCIA_PLAUSIBILIDAD})"
        )


def _imprimir_banxico(validacion: banxico.Validacion, datos: banxico.DatosBanxico) -> None:
    print("\nBanxico: UDI diaria y Cetes a 28 días")
    print(f"  UDI hasta {max(datos.udi)}; última subasta de Cetes el {max(datos.cetes28)}")
    print(
        f"  UDI contra INPC: {len(validacion.udi)} tramos quincenales, "
        f"error máximo {validacion.error_maximo_udi:.1e} (tolerancia {banxico.TOLERANCIA_UDI:.0e})"
    )
    print(
        f"  crecimiento diario parejo en {validacion.dias_revisados} días, "
        f"error máximo {validacion.error_maximo_diario:.1e}"
    )


def _porcentaje(valor: float | None) -> str:
    return "     —" if valor is None else f"{valor:6.2f}%"


def _pesos(valor: float) -> str:
    return f"${valor:,.0f}"


def _imprimir_personal(
    resultado: personal.Resultado, rubros: dict[str, personal.Rubro], nombre_ciudad: str | None
) -> None:
    presupuesto = resultado.presupuesto
    print("Tu inflación personal (cálculos propios con datos del INPC, Fuente: INEGI)")
    lugar = nombre_ciudad or "nacional"
    print(
        f"  ciudad: {lugar} · gasto de {presupuesto.periodo_gasto} · datos hasta {resultado.ultimo}"
    )
    print(f"\n  {'':<22}{'anual':>8}{'mensual':>9}")
    filas = [("Tú", resultado.inflacion(12), resultado.inflacion(1))]
    filas.append(("INPC nacional", resultado.inflacion_inpc(12), resultado.inflacion_inpc(1)))
    if nombre_ciudad:
        filas.append(
            (
                f"INPC {nombre_ciudad.split(',')[0]}",
                resultado.inflacion_ciudad(12),
                resultado.inflacion_ciudad(1),
            )
        )
    for nombre, anual, mensual in filas:
        print(f"  {nombre:<22}{_porcentaje(anual):>8}{_porcentaje(mensual):>9}")

    if resultado.inflacion(12) is not None:
        print("\n  Lo que más movió tu inflación anual (puntos porcentuales):")
        for clave, puntos in list(resultado.incidencias_por_rubro(12).items())[:5]:
            print(f"    {puntos:+5.2f}  {rubros[clave].nombre}")

    print("\n  De dónde sale tu cifra:")
    contados = personal.rubros_que_cuentan(presupuesto)
    print(
        f"    {_pesos(resultado.total_cubierto)} al mes en {len(contados)} rubros que mide el INPC"
    )
    print(f"    {resultado.porcentaje_directo:5.1f}% asignado directo a un genérico")
    print(
        f"    {resultado.porcentaje_imputado:5.1f}% repartido con ponderadores oficiales (imputado)"
    )
    if resultado.porcentaje_propio:
        print(f"    {resultado.porcentaje_propio:5.1f}% con el aumento que tú capturaste")
    if nombre_ciudad:
        nacionales = 100 - resultado.porcentaje_ciudad - resultado.porcentaje_propio
        print(
            f"    Precios: {resultado.porcentaje_ciudad:.1f}% de tu ciudad y {nacionales:.1f}% "
            "nacionales (lo de precio casi único o que tu ciudad no cotiza)"
        )
    if presupuesto.vivienda_propia == "gasto_efectivo":
        print("    Vivienda propia: fuera (modo gasto_efectivo)")
    if resultado.total_no_cubierto:
        total = resultado.total_cubierto + resultado.total_no_cubierto
        print(
            f"    {_pesos(resultado.total_no_cubierto)} al mes que el INPC no mide "
            f"({100 * resultado.total_no_cubierto / total:.1f}% de tu gasto): "
            + ", ".join(c for c, monto in presupuesto.no_cubierto.items() if monto)
        )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bolsillometro",
        description="Datos del INPC (Fuente: INEGI) para calcular tu inflación personal.",
    )
    subcomandos = parser.add_subparsers(dest="comando", required=True)

    p_actualizar = subcomandos.add_parser(
        "actualizar", help="descarga del INEGI, valida la reconstrucción y escribe los datos"
    )
    p_verificar = subcomandos.add_parser(
        "verificar", help="reconstruye el INPC con los datos locales (sin red)"
    )
    p_ciudades = subcomandos.add_parser(
        "actualizar-ciudades",
        help="descarga las 55 ciudades del INEGI, las valida contra el nacional y las escribe",
    )
    p_banxico = subcomandos.add_parser(
        "actualizar-banxico",
        help="descarga UDI y Cetes de Banxico, valida la UDI contra el INPC y los escribe",
    )
    p_plantilla = subcomandos.add_parser(
        "plantilla", help="escribe un presupuesto.toml comentado para llenar"
    )
    p_plantilla.add_argument(
        "salida", type=Path, nargs="?", default=Path("presupuesto.toml"), help="archivo a escribir"
    )
    p_mi = subcomandos.add_parser("mi-inflacion", help="calcula tu inflación personal")
    p_mi.add_argument("presupuesto", type=Path, help="tu presupuesto.toml")
    for subparser in (p_actualizar, p_verificar, p_ciudades, p_banxico, p_plantilla, p_mi):
        subparser.add_argument(
            "--datos", type=Path, default=Path("data"), help="directorio de datos"
        )
        if subparser is p_actualizar or subparser is p_verificar:
            subparser.add_argument(
                "--detalle", action="store_true", help="muestra todos los periodos"
            )

    args = parser.parse_args(argv)
    if args.comando == "plantilla":
        if args.salida.exists():
            print(f"{args.salida} ya existe; no lo sobrescribo.", file=sys.stderr)
            return 1
        claves = (
            [c.clave for c in ciudades.leer_catalogo(args.datos)]
            if (args.datos / ciudades.DIRECTORIO).exists()
            else None
        )
        args.salida.write_text(personal.plantilla(personal.cargar_rubros(), claves), "utf-8")
        print(f"Plantilla escrita en {args.salida}. Llénala y corre:")
        print(f"  bolsillometro mi-inflacion {args.salida}")
        return 0

    if args.comando == "mi-inflacion":
        rubros = personal.cargar_rubros()
        try:
            presupuesto = personal.leer_presupuesto(args.presupuesto.read_text("utf-8"), rubros)
            datos_ciudades = None
            nombre_ciudad = None
            if presupuesto.ciudad != personal.NACIONAL:
                datos_ciudades = ciudades.cargar(args.datos)
                nombre_ciudad = next(
                    (c.nombre for c in datos_ciudades.ciudades if c.clave == presupuesto.ciudad),
                    None,
                )
            resultado = personal.calcular(
                presupuesto, rubros, disco.cargar(args.datos), datos_ciudades
            )
        except (personal.ErrorPresupuesto, OSError) as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1
        _imprimir_personal(resultado, rubros, nombre_ciudad)
        return 0

    if args.comando == "actualizar-ciudades":
        try:
            resumen_ciudades = ciudades.actualizar(args.datos)
        except ciudades.ErrorCiudades as error:
            print(f"Error de validación: {error}", file=sys.stderr)
            return 1
        nuevos = ", ".join(map(str, resumen_ciudades.nuevos[-6:])) or "ninguno"
        print(f"Datos por ciudad escritos en {args.datos / ciudades.DIRECTORIO}/")
        print(f"  periodos mensuales nuevos: {nuevos}")
        _imprimir_ciudades(resumen_ciudades.validacion)
        return 0

    if args.comando == "actualizar-banxico":
        try:
            resumen_banxico = banxico.actualizar(args.datos)
        except banxico.ErrorBanxico as error:
            print(f"Error de validación: {error}", file=sys.stderr)
            return 1
        print(f"Datos de Banxico escritos en {args.datos / banxico.DIRECTORIO}/")
        print(
            f"  días de UDI nuevos: {resumen_banxico.nuevas_udi}; "
            f"subastas de Cetes nuevas: {resumen_banxico.nuevas_subastas}"
        )
        _imprimir_banxico(resumen_banxico.validacion, banxico.cargar(args.datos))
        return 0

    try:
        if args.comando == "actualizar":
            resumen = actualizar(args.datos)
            resultado = resumen.reconstruccion
            nuevos_m = ", ".join(map(str, resumen.nuevos_mensual[-6:])) or "ninguno"
            nuevos_q = ", ".join(map(str, resumen.nuevos_quincenal[-6:])) or "ninguno"
            print(f"Datos escritos en {args.datos}/")
            print(f"  periodos mensuales nuevos: {nuevos_m}")
            print(f"  periodos quincenales nuevos: {nuevos_q}")
        else:
            resultado = verificar(args.datos)
    except ErrorValidacion as error:
        print(f"Error de validación: {error}", file=sys.stderr)
        return 1

    _imprimir_reconstruccion(resultado, args.detalle)
    if not resultado.cumple:
        print("\nLa reconstrucción no cuadra con el INPC publicado.", file=sys.stderr)
        return 1
    print("\nLa reconstrucción cuadra con el INPC publicado (±0.001).")

    if args.comando == "verificar" and (args.datos / ciudades.DIRECTORIO).exists():
        try:
            _imprimir_ciudades(ciudades.verificar(args.datos))
        except ciudades.ErrorCiudades as error:
            print(f"\nLos datos por ciudad no pasan la validación: {error}", file=sys.stderr)
            return 1
        print("\nLos datos por ciudad son consistentes con el nacional.")

    if args.comando == "verificar" and banxico.existe(args.datos):
        try:
            _imprimir_banxico(banxico.verificar(args.datos), banxico.cargar(args.datos))
        except banxico.ErrorBanxico as error:
            print(f"\nLos datos de Banxico no pasan la validación: {error}", file=sys.stderr)
            return 1
        print("\nLa UDI de Banxico cuadra con el INPC del INEGI.")
    return 0
