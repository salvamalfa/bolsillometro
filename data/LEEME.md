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
