# Datos del INPC

Índices del INPC nacional por genérico y ponderadores oficiales, descargados del INEGI por
`bolsillometro actualizar`. Cada corrida valida que el INPC publicado se reconstruya con los
292 genéricos (±0.001) antes de escribir aquí.

Fuente: INEGI, Índice Nacional de Precios al Consumidor (INPC). Base 2ª quincena de julio de
2018 = 100; canasta y ponderadores 2024. Cálculos propios con datos del INPC. No es un producto
oficial del INEGI ni de Banco de México.

## Archivos

| Archivo | Contenido |
|---|---|
| `inpc_mensual.csv` | Una fila por mes desde `2018-01`. Columnas: `periodo`, `general` (INPC) y `001`…`292` (genéricos). |
| `inpc_quincenal.csv` | Igual, una fila por quincena desde `2018-01-1Q`. |
| `ponderadores_2024.csv` | `codigo`, `generico`, `division`, `grupo` y `clase` (CCIF 2018), `durabilidad` y `ponderador` (suman 100). |
| `catalogo.csv` | `codigo`, `generico`, `concepto` (clasificación por objeto del gasto) e ids de las series del INEGI (`id_mensual`, `id_quincenal`). |
| `metadatos.json` | Último periodo publicado, factor de encadenamiento y resultado de la reconstrucción. |
| `fuente/ponderadores_inpc_2q_jul_2024.xlsx` | XLSX original de ponderadores, tal como lo publica el INEGI. |
| `ciudades/<clave>_mensual.csv` | Una por ciudad (55), con la misma forma que `inpc_mensual.csv`: una fila por mes desde `2018-01` (o `2018-07` en las 9 ciudades que entraron con la base 2018), `general` (INPC de la ciudad) y `001`…`292`. |
| `ciudades/catalogo.csv` | `clave` (la del nombre de archivo, p. ej. `pachuca` o `cdmx`), `nombre`, `id_nodo` (tema del INEGI) e `id_general` (serie del índice general). |
| `ciudades/metadatos.json` | Último mes, resultado de la validación y, por ciudad, los genéricos sin dato en el último mes. |

## Convenciones

- Los valores son los que publica el INEGI, sin ceros a la derecha. Una celda vacía significa
  que no hay dato (`NA` o `N/E` en el INEGI). 41 genéricos empiezan después de enero de 2018:
  25 con la base 2018 (julio de 2018) y 16 con la canasta 2024 (2Q de julio de 2024 en la serie
  quincenal; agosto de 2024 en la mensual, salvo uno que empieza en junio).
- Los valores anteriores a la 2ª quincena de julio de 2018 tienen más decimales porque el
  INEGI los publica re-expresados desde bases anteriores.
- Desde la 1ª quincena de agosto de 2024 las series están encadenadas en la 2ª quincena de
  julio de 2024 y ya no son aditivas. Para agregar genéricos, cada uno se re-referencia con su
  valor quincenal de la 2Q jul-2024; ver `src/bolsillometro/reconstruccion.py`.
- Los datos del INPC no se revisan una vez publicados, así que cada actualización solo agrega
  filas.

## Por ciudad

`bolsillometro actualizar-ciudades` baja la estructura "Por ciudad" del INEGI (solo mensual) y
la valida contra el nacional antes de escribir `ciudades/`:

- **Estructura:** 55 ciudades, cada una con los mismos 292 genéricos que el nacional y con dato
  hasta el mismo mes.
- **Acotamiento:** de ago-2018 a jul-2024, antes del eslabón de la canasta 2024, el índice
  nacional de cada genérico es un promedio ponderado de sus ciudades. Por eso debe quedar entre
  el mínimo y el máximo de ellas (±0.001 por redondeo). Si un id quedara asignado al genérico o a
  la ciudad equivocada, esta prueba falla.
- **Plausibilidad:** la inflación anual publicada de cada ciudad contra la que dan sus genéricos
  con los ponderadores nacionales (base ago-2024), con tolerancia de ±2 puntos porcentuales.
  No puede ser exacta porque el INEGI no publica pesos genérico × ciudad.

46 ciudades traen datos desde ene-2018 y las 9 que entraron con la base 2018 (p. ej.
Pachuca), desde jul-2018. Una celda vacía también puede ser `ND` en el INEGI. Desde la
canasta 2024, algunos genéricos ya no se cotizan en ciertas ciudades (p. ej. gas natural y
metro en Pachuca); `metadatos.json` los lista y para ellos se usa el índice nacional. El INEGI
advierte que los índices por ciudad tienen muestras chicas y "solo tienen valor informativo",
así que conviene leerlos en variación anual.
