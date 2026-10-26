"""Periodos del INPC: meses y quincenas.

INEGI etiqueta los periodos como ``Ene 2024`` (mensual) o ``1Q Ene 2024`` (quincenal).
En los archivos de ``data/`` se escriben como ``2024-01`` y ``2024-01-1Q``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

MESES = ("Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic")

_ETIQUETA_INEGI = re.compile(r"^(?:([12])Q\s+)?([A-Za-z]{3})\s+(\d{4})$")
_TEXTO = re.compile(r"^(\d{4})-(\d{2})(?:-([12])Q)?$")


@dataclass(frozen=True, order=True)
class Periodo:
    """Un mes (``quincena=0``) o una quincena (``1`` o ``2``) del INPC."""

    anio: int
    mes: int
    quincena: int = 0

    def __post_init__(self) -> None:
        if not 1 <= self.mes <= 12:
            raise ValueError(f"Mes inválido: {self.mes}")
        if self.quincena not in (0, 1, 2):
            raise ValueError(f"Quincena inválida: {self.quincena}")

    @property
    def es_quincenal(self) -> bool:
        return self.quincena != 0

    @classmethod
    def desde_etiqueta_inegi(cls, etiqueta: str) -> Periodo:
        """Convierte ``"Ene 2024"`` o ``"1Q Ene 2024"`` en un ``Periodo``."""
        coincidencia = _ETIQUETA_INEGI.match(etiqueta.strip())
        if not coincidencia:
            raise ValueError(f"Etiqueta de periodo no reconocida: {etiqueta!r}")
        quincena, mes, anio = coincidencia.groups()
        nombre_mes = mes.capitalize()
        if nombre_mes not in MESES:
            raise ValueError(f"Mes no reconocido: {mes!r}")
        return cls(int(anio), MESES.index(nombre_mes) + 1, int(quincena or 0))

    @classmethod
    def desde_texto(cls, texto: str) -> Periodo:
        """Convierte ``"2024-01"`` o ``"2024-01-1Q"`` en un ``Periodo``."""
        coincidencia = _TEXTO.match(texto.strip())
        if not coincidencia:
            raise ValueError(f"Periodo no reconocido: {texto!r}")
        anio, mes, quincena = coincidencia.groups()
        return cls(int(anio), int(mes), int(quincena or 0))

    def __str__(self) -> str:
        texto = f"{self.anio:04d}-{self.mes:02d}"
        return f"{texto}-{self.quincena}Q" if self.es_quincenal else texto

    def etiqueta_inegi(self) -> str:
        etiqueta = f"{MESES[self.mes - 1]} {self.anio}"
        return f"{self.quincena}Q {etiqueta}" if self.es_quincenal else etiqueta

    def desplazar(self, n: int) -> Periodo:
        """Avanza (o retrocede, si ``n`` es negativo) ``n`` periodos de la misma frecuencia."""
        if self.es_quincenal:
            indice = (self.anio * 12 + self.mes - 1) * 2 + self.quincena - 1 + n
            meses, quincena = divmod(indice, 2)
            anio, mes = divmod(meses, 12)
            return Periodo(anio, mes + 1, quincena + 1)
        anio, mes = divmod(self.anio * 12 + self.mes - 1 + n, 12)
        return Periodo(anio, mes + 1)

    def anterior(self, n: int = 1) -> Periodo:
        return self.desplazar(-n)
