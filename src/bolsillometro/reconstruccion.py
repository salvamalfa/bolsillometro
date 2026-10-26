"""Reconstrucción del INPC publicado a partir de sus 292 genéricos y los ponderadores oficiales.

Es la prueba de que el motor y los datos están bien: con los pesos del INEGI, el índice
agregado debe dar el INPC publicado con una diferencia de a lo más una milésima.

Desde la 1Q de agosto de 2024 el INPC usa la canasta y ponderadores 2024, encadenados en la
2Q de julio de 2024. Después del eslabón las series publicadas ya no son aditivas, así que cada
genérico se re-referencia con su valor quincenal de la 2Q jul-2024 (también para las series
mensuales), se promedia con los ponderadores y se multiplica por el INPC de esa quincena / 100.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from .indices import Serie, indice_ponderado, valores_en
from .lectura import Ponderador
from .periodos import Periodo

BASE_PONDERADORES = Periodo(2024, 7, 2)
INICIO_MENSUAL = Periodo(2024, 8)
INICIO_QUINCENAL = Periodo(2024, 8, 1)
TOLERANCIA = 0.001


@dataclass(frozen=True)
class Comparacion:
    periodo: Periodo
    reconstruido: float
    publicado: float

    @property
    def diferencia(self) -> float:
        """Reconstruido (redondeado a tres decimales, como publica el INEGI) menos publicado."""
        return round(round(self.reconstruido, 3) - self.publicado, 3)

    @property
    def cumple(self) -> bool:
        return abs(self.diferencia) <= TOLERANCIA


def factor_encadenamiento(quincenal: Mapping[str, Serie]) -> float:
    """INPC de la 2Q jul-2024 / 100."""
    valor = quincenal["general"].get(BASE_PONDERADORES)
    if valor is None:
        raise KeyError(f"Falta el INPC de {BASE_PONDERADORES}")
    return valor / 100


def reconstruir_inpc(
    series: Mapping[str, Serie],
    quincenal: Mapping[str, Serie],
    ponderadores: Iterable[Ponderador],
) -> list[Comparacion]:
    """Compara el INPC reconstruido contra el publicado, periodo por periodo.

    ``series`` son las series mensuales o quincenales (``"general"`` y un código por
    genérico); ``quincenal`` aporta los valores de la 2Q jul-2024 para re-referenciar.
    """
    pesos = {p.codigo: p.ponderador for p in ponderadores}
    base = valores_en({codigo: quincenal[codigo] for codigo in pesos}, BASE_PONDERADORES)
    general = series["general"]
    inicio = INICIO_QUINCENAL if any(p.es_quincenal for p in general) else INICIO_MENSUAL

    agregado = indice_ponderado(
        {codigo: series[codigo] for codigo in pesos},
        pesos,
        base,
        factor_encadenamiento(quincenal),
    )
    return [
        Comparacion(periodo, valor, general[periodo])
        for periodo, valor in agregado.items()
        if periodo >= inicio and general.get(periodo) is not None
    ]


def error_maximo(comparaciones: Iterable[Comparacion]) -> float:
    return max((abs(c.diferencia) for c in comparaciones), default=0.0)
