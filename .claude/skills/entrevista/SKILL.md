---
name: entrevista
description: Entrevista a una persona con el cuestionario estandarizado de Bolsillómetro, arma su presupuesto y le da su inflación personal. Úsalo cuando alguien quiera saber su inflación, "hacer la entrevista" o capturar su gasto.
---

# Entrevista de Bolsillómetro

**Objetivo:** que la persona obtenga **una cifra, su inflación personal**, sin llenar archivos.
Tú haces las preguntas, armas el presupuesto y corres el cálculo.

## Reglas

- **Privacidad:** no pidas nombres, cuentas, estados de cuenta ni datos bancarios; solo montos
  aproximados. Guarda todo en `presupuestos/`, que git ignora. Nunca hagas commit de esa carpeta
  ni pegues las respuestas en un PR o issue.
- **Lenguaje común:** usa el texto de cada pregunta tal como está en el cuestionario. No hables
  de genéricos, ponderadores ni del INPC salvo que la persona pregunte.
- **Aproximado está bien:** si dan un rango ("entre 3 y 4 mil"), usa el punto medio. Si no saben,
  pide una idea ("¿más o menos que mil?"); si siguen sin saber, pon 0 y dilo al final.
- **Frecuencia:** si responden por otro periodo que el de la pregunta (recibo bimestral, gasto
  semanal, pago anual), guarda `{"monto": x, "cada": "bimestre"}` (`mes`, `bimestre`,
  `trimestre`, `semestre`, `año`); si es semanal, multiplica por 4.3 y guárdalo como mensual.

## Pasos

1. Lee `src/bolsillometro/catalogos/cuestionario.toml`. Las preguntas van **en ese orden**.
   Sáltate las que tengan `si` y no se cumpla (p. ej. gasolina si no tienen auto).
2. **Ciudad:** pregunta con AskUserQuestion. Si la persona dice una ciudad que no está en
   `data/ciudades/catalogo.csv`, elige la más cercana y díselo. Usa la `clave` del catálogo.
3. **Opciones** (`tipo = "opcion"`): AskUserQuestion con las opciones del cuestionario.
4. **Montos:** pregunta de 3 a 5 por mensaje, en texto, numerados, para que contesten rápido.
   Los `porcentaje` con `opcional = true` se pueden saltar (no los guardes).
5. Al terminar, muestra un resumen corto de lo que entendiste (rubro y monto al mes) y pide que
   lo confirme o corrija.
6. Guarda las respuestas en `presupuestos/<alias>.json` (alias corto, sin datos personales),
   como `{id: valor}` con los ids del cuestionario.
7. Corre `python -m bolsillometro entrevista presupuestos/<alias>.json`. Escribe
   `presupuestos/<alias>.toml` y muestra el reporte.
8. Da la respuesta empezando por **la cifra**: "Tu inflación de los últimos 12 meses es X%".
   Luego, en una o dos frases, qué la subió y si los Cetes le ganaron. Ofrece `--detalle` solo
   si quieren comparar con el INPC o ver el desglose.

## Si algo falla

`bolsillometro entrevista` dice qué pregunta tiene un valor inválido; corrígelo con la persona y
vuelve a correrlo. Si faltan datos (`data/`), corre antes `python -m bolsillometro verificar`.
