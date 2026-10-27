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
