# Inflación personal en México: qué publica INEGI del INPC a nivel genérico, cómo obtenerlo de forma programática y cómo calcular un índice personal re-ponderado

Notas de investigación al 2026-10-26. "Verificado (curl)" significa que el endpoint se probó desde este entorno ese día. Las cifras de 2026 vienen de boletines de INEGI y de descargas hechas ese mismo día.

---

## 1. Estructura vigente del INPC en 2026: base, genéricos, jerarquías, ciudades y calendario

### Takeaway
A octubre de 2026 el INPC conserva la **base 2ª quincena de julio de 2018 = 100**. No hubo cambio de base. Desde la 1ª quincena de agosto de 2024 se calcula con la **"Actualización de Canasta y Ponderadores 2024"**: **292 genéricos** (antes 299), ponderadores de la **ENIGH Estacional 2022** (actualizados vía precios relativos a la 2Q jul-2024), **CCIF 2018** y **índices encadenados**. Se cotiza en **55 áreas geográficas** y se publica quincenal y mensualmente. El boletín de la 1Q de octubre de 2026 sigue citando la ENIGH Estacional 2022, así que todavía no hay una actualización con la ENIGH 2024.

### Cited Findings
- La base sigue en la 2Q de julio de 2018 = 100. La actualización 2024 renovó la canasta y los ponderadores con la ENIGH Estacional 2022 "manteniendo 2018 como el año base". El índice actualizado se publica desde la 1Q de agosto de 2024. — [Banxico, Recuadro 4, Informe Trimestral abr-jun 2024](https://www.banxico.org.mx/publicaciones-y-prensa/informes-trimestrales/recuadros/%7BB2DB3F5A-4FA5-E527-3A74-5B3998702397%7D.pdf)
- Cambio de canasta: 259 genéricos se quedan igual, 20 genéricos de 2018 se desagregan en 24 y otros 20 se fusionan en 9. Se pasa de 299 a 292. — [Banxico, Recuadro 4](https://www.banxico.org.mx/publicaciones-y-prensa/informes-trimestrales/recuadros/%7BB2DB3F5A-4FA5-E527-3A74-5B3998702397%7D.pdf); [INEGI, presentación "INPC Actualización 2024", 22-ago-2024](https://en.www.inegi.org.mx/contenidos/programas/inpc/2018a/doc/present_resul_2024.pdf)
- Comparativo 2018 vs 2024 (INEGI):

  | | 2018 | 2024 |
  |---|---|---|
  | Periodo de referencia de precios y ponderadores | 2Q jul 2018 | 2Q jul 2024 |
  | Genéricos | 299 | 292 |
  | Clasificación principal | CCIF 1999 | CCIF 2018 |
  | Fuente de ponderadores | ENGASTO 2012-2013 + ENIGH 2014 | ENIGH 2022 (12 meses) |
  | Representatividad de ponderadores | nacional | nacional |
  | Productos cotizados | 120,454 | 123,485 |
  | Cotizaciones mensuales | ≈319 mil | ≈341 mil |
  | Áreas geográficas | 55 | 55 |

  — [INEGI, presentación Actualización 2024](https://en.www.inegi.org.mx/contenidos/programas/inpc/2018a/doc/present_resul_2024.pdf)
- Para entrar a la canasta, un genérico debe pesar ≥0.01% del gasto nacional. Los genéricos que bajan de ese umbral no dejan de cotizarse: sus productos específicos se agrupan dentro de otros genéricos. — [INEGI, presentación Actualización 2024](https://en.www.inegi.org.mx/contenidos/programas/inpc/2018a/doc/present_resul_2024.pdf)
- Historia del número de genéricos: 172 (1978), 302 (1980), 313 (1994), 315 (2002), 283 (2010 y 2013), 299 (2018), 292 (2024). Ciudades: 16, 35, 46, 46, 46, 46, 55, 55. — [INEGI, presentación Actualización 2024](https://en.www.inegi.org.mx/contenidos/programas/inpc/2018a/doc/present_resul_2024.pdf)
- Ponderadores por componente (Cuadro 20, actualizados vía precios relativos a la 2Q jul-2024; entre paréntesis, 2018):
  - Subyacente 76.74 (75.55)
    - Mercancías 37.53
      - Alimentos, bebidas y tabaco 17.21
      - Mercancías no alimenticias 20.32
    - Servicios 39.21
      - Vivienda 18.05
      - Educación (colegiaturas) 2.52
      - Otros servicios 18.64
  - No subyacente 23.26 (24.45)
    - Agropecuarios 10.66
      - Frutas y verduras 4.78
      - Pecuarios 5.88
    - Energéticos y tarifas autorizadas por el gobierno 12.60
      - Energéticos 8.05
      - Tarifas autorizadas por el gobierno 4.55

  — [INEGI, Documento metodológico INPC 2024](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf). Banxico redondea "Otros servicios" a 18.63. — [Banxico, Recuadro 4](https://www.banxico.org.mx/publicaciones-y-prensa/informes-trimestrales/recuadros/%7BB2DB3F5A-4FA5-E527-3A74-5B3998702397%7D.pdf)
- Ponderadores por las 13 divisiones CCIF 2018 (Cuadro 21):

  | División | Peso |
  |---|---|
  | 01 Alimentos y bebidas no alcohólicas | 22.04 |
  | 02 Bebidas alcohólicas y tabaco | 2.29 |
  | 03 Ropa y calzado | 4.26 |
  | 04 Vivienda, agua, electricidad y gas | 20.88 |
  | 05 Mobiliario, equipo doméstico y mantenimiento rutinario del hogar | 5.34 |
  | 06 Salud | 4.13 |
  | 07 Transporte | 13.48 |
  | 08 Información y comunicación | 4.74 |
  | 09 Recreación, deporte y cultura | 2.53 |
  | 10 Servicios educativos | 2.49 |
  | 11 Restaurantes y servicios de alojamiento | 11.55 |
  | 12 Seguros y servicios financieros | 0.24 |
  | 13 Cuidado personal, protección social y bienes diversos | 6.03 |

  — [INEGI, Documento metodológico INPC 2024](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- Ponderadores por los 8 grupos de Objeto del gasto (Cuadro 22): Alimentos, bebidas y tabaco 27.87; Ropa, calzado y accesorios 4.41; Vivienda 23.79; Muebles, aparatos y accesorios domésticos 4.96; Salud y cuidado personal 9.50; Transporte 13.72; Educación y esparcimiento 7.29; Otros servicios 8.46. — [INEGI, Documento metodológico INPC 2024](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- El INPC también se publica por SCIAN 2023 y por durabilidad. El XLSX oficial clasifica los 292 genéricos en 160 no duraderos, 48 semiduraderos, 25 duraderos y 59 servicios (conteo propio sobre el archivo). — [INEGI, presentación Actualización 2024](https://en.www.inegi.org.mx/contenidos/programas/inpc/2018a/doc/present_resul_2024.pdf); [XLSX "Ponderadores INPC segunda quincena de julio de 2024"](https://www.inegi.org.mx/rnm/index.php/catalog/1015/download/32034)
- Cálculo en dos etapas: (1) índices elementales por genérico y área geográfica con **Jevons** (media geométrica de relativos de precio); (2) índices superiores con **Laspeyres**. Hay 235 genéricos con muestreo probabilístico y 57 con muestreo no probabilístico. — [INEGI, Boletín 633/26, INPC 1Q oct-2026](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_1q2026_10.pdf)
- Publicación: en el DOF los días 10 y 25 de cada mes, o el día hábil anterior. INEGI lo difunde en su portal el día previo a las 8:00 h. La 1Q del mes sale el 25 de ese mes; el dato mensual y la 2Q, el 10 del mes siguiente. **Los datos publicados son definitivos y no se revisan.** — [INEGI, Documento metodológico INPC 2024](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf); [Boletín 633/26](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_1q2026_10.pdf)
- En 2026 INEGI publica boletines separados ("Boletín de indicador"):
  - Mensual de agosto 2026 (9-sep-2026, n.º 586/26): INPC 145.462, +0.20% mensual, 3.26% anual. Anuncia la "próxima publicación mensual: 8 de octubre de 2026". — [INEGI, Boletín 586/26](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_2q2026_09.pdf)
  - Quincenal 1Q oct-2026 (22-oct-2026, n.º 633/26): INPC 146.739, +0.41% quincenal, 3.62% anual; subyacente 3.78% anual. Anuncia la "próxima publicación quincenal: 24 de noviembre de 2026". — [INEGI, Boletín 633/26](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_1q2026_10.pdf)
- La ficha metodológica del boletín de octubre de 2026 describe alrededor de 123 mil productos específicos en 292 genéricos, ponderadores de la ENIGH Estacional 2022 y 55 áreas en las 32 entidades. — [INEGI, Boletín 633/26](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_1q2026_10.pdf)
- **Índice mensual = promedio simple de las dos quincenas** (verificado numéricamente): INPC 1Q sep-2026 = 146.010 y 2Q sep-2026 = 146.140 (serie quincenal SP8664 de Banxico). El promedio es 146.075, igual al INPC mensual de septiembre de 2026. — [Banxico SIE, cuadro CP155](https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=8&accion=consultarCuadro&idCuadro=CP155&locale=es); [INEGI, exportación CSV del INPC Nacional mensual](https://www.inegi.org.mx/app/indicesdeprecios/Estructura.aspx?idEstructura=112001700030)
- La componente subyacente "excluye bienes y servicios con alta volatilidad o cuyos precios no responden a condiciones de mercado". — [Boletín 633/26](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_1q2026_10.pdf)

### Inferences
- El "≈299 genéricos" de la pregunta corresponde a la canasta 2018 y ya está desactualizado. Hoy son 292, con códigos 001–292 de la canasta 2024.
- Que la base siga en 2Q jul-2018 = 100 es solo una convención de nivel. El periodo de referencia de precios y ponderadores es la 2Q jul-2024, y el sistema ya es un Laspeyres encadenado.
- Como no hay revisiones, el repo puede guardar en caché todo lo descargado. Basta con traer cada quincena el dato nuevo.

### Gaps
- No encontré un anuncio oficial con fecha para la siguiente actualización de canasta y ponderadores. La ENIGH 2024 se publicó en 2025, pero el boletín del 22-oct-2026 sigue citando la ENIGH Estacional 2022. Conviene revisar el calendario y la "consulta pública" de INEGI.

---

## 2. Dónde se publican los índices por genérico y los ponderadores oficiales; desagregación por ciudad, región y estrato

### Takeaway
INEGI publica los índices de los 292 genéricos (nacional, quincenal y mensual) y también **por cada una de las 55 ciudades**. Lo hace en su aplicación "Índices de Precios" (`/app/indicesdeprecios/`), que exporta a CSV, XLS, XML, HTML e **IQY** sin token. Los **ponderadores nacionales por genérico** están en un XLSX oficial y en los anexos del documento metodológico (C: CCIF; D: SCIAN; E: entidad; F: área geográfica). **No encontré publicada una matriz de ponderadores genérico × ciudad.** El único índice por ingreso que publica INEGI cubre 4 estratos de salario mínimo y llega solo al nivel de las 13 divisiones CCIF. Banxico SIE no tiene datos a nivel genérico.

### Cited Findings
- **Ponderadores oficiales por genérico (XLSX):** "Canasta del INPC y ponderadores actualizados a la segunda quincena de julio de 2024". El archivo se llama `Ponderadores INPC segunda quincena de julio de 2024.xlsx` (27 KB), tiene una hoja con la canasta CCIF 2018, la durabilidad y el ponderador, 292 genéricos y suma 100. Descarga directa verificada (curl, HTTP 200). — [INEGI RNM, catálogo 1015, materiales relacionados](https://www.inegi.org.mx/rnm/index.php/catalog/1015/related-materials); [descarga XLSX](https://www.inegi.org.mx/rnm/index.php/catalog/1015/download/32034)
- Los genéricos de mayor peso nacional según ese XLSX (%):

  | Genérico | Peso | Genérico | Peso |
  |---|---|---|---|
  | 139 Vivienda propia | 13.7742 | 014 Tortilla de maíz | 1.8672 |
  | 265 Loncherías, fondas, torterías y taquerías | 5.0479 | 022 Pollo | 1.7883 |
  | 214 Gasolina de bajo octanaje | 4.8245 | 018 Carne de res | 1.7028 |
  | 268 Restaurantes y similares | 2.8006 | 224 Colectivo | 1.5995 |
  | 138 Renta de vivienda | 2.7889 | 145 Gas doméstico LP | 1.4661 |
  | 206 Automóviles | 2.5590 | 235 Paquetes de internet, telefonía y TV de paga | 1.2347 |
  | 269 Otros alimentos cocinados | 2.1484 | 100 Refrescos envasados | 1.2335 |
  | 233 Servicio de telefonía móvil | 1.8964 | 260 Universidad | 1.1334 |
  | | | 144 Electricidad | 1.1235 |

  Otros pesos útiles: 237 Streaming de películas y música 0.1035; 227 Transporte aéreo 0.2776; 271 Seguro de automóvil 0.2378; 213 Gasolina de alto octanaje 0.5053. El mínimo es 165 Artículos y utensilios para el hogar, con 0.0104. — [XLSX oficial](https://www.inegi.org.mx/rnm/index.php/catalog/1015/download/32034)
- Los anexos del documento metodológico traen la canasta con ponderadores por CCIF (anexo C), SCIAN 2023 (anexo D), entidad federativa (anexo E) y área geográfica (anexo F). — [INEGI, Documento metodológico INPC 2024](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- El anexo F da el peso de cada área dentro del total nacional, no por genérico. Ejemplos: ZM Ciudad de México 22.4293; Guadalajara 6.4169; Monterrey 5.4385; Tijuana 2.3328; Mexicali 1.9436; Morelia 1.8868; Mérida 1.8707; **Pachuca 1.6621**; Tulancingo 0.3036. — [INEGI, Documento metodológico INPC 2024, anexo F](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- Internamente INEGI usa ponderadores por ciudad-genérico para pasar de los índices de ciudad al índice nacional del genérico. Esos ponderadores salen de la ENIGH Estacional 2022 actualizada vía precios relativos. Las fórmulas de la sección 9.2 usan ω_lk, el ponderador del genérico k en el área l. — [INEGI, Documento metodológico INPC 2024](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- La ENIGH Estacional 2022 alcanzó "buena representatividad estadística" a nivel nacional, por entidad federativa y por genérico nacional. No se menciona representatividad genérico × ciudad. — [INEGI, Documento metodológico INPC 2024, §3.2.5](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- Índices publicados (Figura 4 del documento): nacional; 55 áreas geográficas; entidad federativa; región; tamaño de localidad; CCIF 2018; Objeto del gasto; componentes subyacente/no subyacente; SCIAN 2023; Canasta Básica; Canasta de Consumo Mínimo; **por estratos de gasto**. — [INEGI, Documento metodológico INPC 2024, §10](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- Estructuras de la app "Índices de Precios" (títulos verificados con curl contra `ObtieneTituloAgrupador`):

  | idEstructura | Contenido |
  |---|---|
  | 112001700030 | INPC Nacional (mensual), por objeto del gasto: 573 series, de ellas **292 genéricos** |
  | 112001600030 | INPC Nacional quincenal: 292 genéricos, último dato 1Q oct-2026 |
  | 112001700060 | "Por ciudad": 55 ciudades × 292 genéricos = 16,060 series de genérico |
  | 112001700040 | Por región |
  | 112001700050 | Según tamaño de la localidad |
  | 112001700070 | Por entidad federativa |
  | 112001700080 | CCIF 2018 mensual |
  | 112001700090 | CCIF 2018 por estrato de gasto |
  | 112001700100 | Otros tabulados (canasta básica) |

  — [INEGI Índices de Precios, INPC Nacional mensual](https://www.inegi.org.mx/app/indicesdeprecios/Estructura.aspx?idEstructura=112001700030&T=%C3%8Dndices+de+Precios+al+Consumidor&ST=INPC+Nacional+%28mensual%29); [servicio ArbolAjaxInteraccion.asmx](https://www.inegi.org.mx/app/indicesdeprecios/servicios/ArbolAjaxInteraccion.asmx)
- **Índices por estrato de ingreso:** la estructura 112001700090 tiene 56 series: 4 estratos × (índice general + 13 divisiones CCIF). Los estratos son "Hasta un salario mínimo" (id 909188), "Entre 1 y 3 salarios mínimos" (909202), "Entre 3 y 6 salarios mínimos" (909216) y "Superior a 6 salarios mínimos" (909230). No hay genéricos por estrato. Verificado (curl). — [INEGI Índices de Precios](https://www.inegi.org.mx/app/indicesdeprecios/servicios/ArbolAjaxInteraccion.asmx)
- Ejemplos de ids internos de la app:
  - Nacional mensual: Índice general 865586; 014 Tortilla de maíz 865594; 292 Servicios profesionales 866044.
  - Nacional quincenal: Índice general 821908; Tortilla de maíz 821916.
  - Pachuca, Hgo.: Índice general 886350; Tortilla de maíz 886358; 138 Renta 886562; 139 Vivienda propia 886564; 144 Electricidad 886570; 214 Gasolina de bajo octanaje 886711; 233 Telefonía móvil 886578; 237 Streaming 886751; 260 Universidad 886732; 265 Loncherías 886773.

  Verificado (curl). — [INEGI Índices de Precios](https://www.inegi.org.mx/app/indicesdeprecios/servicios/ArbolAjaxInteraccion.asmx)
- Las exportaciones CSV incluyen un "Aviso" en los metadatos de cada serie: "Las desagregaciones del INPC solo tienen valor informativo." — [Exportación CSV de INEGI](https://www.inegi.org.mx/app/indicesdeprecios/Exportacion.aspx?INPtipoExporta=CSV)
- **Banxico SIE no tiene genéricos.** Su sección "Índices de Precios al Consumidor y UDIS" solo ofrece:
  - Principales índices: 18 series, mensual desde ene-1969 y quincenal desde 1Q ene-1988.
  - Inflación: 9 series mensuales y 2 quincenales (estas desde 1Q ene-2022).
  - Otros indicadores de precios: 6 series de variación anual desde 2011.

  La propia sección aclara que desde el 15-jul-2011 INEGI tiene la facultad exclusiva de elaborar y publicar los índices nacionales de precios. — [Banxico SIE, directorio de precios](https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=8&accion=consultarDirectorioCuadros&locale=es)
- Series mensuales de Banxico (cuadro CP154):

  | Serie | Contenido | Serie | Contenido |
  |---|---|---|---|
  | SP1 | INPC | SP74630 | No subyacente |
  | SP74625 | Subyacente | SP56337 | Agropecuarios |
  | SP74626 | Mercancías | SP56385 | Frutas y verduras |
  | SP66540 | Alimentos, bebidas y tabaco | SP56386 | Pecuarios |
  | SP74627 | Mercancías no alimenticias | SP74631 | Energéticos y tarifas autorizadas por el gobierno |
  | SP74628 | Servicios | SP56373 | Energéticos |
  | SP66542 | Vivienda | SP74640 | Tarifas autorizadas por el gobierno |
  | SP56339 | Educación (colegiaturas) | | |
  | SP74629 | Otros servicios | | |

  El INPC quincenal es SP8664 (cuadro CP155). — [Banxico SIE CP154](https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=8&accion=consultarCuadro&idCuadro=CP154&locale=es); [CP155](https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=8&accion=consultarCuadro&idCuadro=CP155&locale=es)
- INEGI también publica el Índice de Precios de la Canasta de Consumo Mínimo (subconjunto de 170 genéricos tras las fusiones; antes 176), definido con Coneval. — [INEGI, Documento metodológico INPC 2024, §10.2](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf); [Boletín 633/26](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_1q2026_10.pdf)

### Inferences
- Para un usuario de un municipio de Hidalgo que no es área del INPC, la ciudad del INPC más cercana es **Pachuca**: es una de las 55 áreas y tiene sus 292 genéricos publicados. Tulancingo, también en Hidalgo, es otra área.
- Para re-ponderar con gasto propio, el ponderador oficial importa poco, porque uno pone su propio peso. Sí sirve como referencia ("mi canasta vs la del hogar promedio") y para verificar la agregación.
- La falta de una matriz ciudad × genérico pública impide reconstruir exactamente el INPC de Pachuca. Pero si se usan índices de Pachuca por genérico con pesos personales, esa matriz no hace falta.

### Gaps
- No encontré un archivo público con los ponderadores genérico × ciudad ni genérico × estrato. El documento menciona ponderaciones "ciudad-genérico-estrato (bajo, medio y alto)" para vivienda, pero solo como uso interno.
- No verifiqué si existen descargas masivas tipo "datos abiertos" (CSV completo de todas las ciudades) fuera de la app. La página del programa (`/programas/inpc/2018a/`) se arma con JavaScript y no se pudo leer.

---

## 3. Acceso programático: API de INEGI (BIE/BISE), API SIE de Banxico, IQY, exportación directa, librerías

### Takeaway
Hay tres vías:
1. **Sin token (la más práctica para genéricos y ciudades):** los endpoints de la app "Índices de Precios" (POST a `Exportacion.aspx` → CSV/XLS/XML, o `GeneraIQY.aspx` → archivo `.iqy`). Es la misma tecnología de "consulta web" en Excel que usa Banxico. Funciona a la fecha (verificado), pero **no está documentada como API**.
2. **API de Indicadores de INEGI** (v2.0, token gratuito, JSON/XML/JSONP, también SDMX/PC-Axis/JSON-stat). La documentación de ejemplo usa la fuente **BISE**. No pude confirmar sin token los ids BIE de los genéricos.
3. **API SIE de Banxico** (token, límites documentados). Solo sirve para los agregados del INPC.

### Cited Findings
- **INEGI API, formato:** `https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{id}/{idioma}/{área}/{reciente true|false}/{fuente}/2.0/{token}?type=json|jsonp|xml`.
  - Área: 00 nacional, 99 entidad, 999 municipio. "Reciente" true devuelve solo el último dato.
  - Catálogos: CL_INDICATOR, CL_UNIT, CL_NOTE, CL_SOURCE, CL_TOPIC, CL_FREQ, CL_GEO_AREA.
  - Hay un "Constructor de consultas", y salidas SDMX, PC-Axis y JSON-stat.
  - "Para utilizar la API es necesario mandarle un token válido, el cual puede obtener al registrarse."
  - Los ejemplos usan `.../BISE/2.0/...`, p. ej. el indicador 1002000001.

  — [INEGI, API del Banco de Indicadores](https://www.inegi.org.mx/servicios/api_indicadores.html)
- **Prueba sin token (curl, 2026-10-26):**
  - `INDICATOR/628194/es/0700/false/BIE/2.0/<token-falso>` → HTTP 400 `["ErrorInfo:No se encontraron resultados","ErrorDetails:No se encontraron resultados","ErrorCode:100"]`. Pasa igual con área `00` y con fuente `BIE-BISE`.
  - `CL_INDICATOR/628194/es/BIE/2.0/<token-falso>` → `["ErrorInfo:No autorizado","ErrorDetails:No autorizado","ErrorCode:110"]`.
  - Sin el segmento de token → HTTP 404 en HTML.

  Es decir, sin token el endpoint de datos devuelve "sin resultados" en lugar de un error claro de autenticación. — [Endpoint API INEGI](https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/628194/es/0700/false/BIE/2.0/00000000-0000-0000-0000-000000000000?type=json)
- La página de la API no documenta límites de consultas (no los encontré en el texto). — [INEGI, API del Banco de Indicadores](https://www.inegi.org.mx/servicios/api_indicadores.html)
- **Exportación sin token desde la app de precios (verificada):**
  - `POST https://www.inegi.org.mx/app/indicesdeprecios/Exportacion.aspx?INPtipoExporta=CSV` con los campos del formulario `INPExporta`.
  - Campos: `idEstructura`, `cuadro` y `cvEstructura` (p. ej. 112001700030); `_formato=CSV`; `_anioI` y `_anioF` (años); `_meta=0|1`; `_tipo` (`Niveles`, `Mensual`, `Acumulada` o `Anual`); `_info`; `_orient=vertical`; `pf=inp`; `st`; `esquema=`; `_series=c|<id1>,<id2>,...,`.
  - Devuelve `text/csv; charset=Windows-1252` con cabeceras de metadatos (título, periodo disponible, periodicidad, base, aviso) y una fila por periodo.
  - Valores faltantes: "NA" (antes del inicio de la serie, p. ej. genéricos nuevos de 2024) y "N/E".
  - Se exportaron las **293 series (general + 292 genéricos) en una sola petición** (≈157–239 KB).
  - Valores confirmados: INPC sep-2026 = 146.075; Tortilla de maíz (nacional) sep-2026 = 163.374; Botanas elaboradas con cereales = 186.169.

  — [INEGI Índices de Precios, Exportacion.aspx](https://www.inegi.org.mx/app/indicesdeprecios/Exportacion.aspx?INPtipoExporta=CSV); campos tomados de [ExportacionAjaxInteraccion.min.js](https://www.inegi.org.mx/app/indicesdeprecios/scripts/ExportacionAjaxInteraccion.min.js)
- **IQY:** la app sigue ofreciendo exportar en CSV, HTML, IQY, XLS y XML. `GeneraIQY.aspx` devuelve un archivo `text/x-ms-iqy` (p. ej. `INP_c20261026091128.IQY`) que apunta a `https://www.inegi.org.mx/app/indicesdepreciosv2/Exportacion.aspx`. Los parámetros POST incluyen `_series=c|865594,...&_formato=IQY&_anioI=["añoInicial","Año inicial"]...`, es decir, Excel le pide al usuario el año inicial y final. Verificado (curl). Así funcionan las hojas de Banxico "conectadas a INEGI vía .IQY". — [INEGI Índices de Precios, GeneraIQY.aspx](https://www.inegi.org.mx/app/indicesdeprecios/GeneraIQY.aspx)
- **Árbol de series (ids) sin token:**
  - `POST https://www.inegi.org.mx/app/indicesdeprecios/servicios/ArbolAjaxInteraccion.asmx/ObtieneNodos` con JSON `{"idNodo":"112001700030","tituloPrincipal":"","subTitulo":"","esquemaBD":"","paramfuente":"","paramEstructura":"112001700030","notas":[]}`.
  - Devuelve HTML dentro de `{"d": ...}`; cada serie aparece como `ShowMoreInformation('<idSerie>','<claveJerárquica>','<título>')`.
  - Otros métodos: `EncabezadoPeriodos`, `ObtieneTituloAgrupador`, `InformationMetadatosSerie`.
  - La estructura "Por ciudad" pesa ≈63 MB y tardó más de 120 s.

  Verificado (curl). — [ArbolAjaxInteraccion.asmx](https://www.inegi.org.mx/app/indicesdeprecios/servicios/ArbolAjaxInteraccion.asmx)
- **API SIE de Banxico:**
  - Token de 64 caracteres, que se solicita en `/SieAPIRest/service/v1/token`. Se envía en el encabezado `Bmx-Token` o como parámetro `token`.
  - Endpoints: `GET /series/{idSerie}/datos/oportuno`, `/series/{id}/datos`, `/series/{id}/datos/{fechaIni}/{fechaFin}` y metadatos.
  - Formatos JSON, JSONP y XML; acepta gzip.

  — [Banxico, SIE API REST](https://www.banxico.org.mx/SieAPIRest/service/v1/)
- **Límites SIE:**

  | Tipo de consulta | Endpoints | Por ventana | Por día |
  |---|---|---|---|
  | Oportuna y metadatos | `series`, `series/:id`, `datos/oportuno` | 80 en 1 minuto | 40,000 |
  | Histórica | `datos`, rango de fechas | 200 en 5 minutos | 10,000 |

  Si se excede la ventana, el token se bloquea hasta que termine. Si se excede el límite diario, se bloquea hasta el fin del día natural (hora CDMX). — [Banxico, límites de consultas SIE](https://www.banxico.org.mx/SieAPIRest/service/v1/doc/limiteConsultas)
- Prueba SIE sin token: `GET /SieAPIRest/service/v1/series/SP1/datos/oportuno` → HTTP 400 `{"error":{"mensaje":"Token inválido",...}}`. Verificado (curl). — [Banxico SIE API](https://www.banxico.org.mx/SieAPIRest/service/v1/series/SP1/datos/oportuno)
- **Librerías (estado en PyPI y CRAN al 2026-10-26):**

  | Paquete | Versión y fecha | Notas |
  |---|---|---|
  | `INEGIpy` | 2.0.0 (2026-02-12) | Clases para Banco de Indicadores, DENUE, Marco Geoestadístico y Ruteo; módulo "Series" (PIB, INPC…) "en construcción" |
  | `pyinegi` | 0.1.0 (2026-08-31) | Cliente tipado de la API de Indicadores; token en `INEGI_TOKEN` |
  | `sie-banxico` | 0.0.1 (subida 2022-01-02) | Wrapper de la API SIE |
  | `mxinflation` | — | No existe en PyPI (404) |
  | `inegiR` (R) | — | **Retirado de CRAN, archivado el 2026-06-01** |
  | `siebanxicor` (R) | 1.0.0 (2018-10-30) | En CRAN |
  | `banxicoR` (R) | 0.9.0 (2016-08-17) | En CRAN |

  — [PyPI INEGIpy](https://pypi.org/project/INEGIpy/); [PyPI pyinegi](https://pypi.org/project/pyinegi/); [PyPI sie-banxico](https://pypi.org/project/sie-banxico/); [CRAN inegiR](https://cran.r-project.org/package=inegiR); [CRAN siebanxicor](https://cran.r-project.org/package=siebanxicor); [CRAN banxicoR](https://cran.r-project.org/package=banxicoR)
- El config JS de los componentes BIINEGI (versión 1.2.2) dice: "20.01.2025 SNM Configuración solo a API indicadores V1_3". Es una API interna distinta de la pública v2.0. — [INEGI, config.min.js](https://www.inegi.org.mx/componentes/biinegi/config.min.js?1.0.7)

### Inferences
- Para el repo, la ruta más robusta para genéricos y ciudades es el POST a `Exportacion.aspx`: no pide token, trae las 292 series en una sola petición y su id está atado a la estructura de la app. El riesgo es que no está documentada y puede cambiar (ya existe un `indicesdepreciosv2`). Conviene: (a) guardar en caché los CSV versionados en el repo, ya que los datos no se revisan; (b) validar cada corrida reconstruyendo el INPC nacional (ver §4); (c) tener la API oficial con token como respaldo cuando se mapeen los ids BIE.
- No hace falta reproducir el IQY en Python. El IQY solo hace un POST con los mismos parámetros que la exportación CSV.
- Para los agregados oficiales (general, subyacente, etc.) y validaciones, SP1 y SP8664 del SIE o la propia exportación de INEGI bastan. Por los límites (10,000 consultas históricas al día), el SIE no es cuello de botella.

### Gaps
- No pude confirmar sin token los ids del BIE/BISE de la API pública para los 292 genéricos, ni si coinciden con los ids internos de la app (p. ej. 865594). Hace falta un token y el "Constructor de consultas".
- No verifiqué que 628194 sea el INPC general en el BIE de la API. Con token falso responde "sin resultados", sin distinguir.
- No encontré documentación oficial sobre límites de la API de INEGI ni sobre la vigencia de los endpoints IQY y Exportación.

---

## 4. Matemática correcta: Laspeyres encadenado, re-ponderación, inflación mensual y anual, e incidencias

### Takeaway
El INPC es un **Laspeyres (tipo Lowe/Young) en dos etapas**: Jevons dentro del genérico y aritmética ponderada arriba. Los ponderadores son de gasto, actualizados por precios al periodo de referencia (2Q jul-2024), y hay **un eslabón de encadenamiento en la 2Q jul-2024**. Después del eslabón, las series publicadas **ya no son aditivas**. Para agregar, primero se re-referencia cada índice a la 2Q jul-2024 = 100 (θ_j = 100 / I_j^{2Q jul-24}), luego se promedia con los pesos y al final se multiplica por el factor de encadenamiento. Con este procedimiento **reproduje exactamente el INPC publicado** a partir de los 292 genéricos y el XLSX oficial.

### Cited Findings
- **Laspeyres:** P_L^{0:t} = Σ_i p_i^t q_i^0 / Σ_i p_i^0 q_i^0 = Σ_i (p_i^t / p_i^0) ω_i^0, con ω_i^0 = p_i^0 q_i^0 / Σ p^0 q^0. El CFF, art. 20-Bis, obliga a usar Laspeyres. — [INEGI, Documento metodológico INPC 2024, §3.2.1](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- INEGI explica que Laspeyres supone preferencias "Leontief": no hay sustitución entre genéricos y las elasticidades cruzadas son nulas. — [INEGI, Documento metodológico INPC 2024](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- **Agregación superior:** I_INS^t = Σ_k ω_k I_k^t con Σ ω_k = 1, donde I_k es el índice del genérico con base 2Q jul-2024 y ω_k el ponderador fijo "de acuerdo con la estructura de gasto en la 2ª quincena de julio de 2024". El INPC promedia 235 genéricos probabilísticos y 57 no probabilísticos. — [INEGI, Documento metodológico INPC 2024, §9.2–9.3](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- **Actualización de ponderadores por precios relativos:**
  - Factor por genérico y área: F_lk = I_lk^t / I_lk^{t−1}.
  - Gasto actualizado: GA_lkh = G_lkh · F_lk.
  - Así se lleva el gasto de 2022 (periodo de referencia de las ponderaciones) a la 2Q jul-2024 (periodo de referencia de los precios).

  — [INEGI, Documento metodológico INPC 2024, §5.3](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- **Encadenamiento:**
  - Factor: f_h = I_{h,ENGASTO12}^{2QJul2024} / 100, que se fija una sola vez en el traslape.
  - Índice publicado: I_{h,E}^t = f_h · I_{h,ENIGH E22}^t.
  - "El encadenamiento le quita a la serie su característica aditiva."
  - Procedimiento oficial para recalcular agregados: (I) θ_j = 1/f_h = 100 / I_j^{2QJul24}; (II) multiplicar cada índice publicado por θ_j; (III) agregar con los pesos vigentes; (IV) multiplicar por f_h.

  — [INEGI, Documento metodológico INPC 2024, pp. 59-61](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf); [Banxico, Recuadro 4](https://www.banxico.org.mx/publicaciones-y-prensa/informes-trimestrales/recuadros/%7BB2DB3F5A-4FA5-E527-3A74-5B3998702397%7D.pdf)
- El ejemplo numérico del documento metodológico no cuadra con los datos publicados. El documento usa INPC ago-2024 = 134.471, f = 1.34065 y pesos 0.7718/0.2282. Lo publicado por INEGI es INPC ago-2024 = **136.013** y INPC 2Q jul-2024 = **136.095**, y el Cuadro 20 da 76.74/23.26. Conclusión: el ejemplo es ilustrativo. — [INEGI, Documento metodológico INPC 2024](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf); valores publicados vía [exportación CSV de INEGI](https://www.inegi.org.mx/app/indicesdeprecios/Estructura.aspx?idEstructura=112001700030)
- **Reconstrucción propia (verificada el 2026-10-26):**
  - Insumos: los 292 genéricos nacionales mensuales (estructura 112001700030), su valor quincenal de la 2Q jul-2024 (estructura 112001600030) y los pesos del [XLSX oficial](https://www.inegi.org.mx/rnm/index.php/catalog/1015/download/32034).
  - Cálculo: INPC^t = (I_INPC^{2QJul24} / 100) · Σ_k (ω_k/100) · (I_k^t / I_k^{2QJul24}) · 100, con I_INPC^{2QJul24} = 136.095.

  | Mes | Reconstruido | Publicado |
  |---|---|---|
  | ago-2024 | 136.013 | 136.013 |
  | dic-2024 | 137.948 | 137.949 |
  | ago-2025 | 140.867 | 140.867 |
  | ago-2026 | 145.461 | 145.462 |
  | sep-2026 | 146.075 | 146.075 |

  El rebase se hace con el índice **quincenal** de la 2Q jul-2024, también para las series mensuales. Para jul-2024 y meses anteriores la fórmula no aplica: rigen los pesos viejos y 15 genéricos nuevos no tienen datos.
- **Incidencias:** INEGI las define como "la contribución, en puntos porcentuales, de cada componente del INPC a la inflación general… se calcula utilizando los ponderadores de cada subíndice, así como los precios relativos y sus respectivas variaciones". También advierte discrepancias por redondeo. — [INEGI, Boletín 633/26](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_1q2026_10.pdf)
- Estacionalidad de la ponderación: la ENIGH Estacional se levanta los cuatro trimestres del año, lo que capta mejor el gasto estacional. — [Banxico, Recuadro 4](https://www.banxico.org.mx/publicaciones-y-prensa/informes-trimestrales/recuadros/%7BB2DB3F5A-4FA5-E527-3A74-5B3998702397%7D.pdf)

### Inferences
Fórmulas recomendadas para el repo. Se derivan de la metodología citada y siguen la práctica estándar del Manual del IPC.

1. **Re-referenciar los genéricos al periodo base b del índice personal:** R_k^t = I_k^t / I_k^b. Para replicar a INEGI, b = 2Q jul-2024. Para un índice personal, b puede ser cualquier periodo, p. ej. dic-2025.
2. **Pesos personales.**
   - Con gasto e_k del periodo e (p. ej. 12 meses de movimientos bancarios), la participación es s_k^e = e_k / Σ e_j.
   - Si e ≠ b, conviene actualizarla por precios como hace INEGI ("ponderador tipo Lowe"): s_k^b ∝ s_k^e · (I_k^b / I_k^e), normalizado a 1.
   - Sin este paso, el índice queda "tipo Young", con pesos de gasto en lugar de pesos de cantidad.
3. **Índice personal** (Laspeyres/Lowe): P^t = 100 · Σ_k s_k^b · R_k^t.
   - Inflación mensual: π_m = P^t / P^{t−1} − 1.
   - Inflación anual: P^t / P^{t−12} − 1.
   - Para la quincena se usan las series quincenales, con quincena-1 o quincena-24 como comparación.
   - Mensual = promedio de las dos quincenas (verificado en §1). Para ser consistente con INEGI, conviene usar directamente las series mensuales publicadas.
4. **Ponderador efectivo e incidencia** dentro de un mismo eslabón:
   - ω_k^{ef}(t−s) = s_k^b · R_k^{t−s} / Σ_j s_j^b · R_j^{t−s}.
   - C_k(t−s→t) = ω_k^{ef}(t−s) · (R_k^t / R_k^{t−s} − 1) · 100 = 100 · s_k^b · (R_k^t − R_k^{t−s}) / Σ_j s_j^b · R_j^{t−s}.
   - Σ_k C_k reproduce exactamente π(t−s→t). Usar el ponderador base s_k en lugar del efectivo es el error típico: la suma ya no cuadra, sobre todo en genéricos que se desvían mucho, como frutas, verduras o electricidad.
5. **Cambio de pesos en el tiempo** (p. ej. actualización anual con el gasto bancario del año anterior):
   - Encadenar en un periodo de traslape L: P^t = P^L · Σ_k s_k^{(nuevo)} · (I_k^t / I_k^L).
   - Las incidencias que cruzan el eslabón se descomponen con (1+a)(1+b) − 1 = Σ C_k^a · (1+b) + Σ C_k^b, donde a es la inflación previa al eslabón (pesos viejos) y b la posterior (pesos nuevos).
   - Esta asignación del término cruzado es una convención. Hay otras, p. ej. Ribe/Eurostat.
6. **Validación automática:** con s_k = ω_k oficial y b = 2Q jul-2024, P^t × 1.36095 debe dar el INPC publicado con error de ±0.001.

### Gaps
- No encontré una nota de INEGI ni de Banxico que fije la fórmula exacta de incidencias con encadenamiento, en especial cómo reparten el término cruzado en las incidencias anuales que cruzan agosto de 2024. Las incidencias de INEGI son las de referencia, pero su convención para cruzar eslabones no está documentada en lo revisado.

---

## 5. Problemas metodológicos de un índice personal

### Takeaway
El cálculo es factible. Los riesgos principales están en el **mapeo gasto bancario → genérico** y en unos cuantos genéricos que pesan mucho y se comportan distinto: **vivienda propia** (renta imputada, 13.77%), **gasolina** (tope "voluntario" de la Magna), **electricidad** (subsidio de verano, distinto por ciudad), **colegiaturas** y genéricos estacionales. También influyen las muestras pequeñas por ciudad, que INEGI advierte "solo tienen valor informativo", las rupturas de canasta y lo que el INPC no cubre por diseño (impuestos, intereses, deuda).

### Cited Findings
- **Vivienda propia = renta imputada.** El genérico 139 Vivienda propia representa "el servicio de alojamiento que es consumido por el hogar". Su ponderación sale de la renta que el propio informante estima en la ENIGH, con corrección por sesgo. El índice se calcula con el **enfoque de renta equivalente**: las cotizaciones de viviendas rentadas sirven para ambos genéricos. Los precios son los mismos, pero los índices difieren porque se ponderan por ciudad-genérico-estrato (bajo, medio, alto). — [INEGI, Documento metodológico INPC 2024, §5.2.1 y §8.5](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- Peso de 139 Vivienda propia: 13.7742%, el mayor de la canasta. Peso de 138 Renta de vivienda: 2.7889%. — [XLSX oficial](https://www.inegi.org.mx/rnm/index.php/catalog/1015/download/32034)
- Muestra de renta: cada vivienda se visita una vez por semestre, con al menos 4 rentas reportadas por quincena y ciudad. La renta no incluye agua, luz ni mantenimiento. — [INEGI, Documento metodológico INPC 2024](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- **Exclusiones por diseño:**
  - De 850 conceptos de gasto de la ENIGH se usaron 773. Se excluyeron actividades ilícitas, impuestos y segundas residencias.
  - Tampoco entran transferencias a otros hogares, gastos no significativos, productos de precio difícil de determinar o declarados con poca veracidad, ni lo que no es gasto de consumo (contribuciones a la seguridad social, impuestos, pago de deudas).
  - Siete genéricos (cerveza, tequila, cigarrillos, etc.) se ajustaron por subdeclaración.

  — [INEGI, Documento metodológico INPC 2024, §3.2.5–3.2.6](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- La división 12 "Seguros y servicios financieros" pesa solo 0.24% del INPC. — [INEGI, Documento metodológico INPC 2024, Cuadro 21](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- En el XLSX oficial, esa división 12 tiene **un solo genérico**: 12 → 12.1 Seguros → 12.1.4 Seguros relacionados con el transporte → 271 Seguro de automóvil (0.2378). **No hay ningún genérico de servicios financieros** (comisiones, intereses). También existe 220 Trámites vehiculares (0.1430). — [XLSX oficial](https://www.inegi.org.mx/rnm/index.php/catalog/1015/download/32034)
- **Electricidad:** CFE es el único proveedor y aplica tarifas 1, 1A–1F según región, temporada (verano y fuera de verano) y rango de consumo (25 a 10 mil kWh). El índice se calcula con un modelo de tarifas ponderadas: cada mes se usan 1,161 precios promedio. — [INEGI, Documento metodológico INPC 2024](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- En la 1Q de octubre de 2026, la no subyacente subió 0.98% y "energéticos y tarifas" 1.85% quincenal, "en mayor medida, por la conclusión del subsidio al programa de tarifas eléctricas de temporada de verano en 18 ciudades del país". — [INEGI, Boletín 633/26](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_1q2026_10.pdf)
- La prensa reporta ajustes a la baja por temporada cálida en 11 ciudades en mayo de 2026. No es fuente primaria y no coincide con las "18 ciudades" del boletín de octubre; probablemente el programa arranca en fechas distintas según la ciudad. — [Luz Noticias, 29-may-2026](https://www.luznoticias.mx/2026-05-29/mexico/baja-tarifa-electrica-11-ciudades-de-mexico-tendran-recibos-de-luz-mas-baratos/290978)
- Electricidad en **Pachuca**, variación mensual 2026 (exportación INEGI, serie 886570): ene +1.01%, feb +0.16%, mar +2.25%, abr −1.96%, may +1.11%, jun −0.09%, jul +0.09%, ago −0.02%, sep +0.02%. — [INEGI, exportación CSV "Por ciudad"](https://www.inegi.org.mx/app/indicesdeprecios/Exportacion.aspx?INPtipoExporta=CSV)
- **Gasolina:** el gobierno federal y los gasolineros mantienen un acuerdo "voluntario" para vender la Magna por debajo de 24 pesos/litro. Según la prensa, se renovó para llegar a marzo de 2027, y Profeco reporta un promedio nacional de 23.68 pesos/l y ≈90% de las estaciones bajo el tope. Son notas de prensa, no el comunicado oficial. — [Tiempo.com.mx](https://www.tiempo.com.mx/nacional/mantendran-gasolina-magna-por-debajo-de-24-pesos-hasta-marzo-de-2027/); [UnoTV](https://www.unotv.com/negocios/anuncian-precio-maximo-de-gasolina-magna-para-2026-se-mantendra-en-24-pesos/)
- Gasolina de bajo octanaje pesa 4.8245% en el INPC. En Pachuca su variación mensual en 2026 estuvo entre −0.13% y +0.46% (serie 886711). — [XLSX oficial](https://www.inegi.org.mx/rnm/index.php/catalog/1015/download/32034); [exportación CSV de INEGI](https://www.inegi.org.mx/app/indicesdeprecios/Exportacion.aspx?INPtipoExporta=CSV)
- **Muestreo no probabilístico (57 genéricos)** para precios regulados, autorizados o de pocos oferentes: electricidad, telefonía móvil, agua, cuotas de autopista, Metro, expedición de documentos públicos. Pasaron a no probabilístico "Streaming de películas y música", "Consolas, discos y descargas de videojuegos" y reproductores de audio y video, que se cotizan en plataformas. — [INEGI, Documento metodológico INPC 2024](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- **Calidad y faltantes:**
  - El ajuste explícito es "costeo directo". El implícito es la "imputación de la media global", que también se usa para precios faltantes tras 3 a 5 revisitas.
  - Se sustituye el producto por otro de características similares. No se mencionan métodos hedónicos en la sección revisada.

  — [INEGI, Documento metodológico INPC 2024, §8.1–8.2](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- **Estacionales:** los alimentos estacionales (mango, guayaba, mandarina) se cotizan solo en temporada; fuera de ella se imputa la media global y no se "arrastran" precios. Ropa y calzado tienen surtidos por estación. — [INEGI, Documento metodológico INPC 2024, §8.4](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463918639.pdf)
- Ejemplo de estacionalidad fuerte en los datos: el genérico nacional 292 Servicios profesionales pasó de 157.400 (ago-2026) a 131.524 (sep-2026), y de 146.167 (ago-2025) a 123.693 (sep-2025). No investigué la causa. — [exportación CSV de INEGI](https://www.inegi.org.mx/app/indicesdeprecios/Exportacion.aspx?INPtipoExporta=CSV)
- **Colegiaturas:** en la 1Q de octubre de 2026 variaron 0.00% quincenal y 5.84% anual. Es decir, el ajuste se concentra en el inicio del ciclo escolar. — [Boletín 633/26](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_1q2026_10.pdf)
- **Rupturas de canasta en 2024:**
  - 15 genéricos nuevos inician series propias. Ejemplos con su peso: Paquetes para fiesta 0.69; Servicios de mantenimiento, reparación y seguridad de la vivienda 0.22; Streaming de películas y música 0.10; Toallas, cortinas y otros blancos 0.06; Complementos de vestir 0.05; Cilantro, epazote y perejil 0.03; Museos 0.03; Servicios recreativos y centros nocturnos 0.02; Bebidas energéticas 0.02.
  - Otros genéricos se fusionaron, p. ej. camarón + otros mariscos, o periódicos + revistas.

  — [INEGI, presentación Actualización 2024](https://en.www.inegi.org.mx/contenidos/programas/inpc/2018a/doc/present_resul_2024.pdf)
- En las exportaciones, los genéricos nuevos aparecen como "NA" antes de su inicio. Algunos genéricos de 2018 tienen series desde 1970 (Tortilla de maíz); otros desde 2002 (Servicios profesionales) o desde jul-2018 (Botanas). — [exportación CSV de INEGI](https://www.inegi.org.mx/app/indicesdeprecios/Exportacion.aspx?INPtipoExporta=CSV)
- **Cambios de patrón que motivaron la actualización:** más gasto en internet; streaming que sustituye a CD y DVD; compras en línea (Trivago, Expedia, Amazon); menor gasto relativo en gasolina por el home office; caída de colegiaturas privadas por la pandemia. Resultado: educación −30%, energéticos −19% y vivienda +16% en ponderación. — [INEGI, presentación Actualización 2024](https://en.www.inegi.org.mx/contenidos/programas/inpc/2018a/doc/present_resul_2024.pdf)
- **Heterogeneidad por hogar:** IMCO documenta con la ENIGH 2020 que los deciles bajos dedican más gasto a alimentos y enfrentan inflaciones distintas. Investigación Económica (UNAM, 2024) propone una metodología de inflación por hogar y decil; esta referencia la conozco solo por el resumen del buscador, no la leí completa. — [IMCO, "Inflación de los hogares en México", 2022](https://imco.org.mx/wp-content/uploads/2022/05/Inflación-de-los-hogares-en-México_IMCO_20220511-1.pdf); [Investigación Económica v84 n331](https://www.scielo.org.mx/pdf/ineco/v84n331/0185-1667-ineco-84-331-40.pdf)

### Inferences
- **Vivienda.**
  - Si el usuario es dueño, hay dos conceptos posibles. (a) "Consumo", como hace INEGI: incluir vivienda propia con un peso igual a su renta imputada estimada. (b) "Gasto efectivo" (out-of-pocket): excluirla, y excluir también la hipoteca, porque el pago de deuda y los intereses no están en el INPC.
  - Si renta, usar 138 Renta de vivienda con su renta real como peso.
  - En ningún caso hay que mapear el pago de hipoteca a vivienda propia: son conceptos distintos.
- **Mapeo bancario.** La categoría del comercio no equivale a un genérico. Un ticket de supermercado mezcla decenas de genéricos, y las compras en efectivo (tianguis, combis, fondas) no aparecen en el banco.
  - Opción práctica: repartir el gasto de supermercado con la estructura oficial dentro de la división o grupo (p. ej. los pesos CCIF 01.1 del XLSX). Para tortillería, gasolinera, CFE, telefonía o colegiatura, el mapeo es 1 a 1.
  - Para la combi, el genérico 224 Colectivo pesa 1.5995% nacional, y Pachuca tiene índice propio.
- **Ciudad vs nacional.** Para los bienes locales (vivienda, transporte local, electricidad, alimentos frescos, loncherías), conviene usar los índices de Pachuca. Para los bienes de precio casi nacional (automóviles, streaming, telefonía móvil, gasolina con tope), el índice nacional tiene menos ruido. Una regla mixta razonable: el índice de ciudad cuando el genérico es local y pesa en la canasta propia, y el nacional en otro caso. Hay que documentar la elección.
- **Ruido de muestra.** Los índices ciudad × genérico se basan en pocas cotizaciones y el muestreo de ponderadores no garantiza representatividad a ese nivel. Mostrar la inflación personal anual y, si se quiere, un promedio móvil de 3 meses, antes que la quincenal pura.
- **Sustitución.** Al ser un Laspeyres con pesos fijos, el índice personal sobreestima el costo de vida si el usuario sustituye, p. ej. pollo por res cuando la res sube. Actualizar los pesos cada año con el gasto bancario y encadenar (§4, punto 5) reduce el sesgo.
- **Fuera de la canasta o mal representado:** comisiones e intereses de tarjeta (no hay genéricos financieros), impuestos como predial o tenencia (sí existe 220 Trámites vehiculares, con 0.1430), seguros distintos al de auto (el único seguro es 271 Seguro de automóvil), gastos en el extranjero, suscripciones digitales más allá del streaming de video y música (software, apps, nube), y donativos.
  - Opciones: excluirlos del índice y reportarlos aparte como "gasto no cubierto", o asignarles el índice general o el subyacente como proxy.
  - Las colegiaturas privadas sí están: Universidad pesa 1.1334, más primaria, secundaria, etc. Pero el índice mide variaciones promedio, no el nivel ni la política de una escuela en particular. Si se conoce el aumento real de la propia colegiatura, conviene usar ese dato en lugar del índice.
- **Precios administrados.** La gasolina con tope, la electricidad con subsidio estacional y otras tarifas oficiales hacen que la inflación personal dependa mucho de la ciudad y de la temporada. Por eso es mejor presentar la variación anual que la quincenal.

### Gaps
- No verifiqué en fuente oficial de la SHCP la vigencia exacta del acuerdo de gasolina ni el número oficial de ciudades con subsidio eléctrico en 2026.
- No encontré estadísticas públicas del número de cotizaciones por genérico × ciudad que permitan cuantificar el error muestral.
- No encontré un recuadro de Banxico sobre inflación por deciles o tipo de hogar en lo revisado.

---

## 6. Cambios recientes (2024–2026): base, genéricos nuevos, formatos, IQY, API

### Takeaway
El cambio grande fue la **Actualización 2024** (ago-2024). Trajo canasta de 292 genéricos con CCIF 2018 y SCIAN 2023, ponderadores ENIGH Estacional 2022, índices encadenados sin cambio de base y genéricos nuevos como streaming. INEGI y Banxico dicen que se buscarán **actualizaciones más frecuentes, cada dos años**, ligadas a la ENIGH, pero a oct-2026 no se ha aplicado ninguna. En 2026 los boletines tienen un formato nuevo (mensual y quincenal por separado). La app de precios sigue exportando IQY, CSV y XLS. La API pública sigue en v2.0 y sus ejemplos usan BISE. En R, `inegiR` salió de CRAN.

### Cited Findings
- INEGI: "A partir de 2024, se buscarán actualizaciones más frecuentes con índices encadenados". — [INEGI, presentación Actualización 2024](https://en.www.inegi.org.mx/contenidos/programas/inpc/2018a/doc/present_resul_2024.pdf)
- Banxico: "el INEGI planea realizar revisiones cada dos años, de tal manera que siempre consideren la información más reciente de la ENIGH". — [Banxico, Recuadro 4](https://www.banxico.org.mx/publicaciones-y-prensa/informes-trimestrales/recuadros/%7BB2DB3F5A-4FA5-E527-3A74-5B3998702397%7D.pdf)
- La consulta pública de 2023 propuso el Laspeyres encadenado para "actualizaciones bianuales". Esto lo conozco por el resumen del buscador, no leí el documento. — [INEGI, ActINPC_23](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2023/especiales/ActINPC_23.pdf)
- Como precedente, en 2013 se aplicó un encadenamiento similar: cambiaron los ponderadores manteniendo la base 2Q dic-2010. — [Banxico, Recuadro 4](https://www.banxico.org.mx/publicaciones-y-prensa/informes-trimestrales/recuadros/%7BB2DB3F5A-4FA5-E527-3A74-5B3998702397%7D.pdf)
- A oct-2026 la ficha del boletín sigue citando 292 genéricos y la ENIGH Estacional 2022. — [Boletín 633/26](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_1q2026_10.pdf)
- En los boletines, las divisiones ya usan nombres CCIF 2018, p. ej. "Bebidas alcohólicas, tabaco y estupefacientes" e "Información y comunicación". La 1Q de octubre de 2026 tuvo una variación anual de −1.73% en "Información y comunicación". — [Boletín 633/26](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_1q2026_10.pdf)
- La app de precios (v1) sigue ofreciendo exportación CSV, HTML, IQY, XLS y XML. Los IQY generados ya apuntan a `/app/indicesdepreciosv2/Exportacion.aspx`. Verificado (curl, 2026-10-26). — [INEGI Índices de Precios](https://www.inegi.org.mx/app/indicesdeprecios/Estructura.aspx?idEstructura=112000200030&T=%C3%8Dndices%20de%20Precios%20al%20Consumidor&ST=Principales%20%C3%ADndices); [GeneraIQY.aspx](https://www.inegi.org.mx/app/indicesdeprecios/GeneraIQY.aspx)
- La API pública de INEGI se documenta como v2.0, con ejemplos en la fuente BISE. — [INEGI, API del Banco de Indicadores](https://www.inegi.org.mx/servicios/api_indicadores.html)
- `inegiR` fue retirado de CRAN y archivado el 2026-06-01. `INEGIpy` publicó la v2.0.0 en feb-2026 y `pyinegi` la v0.1.0 en ago-2026. — [CRAN inegiR](https://cran.r-project.org/package=inegiR); [PyPI INEGIpy](https://pypi.org/project/INEGIpy/); [PyPI pyinegi](https://pypi.org/project/pyinegi/)
- Genéricos "digitales" nuevos o desagregados en 2024: "Streaming de películas y música" (peso 0.10), separado de "Películas y música"; "Instrumentos musicales y descargas de audio y video". Fusiones: "Reproductores de audio y video". — [INEGI, presentación Actualización 2024](https://en.www.inegi.org.mx/contenidos/programas/inpc/2018a/doc/present_resul_2024.pdf)

### Inferences
- El repo debe asumir que **el próximo eslabón puede llegar en cualquier momento**, probablemente con la ENIGH 2024. Cuando llegue habrá un nuevo periodo de traslape, nuevos pesos oficiales y posibles altas, bajas y fusiones de genéricos, con códigos que pueden cambiar. Diseño sugerido:
  - (a) Guardar los pesos oficiales con su "vigencia" (desde la 1Q de agosto de 2024).
  - (b) Hacer la validación contra el INPC publicado por eslabón.
  - (c) Llevar una tabla de correspondencia de genéricos entre canastas.
  - (d) Para el índice personal, encadenar en el periodo de traslape oficial cuando un genérico desaparezca o se fusione.
- No hay señal de que INEGI vaya a retirar el IQY. Aun así, el POST CSV es más fácil de automatizar (GitHub Actions o cron los días 9-10 y 24-25 de cada mes, después de las 8:00 h del día previo a la publicación en el DOF).

### Gaps
- No encontré si INEGI anunció fecha o consulta pública para la actualización 2026–2027 del INPC con la ENIGH 2024.
- No verifiqué si `indicesdepreciosv2` es una app pública nueva ni si la v1 se va a deprecar.
