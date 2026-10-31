"""Motor de índices: Laspeyres/Lowe con ponderadores propios.

Notación (la misma del reporte en ``docs/00-investigacion-inicial.md``):

- ``I_k(t)``: índice publicado del genérico ``k`` en el periodo ``t``.
- ``I_k(b)``: su valor en el periodo base ``b`` del índice que se construye.
- ``s_k``: peso del genérico ``k`` (participación en el gasto), con ``Σ s_k = 1``.

El índice agregado es ``P(t) = f · 100 · Σ_k s_k · I_k(t) / I_k(b)``, donde ``f`` es un
factor de encadenamiento (1 para un índice propio; el INPC de la 2Q jul-2024 / 100 para
reproducir el INPC publicado). Cuando cambian los pesos, ``encadenar`` une los tramos en el
periodo de traslape (fórmula 5 del reporte) y ``rendimiento_real`` compara una inversión
contra la inflación (fórmula 7).
"""

from __future__ import annotations

from collections.abc import Mapping

from .periodos import Periodo

Serie = Mapping[Periodo, float | None]


def normalizar(pesos: Mapping[str, float]) -> dict[str, float]:
    """Escala los pesos para que sumen 1; descarta los que valen cero."""
    total = sum(pesos.values())
    if total <= 0:
        raise ValueError("Los pesos deben sumar más que cero")
    return {codigo: peso / total for codigo, peso in pesos.items() if peso}


def valores_en(series: Mapping[str, Serie], periodo: Periodo) -> dict[str, float]:
    """Valor de cada serie en ``periodo``; falla si a alguna le falta el dato."""
    valores = {}
    for codigo, serie in series.items():
        valor = serie.get(periodo)
        if valor is None:
            raise KeyError(f"La serie {codigo} no tiene dato en {periodo}")
        valores[codigo] = valor
    return valores


def pesos_lowe(
    gasto: Mapping[str, float],
    indices_periodo_gasto: Mapping[str, float],
    indices_base: Mapping[str, float],
) -> dict[str, float]:
    """Lleva participaciones de gasto del periodo ``e`` al periodo base ``b``.

    ``s_k(b) ∝ s_k(e) · I_k(b) / I_k(e)``. Es la actualización por precios relativos que
    hace el INEGI; sin ella el índice sería "tipo Young" en lugar de "tipo Lowe".
    """
    participaciones = normalizar(gasto)
    return normalizar(
        {
            codigo: peso * indices_base[codigo] / indices_periodo_gasto[codigo]
            for codigo, peso in participaciones.items()
        }
    )


def indice_ponderado(
    series: Mapping[str, Serie],
    pesos: Mapping[str, float],
    base: Mapping[str, float],
    factor: float = 1.0,
) -> dict[Periodo, float]:
    """``P(t) = factor · 100 · Σ_k s_k · I_k(t) / I_k(b)``.

    ``base`` trae ``I_k(b)`` para cada genérico con peso. Solo se calculan los periodos en
    que todos los genéricos con peso tienen dato.
    """
    pesos = normalizar(pesos)
    faltantes = [codigo for codigo in pesos if codigo not in series or codigo not in base]
    if faltantes:
        raise KeyError(f"Faltan series o valores base para: {', '.join(sorted(faltantes))}")

    periodos = set.intersection(
        *({p for p, v in series[codigo].items() if v is not None} for codigo in pesos)
    )
    return {
        periodo: factor
        * 100
        * sum(peso * series[codigo][periodo] / base[codigo] for codigo, peso in pesos.items())
        for periodo in sorted(periodos)
    }


def variacion(serie: Serie, periodo: Periodo, rezago: int = 1) -> float:
    """Variación porcentual de ``periodo`` contra ``rezago`` periodos antes.

    Con series mensuales, ``rezago=1`` es la inflación mensual y ``rezago=12`` la anual;
    con quincenales, ``rezago=24`` es la anual.
    """
    actual = serie.get(periodo)
    previo = serie.get(periodo.anterior(rezago))
    if actual is None or previo is None:
        raise KeyError(f"Faltan datos para la variación de {periodo} con rezago {rezago}")
    return (actual / previo - 1) * 100


