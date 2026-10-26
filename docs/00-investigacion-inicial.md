# Tu inflación personal cabe en 292 genéricos

Sí, la idea tiene sentido y es viable hoy. Además, la matemática, que es lo que más te preocupa, ya está resuelta. **INEGI publica gratis y sin token los índices de los 292 genéricos del INPC, para el país y para 55 ciudades.** Salen por la misma exportación que alimenta los .IQY que usabas en Banxico. Con esos índices y el XLSX oficial de ponderadores, **el INPC publicado se reconstruye con un error de una milésima**. Lo difícil son los datos de gasto. En México **las reglas de open finance para datos transaccionales siguen sin publicarse**, los agregadores solo venden a empresas y un cargo que dice "WALMART $1,500" no dice qué genéricos compraste. Por eso el diseño honesto es local-first: presupuesto declarado y archivos que tú controlas (CSV del banco, XML de CFDI), clasificados por niveles de confianza y con el LLM solo como clasificador. El episodio #292 de *Revolución de la Riqueza* acierta en que tu inflación es un "vector" distinto al promedio. Pero su receta de vaciar estados de cuenta en un chatbot no puede separar precio de cantidad. Y su "vara del 8% anual en dólares" no mide inflación de consumo: es un costo de oportunidad patrimonial derivado de la masa monetaria. Hoy nadie combina transacciones reales con genéricos del INPC: ningún banco, fintech, oficina de estadística ni repositorio. El antecedente más cercano es un Recuadro de Banxico de 2022 que hizo el mismo ejercicio con la ENIGH. El riesgo principal no es técnico ni legal, es de uso. Estas calculadoras atraen atención cuando la inflación sube y luego se olvidan. Por eso el número tiene que amarrarse a decisiones concretas, como tu aumento de sueldo o el rendimiento real de tu portafolio. Y si llega dinero, primero vendrá de becas y clientes B2B, no de suscripciones individuales.

## Veredicto: es viable si mides la composición de tu gasto y no prometes medir los precios que pagas

