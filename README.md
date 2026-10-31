# Bolsímetro

**Tu inflación personal con datos del INPC (Fuente: INEGI).**

Proyecto open source para que cualquier persona en México calcule **su propia inflación**:
los índices de los 292 genéricos del INPC re-ponderados con su propio gasto.
Sirve para conocer tu costo de vida real y como benchmark de tus inversiones
(rendimiento real contra *tu* inflación, no contra la de un hogar promedio).

> Estado: fase 1 en curso. Ya están los datos nacionales y de las 55 ciudades, validados contra el INPC publicado,
> y la UDI y los Cetes de Banxico, validados contra el INPC.
> Ya calcula tu inflación personal en la web, con Claude o desde la línea de comandos; lo que sigue está en [`pendientes/`](pendientes/README.md).

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

## Calcula tu inflación

**En la web:** abre [`web/index.html`](web/index.html) en tu navegador (o la página publicada en
GitHub Pages). Contestas unas 25 preguntas con rangos y te da tu inflación de los últimos 12
meses. Todo se calcula en tu navegador; tus respuestas no se envían a ningún lado.

**Con Claude:** la entrevista conversada: en Claude Code, dentro de este repo, pide "hazme la
entrevista" (skill [`entrevista`](.claude/skills/entrevista/SKILL.md)). Claude te hace las
preguntas del [cuestionario estandarizado](src/bolsillometro/catalogos/cuestionario.toml) en
lenguaje común (renta, súper, luz, gasolina, colegiaturas…), arma tu presupuesto y te da **una
cifra: tu inflación de los últimos 12 meses**, qué la subió y si tus ahorros en Cetes le
ganaron. Tus respuestas se guardan en `presupuestos/`, que git ignora: no salen de tu máquina.

También se puede a mano:

```
pip install -e .
bolsillometro entrevista respuestas.json        # respuestas del cuestionario → presupuesto.toml
bolsillometro plantilla mi-presupuesto.toml     # o llenar los 32 rubros directamente
bolsillometro mi-inflacion mi-presupuesto.toml  # --detalle compara con el INPC y desglosa
```

Hay un ejemplo en [`ejemplos/pachuca-renta-auto.toml`](ejemplos/pachuca-renta-auto.toml).

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
python -m bolsillometro actualizar-banxico    # UDI y Cetes; valida la UDI contra el INPC
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
| `banxico.py` | UDI y Cetes a 28 días del SIE de Banxico: descarga, validación de la UDI contra el INPC y rendimientos de fin de mes a fin de mes. |
| `red.py` | Cliente HTTP con reintentos, común al INEGI y a Banxico. |
| `personal.py` | Tu inflación: presupuesto en TOML, catálogo de rubros (`catalogos/rubros.csv`) y cálculo con precios de tu ciudad o nacionales. |
| `cuestionario.py` | Del cuestionario estandarizado (`catalogos/cuestionario.toml`) a un presupuesto: frecuencias, condiciones y reparto oficial entre rubros. |
| `reporte.py` | El reporte en lenguaje claro: una cifra, qué la movió y si los Cetes le ganaron; `--detalle` para el resto. |
| `web.py` | Exporta lo que necesita la web (`web/datos/`): los últimos 15 meses de precios, rubros, cuestionario y Cetes. |
| `web/` | La web estática: la misma entrevista y el mismo cálculo en JavaScript (`calculo.js`), probado contra Python. |

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
