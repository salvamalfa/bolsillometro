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
2. **Presupuesto declarado.** Un archivo (YAML o CSV) con 15 a 40 rubros en lenguaje común:
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
   - Un CLI (`bolsillometro mi-inflacion presupuesto.yaml`).
   - Una web estática que calcula en el navegador, sin servidor y sin que los datos salgan.

## Decisiones abiertas (para el plan)

- [ ] ¿La web estática entra en la fase 1 o se deja para después del CLI?
- [ ] ¿Cuál es la lista de rubros (15, 25 o 40) y su mapeo a genéricos?
- [ ] ¿Formato del presupuesto: YAML, CSV o ambos?
- [ ] ¿De dónde salen Cetes y UDI?
  - El API SIE de Banxico pide token (gratis, con límites de consulta).
  - La alternativa es capturarlos a mano o desde otra fuente pública.
- [ ] ¿Se incluye ya un import de CSV genérico del banco o se deja para la fase 2?
- [ ] ¿Ciudades en `data/` como un solo CSV o uno por ciudad? Importa por el tamaño y por
  los diffs de cada actualización.
