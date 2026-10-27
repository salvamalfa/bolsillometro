# Pendientes

Lo que quedó abierto al cerrar la sesión del 26-oct-2026. Al retomarlo, empieza por aquí.

## Dónde estamos

- La **fase 0 ya está en `main`** (PR #2). El pipeline descarga del INEGI los 292 genéricos
  nacionales, mensuales y quincenales desde 2018, más los ponderadores 2024. Antes de escribir
  `data/` reconstruye el INPC publicado con error de ±0.001.
- Los datos llegan hasta **2026-09** (mensual) y **2026-10-1Q** (quincenal).
- El workflow `actualizar-datos.yml` ya se probó a mano en `main`: los runners de GitHub
  sí llegan al INEGI. El próximo dato (2Q de octubre) sale hacia el 9 de noviembre y debe
  entrar solo, con un commit `datos: INPC hasta …`.
- El repo se llama `salvamalfa/bolsillometro`. Antes se llamaba `combis-zempoala`.

## Próximo paso técnico: la fase 1

Ver [`fase-1.md`](fase-1.md). Las decisiones ya se tomaron y el plan va en 6 PRs. El primero
(fórmulas 5 y 7 del motor) está hecho; sigue el de datos por ciudad.

## Pendientes no técnicos (antes del lanzamiento público)

- [ ] **Marca en el IMPI:** buscar "Bolsillómetro" en MARCia: marcas idénticas y fonéticamente
  parecidas, en las clases 9, 35, 36 y 42. Conviene que un agente de propiedad industrial
  confirme las clases antes de presentar la solicitud.
- [ ] **Dominios:** registrar juntos `bolsillometro.com`, `.mx` y `.app`. El 26-oct-2026 los
  tres se veían libres, pero eso era solo una señal, no una garantía.
- [ ] **Abogado mexicano:** confirmar tres puntos:
  - Que mostrar "tu inflación como benchmark" no cruza a asesoría de inversiones (LMV art. 225).
  - Qué exige la LFPDPPP 2025 si algún día se guardan datos de usuarios.
  - Las reglas de PROFECO para una suscripción opcional.
- [ ] **Reglas para exempleados de Banxico:** revisarlas antes de buscar alianzas con Banxico o
  con el MIDE, o de usar frases que suenen a información interna.

## Limpieza opcional del repo en GitHub

- [ ] Borrar la rama `claude/inflacion-personal`. Ya se fusionó con squash, pero conserva los
  dos commits originales.
- [ ] Borrar la rama `claude/zempoala-combi-app-gxbqvi`, que es del proyecto de combis.

## Notas para la próxima sesión

- **Decisiones ya tomadas:**
  - El código es propio, construido desde cero. No se hacen forks ni se depende de otros
    repos del INPC.
  - Paquete y CLI `bolsillometro`, licencia MIT, Python 3.11 o más.
  - Solo `requests` y `openpyxl` como dependencias.
  - Identificadores y docstrings en español.
- **Diseño local-first:** los movimientos y facturas del usuario nunca salen de su máquina.
  Hacia fuera solo salen agregados.
- **Antes de cada push:** correr `ruff format --check src tests`, `ruff check src tests` y
  `pytest`. Las 55 pruebas deben pasar, incluida la reconstrucción con los datos reales.
- **Notas del episodio:** las del podcast (*Revolución de la Riqueza* #292) no se subieron al
  repo porque citaban demasiado texto del episodio. Su resumen está en
  `docs/00-investigacion-inicial.md`.
- **Cómo funciona el INEGI:** los endpoints, ids de estructura y la receta de reconstrucción
  están en `docs/notas/01-datos-inegi-metodologia.md` y en `src/bolsillometro/inegi.py`.
