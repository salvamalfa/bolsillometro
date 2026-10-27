# Registro de cambios

Lo que ya está en `main`, por fase y con el número de su PR. El formato sigue
[Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/). Las actualizaciones automáticas
de datos (`datos: INPC hasta …`) no se anotan aquí; están en el historial de git.

## Sin publicar

### Fase 1: MVP (en curso)

- **La web** (#11): `web/index.html` hace la misma entrevista con botones de rango, una pregunta
  por pantalla, y muestra una sola cifra, lo que la subió y si los Cetes le ganaron. Calcula en
  el navegador con `web/calculo.js`, que da lo mismo que Python (±1e-9) en cinco perfiles; los
  datos (`web/datos/`, ~2 MB, una ciudad por archivo) los exporta `bolsillometro web` y el
  workflow los regenera con cada actualización. Workflow para publicar en GitHub Pages.
- **Ajustes tras la primera entrevista** (#10): la primera entrevista real (el dueño del
  proyecto, 27-oct-2026) salió bien con preguntas de opción por rango, así que el cuestionario
  ahora trae `[escalas]` estándar (a lo más 4 opciones, con un valor representativo cada una)
  y las respuestas pueden ser el texto de la opción. El reporte dice "la Ciudad de México" en
  vez del nombre del INEGI.
- **Entrevista y reporte de una cifra** (#9): cuestionario estandarizado de 33 preguntas en
  lenguaje común (`catalogos/cuestionario.toml`), `bolsillometro entrevista respuestas.json` y
  el skill `entrevista` para que Claude haga las preguntas y arme el presupuesto. El reporte
  empieza con una sola cifra, tu inflación de 12 meses, y dice qué rubros la subieron y si los
  Cetes a 28 días le ganaron; `--detalle` agrega la comparación con el INPC y el desglose.
- **Presupuesto y cálculo personal** (#8): `bolsillometro plantilla` y
  `bolsillometro mi-inflacion presupuesto.toml`. 32 rubros que cubren los 292 genéricos
  (`catalogos/rubros.csv`), precios de la ciudad o nacionales según el genérico, vivienda propia
  en modo "gasto efectivo" o "consumo", aumento propio por rubro y gasto no cubierto aparte. Un
  presupuesto con el gasto del hogar promedio reproduce la inflación del INPC (±0.002 pp).
- **Cetes y UDI de Banxico** (#7): UDI diaria y Cetes a 28 días por subasta en
  `data/banxico/`, bajados del SIE sin token. La UDI se valida contra el INPC del INEGI tramo
  por tramo y día por día (210 tramos y 3,195 días desde 2018, error máximo 1.6e-7). Comando
  `actualizar-banxico`, rendimientos de fin de mes a fin de mes y paso propio en el workflow.
- **Datos por ciudad** (#5): 55 ciudades × 292 genéricos, mensual, en `data/ciudades/`.
  Comando `actualizar-ciudades`, validación por título, acotamiento y plausibilidad, y paso
  propio en el workflow. Desde la canasta 2024 algunos genéricos ya no se cotizan en ciertas
  ciudades (metro en 52, gas natural en 35, museos en 23, transporte escolar en 18).
- **Motor: fórmulas 5 y 7** (#4): `encadenar` (cambio de pesos en un eslabón),
  `incidencias_encadenadas` y `rendimiento_real`. Con datos reales, encadenar los ponderadores
  oficiales en jul-2025 sigue reconstruyendo el INPC con ±0.001. Plan de la fase en 6 PRs.

## 0.1.0: fase 0, datos y motor (26-oct-2026)

- **Pendientes al cierre de la fase 0** (#3).
- **Bolsillómetro sustituye al proyecto de combis Zempoala** (#2):
  - Investigación de viabilidad y notas con fuentes en `docs/`.
  - Pipeline que descarga del INEGI los 292 genéricos nacionales (mensual y quincenal desde
    2018) y los ponderadores 2024, y valida que el INPC se reconstruya con ±0.001.
  - Motor Laspeyres/Lowe, CLI `actualizar` y `verificar`, y workflows de pruebas y de
    actualización automática.

## Anterior: combis Zempoala (deprecado)

- Investigación inicial del proyecto de combis (#1). Su contenido sigue en el historial de git.
