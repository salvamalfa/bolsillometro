# Combis Zempoala — Investigación inicial

**Fecha:** 2026-09-19
**Estado:** documento de exploración. No es un plan de implementación ni un compromiso de arquitectura.
**Contexto:** ruta de combis Zempoala (Hidalgo) ↔ Pachuca y destinos intermedios. Operación con
base/paradero, orden de salida por turnos y una *checadora* que registra qué unidad llegó a formarse.

---

## 1. El problema no es uno, son cinco

La idea inicial ("un Uber de combis") mezcla cinco productos con dificultad, costo y riesgo social muy
distintos. Separarlos es la decisión más importante de todo el proyecto.

| # | Problema | Quién sufre | Dificultad técnica | Dependencia de terceros |
|---|----------|-------------|--------------------|-------------------------|
| A | Coordinación de la fila: quién se formó, quién sigue, quién falta hoy | Chofer, checadora, dueño | **Baja** | Solo la checadora + N choferes |
| B | Información al pasajero: rutas, precios, horarios, frecuencia | Pasajero | Baja | Nadie (es contenido) |
| C | Tiempo real: dónde viene la combi, en cuánto llega | Pasajero | **Alta** | Todos los choferes, hardware, batería |
| D | Bolsa de choferes / relevos por día | Dueño de unidad, chofer eventual | Media | Masa crítica de ambos lados |
| E | Reputación: estrellas a choferes y estado de unidades | Pasajero (y nadie más quiere esto) | Baja técnica, **alta social** | Aceptación del gremio |

**Hallazgo central:** el orden de valor no es el orden de dificultad.

El dolor concreto que describes —tu papá marcándole a la checadora para saber si la combi 3 ya se
formó— **no se resuelve con GPS**. Se resuelve con un tablero compartido de turnos que la checadora
actualiza y todos ven. Eso es problema (A), es lo más barato de construir, no requiere hardware, no
requiere que los pasajeros adopten nada, y beneficia primero a quien tiene el teléfono en la mano.

El "Uber" (C) es la parte cara, frágil y la que depende de que **todos** los choferes cooperen todos
los días. Si se intenta primero, lo más probable es que el proyecto muera antes de dar valor.

### El atajo importante sobre el ETA

No se necesita GPS para dar un tiempo estimado útil al pasajero. Si el sistema sabe
*"la combi 3 salió de la base a las 10:42"* y sabe que el tramo base → San Antonio tarda ~12 min en
promedio a esa hora, ya se puede mostrar *"próxima combi a San Antonio ≈ 10:54"*. Esa predicción sale
gratis del producto (A). El GPS mejora la precisión, no la habilita.

