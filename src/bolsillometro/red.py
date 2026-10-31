"""Cliente HTTP con reintentos, común a las fuentes (INEGI y Banxico)."""

from __future__ import annotations

import time

import requests

from . import __version__

ENCABEZADOS = {"User-Agent": f"bolsillometro/{__version__}"}


class ErrorFuente(RuntimeError):
    """Una fuente respondió algo distinto de lo esperado."""


class ClienteHTTP:
    """Reintenta errores de red y HTTP 5xx con espera creciente; falla con ``self.Error``."""

    Error: type[ErrorFuente] = ErrorFuente

    def __init__(
        self,
        sesion: requests.Session | None = None,
        timeout: float = 180,
        reintentos: int = 3,
        espera: float = 5,
    ) -> None:
        self.sesion = sesion or requests.Session()
        self.sesion.headers.update(ENCABEZADOS)
        self.timeout = timeout
        self.reintentos = reintentos
        self.espera = espera

    def _pedir(
        self, metodo: str, url: str, timeout: float | None = None, **kwargs
    ) -> requests.Response:
        for intento in range(1, self.reintentos + 1):
            try:
                respuesta = self.sesion.request(
                    metodo, url, timeout=timeout or self.timeout, **kwargs
                )
                if respuesta.status_code < 500:
                    respuesta.raise_for_status()
                    return respuesta
                error: Exception = self.Error(f"HTTP {respuesta.status_code} en {url}")
            except (requests.ConnectionError, requests.Timeout) as excepcion:
                error = excepcion
            if intento < self.reintentos:
                time.sleep(self.espera * intento)
        raise self.Error(
            f"Sin respuesta válida de {url} tras {self.reintentos} intentos"
        ) from error
