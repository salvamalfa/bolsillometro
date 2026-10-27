# Registro de cambios

Lo que ya está en `main`, por fase y con el número de su PR. El formato sigue
[Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/). Las actualizaciones automáticas
de datos (`datos: INPC hasta …`) no se anotan aquí; están en el historial de git.

## Sin publicar

### Fase 1: MVP (en curso)

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
