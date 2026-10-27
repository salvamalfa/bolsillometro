"""Línea de comandos: ``actualizar``, ``actualizar-ciudades`` y ``verificar``."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from . import ciudades
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
    for subparser in (p_actualizar, p_verificar, p_ciudades):
        subparser.add_argument(
            "--datos", type=Path, default=Path("data"), help="directorio de datos"
        )
        if subparser is not p_ciudades:
            subparser.add_argument(
                "--detalle", action="store_true", help="muestra todos los periodos"
            )

    args = parser.parse_args(argv)
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
    return 0