La premisa tiene buen respaldo. Banxico tomó la canasta de cada hogar de la ENIGH 2020 y la revaluó con el INPC por genérico y ciudad. Encontró que **para el 84.5% de los hogares el costo subió entre 8% y 17%** entre el levantamiento (ago–nov 2020) y junio de 2022. En el quintil más pobre subió 13.3%, contra 11.6% en el más rico ([Banxico, Recuadro 5, Informe Trimestral abr–jun 2022](https://www.banxico.org.mx/publicaciones-y-prensa/informes-trimestrales/recuadros/%7B57BAF692-8130-53E4-1ABE-DD05B28AFE6D%7D.pdf)). En Estados Unidos, con datos de escáner, el rango intercuartil de la inflación anual entre hogares va de **6.2 a 9.0 puntos porcentuales** ([Kaplan y Schulhofer-Wohl, JME 2017](https://gregkaplan.uchicago.edu/s/kaplan_schulhoferwohl_jme_2017.pdf)). La composición del gasto por sí sola ya pesa. Destatis comparó dos hogares con el mismo gasto total: el que tiene auto enfrentaba 1.2 pp más de inflación que el que usa transporte público ([Destatis, dic-2021](https://www.destatis.de/DE/Presse/Pressemitteilungen/2021/12/PD21_N070_611.html)). Un INPC reponderado con tu gasto captura justo eso: si rentas o eres dueño, si te mueves en auto o en combi, y cuánto pesan la comida en casa, la colegiatura o la salud.

En lo técnico no falta ninguna pieza esencial. Tienes los precios oficiales por genérico y ciudad, un procedimiento de agregación documentado y reproducible, librerías para leer CFDI y estándares (MCP) para llevar el cálculo a Claude y ChatGPT. Más abajo vienen la arquitectura, las fórmulas y la hoja de ruta. El cuello de botella es convertir tus movimientos en ponderadores por genérico sin inventar precisión.

Lo que el índice no puede hacer conviene decirlo desde el README. Kaplan y Schulhofer-Wohl encontraron que **la mayor parte de la dispersión viene de que los hogares pagan precios distintos por el mismo tipo de bien**, según la tienda, la marca o la presentación, y no de la mezcla de categorías. Un índice con genéricos del INPC y tus ponderadores captura la composición de tu gasto, pero aplica el precio promedio que cotiza INEGI. Tu inflación "verdadera" está más dispersa que la que mostrará la herramienta. Además, como todo Laspeyres de canasta fija, supone que no sustituyes productos (INEGI habla de preferencias tipo Leontief). Por eso sobrestima tu inflación si cambias res por pollo cuando sube la res ([INEGI, Documento metodológico INPC 2024](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)). La salida práctica tiene tres partes. Primero, llamarlo "tu inflación por composición de gasto". Segundo, actualizar los ponderadores cada año y encadenar. Tercero, permitir que el usuario sustituya el índice por su precio observado en las partidas grandes donde sí lo conoce: la renta, la colegiatura, la prima de gastos médicos.

## El episodio #292 acierta en el diagnóstico pero mezcla dos varas distintas

El episodio se publicó el 25 de octubre de 2026 y dura unos 34 minutos. Es un monólogo de Javier Morodo producido por Sonoro ([Spotify](https://open.spotify.com/episode/5QNs3AwlyJF2si9pqlkhsD); [RSS con capítulos](https://feeds.megaphone.fm/SONORO7313556940)). No hay transcripción oficial, así que lo que sigue sale del audio público. Las citas son fragmentos cortos. El argumento tiene dos capas, y conviene separarlas porque tu proyecto solo hereda una.

**La primera capa, la inflación personal, es sólida.** Morodo dice que el INPC y el CPI se arman con una canasta promedio "que no es la tuya". Resume que "la inflación es un vector" distinto para cada persona. Y aclara que el índice no está mal medido, sino que "está midiendo a otra persona" (min 2:50–5:30). Eso describe bien a un Laspeyres plutocrático, que pondera por el gasto agregado. La investigación mexicana coincide: en años normales, el INPC plutocrático y uno "democrático" casi no difieren, y la brecha se abre en años de inflación alta como 2017 y 2020–2022 ([Márquez Moranchel, *Investigación Económica* 2025](https://www.scielo.org.mx/pdf/ineco/v84n331/0185-1667-ineco-84-331-40.pdf)). Su ejemplo de la renta es literalmente una incidencia: un aumento de 50% en un rubro que pesa ~30% le suma ~15 puntos a tu inflación (min 11:53). Hay dos matices. El subíndice oficial de colegiaturas marcó **5.84% anual** en la 1ª quincena de octubre de 2026: por encima del 3.62% general, pero debajo del "más del 7%" que él menciona ([INEGI, Boletín 633/26](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_1q2026_10.pdf)). Y los seguros de gastos médicos mayores, que él ubica arriba de 14%, **no son un genérico del INPC**. La división 12, "Seguros y servicios financieros", tiene un solo genérico, seguro de automóvil, y pesa 0.24% en total ([XLSX oficial de ponderadores](https://www.inegi.org.mx/rnm/index.php/catalog/1015/download/32034)). Ese hueco juega a tu favor: tu herramienta debe dejar que el usuario capture el aumento real de su prima.

**Donde se queda corto es en la receta práctica.** Le dedica alrededor de un minuto, en el capítulo "Cómo medir tu propia inflación con tus estados de cuenta" (min 11:46). Propone vaciar los estados de cuenta en Claude o ChatGPT y pedirle "compárame un año al otro". La idea es que el modelo separe cuánto más consumiste de cuánto subieron los precios, y promete que "te va a sacar perfecto". El problema es que un estado de cuenta trae fecha, comercio y monto, pero no cantidades ni precios unitarios. Sin un índice de precios externo por categoría, ningún modelo puede separar precio y cantidad. Lo que obtienes es el crecimiento de tu gasto. Es el mismo error de los "métodos" populares que dividen el gasto de un año entre el del anterior ([NBC](https://www.nbcnews.com/business/consumer/calculate-personal-inflation-rate-means-inflation-rate-calculate-rcna28442); [Emma](https://emma-app.com/blog/2021/03/05/how-to-calculate-your-personal-inflation-rate)). Además, pegar estados de cuenta en un chat no es reproducible ni auditable, y le entrega tus datos financieros al proveedor del modelo. Tu proyecto es la versión rigurosa de esa misma intuición: el LLM solo clasifica movimientos en genéricos, los precios los pone INEGI y el cálculo sigue una fórmula publicada.

**La segunda capa, la "vara del 8% anual en dólares", es otra cosa.** Morodo la deriva del crecimiento de M2 en EE.UU. y China y de un índice de liquidez global que, según él, crece ~8% al año desde 2008. Propone "olvidémonos de la inflación" y usar la expansión monetaria como umbral (min 13:10–14:58). Cierra invitando a dejar los Cetes por activos reales (min 33:37) ([newsletter del 26-oct-2026](https://javiermtzmorodo.substack.com/p/senales-confusas-valuaciones-recortadas)). Veo tres problemas:

1. **El crecimiento del dinero no equivale al de los precios.** Una parte se va al crecimiento real de la economía y otra a cambios en la velocidad del dinero.
2. **El INPC excluye los activos por diseño, no por descuido.** INEGI deja fuera de la canasta todo lo que no es consumo: impuestos, pago de deudas, contribuciones ([INEGI, Documento metodológico](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)).
3. **Junta en una cifra dos preguntas distintas.** Una es el costo de vivir. La otra es el precio de los activos "que te hacen rico", que es una pregunta de riqueza relativa y no de poder de compra.

Su aritmética de Cetes sí cuadra (1.065⁹ ≈ 1.76). Pero la conclusión depende de aceptar que tu riqueza debe crecer al ritmo de M2. Toma en cuenta también que el episodio promociona una clase en vivo de diseño patrimonial ([Substack](https://javiermtzmorodo.substack.com/p/que-trabajo-hace-cada-peso-que-tienes)) y que cierra aclarando que su contenido es solo educativo.

Para incorporar el episodio no necesitas rebatirlo, solo separar sus preguntas. Tu herramienta responde "¿mi dinero mantiene mi nivel de vida?" con tu inflación personal en pesos. Y responde "¿mi patrimonio mantiene su posición frente a los activos?" con referencias que el usuario elige y ve lado a lado: INPC, su inflación personal, Cetes, UDI, tipo de cambio, S&P 500 en pesos y, si quiere, crecimiento de M2. Separar la inflación de consumo del costo de oportunidad es justo lo que un ex-Banxico puede aportar a la conversación que abrió el podcast.

## INEGI ya publica todo y el INPC se reconstruye al milésimo

A octubre de 2026 el INPC sigue con base 2ª quincena de julio de 2018 = 100. Desde la 1ª quincena de agosto de 2024 se calcula con la "Actualización de Canasta y Ponderadores 2024" ([Banxico, Recuadro 4, 2024](https://www.banxico.org.mx/publicaciones-y-prensa/informes-trimestrales/recuadros/%7BB2DB3F5A-4FA5-E527-3A74-5B3998702397%7D.pdf); [INEGI, presentación Actualización 2024](https://en.www.inegi.org.mx/contenidos/programas/inpc/2018a/doc/present_resul_2024.pdf)):

- **292 genéricos**, antes 299.
- Ponderadores de la ENIGH Estacional 2022, actualizados por precios relativos a la 2Q de julio de 2024.
- Clasificación CCIF 2018 e índices encadenados.
- Cotización en 55 áreas geográficas.

El cálculo tiene dos etapas: Jevons dentro de cada genérico y Laspeyres para los agregados. Se publica en el DOF los días 10 y 25 (INEGI lo difunde el día anterior) y **los datos no se revisan**, así que puedes guardarlos en caché sin miedo ([INEGI, Boletín 633/26](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_1q2026_10.pdf)). El dato más reciente es la 1Q de octubre de 2026: 146.739 puntos, 3.62% anual y subyacente en 3.78%.

Los genéricos más pesados muestran por qué importa la composición:

| Genérico | Peso en el INPC |
|---|---|
| Vivienda propia | 13.77% |
| Loncherías y taquerías | 5.05% |
| Gasolina de bajo octanaje | 4.82% |
| Restaurantes | 2.80% |
| Renta de vivienda | 2.79% |
| Automóviles | 2.56% |
| Tortilla de maíz | 1.87% |

Fuente: [XLSX oficial de ponderadores](https://www.inegi.org.mx/rnm/index.php/catalog/1015/download/32034).

**No necesitas el IQY para extraer los datos.** La aplicación "Índices de Precios" genera el .iqy con `GeneraIQY.aspx`. Ese archivo solo hace un POST a `Exportacion.aspx` con los mismos parámetros que la exportación a CSV. Con un POST directo bajas **las 293 series (índice general más 292 genéricos) en una sola petición de unos 160–240 KB**. La estructura "Por ciudad" trae 55 × 292 = 16,060 series de genérico ([INEGI, Exportacion.aspx](https://www.inegi.org.mx/app/indicesdeprecios/Exportacion.aspx?INPtipoExporta=CSV); [GeneraIQY.aspx](https://www.inegi.org.mx/app/indicesdeprecios/GeneraIQY.aspx)). Los ponderadores por genérico vienen en un XLSX de 27 KB que suma 100 ([INEGI RNM, catálogo 1015](https://www.inegi.org.mx/rnm/index.php/catalog/1015/related-materials)).

Las otras fuentes sirven menos para esto:

- **API de Indicadores de INEGI.** Pide token, y sin él no se pudo confirmar qué ids corresponden a los genéricos ([INEGI API](https://www.inegi.org.mx/servicios/api_indicadores.html)).
- **SIE de Banxico.** Solo tiene agregados (SP1, SP8664, subyacente y componentes), no genéricos, porque desde 2011 la facultad de elaborar los índices es de INEGI ([Banxico SIE](https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=8&accion=consultarDirectorioCuadros&locale=es)).
- **R.** `inegiR` salió de CRAN el 1-jun-2026 ([CRAN](https://cran.r-project.org/package=inegiR)).
- **Python.** Existen `INEGIpy` y `pyinegi` ([PyPI INEGIpy](https://pypi.org/project/INEGIpy/)).

Bolsillómetro no depende de ninguna de estas librerías ni de otros repos del INPC: el pipeline se construye desde cero sobre la exportación de INEGI.

El riesgo es que la exportación no está documentada como API y ya existe una ruta `indicesdepreciosv2`. La defensa es versionar los CSV en el repo y validar cada corrida contra el INPC publicado.

**Hay dos cosas que INEGI no publica, y ninguna te bloquea.** La primera es la matriz de ponderadores genérico × ciudad, que INEGI usa internamente. No la necesitas, porque usarás índices de ciudad por genérico con pesos propios. La segunda es un índice por estrato a nivel genérico: el que existe cubre solo las 13 divisiones CCIF para 4 estratos de salario mínimo ([INEGI Índices de Precios](https://www.inegi.org.mx/app/indicesdeprecios/servicios/ArbolAjaxInteraccion.asmx)). Ojo con el ruido: las exportaciones avisan que "las desagregaciones del INPC solo tienen valor informativo". Para una persona conviene reportar la inflación anual, o un promedio móvil, y no la quincenal pura. Si vives por Zempoala, tu ciudad INPC más cercana es Pachuca, que tiene publicados sus 292 genéricos.

**La prueba de fuego del repo es reproducir el INPC con los ponderadores oficiales.** Para hacerlo se tomaron los 292 genéricos nacionales mensuales, su valor de la 2Q de julio de 2024 y el XLSX oficial. La reconstrucción cuadra con lo publicado ([exportación CSV de INEGI](https://www.inegi.org.mx/app/indicesdeprecios/Estructura.aspx?idEstructura=112001700030); [XLSX de ponderadores](https://www.inegi.org.mx/rnm/index.php/catalog/1015/download/32034)):

| Mes | INPC reconstruido | INPC publicado |
|---|---|---|
| ago-2024 | 136.013 | 136.013 |
| dic-2024 | 137.948 | 137.949 |
| ago-2025 | 140.867 | 140.867 |
| ago-2026 | 145.461 | 145.462 |
| sep-2026 | 146.075 | 146.075 |

El truco es que **después del eslabón de julio de 2024 las series publicadas ya no son aditivas**. El procedimiento oficial tiene tres pasos ([INEGI, Documento metodológico, pp. 59–61](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)):

1. Re-referenciar cada genérico a la 2Q de julio de 2024 = 100, con θⱼ = 100 / Iⱼ de esa quincena.
2. Promediar con los ponderadores.
3. Multiplicar por el factor de encadenamiento.

El cambio de referencia se hace con el dato quincenal, incluso para las series mensuales. El índice mensual es el promedio simple de las dos quincenas.

### Las fórmulas para reponderar genéricos

Sea `I_k(t)` el índice publicado del genérico k (nacional o de tu ciudad), `b` el periodo base de tu índice y `e_k` tu gasto en el genérico k durante el periodo de referencia `e`, por ejemplo los últimos 12 meses:

```
1) Relativo de precio, re-referenciado a tu base b
   R_k(t) = I_k(t) / I_k(b)

2) Tu ponderador de gasto, actualizado por precios a la base b (tipo Lowe, como INEGI)
   s_k(e) = e_k / Σ_j e_j
   s_k(b) = s_k(e)·[I_k(b)/I_k(e)]  /  Σ_j s_j(e)·[I_j(b)/I_j(e)]

3) Tu índice personal (Laspeyres/Lowe) y tu inflación
   P(t)    = 100 · Σ_k s_k(b) · R_k(t)
   π_m(t)  = P(t)/P(t−1) − 1          (mensual)
   π_a(t)  = P(t)/P(t−12) − 1         (anual)

4) Incidencia del genérico k entre t−s y t, en puntos porcentuales (suman exactamente π)
   C_k = 100 · s_k(b) · [R_k(t) − R_k(t−s)]  /  Σ_j s_j(b)·R_j(t−s)

5) Cambio de tus ponderadores (encadenamiento en el periodo de traslape L)
   P(t) = P(L) · Σ_k s_k(nuevo) · [I_k(t) / I_k(L)]

6) Prueba unitaria: con s_k = ω_k oficial y b = 2Q jul-2024
   INPC(t) = 1.36095 · P(t)   (tolerancia ±0.001)

7) Rendimiento real de tu portafolio contra TU inflación
   r_real = (1 + r_nominal) / (1 + π_personal) − 1
```

Hay dos errores típicos ([INEGI, Documento metodológico](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)):

- **Calcular incidencias con el ponderador base en vez del efectivo.** La fórmula 4 usa implícitamente el ponderador efectivo `s_k·R_k(t−s)/Σ`. Con el base, la suma deja de cuadrar, sobre todo en genéricos volátiles como frutas, verduras o electricidad.
- **Saltarse la actualización por precios.** Si el periodo de tu gasto no coincide con la base, hay que actualizar los ponderadores por precios relativos. Con eso el índice queda tipo Lowe, como el de INEGI; sin ese paso, queda "tipo Young".

Las incidencias que cruzan un eslabón se reparten con la convención (1+a)(1+b) − 1 = ΣCᵃ·(1+b) + ΣCᵇ, donde a es la inflación previa al eslabón y b la posterior. Conviene documentarla, porque INEGI no publica la suya. La fórmula 7 es la que conecta el índice con tu caso de uso de inversión: tu inflación personal se vuelve la tasa mínima que tu portafolio debe superar para no perder nivel de vida.

### Siete casos que necesitan reglas explícitas

Unos cuantos genéricos concentran el peso y se comportan distinto:

- **Vivienda propia (13.77%).** Es renta imputada, que INEGI calcula con el enfoque de renta equivalente. Si eres dueño, decide entre dos conceptos: "consumo", que la incluye con tu renta imputada estimada, o "gasto efectivo", que la excluye. **Nunca mapees la hipoteca a vivienda propia**: el pago de deuda no está en el INPC. Si rentas, usa el genérico 138, renta de vivienda, con tu renta real ([INEGI, Documento metodológico](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)).
- **Gasolina.** Hay un acuerdo "voluntario" para mantener la Magna debajo de 24 pesos por litro, según la prensa ([UnoTV](https://www.unotv.com/negocios/anuncian-precio-maximo-de-gasolina-magna-para-2026-se-mantendra-en-24-pesos/)).
- **Electricidad.** Depende del subsidio de verano por ciudad. En la 1Q de octubre de 2026, el fin del subsidio en 18 ciudades empujó la no subyacente ([Boletín 633/26](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_1q2026_10.pdf)).
- **Colegiaturas.** Se ajustan una vez al año, al inicio del ciclo escolar.
- **Genéricos estacionales.** Por ejemplo, servicios profesionales bajó de 157.4 a 131.5 entre agosto y septiembre de 2026.
- **Ciudad o nacional.** Regla razonable: índice de tu ciudad para lo local (vivienda, transporte colectivo, electricidad, alimentos frescos, loncherías) e índice nacional para lo que tiene precio casi único (autos, streaming, telefonía, gasolina con tope).
- **Lo que no está en la canasta.** Comisiones e intereses de tarjeta, impuestos, seguros distintos al de auto y suscripciones de software ([XLSX](https://www.inegi.org.mx/rnm/index.php/catalog/1015/download/32034)). Lo mejor es reportarlo aparte como "gasto no cubierto" en vez de forzarlo.

Además, el repo debe estar listo para un nuevo eslabón. INEGI y Banxico anunciaron revisiones cada dos años ligadas a la ENIGH, y a octubre de 2026 la canasta sigue en la ENIGH 2022 ([Banxico, Recuadro 4](https://www.banxico.org.mx/publicaciones-y-prensa/informes-trimestrales/recuadros/%7BB2DB3F5A-4FA5-E527-3A74-5B3998702397%7D.pdf)). En la práctica: ponderadores oficiales con fecha de vigencia, una tabla de correspondencia de genéricos entre canastas y encadenamiento en el traslape oficial.

## Una arquitectura local-first en cuatro piezas

El principio rector es que **tus datos crudos nunca salgan de tu máquina**: todo lo que se publica o se hospeda maneja solo precios públicos o agregados anónimos.

```
INEGI (Exportacion.aspx + XLSX ponderadores)
        │  GitHub Actions, días 9–10 y 24–25 de cada mes
        ▼
[1] inpc-data ── CSV/Parquet versionado · pesos con vigencia · prueba "reconstruye el INPC"
        │
        ▼
[2] Núcleo local (Python + CLI)
    tus archivos ─► parsers ─► diccionario de comercios MX ─► clasificador (reglas → LLM opcional)
               ─► crosswalk ClaveProdServ→genérico ─► motor Laspeyres ─► incidencias y benchmarks
        │                                   │
        ▼                                   ▼
[3] MCP local (MCPB / plugin de Claude)   [4] MCP remoto sin estado (presupuesto → índice + gráfica)
    devuelve solo agregados                 ChatGPT / Claude, no guarda nada
```

Las cuatro piezas:

1. **`inpc-data`.** Un dataset público y forkeable: genéricos nacionales y de las 55 ciudades, ponderadores y la prueba de reconstrucción, actualizado por cron después de cada publicación.
2. **El núcleo local.** Hace todo el trabajo pesado en tu computadora, con SQLite local y sin credenciales en el repo.
3. **El MCP local.** Envuelve al núcleo para Claude Desktop y Claude Code, con herramientas como `import_statement`, `import_cfdi_zip`, `set_budget`, `personal_inflation(mes)` y `explain_difference_vs_inpc()`.
4. **El MCP remoto.** Recibe solo montos por categoría que el usuario declara en el chat y devuelve el índice con una gráfica. Como no guarda nada, mantiene mínima tu exposición legal ([Claude, Connectors overview](https://claude.com/docs/connectors/overview); [MCP Apps, ene-2026](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/)).

### De "WALMART $1,500" a genéricos en tres niveles de confianza

Primero, la conexión bancaria no es opción por ahora:

- **Open finance.** La Ley Fintech exige APIs estandarizadas en su artículo 76, pero en seis años solo se publicaron las reglas de datos abiertos (junio de 2020). Las de datos agregados y transaccionales siguen pendientes, con un amparo en trámite por la omisión ([Fiskil, Open Finance Tracker México](https://www.fiskil.com/es/open-finance-tracker/mexico); [Facephi, 2026](https://facephi.com/observatory/en/fintech-law-in-mexico-2026-competition-sandbox-and-new-financial-models/)).
- **Agregadores.** Funcionan con venta directa, certificación y cobro por llamada. El MCP de Belvo, lanzado en agosto de 2026, en México cubre solo **fuentes fiscales y de empleo, no bancarias** ([Belvo MCPs](https://belvo.com/resources/mcps/)). Plaid no cubre México ([Plaid](https://plaid.com/docs/institutions/)).

**Conclusión: el MVP se diseña con datos que el usuario ya controla, y la conexión bancaria queda como un adaptador opcional a futuro.**

Las fuentes, de menor a mayor fricción:

- **Presupuesto declarado.** De 15 a 40 rubros, repartidos en genéricos con la estructura oficial. Funciona en un chat y no requiere datos personales.
- **Exportaciones CSV/XLSX o PDF del banco.** Requieren un parser por banco. No existe uno de código abierto para BBVA México ([PyPI bbva2pandas](https://pypi.org/project/bbva2pandas/)).
- **XML de CFDI que descargas del portal del SAT.** Cada concepto trae una **ClaveProdServ** obligatoria basada en UNSPSC, y `satcfdi` ya los lee ([GitHub python-satcfdi](https://github.com/SAT-CFDI/python-satcfdi); [Facturama](https://facturama.mx/blog/que-significa/catpys-catalogo-producto-servicios/)). El sesgo es que el súper, el tianguis y la combi suelen terminar en la factura global a "público en general", y las personas piden factura sobre todo de lo deducible ([IDC Online](https://idconline.mx/fiscal-contable/2022/06/29/cfdi-40-por-operaciones-con-publico-en-general)).
- **Recibos por correo y OCR de tickets.** Son la fuente más detallada y la de más fricción.

Con esas fuentes, la clasificación tiene tres niveles:

- **Nivel A: comercio → categoría.** Asigna cada movimiento a una de unas 12 divisiones CCIF o de 30 a 50 grupos del INPC. Usa en orden un diccionario abierto de los ~500 comercios mexicanos más comunes, el MCC cuando exista y un LLM obligado a elegir de una lista cerrada de categorías, con caché por comercio y correcciones del usuario.
- **Nivel B: categoría → genéricos, imputado.** El gasto de comercios mixtos como el súper se reparte con los ponderadores oficiales dentro de su grupo.
- **Nivel C: artículo → genérico, observado.** Usa CFDI, recibos o tickets y sustituye a la imputación en la parte que cubre.

**El resultado siempre debe decir qué parte se observó y qué parte se imputó**, por ejemplo "62% observado a nivel genérico, 38% imputado", y mostrar también un índice por grupo, que es más robusto que uno falsamente preciso por genérico. Las precisiones que anuncian los proveedores de categorización, de 92% a 97%, las reportan ellos mismos. Un prestamista encontró errores en ~25% de las transacciones, y su precisión bajaba a ~39% en las categorías que más le importaban ([Uncapped](https://weareuncapped.com/blog/transaction-categorisation-model-lending-ecommerce)). El activo reutilizable más valioso del proyecto sería **un crosswalk público ClaveProdServ → genérico del INPC**. No se encontró ninguno publicado.

### Cómo llevarlo a Claude y ChatGPT sin romper sus reglas

En 2026 las dos plataformas corren sobre MCP.

**Claude:**

- Acepta conectores remotos, conectores locales empaquetados como extensiones MCPB y plugins que combinan skills con conectores. Un servidor local distribuido por npm o PyPI no se lista directo en el directorio: hay que empaquetarlo como MCPB o como plugin ([Claude, Connectors](https://claude.com/docs/connectors/overview); [guía de envío](https://support.claude.com/en/articles/12922490-remote-mcp-server-submission-guide)).
- Anthropic clasifica las finanzas como **caso de alto riesgo**. Exige supervisión humana y aviso al usuario, recolectar solo los datos necesarios, y OAuth 2.0 en servidores con autenticación ([Anthropic Software Directory Policy](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy)).

**ChatGPT:**

- Su Apps SDK también es MCP y soporta MCP Apps desde febrero de 2026.
- OpenAI **prohíbe recolectar contraseñas, códigos OTP y datos de tarjeta**, y no aprueba apps que funcionen como "conectores no oficiales" a servicios de terceros ([OpenAI, guías de envío](https://developers.openai.com/apps-sdk/app-submission-guidelines)). Eso descarta cualquier scraping bancario dentro de ChatGPT.

**Un matiz que debes escribir en la documentación:** aunque el servidor MCP corra en tu máquina, todo lo que una herramienta le devuelve al modelo viaja al proveedor como parte de la conversación. Por eso las herramientas deben devolver agregados (ponderadores por categoría, valores del índice) y nunca listas de movimientos. Antes de que algo llegue al LLM, hay que borrar números de cuenta y CLABE.

### Hoja de ruta: del MVP al plugin y a una capa de pago opcional

| Fase | Plazo sugerido | Entregable | Criterio para pasar a la siguiente |
|---|---|---|---|
| 0. Datos y motor | 2–3 semanas | `inpc-data` con cron, motor Laspeyres, fórmulas 1–7, prueba de reconstrucción | INPC reconstruido ±0.001 desde ago-2024 |
| 1. MVP | 1–2 meses | Modo presupuesto declarado (15–40 rubros), selección de ciudad, incidencias en lenguaje claro, comparativo contra INPC, rendimiento real contra Cetes/UDI; web estática (cálculo en el navegador) + CLI; import de CSV genérico | 20–50 personas lo usan y entienden por qué su cifra difiere del INPC |
| 2. Plugin | 2–4 meses | Parsers de 2–3 bancos, CFDI XML, diccionario de comercios, clasificador con caché; MCP local (MCPB + plugin de Claude); MCP remoto sin estado con gráfica; envío a los directorios de Claude y ChatGPT | Aprobado en al menos un directorio; porcentaje observado vs. imputado visible en cada resultado |
| 3. Capa de pago opcional | 4+ meses | "Análisis mensual con IA" fuera de la plataforma, con pago voluntario; API B2B; solicitudes de becas | Los ingresos cubren hosting y tokens; nunca se venden datos individuales |

## Por qué funcionaría y por qué podría no despegar

El caso a favor es fuerte en lo metodológico y en lo estratégico. En contra pesan la granularidad de los datos y la demanda.

| A favor | En contra |
|---|---|
| Datos oficiales gratuitos a nivel genérico y ciudad, sin token, que no se revisan | La exportación de INEGI no está documentada como API y puede cambiar |
| Método publicado, replicable al milésimo y auditable | Mide composición de gasto, no los precios que tú pagas, que son la mayor fuente de dispersión |
| Usa los precios de INEGI: complementa al INPC en vez de contradecirlo, y evita el choque político de los índices alternativos | De un movimiento bancario solo sale la categoría; un ticket de súper mezcla decenas de genéricos |
| Nicho vacío: nadie combina transacciones con genéricos del INPC | No hay open finance; todo depende de que el usuario suba archivos |
| Se amarra a decisiones: aumento de sueldo, rendimiento real, presupuesto | La demanda es episódica; con inflación de ~3.5%, el atractivo de la novedad es bajo |
| Tu credencial de ex-Banxico da confianza en el método | El efectivo y la informalidad dejan fuera justo el gasto de los deciles bajos |

Los riesgos por categoría y su mitigación:

| Riesgo | Qué puede pasar | Mitigación |
|---|---|---|
| Datos | INEGI cambia o retira `Exportacion.aspx` | CSV versionados en el repo, validación por corrida, API con token como respaldo |
| Datos | Nuevo eslabón con la ENIGH 2024 y genéricos que cambian | Ponderadores con vigencia, tabla de correspondencia, encadenamiento en el traslape |
| Metodología | Falsa precisión al nivel de genérico | Niveles A/B/C, porcentaje observado vs. imputado, índice por grupo junto al de genérico |
| Metodología | Ruido en ciudad × genérico | Reportar el anual o un promedio móvil de 3 meses; regla ciudad/nacional documentada |
| Metodología | Sesgo de sustitución del Laspeyres | Actualización anual de ponderadores con encadenamiento; precio observado del usuario en partidas grandes |
| Privacidad | Los datos que devuelve una herramienta MCP llegan al proveedor del LLM | Devolver solo agregados, borrar CLABE y números de cuenta, opción de LLM local |
| Privacidad | Un servicio hospedado te convierte en "responsable" ante la LFPDPPP | Calculadora remota sin estado; aviso de privacidad y derechos ARCO si algún día guardas datos |
| Regulación | Cruzar a asesoría de inversiones (LMV art. 225) | La herramienta da una referencia, nunca recomienda productos ni asignaciones |
| Regulación | Suscripción con fricción (LFPC) | Cancelación en un clic por el mismo canal, aviso de renovación con 5 días |
| Reputación | Que parezca un producto oficial del INEGI o de Banxico | Leyenda de deslinde y nombre sin "INPC" |
| Demanda | La gente calcula su número una vez y no vuelve | Recordatorios en las fechas de publicación de INEGI, explicación de qué movió tu cifra, uso para negociar sueldo |

Una advertencia sobre la demanda: las calculadoras oficiales se lanzan o relanzan en crisis. La ONS relanzó la suya en marzo de 2022, en plena crisis del costo de vida, y el INDEC lanzó la suya en diciembre de 2024 en un ambiente de desconfianza ([ONS, mar-2022](https://www.ons.gov.uk/economy/inflationandpriceindices/articles/thecostoflivingcurrentandupcomingwork/march2022); [El Economista AR](https://eleconomista.com.ar/economia/el-indec-lanzo-una-calculadora-inflacion-personal-como-funciona-n80342)). En México tienes picos naturales: la "cuesta de enero" con las revisiones salariales, el fin del subsidio eléctrico de verano y los choques de alimentos. En abril de 2026, frutas y verduras subían 21.43% anual con una inflación general de 4.45% ([Expansión](https://expansion.mx/economia/2026/05/07/inflacion-inegi-abril-2026-hogares-pobres-alimentos)).

## Banxico ya hizo el ejercicio una vez; nadie lo ha hecho con transacciones

**Fuera de México**, casi todas las grandes oficinas de estadística ofrecen una calculadora en la que tecleas tu gasto en 5 a 20 categorías:

- **ONS (Reino Unido).** Imputa el gasto promedio de hogares de ingreso similar en las categorías que no llenas. Es la única con un dato público de uso: **más de un millón de usos o personas en 2022**, según dos publicaciones de la propia ONS que no coinciden en la unidad ([ONS](https://www.ons.gov.uk/economy/inflationandpriceindices/articles/howisinflationaffectingyourhouseholdcosts/latest); [ONS blog](https://blog.ons.gov.uk/2022/12/23/the-year-in-numbers/)).
- **Destatis (Alemania).** Pide 18 categorías más un "resto". Con la Universidad de Ulm hizo una prueba A/B: añadir una explicación de por qué tu tasa difiere de la oficial **aumentó la confianza, la utilidad percibida y la intención de volver a usarla** ([Uni Ulm](https://uni-ulm.de/en/mawi/iba/research/research-areas-of-the-professorship-of-business-information-management/explainable-artificial-intelligence/personal-inflation-calculator)).
- **INSEE (Francia).** Relanzó su simulador el 28 de septiembre de 2026 con versión móvil, historia desde 1997 y una pestaña de contribuciones por partida ([INSEE](https://www.insee.fr/fr/statistiques/fichier/version-html/9060739/CP_Simulateur_inflation.pdf)).
- **BCE.** **Descontinuó su calculadora** al migrar de portal ([euro-area-statistics.org](http://www.euro-area-statistics.org/)).
- **Índices por grupo en lugar de calculadora.** Varios países publican índices por grupo de hogares, como los R-CPI-I del BLS por quintil de ingreso ([BLS](https://www.bls.gov/cpi/research-series/r-cpi-i.htm)) o el indicador de Ipea por rango de ingreso en Brasil ([Ipea](https://www.ipea.gov.br/cartadeconjuntura/index.php/2017/11/inflacao-por-faixa-de-renda/)).

**Ninguna usa transacciones reales ni el nivel de genérico.**

**En México no hay calculadora personal.** La "Calculadora de Inflación" de INEGI solo calcula la variación de un índice oficial entre dos fechas ([INEGI](https://en.www.inegi.org.mx/app/indicesdeprecios/documentos/Calculadora_de_Inflacion.pdf)). Lo oficial más cercano son subíndices fijos, como el de la canasta de consumo mínimo. El precedente directo es el **Recuadro 5 de Banxico (agosto de 2022)**, que cruzó el gasto de cada hogar de la ENIGH 2020 con los 299 genéricos y las 55 ciudades. Encontró una brecha de 1.7 pp entre quintiles extremos y diferencias por tipo de hogar: los unipersonales tuvieron −1.83 pp frente a los nucleares, y los hogares con niños menores de 12 años tuvieron alzas mayores ([Banxico, Recuadro 5](https://www.banxico.org.mx/publicaciones-y-prensa/informes-trimestrales/recuadros/%7B57BAF692-8130-53E4-1ABE-DD05B28AFE6D%7D.pdf)). IMCO midió casi 2 pp entre el decil 1 y el 10 en 2022 ([IMCO](https://imco.org.mx/la-inflacion-afecta-mas-a-los-hogares-de-menores-ingresos/)). Márquez Moranchel calculó que los hogares pobres perdieron 6.5% más poder adquisitivo que los ricos entre 2016 y 2023 ([UNAM](https://journals.unam.mx/index.php/rie/article/view/90415)). **Tu herramienta sería ese Recuadro hecho continuo, con gasto real en lugar de la ENIGH.**

**La evidencia académica respalda el uso como referencia para inversiones.** Kukk, Toczynski y Basten usaron datos de cuentas bancarias de Estonia, el mismo tipo de dato que tu proyecto. Encontraron que **por cada punto de inflación personal más alta, el gasto sube 1.4%** y que los hogares también aumentan su inversión en bolsa ([JME 2025](https://ideas.repec.org/a/eee/moneco/v153y2025ics0304393225000716.html)). No existe ningún experimento que le muestre a la gente su propia inflación y mida cómo cambian sus expectativas. Esa pregunta está abierta y tu herramienta podría responderla con consentimiento.

**En el sector privado nadie lo ha automatizado:**

- **Bancos y apps de finanzas personales.** Monzo, Revolut, Nu, Mercado Pago, Fintonic, Emma, YNAB y similares no tienen una función de inflación personal calculada con tus transacciones. A lo más publican artículos que te piden hacer la cuenta a mano. Un ejemplo es BBVA México con "La inflación personal" de 2017 ([BBVA](https://www.bbva.com/es/la-inflacion-personal/)).
- **Apps independientes.** Tienen tracción mínima: ExpensePal obtuvo 8 votos en Product Hunt ([hunted.space](https://www.hunted.space/product/expensepal)). Richify ofrece un "termómetro anti-inflación" para México, pero usa el INPC general ([Richify](https://www.richify.ai/es/termometro-inflacion)).
- **Truflation.** Vive de un token y de vender datos por API. No tiene índice de México ([Truflation](https://truflation.com/documents)).
- **PriceStats.** Mide precios en línea para clientes institucionales. State Street la compró en noviembre de 2025 ([Financial Investigator](https://www.financialinvestigator.nl/en/nieuws-detailpagina/2025/11/10/state-street-acquires-pricestats-global-leader-in-inflation-analytics)).
- **ShadowStats y Chapwood.** Son índices opacos y desacreditados metodológicamente ([Full Stack Economics](https://www.fullstackeconomics.com/p/no-the-real-inflation-rate-isnt-14-percent)).

El riesgo político está documentado: en 2011, Argentina multó con **500 mil pesos argentinos** a consultoras por publicar índices alternativos ([Chequeado](https://chequeado.com/hilando-fino/a-falta-de-datos-de-inflacion/)), y en 2022 el instituto turco TÜİK demandó al grupo independiente ENAG ([Duvar English](https://www.duvarenglish.com/turkish-govt-statistics-office-tuik-files-lawsuit-against-enagroup-over-alternative-inflation-data-news-57435)). Tu proyecto esquiva ese riesgo porque no mide precios propios: repondera los de INEGI.

**En GitHub hay muchos repos pero casi ninguna tracción:**

- La búsqueda "personal inflation" devuelve 138 repos. El más popular tiene **13 estrellas y está inactivo desde 2023** ([GitHub](https://github.com/n8ngo/puffer-personal-inflation-index)).
- `Dahafla/personal-cpi-model` es el más parecido: convierte transacciones de tarjeta en un Laspeyres con el CPI de EE.UU. Tiene 0 estrellas ([GitHub](https://github.com/Dahafla/personal-cpi-model)).
- `kvothesson/guita` es un plugin de Claude Code para Argentina que ajusta gastos tecleados con el IPC general. Ya probó la experiencia de plugin, pero no usa genéricos ni archivos bancarios ([GitHub](https://github.com/kvothesson/guita)).
- Hay unos diez servidores MCP de Banxico y otros diez de INEGI, todos con 0 a 6 estrellas y todos limitados al INPC general ([mcp-banxico](https://github.com/nanisadw3/mcp-banxico); [mcp-inegi](https://github.com/itzamna-mx/mcp-inegi)).

Los envoltorios de datos ya son commodity. Lo diferenciador sería el mapeo a genéricos, el cálculo personal y el diseño de privacidad.

| Precedente | Qué hizo | Lección para ti |
|---|---|---|
| Banxico, Recuadro 5 (2022) | ENIGH 2020 → 299 genéricos × 55 ciudades | El método está validado; falta hacerlo continuo y con gasto real |
| ONS (Reino Unido) | Formulario con imputación por ingreso | Poca captura, imputación y lanzamiento en plena crisis |
| Destatis + Ulm | Prueba A/B de explicabilidad | Explicar por qué difiere tu cifra genera confianza y uso recurrente |
| BCE | Calculadora descontinuada | Sin mantenimiento automatizado, la herramienta muere |
| Kukk et al. (Estonia) | Inflación personal con datos bancarios | La cifra predice decisiones financieras; sirve como referencia para inversiones |
| Truflation / PriceStats | Índices privados de precios, negocio B2B | Al consumidor se llega gratis; el dinero está en B2B |
| Argentina 2011 / Turquía 2022 | Índices alternativos castigados | Usar precios de INEGI elimina el conflicto |
| Dahafla, guita, replica-inpc-mx | Piezas sueltas con tracción nula | El nicho sigue vacío; Bolsillómetro se construye desde cero e integra todo en un solo proyecto |
| Hacker News | "Personal inflation": ≤2 puntos; "pedir aumento por inflación": 55 puntos y 101 comentarios | Interesa más la negociación salarial que la medición abstracta ([HN](https://news.ycombinator.com/item?id=31166006)) |

## Bolsillómetro y Canastómetro encabezan los nombres

La fórmula que mejor funciona es una marca inventada con sabor mexicano y un subtítulo descriptivo. Los dominios se revisaron el 26-oct-2026 con RDAP para .com y .app y con DNS para .mx. **Son señales de disponibilidad, no garantías.**

| Nombre | .com / .app / .mx | GitHub | Veredicto |
|---|---|---|---|
| **Bolsillómetro** (`bolsillometro`) | libres | sin conflictos | Mejor opción: inventado, claro, amigable |
| **Canastómetro** (`canastometro`) | libres | sin conflictos | Mejor opción; evoca la canasta, aunque puede sonar solo a comida |
| **Inflacionómetro** | libres | sin conflictos | Muy claro, algo largo; puede ser objetado por descriptivo |
| **¿Le Ganas?** (`leganas`) | libres | solo repos no relacionados | Ideal para el plugin ("¿le ganas a tu inflación?"); puede sonar a apuestas |
| **TuInflación** / **¿Cuánto Me Sube?** | libres | sin conflictos | Mejor como subtítulo o nombre secundario |

Los nombres a evitar:

- **MiINPC e INPCito.** "INPC" es el nombre de un producto del INEGI. La LFPPI prohíbe registrar sin autorización siglas y nombres de programas de organismos gubernamentales, y los términos de INEGI prohíben sugerir que avala tu producto ([LFPPI art. 173](https://mley.mx/LFPPI/articulo/173/); [INEGI, términos de uso](https://www.inegi.org.mx/inegi/terminos.html)).
- **Cualquier "IPC".** En México, IPC significa el índice bursátil de la BMV ([S&P DJI](https://www.spglobal.com/spdji/es/indices/equity/sp-bmv-ipc/)). Invitaría la confusión con productos de inversión que justamente quieres evitar.
- **MiInflación.** Ya hay tres repos argentinos con ese nombre.
- **¿Cuánto Subió?** Ya lo usan rastreadores de precios en Costa Rica y Paraguay.
- **Lanómetro.** Alguien registró el .com el 20-oct-2026.
- **Varómetro.** El .com está registrado desde 2023.
- **Chivómetro.** "Chivo" también significa chivo expiatorio o soplón ([Chilango](https://www.chilango.com/general/formas-alternas-de-llamar-al-dinero/amp/)).

Estructura recomendada:

- **Marca:** Bolsillómetro.
- **Subtítulo:** "Tu inflación personal con datos del INPC (Fuente: INEGI)".
- **Nombre en las plataformas de IA:** "¿Cuál es mi inflación? — Bolsillómetro".
- **Repo y paquete:** `bolsillometro`, sin acentos; el acento se queda en el logotipo.
- **Dominios:** registrar .com, .mx y .app juntos.

**Falta la búsqueda de marca en el IMPI.** MARCia no se pudo consultar automáticamente. Cada finalista necesita una búsqueda manual de marcas idénticas y fonéticamente parecidas en las clases 9, 35, 36 y 42, y conviene que un agente de propiedad industrial confirme las clases antes de presentar la solicitud.

## Cobrar poco, fuera de la plataforma y lejos de la asesoría de inversiones

**Cómo se sostienen otros proyectos abiertos de finanzas personales:**

- **Maybe Finance.** Es la advertencia. Cerró su app en 2023 después de gastar alrededor de un millón de dólares. La relanzó como código abierto y en julio de 2025 la abandonó para pivotar a B2B. En su despedida explica que sostener una app B2C con sincronización bancaria automática "es una batalla cuesta arriba" ([Maybe v0.6.0](https://github.com/maybe-finance/maybe/releases/tag/v0.6.0)).
- **Ghostfolio.** Vende una versión hospedada de su código AGPL ([Ghostfolio](https://cdn.jsdelivr.net/gh/ghostfolio/ghostfolio@main/README.md)).
- **Firefly III.** Vive solo de donativos ([Firefly III](https://docs.firefly-iii.org/explanation/more-information/donations/)).
- **Actual Budget.** Se financia con Open Collective, donde su mayor donante es una empresa ([Open Collective](https://opencollective.com/actual)).
- **Lunch Money.** No es de código abierto, pero demuestra que **el pago voluntario funciona**: desde 60 dólares al año, sin anuncios ni venta de datos, y más de 13 mil miembros de pago ([Lunch Money](https://lunchmoney.app/about/)).

Tu ventaja frente a Maybe es de costos: un índice personal necesita participaciones mensuales por categoría, no sincronización en tiempo real.

**La escalera de ingresos que mejor encaja**, en orden:

1. **Núcleo gratis para siempre.** Librería con licencia permisiva (MIT/Apache), app hospedable con AGPL y marca registrada para que los forks cambien de nombre.
2. **Calculadora gratuita en modo presupuesto declarado.**
3. **Patrocinios y becas.** FLOSS/fund da entre 10 mil y 100 mil dólares por proyecto al año, y se solicita publicando un `funding.json` ([Zerodha FLOSS/fund](https://zerodha.com/open-source/2025-report/)).
4. **API o marca blanca B2B.** Para fintechs y brokers, para plataformas de nómina y recursos humanos (el salario mínimo de 2026 subió 13%, a 315.04 pesos diarios ([EY México](https://www.ey.com/es_mx/technical/tax/boletines-fiscales/incremento-salarios-minimos-2026))), para medios y para Afores.
5. **Una suscripción muy ligera de "análisis mensual con IA".** Pago voluntario con un piso bajo, de unas decenas de pesos al mes. Incluiría un aviso cuando INEGI publica, una explicación en español claro de qué movió tu cifra, tu historial, alertas como el fin del subsidio eléctrico y apoyo para preparar una negociación salarial.

**Nunca se venden datos individuales.** Si algún día publicas agregados, que sean anónimos, con consentimiento previo y de preferencia abiertos, como bien público.

**Las plataformas de IA sirven como canal de distribución, no de cobro:**

- **ChatGPT.** Hoy no permite vender bienes digitales ni suscripciones dentro de una app. Una app tampoco puede mostrar planes ni promover upgrades. Sí permite que el usuario inicie sesión en una cuenta de pago que ya contrató fuera ([OpenAI, guías de envío](https://developers.openai.com/apps-sdk/app-submission-guidelines); [OpenAI, monetización](https://developers.openai.com/apps-sdk/build/monetization)).
- **Claude.** Su directorio es gratuito y "no es pay-to-play", y no se encontró un mecanismo de pagos para conectores ([Claude, FAQ de socios](https://claude.com/docs/connectors/building/partnership-faq)).
- **Política de uso de Anthropic desde el 12 de noviembre de 2026.** Toda "recomendación personalizada para comprar, vender, mantener o asignar entre productos de inversión específicos" tendrá que revisarla una persona calificada y avisar al usuario que la generó una IA. El contenido educativo general queda excluido ([Anthropic Usage Policy](https://www.anthropic.com/aup)).

**El modelo práctico:** la app y el conector son gratuitos, el pago ocurre en tu sitio y el resultado se diseña como referencia, nunca como recomendación.

**Las líneas regulatorias en México** (esto no es asesoría legal y cada punto debe confirmarlo un abogado mexicano):

| Línea | Qué dice | Cómo diseñar |
|---|---|---|
| Asesoría de inversiones (LMV art. 225) | Dar recomendaciones de inversión individualizadas de forma habitual y profesional requiere registro ante la CNBV y certificación ([LMV 225](https://mley.mx/LMV/articulo/225/)) | Bien: "tu inflación fue 6.1%; para conservar tu nivel de vida necesitas un rendimiento nominal de al menos 6.1%". Mal: "mueve tu dinero a tal fondo" o "asigna 60/40". Comparar contra la tasa de Cetes publicada es zona gris |
| Ley Fintech | Una calculadora no es una de las actividades de ITF que requieren autorización; mover dinero o custodiar fondos sí entra en ese terreno ([Facephi](https://facephi.com/observatory/en/fintech-law-in-mexico-2026-competition-sandbox-and-new-financial-models/)) | Nunca ejecutar operaciones ni pedir credenciales bancarias |
| LFPDPPP 2025 | Vigente desde el 21-mar-2025; la autoridad ahora es la Secretaría Anticorrupción y Buen Gobierno; una nueva finalidad requiere nuevo consentimiento ([Garrigues](https://www.garrigues.com/es_ES/noticia/mexico-nueva-ley-federal-proteccion-datos-personales-posesion-particulares-introduce)) | Todo local, calculadora remota sin estado; aviso de privacidad completo y simplificado si algún día almacenas datos; no está claro si la nueva ley exige consentimiento expreso para datos financieros: confírmalo |
| PROFECO / LFPC (reforma de dic-2025) | Cancelación inmediata, gratuita y por el mismo canal; aviso de renovación con 5 días; multas de hasta ~3 millones de pesos ([El Imparcial](https://www.elimparcial.com/mexico/2025/12/13/ya-esta-en-vigor-nueva-reforma-a-la-ley-federal-del-consumidor-te-protege-de-cobros-fantasma-en-plataformas-de-servicios-digitales/)) | Cancelación en un clic, sin plazos forzosos ni penalizaciones |
| Términos de uso de INEGI | Se permite el uso comercial citando "Fuente: INEGI", siempre que se avise si los datos se transformaron y no se sugiera aval ([INEGI](https://www.inegi.org.mx/inegi/terminos.html)) | Leyenda: "Cálculos propios con datos del INPC (Fuente: INEGI). No es un producto oficial del INEGI ni de Banco de México" |
| IMPI (LFPPI art. 173) | No se pueden registrar nombres descriptivos ni siglas de programas de gobierno ([LFPPI 173](https://mley.mx/LFPPI/articulo/173/)) | Marca inventada y búsqueda en MARCia |

Hay además un punto que esta investigación no cubrió y que es tuyo: revisa las reglas de ética y confidencialidad que aplican a exempleados de Banxico antes de buscar alianzas con el banco o con el MIDE, o de usar frases que suenen a información interna.

**Para la difusión, el terreno es fértil:**

- **Uso de apps sin hábitos.** El 69.1% de quienes tienen cuenta de ahorro ya usa la app del banco. Pero de quienes llevan algún registro de gastos, solo 23.9% hace un presupuesto y 19.5% usa apps o herramientas. La alfabetización financiera lleva estancada en 58/100 desde 2018 ([INEGI, ENIF 2024](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/enif/ENIF2024_CP.pdf); [BBVA Research](https://www.bbvaresearch.com/publicaciones/mexico-educar-para-incluir-rumbo-a-la-sostenibilidad-financiera/)).
- **Semana Nacional de Educación Financiera de la CONDUSEF.** Reunió a más de 75 instituciones en octubre de 2026 ([Excélsior](https://www.excelsior.com.mx/finanzas/aprovecha-semana-educacion-financiera)).
- **MIDE.** Lo crearon Banxico e instituciones financieras privadas, y lo han visitado más de 1.5 millones de niños y jóvenes ([Expansión](https://expansion.mx/finanzas-personales/2025/09/03/el-mide-revela-su-formula-asi-logro-que-la-economia-sea-un-juego-atractivo-para-sus-visitantes)).
- **Podcasts.** Su audiencia mensual en México se estimó en 34 millones en 2022 ([DPL News](https://dplnews.com/?p=133528)).

## Conclusión

Lo nuevo de tu proyecto no es el índice; Banxico ya lo calculó en 2022 y cualquier economista puede escribir un Laspeyres. Lo nuevo es la infraestructura que nadie ha armado en México: un dataset público de genéricos y ciudades que se reconstruye solo, un crosswalk abierto de ClaveProdServ y comercios hacia genéricos, y una forma honesta de reportar cuánto de tu inflación se observó y cuánto se imputó. Ese conjunto sí se puede volver la referencia, porque el campo está vacío y los repos existentes no tienen tracción. También sirve de base para lo que viene: si la CNBV publica las reglas transaccionales, conectar un banco será solo un adaptador más.

El episodio de Morodo te sirve como una pregunta abierta, no como especificación. La gente ya intuye que "su" inflación no es la oficial, pero hoy la mide con herramientas que confunden gasto con precios, y la mezcla con tesis monetarias que no son inflación. Si tu herramienta muestra lado a lado "tu costo de vivir" y la referencia patrimonial que cada quien elija, con la fórmula a la vista, convierte una discusión retórica en un número auditable. Ese es un servicio de educación financiera más valioso que cualquier cifra única, incluida la del 8%.

## Siguientes pasos recomendados

| # | Paso | Cuándo |
|---|---|---|
| 1 | Crear el repo con licencia permisiva, el pipeline `inpc-data` (POST a `Exportacion.aspx` + XLSX de ponderadores) y la prueba que reconstruye el INPC ±0.001 desde ago-2024, todo construido desde cero (hecho: fase 0) | Semanas 1–2 |
| 2 | Implementar las fórmulas 1–7 con incidencias, reglas para vivienda propia y "gasto no cubierto", y elección de ciudad (por ejemplo, Pachuca) | Semanas 2–4 |
| 3 | Publicar el MVP en modo presupuesto declarado como web estática que calcula en el navegador, con explicación de qué movió tu cifra y comparativo de rendimiento real | Mes 2 |
| 4 | Probarlo con 20–50 personas de perfiles distintos (rentan o son dueños, tienen auto o usan transporte público, escuela privada o pública) y medir si entienden la diferencia contra el INPC | Mes 2 |
| 5 | Agregar parsers de CSV de 2–3 bancos, lectura de CFDI y el diccionario de comercios; empezar el crosswalk ClaveProdServ → genérico como dataset abierto | Meses 2–4 |
| 6 | Empaquetar el MCP local (MCPB + plugin de Claude) y el MCP remoto sin estado; enviarlos a los directorios de Claude y ChatGPT con aviso de privacidad y deslinde | Meses 3–4 |
| 7 | Hacer la búsqueda en MARCia (IMPI) para Bolsillómetro y Canastómetro, registrar dominios y consultar a un abogado sobre LMV 225, la LFPDPPP y las reglas para exempleados de Banxico | Antes del lanzamiento público |
| 8 | Lanzar junto con una nota de periodismo de datos (inflación por perfil de hogar) en una fecha de publicación del INPC, idealmente en la cuesta de enero de 2027; preparar la solicitud a FLOSS/fund y un contacto con la SNEF 2027 | Ene–mar 2027 |
| 9 | Solo si hay uso recurrente, abrir el análisis mensual con IA con pago voluntario fuera de la plataforma, y explorar un piloto B2B con nómina o una fintech | Desde el mes 6 |
