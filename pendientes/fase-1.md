# Fase 1: tu primera inflación personal (MVP)

**Objetivo:** que una persona capture su presupuesto y obtenga su inflación personal con los
genéricos del INPC de su ciudad. Todavía no se conectan bancos.

**Para pasar a la fase 2:** que entre 20 y 50 personas con perfiles distintos lo usen y
entiendan por qué su cifra difiere del INPC. Perfiles a cubrir: quien renta y quien es dueño,
quien tiene auto y quien usa transporte público, escuela privada y pública.

Va en 6 PRs; los pasos 1 a 5 ya están en [`CHANGELOG.md`](../CHANGELOG.md) y las decisiones
de la fase, en [`docs/decisiones.md`](../docs/decisiones.md). Falta este:

## 6. Web estática

Hace la misma entrevista (el cuestionario de `catalogos/cuestionario.toml`) y calcula en el
navegador con los mismos datos; importa y exporta el mismo `presupuesto.toml`. No usa
servidor y los datos no salen de la máquina.
