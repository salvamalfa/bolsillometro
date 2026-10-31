"""El pipeline completo, sin red: un cliente falso sirve respuestas armadas con ``data/``."""

import filecmp
from pathlib import Path

import pytest

from bolsillometro import datos as disco
from bolsillometro.inegi import ESTRUCTURA_MENSUAL
from bolsillometro.periodos import Periodo
from bolsillometro.pipeline import ErrorValidacion, actualizar

DATOS = Path(__file__).resolve().parents[1] / "data"
ARCHIVOS = [
    disco.ARCHIVO_MENSUAL,
    disco.ARCHIVO_QUINCENAL,
    disco.ARCHIVO_PONDERADORES,
    disco.ARCHIVO_CATALOGO,
    disco.ARCHIVO_METADATOS,
    disco.ARCHIVO_XLSX,
]


class ClienteFalso:
    """Imita las respuestas del INEGI (árbol, exportación CSV y XLSX) a partir de ``data/``."""

    def __init__(self, datos, xlsx, alterar=None):
        self.datos = datos
        self.xlsx = xlsx
        self.alterar = alterar or {}

    def _columna(self, estructura):
        return "id_mensual" if estructura == ESTRUCTURA_MENSUAL else "id_quincenal"

    def obtener_arbol(self, estructura):
        columna = self._columna(estructura)
        raiz = estructura + "0001"
        nodos, conceptos = [], {}
        for entrada in self.datos.catalogo:
            id_serie = getattr(entrada, columna)
            if entrada.codigo == "general":
                nodos.append((id_serie, raiz + "0010", "Índice general"))
                continue
            if entrada.concepto not in conceptos:
                clave = f"{raiz}0010{len(conceptos) + 1:04d}"
                conceptos[entrada.concepto] = [clave, 0]
                nodos.append((f"9{len(conceptos)}", clave, entrada.concepto))
            concepto = conceptos[entrada.concepto]
            concepto[1] += 1
            nodos.append(
                (
                    id_serie,
                    f"{concepto[0]}{concepto[1]:04d}",
                    f"{entrada.codigo} {entrada.generico}",
                )
            )
        html = "".join(
            f"<td>{t}</td><button onclick=\"ShowMoreInformation('{i}','{c}','{t}','');\">"
            for i, c, t in nodos
        )
        return {"d": html}

    def exportar(self, estructura, ids, anio_inicial, anio_final):
        columna = self._columna(estructura)
        codigo_de = {getattr(e, columna): e.codigo for e in self.datos.catalogo}
        series = self.datos.mensual if estructura == ESTRUCTURA_MENSUAL else self.datos.quincenal
        ids = list(ids)
        periodos = sorted({p for codigo in series for p in series[codigo]})
        lineas = [
            '"Instituto Nacional de Estadística y Geografía",',
            '"",',
            "",
            '"Fecha","' + '","'.join(ids) + '"',
        ]
        for periodo in periodos:
            valores = []
            for id_serie in ids:
                codigo = codigo_de[id_serie]
                valor = self.alterar.get((codigo, periodo), series[codigo].get(periodo))
                valores.append("NA" if valor is None else repr(valor))
            lineas.append(f'"{periodo.etiqueta_inegi()}","' + '","'.join(valores) + '"')
        return "\n".join(lineas) + "\n"

    def descargar_ponderadores(self):
        return self.xlsx


@pytest.fixture(scope="module")
def cliente():
    return ClienteFalso(disco.cargar(DATOS), (DATOS / disco.ARCHIVO_XLSX).read_bytes())


def test_actualizar_regenera_data_byte_por_byte(tmp_path, cliente):
    resumen = actualizar(tmp_path, cliente)
    assert resumen.reconstruccion.cumple
    for archivo in ARCHIVOS:
        assert filecmp.cmp(tmp_path / archivo, DATOS / archivo, shallow=False), archivo


def test_segunda_corrida_no_trae_periodos_nuevos(tmp_path, cliente):
    primera = actualizar(tmp_path, cliente)
    assert primera.nuevos_mensual[0] == Periodo(2018, 1)
    segunda = actualizar(tmp_path, cliente)
    assert segunda.nuevos_mensual == []
    assert segunda.nuevos_quincenal == []


def test_no_escribe_nada_si_la_reconstruccion_no_cuadra(tmp_path, cliente):
    ultimo = max(cliente.datos.mensual["general"])
    publicado = cliente.datos.mensual["general"][ultimo]
    alterado = ClienteFalso(cliente.datos, cliente.xlsx, {("general", ultimo): publicado + 0.01})
    with pytest.raises(ErrorValidacion, match=str(ultimo)):
        actualizar(tmp_path, alterado)
    assert list(tmp_path.iterdir()) == []
