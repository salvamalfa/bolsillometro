# Inflación personal (nombre provisional)

Proyecto open source para que cualquier persona en México calcule **su propia inflación**:
los índices de los 292 genéricos del INPC (Fuente: INEGI) re-ponderados con su propio gasto.
Sirve para conocer tu costo de vida real y como benchmark de tus inversiones
(rendimiento real contra *tu* inflación, no contra la de un hogar promedio).

> Estado: exploración. Todavía no hay código de aplicación.
> Este repo antes era "Combis Zempoala"; ese proyecto se deprecó y su contenido sigue en el historial de git.

## La idea en una fórmula

```
P(t) = 100 · Σ_k s_k · I_k(t) / I_k(b)
```

`I_k(t)` es el índice publicado del genérico k (nacional o de tu ciudad) y `s_k` es la parte de tu gasto
que va a ese genérico. Con los ponderadores oficiales de INEGI la fórmula reproduce el INPC publicado;
con los tuyos, da tu inflación.

## Principios

- **Precios oficiales, pesos propios.** Los precios vienen de INEGI; lo único personal son los ponderadores.
- **Local-first.** Tus movimientos bancarios y facturas no salen de tu máquina; lo que se comparte son agregados.
- **Transparencia.** Cada resultado dice qué parte de tu gasto se observó y qué parte se imputó.
- **Referencia, no recomendación.** No es asesoría de inversiones.

## Documentos

- [`docs/00-investigacion-inicial.md`](docs/00-investigacion-inicial.md) — reporte: viabilidad, fórmulas para
  re-ponderar genéricos, arquitectura local-first, hoja de ruta (MVP → plugin para Claude/ChatGPT → capa de pago opcional),
  precedentes en México y el mundo, ideas de nombre, modelo de negocio y líneas regulatorias.
- [`docs/notas/`](docs/notas/) — notas de investigación con fuentes (algunas en inglés):
  - [`01-datos-inegi-metodologia.md`](docs/notas/01-datos-inegi-metodologia.md) — qué publica INEGI, cómo descargarlo sin token y cómo se reconstruye el INPC.
  - [`02-datos-gasto-y-arquitectura-ia.md`](docs/notas/02-datos-gasto-y-arquitectura-ia.md) — open finance en México, agregadores, CFDI, clasificación de movimientos y MCP.
  - [`03-precedentes-oficiales-y-academicos.md`](docs/notas/03-precedentes-oficiales-y-academicos.md) — calculadoras de oficinas de estadística y evidencia académica.
  - [`04-precedentes-privados-y-open-source.md`](docs/notas/04-precedentes-privados-y-open-source.md) — fintechs, índices alternativos y repos en GitHub.
  - [`05-negocio-regulacion-nombres.md`](docs/notas/05-negocio-regulacion-nombres.md) — monetización, regulación en México, difusión y nombres.

---

Cálculos propios con datos del INPC (Fuente: INEGI). No es un producto oficial del INEGI ni de Banco de México.
