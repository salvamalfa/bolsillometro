# Fase 1: tu primera inflación personal (MVP)

**Objetivo:** que una persona capture su presupuesto y obtenga su inflación personal con los
genéricos del INPC de su ciudad. Todavía no se conectan bancos.

**Para pasar a la fase 2:** que entre 20 y 50 personas con perfiles distintos lo usen y
entiendan por qué su cifra difiere del INPC. Perfiles a cubrir: quien renta y quien es dueño,
quien tiene auto y quien usa transporte público, escuela privada y pública.

## Alcance

1. **Datos por ciudad.** Agregar al pipeline la estructura "Por ciudad" (`112001700060`):
   55 ciudades × 292 genéricos.
   - La descarga es pesada: el árbol pesa ~63 MB y tardó más de 120 s.
   - Validar algo equivalente a la reconstrucción. El INEGI no publica pesos genérico × ciudad,
     así que la reconstrucción exacta del INPC de una ciudad no es posible y hay que definir
     otra prueba.
   - Regla documentada: el índice de la ciudad para lo local (vivienda, transporte colectivo,
     electricidad, alimentos frescos, loncherías) y el nacional para lo que tiene precio casi
     único (autos, gasolina con tope, telefonía, streaming).
2. **Presupuesto declarado.** Un archivo TOML con unos 25 rubros en lenguaje común:
   renta, súper, gasolina, colegiatura, restaurantes, etc.
   - Cada rubro se asigna a sus genéricos. El gasto de un rubro se reparte entre ellos con los
     ponderadores oficiales y queda marcado como **imputado** (nivel B del reporte).
3. **Cálculo personal.** Reusa el motor de `src/bolsillometro/indices.py`:
   `pesos_lowe`, `indice_ponderado`, `variacion` e `incidencias`. Faltan dos fórmulas:
   - **Encadenamiento** cuando el usuario actualiza sus pesos (fórmula 5 del reporte).
   - **Rendimiento real** contra la inflación personal (fórmula 7).
4. **Reglas especiales:**
   - **Vivienda propia:** elegir entre incluir la renta imputada ("consumo") o excluirla
     ("gasto efectivo"). La hipoteca nunca se mapea a vivienda propia.
   - **"Gasto no cubierto":** seguro de gastos médicos, comisiones e intereses, impuestos.
     Se reporta aparte y, si el usuario quiere, con el aumento que él capture.
   - **Precio propio:** en partidas grandes (renta, colegiatura, prima de seguro) el usuario
     puede poner su aumento real en lugar del índice.
5. **Resultados:**
   - Inflación anual y mensual personal contra el INPC.
   - Qué genéricos la mueven, con incidencias en lenguaje claro.
   - Qué parte del gasto se observó y qué parte se imputó.
   - Rendimiento real contra Cetes y UDI.
6. **Interfaz:**
   - Un CLI (`bolsillometro mi-inflacion presupuesto.toml`).
   - Una web estática que calcula en el navegador, sin servidor y sin que los datos salgan.

## Decisiones tomadas (27-oct-2026)

- [x] **Web estática:** entra en la fase 1, pero después del CLI y en su propio PR. Las 20 a 50
  personas de la prueba no van a usar un CLI.
- [x] **Rubros:** unos 25, en lenguaje común.
- [x] **Formato del presupuesto:** TOML. Se lee con `tomllib`, de la biblioteca estándar, sin
  dependencias nuevas. Admite comentarios para una plantilla autoexplicada. Agrupa en un archivo
  la configuración (ciudad, periodo del gasto, modo de vivienda propia), los rubros con su
  aumento propio opcional y el gasto no cubierto. La web importa y exporta el mismo archivo.
- [x] **Cetes y UDI:** se toman de las exportaciones públicas del SIE de Banxico (CSV/IQY sin
  token, como el INEGI), se validan y se versionan en `data/` con el mismo workflow. El API
  REST con token queda como respaldo.
- [x] **Import de CSV del banco:** se deja para la fase 2, junto con los parsers por banco y
  el diccionario de comercios.
- [x] **Ciudades en `data/`:** un CSV por ciudad (`data/ciudades/<clave>_mensual.csv`), con
  la misma forma ancha que el nacional. Un solo CSV tendría 16,060 columnas y cada
  actualización cambiaría una línea enorme. Por ciudad solo se guarda la serie mensual:
  son unos 14 MB contra unos 41 MB con quincenas, y el ruido de la muestra por ciudad hace
  poco útil la quincena.

## Plan por PRs

Cada PR pasa `ruff format --check`, `ruff check` y `pytest` antes del push.

1. [x] **Motor: fórmulas 5 y 7.** `encadenar` (cambio de pesos en un eslabón),
   `incidencias_encadenadas` (convención `(1+a)(1+b) − 1`) y `rendimiento_real`. Prueba
   con datos reales: encadenar los ponderadores oficiales en jul-2025 sigue reconstruyendo el
   INPC con un error máximo de ±0.001.
2. [x] **Datos por ciudad.** Estructura `112001700060` en el pipeline, `data/ciudades/` y un
   catálogo de ciudades con sus ids. El árbol de ~63 MB tiene timeout propio (900 s).
   Validación:
   - Estructura completa: 55 ciudades × 292 genéricos, con los mismos códigos que el nacional.
   - Título: cada exportación nombra su ciudad, para que no se crucen dos ciudades.
   - Acotamiento: de ago-2018 a jul-2024, el nacional de cada genérico queda entre el mínimo y
     el máximo de sus ciudades (19,874 revisiones, 0 fuera de rango).
   - Plausibilidad: inflación anual de cada ciudad contra sus genéricos con los ponderadores
     nacionales, con tolerancia de ±2 pp (máximo real: 1.11 pp). No puede ser exacta, porque
     el INEGI no publica pesos genérico × ciudad.
   - Hallazgo: desde la canasta 2024 algunos genéricos ya no se cotizan en ciertas ciudades
     (metro en 52, gas natural en 35, museos en 23, transporte escolar en 18); para ellos el
     cálculo personal usa el nacional. La lista por ciudad está en
     `data/ciudades/metadatos.json`.
3. [ ] **Cetes y UDI.** Descarga del SIE sin token, mensualizada (UDI de fin de mes, Cetes 28
   de la primera subasta del mes o el promedio, a definir y documentar). Validación de
   continuidad y rangos.
4. [ ] **Presupuesto y cálculo personal.**
   - Catálogo versionado de ~25 rubros → genéricos y regla ciudad/nacional por genérico.
   - `bolsillometro plantilla` escribe un `presupuesto.toml` comentado.
   - `bolsillometro mi-inflacion presupuesto.toml` calcula el índice personal.
   - Reglas especiales:
     - Vivienda propia en modo "consumo" o "gasto efectivo".
     - "Gasto no cubierto" aparte.
     - Precio propio en partidas grandes, como una serie sintética con el aumento capturado.
5. [ ] **Reporte.**
   - Inflación mensual y anual personal contra el INPC.
   - Incidencias en lenguaje claro.
   - Parte del gasto asignada directo a un genérico contra parte repartida con ponderadores
     (imputada).
   - Rendimiento real contra Cetes y UDI.
6. [ ] **Web estática.** Calcula en el navegador con los mismos datos y el mismo formato de
   presupuesto. No usa servidor y los datos no salen de la máquina.
