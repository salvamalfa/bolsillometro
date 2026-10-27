# Fase 1: tu primera inflación personal (MVP)

**Objetivo:** que una persona capture su presupuesto y obtenga su inflación personal con los
genéricos del INPC de su ciudad. Todavía no se conectan bancos.

**Para pasar a la fase 2:** que entre 20 y 50 personas con perfiles distintos lo usen y
entiendan por qué su cifra difiere del INPC. Perfiles a cubrir: quien renta y quien es dueño,
quien tiene auto y quien usa transporte público, escuela privada y pública.

Va en 6 PRs; los pasos 1 a 3 ya están en [`CHANGELOG.md`](../CHANGELOG.md) y las decisiones
de la fase, en [`docs/decisiones.md`](../docs/decisiones.md). Faltan estos:

## 4. Presupuesto y cálculo personal

- **Catálogo de rubros:** unos 25 rubros en lenguaje común (renta, súper, gasolina,
  colegiatura, restaurantes, etc.), versionados con su mapeo a genéricos.
  - El gasto de un rubro se reparte entre sus genéricos con los ponderadores oficiales y
    queda marcado como **imputado** (nivel B del reporte).
- **Regla ciudad o nacional por genérico:**
  - El índice de la ciudad para lo local: vivienda, transporte colectivo, electricidad,
    alimentos frescos y loncherías.
  - El nacional para lo que tiene precio casi único: autos, gasolina con tope, telefonía y
    streaming.
  - También el nacional para los genéricos que la ciudad ya no cotiza; la lista por ciudad
    está en `data/ciudades/metadatos.json`.
- **CLI:**
  - `bolsillometro plantilla` escribe un `presupuesto.toml` comentado.
  - `bolsillometro mi-inflacion presupuesto.toml` calcula el índice personal con el motor de
    `indices.py`.
- **Reglas especiales:**
  - **Vivienda propia:** elegir entre incluir la renta imputada ("consumo") o excluirla
    ("gasto efectivo"). La hipoteca nunca se mapea a vivienda propia.
  - **"Gasto no cubierto":** seguro de gastos médicos, comisiones e intereses, impuestos. Se
    reporta aparte y, si el usuario quiere, con el aumento que él capture.
  - **Precio propio:** en partidas grandes (renta, colegiatura, prima de seguro) el usuario
    puede poner su aumento real en lugar del índice, como una serie sintética.

## 5. Reporte

- Inflación mensual y anual personal contra el INPC.
- Qué genéricos la mueven, con incidencias en lenguaje claro.
- Qué parte del gasto se asignó directo a un genérico y qué parte se repartió con
  ponderadores (imputada).
- Rendimiento real contra Cetes y UDI (fórmula 7).

## 6. Web estática

Calcula en el navegador con los mismos datos y el mismo `presupuesto.toml`, que importa y
exporta. No usa servidor y los datos no salen de la máquina.
