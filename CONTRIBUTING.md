# Cómo contribuir

## Preparar el entorno

Requiere Python 3.11 o más reciente.

```
pip install -e ".[dev]"
```

## Antes de cada push

```
ruff format --check src tests
ruff check src tests
pytest
```

Todas las pruebas deben pasar, incluidas las que usan los datos reales de `data/`: la
reconstrucción del INPC nacional y la validación de las ciudades.

## Convenciones

- **Idioma:** identificadores, docstrings, comentarios, commits y documentos en español.
- **Dependencias:** solo `requests` y `openpyxl`. Una nueva necesita una entrada en
  [`docs/decisiones.md`](docs/decisiones.md).
- **Datos de personas:** los presupuestos y respuestas van en `presupuestos/`, que git ignora.
  Nunca se suben ni se pegan en un PR o issue.
- **Datos:** `data/` no se edita a mano. Se regenera con `bolsillometro actualizar` y
  `bolsillometro actualizar-ciudades`, que validan antes de escribir.
- **Web:** `web/datos/` tampoco se edita a mano: si cambian `data/`, los rubros o el
  cuestionario, corre `bolsillometro web` (lo revisa `tests/test_web.py`). Si cambias el cálculo
  en Python, cambia igual `web/calculo.js`: las pruebas comparan ambos.
- **Commits y PRs:** un PR por paso, fusionado con squash. El título empieza con su área:
  `fase 1: …`, `docs: …` o `datos: …` (este último lo usa solo el workflow).

## Pendientes, decisiones y cambios

- [`pendientes/`](pendientes/README.md) solo tiene lo que sigue abierto.
- El PR que cierra un pendiente lo borra de ahí y lo pasa a su destino:
  - Un paso hecho va a [`CHANGELOG.md`](CHANGELOG.md).
  - Una decisión va a [`docs/decisiones.md`](docs/decisiones.md).
  - Una convención va a este archivo.

## Dónde está qué

- **El INEGI:** endpoints, ids de estructura y receta de reconstrucción en
  [`docs/notas/01-datos-inegi-metodologia.md`](docs/notas/01-datos-inegi-metodologia.md) y
  `src/bolsillometro/inegi.py`.
- **Los datos:** formato y validaciones en [`data/LEEME.md`](data/LEEME.md).
- **Las fórmulas:** en [`docs/00-investigacion-inicial.md`](docs/00-investigacion-inicial.md)
  y `src/bolsillometro/indices.py`.
