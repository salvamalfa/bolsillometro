"""Línea de comandos.

- Datos: ``actualizar``, ``actualizar-ciudades``, ``actualizar-banxico`` y ``verificar``.
- Tu inflación: ``plantilla``, ``mi-inflacion`` y ``entrevista``.
- La web: ``web`` exporta sus datos.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from . import banxico, ciudades, cuestionario, personal, reporte, web
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


def _cargar_ciudades(datos: Path, clave: str) -> tuple[ciudades.DatosCiudades | None, str | None]:
    if clave == personal.NACIONAL:
        return None, None
    datos_ciudades = ciudades.cargar(datos)
    nombre = next(
        (ciudades.nombre_comun(c) for c in datos_ciudades.ciudades if c.clave == clave), None
    )
    return datos_ciudades, nombre


def _reporte(presupuesto: personal.Presupuesto, rubros, datos: Path, detalle: bool) -> str:
    datos_ciudades, nombre_ciudad = _cargar_ciudades(datos, presupuesto.ciudad)
    resultado = personal.calcular(presupuesto, rubros, disco.cargar(datos), datos_ciudades)
    cetes = banxico.cargar(datos).cetes28 if banxico.existe(datos) else None
    return reporte.texto(resultado, rubros, nombre_ciudad, cetes, detalle)


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
    p_entrevista = subcomandos.add_parser(
        "entrevista",
        help="convierte las respuestas del cuestionario (JSON) en presupuesto.toml y lo calcula",
    )
    p_entrevista.add_argument("respuestas", type=Path, help="respuestas.json del cuestionario")
    p_entrevista.add_argument(
        "--salida", type=Path, help="presupuesto a escribir (por omisión, junto a las respuestas)"
    )
    p_web = subcomandos.add_parser(
        "web", help="exporta los datos que usa la web estática (web/datos/) desde data/"
    )
    p_web.add_argument("--salida", type=Path, default=Path("web"), help="carpeta de la web")
    for subparser in (p_mi, p_entrevista):
        subparser.add_argument(
            "--detalle", action="store_true", help="agrega la comparación con el INPC y el desglose"
        )
    for subparser in (
        p_actualizar,
        p_verificar,
        p_ciudades,
        p_banxico,
        p_plantilla,
        p_mi,
        p_entrevista,
        p_web,
    ):
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

    if args.comando == "web":
        escritos = web.exportar(args.datos, args.salida)
        print(
            f"Datos de la web escritos en {args.salida / web.DIRECTORIO_DATOS}/ "
            f"({len(escritos)} archivos)"
        )
        return 0

    if args.comando in ("mi-inflacion", "entrevista"):
        rubros = personal.cargar_rubros()
        try:
            if args.comando == "mi-inflacion":
                presupuesto = personal.leer_presupuesto(args.presupuesto.read_text("utf-8"), rubros)
            else:
                respuestas = json.loads(args.respuestas.read_text("utf-8"))
                claves = (
                    [c.clave for c in ciudades.leer_catalogo(args.datos)]
                    if (args.datos / ciudades.DIRECTORIO).exists()
                    else None
                )
                nacional = disco.cargar(args.datos)
                general_ciudad = None
                if claves and respuestas.get("ciudad") in claves:
                    general_ciudad = ciudades.cargar(args.datos).series[respuestas["ciudad"]][
                        "general"
                    ]
                presupuesto = cuestionario.presupuesto_desde_respuestas(
                    respuestas,
                    cuestionario.cargar_cuestionario(),
                    rubros,
                    nacional,
                    claves,
                    cuestionario.mes_del_gasto(nacional, general_ciudad),
                )
                salida = args.salida or args.respuestas.with_suffix(".toml")
                salida.write_text(personal.a_toml(presupuesto, rubros), "utf-8")
                print(f"Presupuesto escrito en {salida}\n")
            texto = _reporte(presupuesto, rubros, args.datos, args.detalle)
        except (personal.ErrorPresupuesto, OSError, json.JSONDecodeError) as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1
        print(texto, end="")
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
