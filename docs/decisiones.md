# Registro de decisiones

Decisiones de diseño ya tomadas, con su motivo. Una decisión nueva se agrega al final de su
fase; si una cambia, no se borra: se marca como reemplazada y se anota la nueva.

## Fase 0: datos y motor (26-oct-2026)

- **Código propio, desde cero.** No se hacen forks ni se depende de otros repos del INPC: los
  que existen no tienen tracción y el valor está en un dataset que se valida solo.
- **Paquete y CLI `bolsillometro`, licencia MIT, Python 3.11 o más.**
- **Solo `requests` y `openpyxl` como dependencias.** Lo demás sale de la biblioteca estándar.
- **Identificadores y docstrings en español.**
- **Local-first.** Los movimientos y facturas del usuario nunca salen de su máquina; hacia fuera
  solo salen agregados.
- **Descarga sin token desde la app "Índices de Precios" del INEGI** (la exportación que usan
  los `.IQY` de Excel). No es una API documentada, así que el pipeline valida todo antes de
  escribir: el INPC nacional se reconstruye con los 292 genéricos y los ponderadores oficiales
  con error de ±0.001, o no se guarda nada.
- **Datos como CSV versionados en `data/`,** en forma ancha (una fila por periodo, una columna
  por genérico): se abren en Excel y cada actualización agrega una línea al diff.