def incidencias(
    series: Mapping[str, Serie],
    pesos: Mapping[str, float],
    base: Mapping[str, float],
    desde: Periodo,
    hasta: Periodo,
) -> dict[str, float]:
    """Contribución de cada genérico, en puntos porcentuales, a la variación ``desde → hasta``.

    ``C_k = 100 · s_k · (R_k(hasta) − R_k(desde)) / Σ_j s_j · R_j(desde)``, con
    ``R_k = I_k / I_k(b)``. Equivale a usar el ponderador efectivo en ``desde``, por lo que las
    incidencias suman exactamente la variación del índice agregado.
    """
    pesos = normalizar(pesos)
    relativo = {
        codigo: (series[codigo][desde] / base[codigo], series[codigo][hasta] / base[codigo])
        for codigo in pesos
    }
    denominador = sum(peso * relativo[codigo][0] for codigo, peso in pesos.items())
    return {
        codigo: 100 * peso * (relativo[codigo][1] - relativo[codigo][0]) / denominador
        for codigo, peso in pesos.items()
    }


def encadenar(
    anterior: Mapping[Periodo, float],
    series: Mapping[str, Serie],
    pesos_nuevos: Mapping[str, float],
    eslabon: Periodo,
) -> dict[Periodo, float]:
    """Cambia los pesos de un índice en el periodo de traslape ``eslabon`` (``L``).

    ``P(t) = P(L) · Σ_k s_k(nuevo) · I_k(t) / I_k(L)`` para ``t > L``; hasta ``L`` se conserva
    ``anterior``. Los pesos nuevos deben estar referidos a ``L``: si el gasto es de otro
    periodo, llévalos antes con ``pesos_lowe``. Se puede encadenar varias veces.
    """
    if eslabon not in anterior:
        raise KeyError(f"El índice anterior no tiene dato en el eslabón {eslabon}")
    faltantes = [codigo for codigo in pesos_nuevos if codigo not in series]
    if faltantes:
        raise KeyError(f"Faltan series para: {', '.join(sorted(faltantes))}")
    base = valores_en({codigo: series[codigo] for codigo in pesos_nuevos}, eslabon)
    tramo = indice_ponderado(series, pesos_nuevos, base, anterior[eslabon] / 100)
    return {p: v for p, v in anterior.items() if p <= eslabon} | {
        p: v for p, v in tramo.items() if p > eslabon
    }


def incidencias_encadenadas(
    antes: Mapping[str, float], despues: Mapping[str, float]
) -> dict[str, float]:
    """Incidencias de una variación que cruza un eslabón, en puntos porcentuales.

    ``antes`` son las incidencias de ``desde → L`` (suman ``a``) y ``despues`` las de
    ``L → hasta`` (suman ``b``). Con la convención ``(1+a)(1+b) − 1 = Σ Cᵃ·(1+b) + Σ Cᵇ``,
    ``C_k = Cᵃ_k · (1 + b) + Cᵇ_k``, y las incidencias suman la variación total.
    """
    b = sum(despues.values()) / 100
    return {
        codigo: antes.get(codigo, 0.0) * (1 + b) + despues.get(codigo, 0.0)
        for codigo in antes.keys() | despues.keys()
    }


def rendimiento_real(nominal: float, inflacion: float) -> float:
    """``r_real = (1 + r_nominal) / (1 + π) − 1``, todo en porcentaje.

    Con ``π`` tu inflación personal, es lo que tu inversión ganó (o perdió) en poder de
    compra de tu propia canasta durante el mismo periodo.
    """
    if inflacion <= -100:
        raise ValueError("La inflación debe ser mayor que -100%")
    return ((1 + nominal / 100) / (1 + inflacion / 100) - 1) * 100
