# Bolsillómetro

**Tu inflación personal con datos del INPC (Fuente: INEGI).**

Proyecto open source para que cualquier persona en México calcule **su propia inflación**:
los índices de los 292 genéricos del INPC re-ponderados con su propio gasto.
Sirve para conocer tu costo de vida real y como benchmark de tus inversiones
(rendimiento real contra *tu* inflación, no contra la de un hogar promedio).

> Estado: fase 1 en curso. Ya están los datos nacionales y de las 55 ciudades, validados contra el INPC publicado.
> Todavía no hay cálculo personal; lo que sigue está en [`pendientes/`](pendientes/README.md).
> Este repo antes era "Combis Zempoala"; ese proyecto se deprecó y su contenido sigue en el historial de git.

## La idea en una fórmula

```
P(t) = 100 · Σ_k s_k · I_k(t) / I_k(b)
```

`I_k(t)` es el índice publicado del genérico k (nacional o de tu ciudad) y `s_k` es la parte de tu gasto
que va a ese genérico. Con los ponderadores oficiales del INEGI la fórmula reproduce el INPC publicado;
con los tuyos, da tu inflación.

## Principios

- **Precios oficiales, pesos propios.** Los precios vienen del INEGI; lo único personal son los ponderadores.
- **Local-first.** Tus movimientos bancarios y facturas no salen de tu máquina; lo que se comparte son agregados.
- **Transparencia.** Cada resultado dice qué parte de tu gasto se observó y qué parte se imputó.
- **Referencia, no recomendación.** No es asesoría de inversiones.

## Fase 0: datos del INEGI

El paquete `bolsillometro` descarga del INEGI, sin token, los índices nacionales de los 292 genéricos
(mensuales y quincenales, desde 2018) y los ponderadores oficiales de la canasta 2024. Antes de guardar
nada, comprueba que con esos datos se reconstruye el INPC publicado, periodo por periodo, con un error
de a lo más una milésima. Si el INEGI cambia algo, el pipeline falla en lugar de guardar datos malos.

Requiere Python 3.11 o más reciente.

```
pip install -e ".[dev]"
python -m bolsillometro actualizar   # descarga, valida y escribe data/
python -m bolsillometro verificar    # reconstruye el INPC con data/, sin red (--detalle para ver todo)
python -m bolsillometro actualizar-ciudades   # 55 ciudades, ~10 min; valida contra el nacional
pytest                               # pruebas, incluida la reconstrucción con los datos reales
```

Resultado actual de `verificar`: 26 meses (ago-2024 a sep-2026) y 53 quincenas (1Q ago-2024 a
1Q oct-2026) reconstruidos con error máximo de 0.001.

Los datos viven en [`data/`](data/LEEME.md) como CSV versionados (una fila por periodo, una columna
por genérico). El workflow [`actualizar-datos.yml`](.github/workflows/actualizar-datos.yml) corre en
los días de publicación del INPC y hace commit solo cuando hay datos nuevos.

| Módulo | Qué hace |
|---|---|
| `inegi.py` | Cliente de la app "Índices de Precios" del INEGI (la misma exportación que usan los .IQY de Excel). |
| `lectura.py` | Lee el árbol de series, la exportación CSV y el XLSX de ponderadores. |
| `indices.py` | Motor Laspeyres/Lowe: índice ponderado, pesos tipo Lowe, variaciones, incidencias, encadenamiento y rendimiento real. |
| `reconstruccion.py` | Reconstruye el INPC con los ponderadores oficiales y lo compara con el publicado. |
| `pipeline.py` | Descarga, valida y escribe `data/`. |
| `ciudades.py` | INPC por ciudad (55 ciudades × 292 genéricos, mensual): descarga, validación contra el nacional y `data/ciudades/`. |

## Documentos

- [`pendientes/`](pendientes/README.md): lo que sigue abierto, incluidos los pasos que faltan de la fase 1.
- [`CHANGELOG.md`](CHANGELOG.md): lo que ya está hecho, por fase y PR.
- [`docs/decisiones.md`](docs/decisiones.md): las decisiones de diseño ya tomadas y su motivo.
- [`CONTRIBUTING.md`](CONTRIBUTING.md): cómo preparar el entorno, qué correr antes de cada push y las convenciones.
- [`docs/00-investigacion-inicial.md`](docs/00-investigacion-inicial.md): reporte con la viabilidad, las fórmulas para
  re-ponderar genéricos, la arquitectura local-first, la hoja de ruta (MVP → plugin para Claude/ChatGPT → capa de pago
  opcional), los precedentes en México y el mundo, las ideas de nombre, el modelo de negocio y las líneas regulatorias.
- [`docs/notas/`](docs/notas/): notas de investigación con fuentes (algunas en inglés):
  - [`01-datos-inegi-metodologia.md`](docs/notas/01-datos-inegi-metodologia.md): qué publica el INEGI, cómo descargarlo sin token y cómo se reconstruye el INPC.
  - [`02-datos-gasto-y-arquitectura-ia.md`](docs/notas/02-datos-gasto-y-arquitectura-ia.md): open finance en México, agregadores, CFDI, clasificación de movimientos y MCP.
  - [`03-precedentes-oficiales-y-academicos.md`](docs/notas/03-precedentes-oficiales-y-academicos.md): calculadoras de oficinas de estadística y evidencia académica.
  - [`04-precedentes-privados-y-open-source.md`](docs/notas/04-precedentes-privados-y-open-source.md): fintechs, índices alternativos y repos en GitHub.
  - [`05-negocio-regulacion-nombres.md`](docs/notas/05-negocio-regulacion-nombres.md): monetización, regulación en México, difusión y nombres.

## Licencia

[MIT](LICENSE).

---

Cálculos propios con datos del INPC (Fuente: INEGI). No es un producto oficial del INEGI ni de Banco de México.