- **Las notas del podcast** (*Revolución de la Riqueza* #292) no se suben al repo porque citaban
  demasiado texto del episodio. Su resumen está en
  [`00-investigacion-inicial.md`](00-investigacion-inicial.md).

## Fase 1: MVP (27-oct-2026)

- **Web estática después del CLI, dentro de la fase 1 y en su propio PR.** Las 20 a 50 personas
  de la prueba no van a usar un CLI, pero primero hay que tener el cálculo.
- **Unos 25 rubros en lenguaje común.** Con 15 habría que imputar demasiado (todo el súper en
  un solo rubro) y con 40 la gente deja rubros en blanco.
- **Presupuesto en TOML.** Se lee con `tomllib`, sin dependencias nuevas; admite comentarios
  para una plantilla autoexplicada; agrupa en un archivo la configuración (ciudad, periodo del
  gasto, modo de vivienda propia), los rubros con su aumento propio opcional y el gasto no
  cubierto. CSV obligaba a columnas raras o a un segundo archivo, y YAML agregaba una
  dependencia. La web importa y exporta el mismo archivo.
- **Cetes y UDI de las exportaciones públicas del SIE de Banxico, sin token,** como el INEGI.
  El API REST con token queda como respaldo.
- **El import de CSV del banco pasa a la fase 2.** Sin el diccionario de comercios y el
  clasificador solo sumaría montos a mano.
- **Ciudades: un CSV mensual por ciudad** (`data/ciudades/<clave>_mensual.csv`). Un solo CSV
  tendría 16,060 columnas y cada actualización cambiaría una línea enorme. Sin quincenas: son
  unos 13 MB contra unos 41 MB, y el ruido de la muestra por ciudad hace poco útil la quincena.
- **Las ciudades se bajan una por exportación.** Juntar 5 tardó más y con 11 el INEGI respondió
  con HTTP 500.
- **Validación de ciudades sin reconstrucción exacta,** porque el INEGI no publica pesos
  genérico × ciudad. En su lugar:
  - El título de cada exportación debe nombrar su ciudad.
  - Acotamiento: de ago-2018 a jul-2024, el nacional de cada genérico debe quedar entre el
    mínimo y el máximo de sus ciudades (±0.001).
  - Plausibilidad: la inflación anual de cada ciudad contra la de sus genéricos con pesos
    nacionales, con tolerancia de ±2 pp (el máximo observado fue 1.11 pp).
- **Las ciudades van en su propio paso y commit del workflow,** y solo cuando el nacional trae
  un mes nuevo: tardan unos 10 minutos y, si fallan, el dato nacional ya quedó guardado.
- **En `data/` las ciudades pueden ir atrás del nacional, nunca adelante.** Entre los dos pasos
  del workflow (o si la descarga por ciudad falla un día), `data/` trae un mes nacional que las
  ciudades todavía no; las pruebas y `verificar` lo aceptan si todas las ciudades llegan al
  mismo mes. Lo que sí se exige es que una descarga nueva por ciudad llegue al mes del
  nacional, porque el INEGI publica ambos el mismo día.
- **Banxico: series tal como se publican.** Se guardan la UDI diaria y la tasa de cada subasta
  de Cetes, sin mensualizar; lo mensual se calcula al usarlas, para que el criterio quede en el
  código y no en los datos.
- **Rendimientos de fin de mes a fin de mes.** La UDI se toma el último día de cada mes. Los
  Cetes se reinvierten cada 28 días a la tasa de la última subasta, con `tasa · días / 360`, y
  el último tramo se prorratea. Es lo que obtendría alguien que compra Cetes a 28 días y los
  renueva. El INPC mensual es un promedio del mes, así que la comparación tiene medio mes de
  desfase; para la variación anual es despreciable.
- **La UDI se valida contra el INPC.** Como Banxico la deriva del INPC quincenal con una regla
  fija, cuadrar tramo por tramo y día por día confirma a la vez la descarga de Banxico y la del
  INEGI.
- **Banxico corre en cada ejecución del workflow, antes que las ciudades.** Son dos peticiones
  chicas; si fallan, el dato nacional ya quedó guardado.
- **`red.py` comparte los reintentos** entre el cliente del INEGI y el de Banxico, en lugar de
  duplicarlos.
- **32 rubros** (aprobados el 27-oct-2026), en `src/bolsillometro/catalogos/rubros.csv`: cada
  genérico en exactamente un rubro. Es un catálogo curado, versionado con el código y no en
  `data/`, que solo trae lo que se descarga. Vivienda propia queda solo con la renta imputada
  (139); los derechos de agua (142) son un rubro propio porque son un pago real, y la reparación
  menor (140) va con mantenimiento.
- **Índice nacional para lo de precio casi único,** aunque elijas ciudad: gasolinas, autos, motos y
  bicis, telefonía, internet, TV de paga, streaming y avión. También para lo que tu ciudad ya no
  cotiza. Todo lo demás usa los precios de tu ciudad.
- **El mes del gasto es la base del índice personal** (`P(e) = 100`). El gasto de cada rubro se
  reparte entre sus genéricos con los ponderadores oficiales llevados a ese mes por precios
  relativos, igual que el INEGI; por eso el hogar promedio reproduce el INPC. Debe ser de
  ago-2024 en adelante, cuando rige la canasta 2024.
- **Aumento propio como serie que crece parejo cada mes:** `(1 + a)^(meses/12)`. Sirve para
  partidas que suben una vez al año (renta, colegiatura) y que la persona conoce mejor que el
  índice.
- **Vivienda propia fuera por omisión** (modo `gasto_efectivo`): la mayoría de quien es dueño no
  piensa en su casa como un gasto mensual. El modo `consumo` la incluye con la renta estimada.
- **Una sola cifra** (27-oct-2026): el reporte da tu inflación de los últimos 12 meses y nada
  más al frente. El INPC nacional y el de tu ciudad son referencias que confunden ("¿cuál es la
  mía?"); solo aparecen con `--detalle`. Sí se muestra si los Cetes le ganaron, porque responde
  la pregunta de inversión del proyecto.
- **Onboarding por entrevista, no por archivo** (27-oct-2026): las personas no llenan el TOML;
  quien entrevista (Claude con el skill `entrevista`, después la web y el plugin) hace las
  preguntas del cuestionario estandarizado, en orden y con el mismo texto, y
  `bolsillometro entrevista` convierte las respuestas. El cuestionario es un archivo de datos
  para que todas las interfaces pregunten lo mismo.
- **Preguntas que agrupan rubros:** "comida para la casa" llena súper, carne, lácteos, frutas y
  refrescos; "comer fuera", restaurantes y comida para llevar; "limpieza y cuidado personal",
  esos dos. El monto se reparte con los ponderadores oficiales: la persona no tiene por qué
  saber cuánto de su súper es carne.
- **Lo irregular se pregunta al año** (ropa, muebles, viajes, servicio del auto) y se divide
  entre 12. La compra de auto no se pregunta: es irregular y su peso distorsionaría el mes.
- **El mes del gasto en la entrevista es el último con datos:** las respuestas describen un mes
  típico de hoy.
- **`presupuestos/` está en `.gitignore`:** las respuestas de una persona nunca se suben.
- **Respuestas por rango, con escalas en el cuestionario** (27-oct-2026, tras la primera
  entrevista): contestar eligiendo un rango es más rápido que escribir cifras. Las opciones y su
  valor representativo viven en `[escalas]` del cuestionario, no en cada interfaz, para que
  Claude, la web y el plugin den el mismo resultado con las mismas respuestas. Siempre se puede
  dar un monto exacto.
- **Nombre común de la ciudad en el reporte:** "la Ciudad de México" en vez de "Area
  Metropolitana de la Cd. de México" (`ciudades.NOMBRES_COMUNES`); el catálogo conserva el
  nombre del INEGI.
