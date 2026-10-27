# Fase 1: tu primera inflación personal (MVP)

**Objetivo:** que una persona capture su presupuesto y obtenga su inflación personal con los
genéricos del INPC de su ciudad. Todavía no se conectan bancos.

**Para pasar a la fase 2:** que entre 20 y 50 personas con perfiles distintos lo usen y
entiendan por qué su cifra difiere del INPC. Perfiles a cubrir: quien renta y quien es dueño,
quien tiene auto y quien usa transporte público, escuela privada y pública.

Va en 6 PRs; los pasos 1, 2 y 4 ya están en [`CHANGELOG.md`](../CHANGELOG.md) y las decisiones
de la fase, en [`docs/decisiones.md`](../docs/decisiones.md). Faltan estos:

## 3. Cetes y UDI

- Bajarlos de las exportaciones públicas del SIE de Banxico, sin token.
- Mensualizarlos con un criterio documentado: por ejemplo, UDI de fin de mes y Cetes a 28 días
  de la primera subasta del mes, o su promedio.
- Validar continuidad y rangos, y versionarlos en `data/` con el mismo workflow.

## 5. Reporte

- Inflación mensual y anual personal contra el INPC.
- Qué genéricos la mueven, con incidencias en lenguaje claro.
- Qué parte del gasto se asignó directo a un genérico y qué parte se repartió con
  ponderadores (imputada).
- Rendimiento real contra Cetes y UDI (fórmula 7).

## 6. Web estática

Calcula en el navegador con los mismos datos y el mismo `presupuesto.toml`, que importa y
exporta. No usa servidor y los datos no salen de la máquina.