Esta es exactamente la lógica de [TheTransitClock](https://thetransitclock.github.io/): consume
posiciones de vehículos y produce predicciones de llegada. La diferencia es que el arranque puede
hacerse con eventos de salida en vez de posiciones continuas.

---

## 2. Proyectos existentes de los que se puede partir

### 2.1 Lado pasajero / transporte informal (lo más cercano al caso)

**[Trufi Core](https://github.com/trufi-association/trufi-core) / [Trufi App](https://github.com/trufi-association/trufi-app)** — Trufi Association.
Es el hallazgo más relevante. Está construido **específicamente** para transporte informal de
mercados emergentes: minibuses con rutas conocidas pero no documentadas y sin paradas oficiales
(trufis en Bolivia, matatus en Kenia, daladalas en Tanzania, tro-tros en Ghana). O sea, combis.

- Stack: Flutter (Dart 3.10+), MapLibre GL, monorepo modular.
- Backend: instancia de [OpenTripPlanner](https://www.opentripplanner.org/) (soporta OTP 1.5 / 2.4 / 2.8) + feed GTFS, y opcionalmente GTFS-RT para posiciones en vivo.
- Ya trae: planeación multimodal, marcadores de vehículos en tiempo real vía GTFS-RT, navegación paso a paso, búsqueda offline, español incluido.
- Tienen un programa explícito, ["Trufi in Your City"](https://www.trufi-association.org/projects/trufi-in-your-city/), para desplegar la app en una ciudad nueva.
- **Licencia: GPL-3.0.** Si se forkea y se distribuye la app, el código derivado debe publicarse bajo GPL-3. Para un proyecto comunitario no es problema, pero hay que decidirlo a conciencia desde el día 1, no después.
- Actividad: ~1,456 commits, 111 estrellas, 53 forks.

**Advertencia de escala:** Trufi está pensado para una *ciudad* con decenas de rutas. Zempoala–Pachuca
es esencialmente **una ruta con ramales**. Montar OpenTripPlanner + GTFS + Flutter para eso es usar
un martillo hidráulico para un clavo. Es la referencia correcta para el diseño y el modelo de datos,
probablemente no el fork correcto para empezar.

**[OneBusAway](https://github.com/OneBusAway)** (Open Transit Software Foundation) — apps Android
(Java/Kotlin), iOS (Swift, OBAKit), web en SvelteKit, backend histórico en Java/Spring migrando a Go.
Maduro y serio, pero diseñado para agencias de transporte formales con GTFS oficial. Demasiado
pesado para este caso; útil como referencia de UX de "próximas llegadas".

**[TheTransitClock](https://github.com/TheTransitClock/transitime)** — motor de predicción de
llegadas. Entra GTFS-RT de posiciones, sale GTFS-RT de TripUpdates. Java. Vale la pena estudiarlo,
probablemente no desplegarlo al inicio.

### 2.2 Precedentes en México y mapeo de rutas informales

**[MapMap](https://github.com/CodeandoMexico/mapmap)** (Codeando México / [Codeando Xalapa](https://github.com/codeandoxalapa/mapmap)) —
app Android para mapear rutas de transporte público y **generar GTFS**. Captura trazas
georreferenciadas sin consumir datos móviles, marca paradas y cuenta ascensos/descensos. Usada en
mapatones en Veracruz, Michoacán, BCS, y también en Ecuador, Colombia y República Dominicana.
Es la herramienta directa para levantar el dato base de la ruta Zempoala–Pachuca.

**[Hub de Datos de Transporte Público en México](https://hdtp.codeandomexico.org/)** — datos abiertos
y recursos sobre digitalización del transporte en México. Primer lugar donde buscar si ya existe
algo de Hidalgo.

**[Mapatón CDMX](https://nextcity.org/urbanist-news/big-data-mexico-city-mapathon-gamifies-crowdsourcing)**
(Laboratorio para la Ciudad, 2016) — mapeo colaborativo gamificado de la red de peseros: 3,594
participantes, 51,308 km de rutas, ~685,188 minutos de rastreo GPS. Resultado publicado como GTFS
abierto e integrado a Google Maps. **Lección incómoda:** el laboratorio fue desmantelado en 2018 al
cambiar la administración. Los proyectos que dependen de una institución mueren con ella; los que
dependen de los propios operadores, no.

**[Digital Matatus](https://www.digitalmatatus.com/)** (MIT + Columbia + Universidad de Nairobi) —
el precedente académico. Mapearon con celulares más de 3,000 paradas de matatus y las convirtieron a
GTFS, trabajando con la comunidad GTFS para **modificar el estándar** y que acomodara sistemas
semiformales. El [paper](https://www.sciencedirect.com/science/article/pii/S0966692315001878) es
lectura obligada: describe metodología de campo, no solo código.

**Pachuca / Hidalgo:** existe [rutas.pachuca.info](https://rutas.pachuca.info/), el
[Tuzobús](https://ruts.hidalgo.gob.mx/ver/7679) tiene mapa y app, y está el
[Sistema de Transporte Convencional de Hidalgo](https://stch.hidalgo.gob.mx/). No encontré GTFS
público de combis de Pachuca ni de Zempoala. **Probablemente el dato de esta ruta no existe en
ningún lado y habría que crearlo.** Eso es un activo, no un obstáculo.

### 2.3 Lado operativo (la fila, los turnos, la flotilla)

Aquí está el hueco. La parte que resuelve *tu* problema real es la que **no** existe como open source
maduro. Lo que hay:

- **[fleetMS](https://github.com/ppolle/fleetMS)** — sistema de gestión de flotilla para SACCOs de matatus.
- **[e-matatu-system](https://github.com/StephenKairu/e-matatu-system)** — sistema web para digitalizar operaciones de transportistas: rutas, viajes, horarios de salida, perfiles de tripulación.
- **[MatatuOS](https://matatuos.com/)** — comercial, no open source. Su planteamiento vale oro: *no fuerzan al transporte informal a un modelo rígido; parten de los flujos que ya existen (efectivo, M-Pesa, conductores, paraderos, coordinación por WhatsApp) y le montan encima una capa digital.* Esa es la actitud correcta para Zempoala.

**Conclusión sobre forkear:** no hay un proyecto para forkear que resuelva el núcleo. Sí hay piezas
excelentes para **reutilizar** (Traccar para GPS, GTFS/OTP para rutas, Trufi como referencia de UX).
El módulo de fila/turnos/relevos hay que escribirlo, y es chico.

---

## 3. Stack tecnológico

### 3.1 La decisión más importante: PWA, no app nativa

Para el arranque, una **aplicación web progresiva** (se abre en el navegador, se puede "instalar" en
la pantalla de inicio) gana sobre apps nativas:

- Sin tiendas de aplicaciones, sin revisiones, sin esperar aprobación para un fix.
- Se comparte con un link por WhatsApp. En un pueblo, la distribución *es* WhatsApp.
- Una sola base de código, actualizaciones instantáneas para todos.
- Funciona en Android de gama baja, que es el parque real.

Solo se necesita app nativa (o una nativa adicional, solo para choferes) cuando haga falta rastreo
GPS en segundo plano confiable. Ver §3.3.

Contexto de adopción: la [ENDUTIH 2025 del INEGI](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/endutih/ENDUTIH_25_RR.pdf)
reporta 86.1% de la población de 6+ años como usuaria de internet, 97.3% de esas personas se conectan
por smartphone, y en localidades rurales el uso de internet pasó de 68.5% a 75.2% en un año — el
mayor crecimiento anual en ocho años. El teléfono está; lo que no está tan extendido es el uso
transaccional (pagos en línea, banca), con brechas urbano-rural de ~21 puntos. **Implicación de
diseño: sí a la app, no a los pagos digitales en la versión 1.** El pasaje sigue siendo en efectivo.

### 3.2 Stack propuesto para la fase inicial

| Capa | Opción | Por qué |
|------|--------|---------|
| Frontend | React + Next.js (PWA) o SvelteKit | Un solo código, instalable, offline básico |
| Backend + DB | Supabase (Postgres + Realtime + Auth) | Realtime es el corazón del tablero de fila; ahorra escribir servidor |
| Auth | OTP por SMS o WhatsApp | Nadie aquí se registra con email y contraseña |
| Mapas | MapLibre GL + OpenStreetMap | Gratis y sin límites de cuota; Google Maps cobra por carga de mapa |
| Datos de ruta | GTFS con `frequencies.txt` | Estándar para servicio por frecuencia, no por horario fijo |
| Rastreo GPS (fase 2) | [Traccar](https://github.com/traccar/traccar) autohospedado | Ver §3.3 |
| Hosting | Vercel/Railway + Supabase, capas gratuitas | ~0–25 USD/mes al inicio |

**Sobre GTFS:** las combis no tienen horario, tienen frecuencia. El estándar ya contempla esto con
`frequencies.txt` y `exact_times=0`: viajes que no siguen horario fijo sino que mantienen un
*headway* (intervalo entre salidas). Es exactamente el modelo correcto. Advertencia documentada en
las [mejores prácticas de GTFS-RT](https://github.com/google/transit/blob/master/gtfs-realtime/best-practices/best-practices.md):
en servicio por frecuencia, las predicciones cerca del inicio de la ruta son poco confiables, y hay
que enviar `time` absoluto en lugar de `delay`. Modelar en GTFS desde el principio abre la puerta a
que un día esto aparezca en Google Maps sin rehacer nada.

### 3.3 Rastreo GPS: teléfono vs. dispositivo

Tu intuición es correcta: para saber dónde viene la combi hay que instalar algo. Tres caminos:

**Opción 1 — Teléfono del chofer con [Traccar Client](https://github.com/traccar/traccar-client)**
- Costo: **$0** de hardware. App open source que manda posición a *tu* servidor, sin anuncios ni terceros.
- [Traccar](https://www.traccar.org/) servidor: Java, open source, cualquier SQL, API REST, más de 200 protocolos y 2000+ modelos de dispositivos. Autohospedable. Geocercas, alertas, reportes ya incluidos.
- Ventaja estratégica enorme: **el mismo servidor sirve después para trackers dedicados**, sin cambiar la app del pasajero.
- Riesgos reales: el chofer olvida abrir la app; la batería; y sobre todo los fabricantes. MIUI (Xiaomi) mata servicios en segundo plano salvo que se activen "autostart" y excepción de batería; EMUI (Huawei) detiene un foreground service a los 5–10 min de apagar la pantalla si la app no está en "apps protegidas". Android 14+ endureció el acceso a ubicación en background.
- Mitigación: cargador en la combi (no opcional), `PRIORITY_BALANCED_POWER_ACCURACY` en vez de alta precisión (alta precisión sostenida consume ~7–12% de batería por hora), intervalos largos, y foreground service con notificación persistente solo durante el turno.

**Opción 2 — Rastreador dedicado en la unidad**
- Hardware: ~$500–$1,500 MXN por unidad (OBD o cableado) más SIM IoT.
- No depende del chofer ni de su teléfono. Se alimenta del vehículo.
- Habla protocolos que Traccar ya entiende → se conecta al mismo servidor.
- Esta es la opción correcta *después* de validar, no antes.

**Opción 3 — Servicio comercial de rastreo (LoJack, Navego, etc.)**
- En México los planes rondan **$200–$600 MXN mensuales por vehículo** para funciones básicas, y hasta $1,000+ para avanzadas. LoJack, por ejemplo, publica esquemas de ~$495 MXN/mes a 24 meses más instalación.
- Para una flotilla de N combis esto se vuelve el costo dominante del proyecto y el dato queda en manos de un tercero. **No recomendado** para este caso.

**Recomendación:** empezar con opción 1 en una sola unidad (la de tu papá) para medir qué tan bien
funciona en la vida real, y pasar a opción 2 solo si el piloto demuestra valor.

### 3.4 Una idea que evita el GPS por completo en la v1

Geocerca + evento manual. La checadora marca "combi 3 salió" con un botón. Eso es un dato de
altísima calidad (viene de la persona que ya hace ese trabajo) y alimenta el ETA de §1. El GPS se
vuelve un *upgrade* de precisión, no un requisito de lanzamiento. Reduce el riesgo del proyecto a
una fracción.

---

## 4. Lo que hunde estos proyectos (y no es el código)

Esto es más importante que cualquier decisión de stack.

**La checadora no es un problema a automatizar, es la aliada.**
Ella ya es la fuente de verdad del sistema. Si la app se presenta como "ya no necesitamos checadora",
el proyecto muere en una semana por resistencia. Si se presenta como "ya no le van a estar marcando
cada cinco minutos, usted marca en la pantalla y todos ven", se vuelve la principal promotora. Su
adopción es el único punto de falla verdaderamente crítico del producto (A).

**La ubicación de las combis es un dato políticamente cargado.**
Saber dónde está cada unidad habilita control, sanciones, comparación entre choferes y ventaja
competitiva entre rutas. Antes de escribir código hay que acordar explícitamente: ¿quién ve la
posición de quién? Propuesta razonable: el pasajero ve *la posición de la próxima combi*, sin nombre
de chofer; el dueño ve su unidad; nadie ve un historial de todos. Y solo durante el turno: rastreo
24/7 del teléfono personal de un chofer es inaceptable y además ilegalmente incómodo bajo la LFPDPPP.

**Las estrellas a choferes son la función más peligrosa del producto.**
En Uber funcionan porque hay miles de conductores anónimos. En un pueblo donde todos se conocen y son
compadres, una calificación pública de 3 estrellas es un conflicto personal, no un dato. Sugerencia:
en la v1, feedback privado que solo ve el dueño de la unidad, y reportes de estado del vehículo
(llanta, frenos, limpieza) que son objetivos y no señalan a una persona. Las estrellas públicas,
si acaso, mucho después y con acuerdo del gremio.

**Se compite contra un grupo de WhatsApp.**
Muy probablemente ya existe uno. Si escribir "ya me formé" en la app no es más rápido que escribirlo
en WhatsApp, la app pierde. El listón de UX para el chofer es: **un tap, menos de 3 segundos, sin
teclado, funcionando con señal mala.** Considerar además que la app *mande* a WhatsApp en vez de
pretender reemplazarlo.

**La concesión y la organización de la ruta.**
El transporte en Hidalgo opera por concesiones y organizaciones/sindicatos. Un sistema que hace
visible el orden de turnos toca intereses. Vale más tener el permiso informal de quien manda en la
ruta antes de la primera línea de código que después del lanzamiento.

**Masa crítica en dos lados.**
La bolsa de choferes (D) solo sirve si hay choferes esperando *y* dueños buscando. Con una ruta sola
no hay volumen. Esta función tiene sentido cuando ya estén varias unidades adentro, y arranca mejor
como un directorio verificado (licencia cargada y validada, referencias) que como un marketplace con
asignación automática.

---

## 5. Respuestas directas a tus preguntas

**¿Es posible?** Sí, y además es de los casos donde la tecnología es la parte fácil. El producto
mínimo que resuelve el dolor de tu papá es pequeño: una pantalla con la lista de turnos del día, un
botón "ya me formé" para el chofer, y la vista de la checadora. Eso es cuestión de semanas, no de
meses, y no necesita GPS, ni hardware, ni tiendas de apps.

**¿Hay algo que forkear?** No para el núcleo. Sí para las piezas: **Traccar** te ahorra escribir toda
la infraestructura de GPS; **Trufi Core** es la mejor referencia de producto para transporte informal
y es forkeable si algún día quieres la experiencia completa de pasajero (ojo con GPL-3);
**MapMap** es la herramienta mexicana para levantar el dato de la ruta.

**¿Qué stack?** PWA con React/Next.js + Supabase (Postgres + Realtime) + MapLibre/OSM para empezar;
Traccar autohospedado cuando entre el GPS; GTFS con `frequencies.txt` como modelo de datos de ruta
desde el día 1.

**¿Qué instalar en las combis?** Nada al principio. Después, la app Traccar Client en el teléfono del
chofer con cargador en la unidad ($0). Rastreador dedicado (~$500–1,500 MXN únicos) solo si el piloto
lo justifica. Evitar los servicios mensuales de $200–600 MXN por unidad.

**¿Por dónde empezar?** Por ir al paradero una semana con un cuaderno antes de programar: cuántas
unidades hay, cómo se decide el orden, cuántos minutos tarda el recorrido a cada punto por hora del
día, qué pasa cuando falta una unidad, y qué le pediría la checadora a una herramienta. Ese cuaderno
vale más que cualquier framework.

---

## 6. Fuentes

- [Trufi Core (GitHub)](https://github.com/trufi-association/trufi-core) · [Trufi Association](https://www.trufi-association.org/) · [Trufi in Your City](https://www.trufi-association.org/projects/trufi-in-your-city/) · [Trufi App Goes Open Source](https://www.trufi-association.org/trufi-app-goes-open-source/)
- [OneBusAway (GitHub)](https://github.com/OneBusAway) · [Open Transit Software Foundation](https://opentransitsoftwarefoundation.org/onebusaway)
- [TheTransitClock](https://thetransitclock.github.io/) · [transitime (GitHub)](https://github.com/TheTransitClock/transitime)
- [Traccar](https://www.traccar.org/) · [traccar/traccar](https://github.com/traccar/traccar) · [traccar/traccar-client](https://github.com/traccar/traccar-client)
- [MapMap — Codeando México](https://github.com/CodeandoMexico/mapmap) · [MapMap — Codeando Xalapa](https://github.com/codeandoxalapa/mapmap)
- [Hub de Datos de Transporte Público en México](https://hdtp.codeandomexico.org/)
- [Digital Matatus](https://www.digitalmatatus.com/) · [Paper: The digital matatu project](https://www.sciencedirect.com/science/article/pii/S0966692315001878) · [MIT News](https://news.mit.edu/2015/digital-matatus-project-makes-invisible-visible-0826)
- [Mapatón CDMX — Next City](https://nextcity.org/urbanist-news/big-data-mexico-city-mapathon-gamifies-crowdsourcing) · [Fast Company](https://www.fastcompany.com/3058475/mapping-mexico-citys-vast-informal-transit-system)
- [fleetMS](https://github.com/ppolle/fleetMS) · [e-matatu-system](https://github.com/StephenKairu/e-matatu-system) · [MatatuOS](https://matatuos.com/)
- [GTFS Reference](https://github.com/google/transit/blob/master/gtfs/spec/en/reference.md) · [GTFS-Realtime Best Practices](https://github.com/google/transit/blob/master/gtfs-realtime/best-practices/best-practices.md) · [Frequency-based service](https://e-lo.github.io/GTFS_Realtime_Best-Practices/Frequency-based/)
- [awesome-transit (MobilityData)](https://github.com/MobilityData/awesome-transit)
- [Android: optimizar el uso de ubicación](https://developer.android.com/develop/sensors-and-location/location/battery/scenarios) · [Ubicación y batería](https://developer.android.com/develop/sensors-and-location/location/battery)
- [INEGI — ENDUTIH 2025 (resultados)](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/endutih/ENDUTIH_25_RR.pdf) · [Análisis The CIU](https://www.theciu.com/publicaciones-2/2026/6/29/endutih-2025-nuevas-brechas-de-conectividad)
- [Costos de rastreo GPS en México — Obit](https://rastreador-gps.obit.com.mx/blog/gps-para-autos-mexico-como-funciona-cuanto-cuesta/) · [ZeekGPS](https://zeekgps.com/cuanto-cuesta-un-servicio-de-rastreo-satelital-en-mexico/) · [LoJack México](https://lojack.com.mx/)
- [Tuzobús — Gobierno de Hidalgo](https://ruts.hidalgo.gob.mx/ver/7679) · [Sistema de Transporte Convencional de Hidalgo](https://stch.hidalgo.gob.mx/) · [Rutas Pachuca](https://rutas.pachuca.info/)
