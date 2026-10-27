# Pendientes

Aquí solo vive lo que sigue abierto. Al retomar el proyecto, empieza por aquí.

## Ciclo de vida

Cuando un pendiente se cierra, se borra de esta carpeta en el mismo PR que lo cierra:

| Al cerrarse… | …pasa a |
|---|---|
| Un paso de código o de datos | [`CHANGELOG.md`](../CHANGELOG.md), con el número de su PR. |
| Una decisión | [`docs/decisiones.md`](../docs/decisiones.md), con fecha y motivo. |
| Una convención de trabajo | [`CONTRIBUTING.md`](../CONTRIBUTING.md). |
| Todo lo demás | Solo el historial de git. |

Cuando se termina una fase, se borra su archivo (`fase-N.md`).

## Técnicos

- [ ] **Fase 1, paso 6:** la web estática; ver [`fase-1.md`](fase-1.md).
- [ ] **Primera actualización automática:** el INEGI publica la 2Q de octubre y el mensual de
  octubre hacia el 9-nov-2026. Confirmar que `actualizar-datos.yml` haga sus commits solos:
  `datos: INPC hasta 2026-10-2Q`, el de UDI y Cetes de Banxico y
  `datos: INPC por ciudad hasta 2026-10`.

## No técnicos (antes del lanzamiento público)

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

- [ ] Borrar las ramas ya fusionadas con squash: `claude/inflacion-personal` (#2),
  `claude/fase-1-motor` (#4) y `claude/fase-1-ciudades` (#5). Conservan los commits
  originales, pero el contenido ya está en `main`.
- [ ] Borrar la rama `claude/zempoala-combi-app-gxbqvi`, que es del proyecto de combis.
