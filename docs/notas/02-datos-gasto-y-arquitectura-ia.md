# The user-data side of a personal-inflation product in Mexico: getting spending data, mapping it to INPC genéricos, and delivering it as an open-source repo and an AI plugin (status as of 2026-10-26)

Scope note: these notes cover how a person's spending data is obtained and categorized, and how the product could be delivered (repo, MCP server, Claude/ChatGPT). INEGI's publication of INPC data (API, release calendar) is assumed to be covered by other researchers and is only touched on here. Unless marked otherwise, all dates are 2025–2026. Many sources are vendor blogs or trade press; I flag this where it matters.

---

## 1. Open banking / open finance in Mexico (Ley Fintech Art. 76): has transactional open finance actually been implemented?

### Takeaway
No. As of mid/late 2026, Mexico has secondary rules only for **open data** (CNBV, June 2020) and Banxico's narrow 2020 rules for credit bureaus and clearinghouses. The rules for **aggregated** and **transactional** data, the layer a personal-inflation app would need, are still unpublished six years after the legal deadline. An amparo (Dec 2025/Jan 2026) is pending, and the CNBV said in 2026 that it would "review" open-finance regulation but gave no timeline. A personal-inflation product cannot rely on regulated bank-transaction APIs in 2026–2027.

### Cited Findings
- Ley Fintech (2018) Art. 76 requires sharing data "mediante APIs estandarizadas" in three categories: open data, aggregated data and transactional data. Transactional data requires the customer's prior express consent. Regulators are the CNBV and Banxico. — [Fiskil Open Finance Tracker – México](https://www.fiskil.com/es/open-finance-tracker/mexico)
- Only the open-data rules (ATM/branch locations and product information) have been published, in the DOF on 4 June 2020. Aggregated and transactional rules remain pending "en 2026, muy por encima del plazo legal", with "sin cronograma oficial". — [Fiskil tracker](https://www.fiskil.com/es/open-finance-tracker/mexico); see also [LatamFintech: CNBV emite las primeras reglas y estándares de open finance](https://www.latamfintech.co/articles/cnbv-emite-las-primeras-reglas-y-estandares-de-open-finance-en-mexico) (2020)
- The CNBV had 24 months to publish these rules. More than five years later they are not finalized. — [Facephi Observatory, Open Banking & CNBV biometrics 2026](https://facephi.com/observatory/en/open-banking-facial-biometrics-cnbv-mexico/)
- Banxico's first secondary rules (Circular 2/2020) apply only to sociedades de información crediticia and cámaras de compensación. Rules for banks, cooperatives and other entities were left to be issued. — [Basham: Circular 2/2020](https://basham.com.mx/en/circular-2-2020-primeras-reglas-secundarias-referentes-al-open-banking/)
- **Litigation:** two entrepreneurs filed an amparo against the CNBV, Banxico and SHCP on 10 Dec 2025 over the failure to issue the transactional/aggregated rules, arguing that it blocks business projects. A 2026 timeline marks it "en trámite". — [Facephi Observatory (ES)](https://facephi.com/observatory/open-banking-biometria-facial-cnbv-mexico/). A different summary attributes the amparo to entrepreneurs from "Equipo Colosio" and dates it to January 2026 ([Facephi, Fintech Law in Mexico 2026](https://facephi.com/observatory/en/fintech-law-in-mexico-2026-competition-sandbox-and-new-financial-models/)). **Dates conflict.** FinTech Futures also reported that the "CNBV [is] reportedly facing legal action over delays publishing open finance rules" ([FinTech Futures](https://www.fintechfutures.com/?p=15284082), headline only: page returned 403).
- At Fintech México Festival 2026, the CNBV announced its intention to push a regulatory review of crypto assets and open finance. As of July 2026 there was no public timeline and no published rules. — [Facephi, Fintech Law in Mexico 2026](https://facephi.com/observatory/en/fintech-law-in-mexico-2026-competition-sandbox-and-new-financial-models/)
- Trade press in May 2025 described a "pausa en la regulación del open finance" in Mexico. — [Descubre.vc, 28 May 2025](https://www.descubre.vc/noticia/belvo-impulsa-datos-alternativos-en-m-xico-pese-a-pausa-del-open-finance-2025-05-28)
- (Older, 2018) Hogan Lovells: the Fintech Law did not mandate open access for payment-initiation services (unlike PSD2), and such services had already appeared in Mexico "facilitated by screen-scraping". — [Hogan Lovells 2018](https://www.hoganlovells.com/~/media/hogan-lovells/pdf/2018/v3_global_mexico.pdf?la=en)
- An extended search for Sept–Oct 2026 announcements of aggregated or transactional rules turned up nothing. — (search, 2026-10-26; secondary sources only, including [Fiskil](https://www.fiskil.com/es/open-finance/mexico) and [Excélsior column "Ley Fintech: tiempo de actualización"](https://www.excelsior.com.mx/opinion/columnista-invitado-1/ley-fintech-tiempo-actualizacion))

### Inferences
- Even if the CNBV published transactional-data rules in 2027, the UK and Brazil experience suggests an 18–36-month implementation path (API standards, registration of data recipients, bank build-out). A regulated "connect your bank" flow open to an individual open-source developer is unlikely before ~2028. Recipients would in any case probably need to be authorized or registered entities, not hobby projects. (Inference; Mexico's eventual recipient-registration rules are unknown.)
- The product should be designed around data the user already controls (exports, statements, CFDI, receipts, declared budgets), with open finance as a future optional connector.

### Gaps
- I could not reach the primary DOF/CNBV/Banxico documents or the amparo file. The amparo's case number, court and current status are unknown.
- I found no official statement after July 2026 on the CNBV "revisión regulatoria".
- I did not verify whether the CNBV has taken any formal position on screen scraping (whether it is permitted, tolerated or to be prohibited once APIs exist).

---

## 2. Private aggregators in Mexico (Belvo, Finerio Connect, Syncfy, Prometeo, Fintoc, Plaid)

### Takeaway
Aggregators exist, but they are **B2B, sales-gated and usage-priced**, with no public self-serve pricing. In Mexico they have **shifted toward government data (SAT invoices/tax returns, IMSS employment)** and payments rather than bank-transaction aggregation. Belvo's new (Aug 2026) MCP for AI agents lists only **"employment and fiscal sources in Mexico"**, not banking. Plaid does not cover Mexico. None is a realistic dependency for an individual's open-source project. At most there is an optional "bring your own API key" adapter, or Belvo's SAT invoices endpoint.

### Cited Findings
**Belvo**
- Mexico represents 60% of Belvo's business, with a strong focus on SAT and IMSS data for credit evaluation. Belvo raised a US$15M round (2025) to strengthen Mexico and its AI integration. — [Descubre.vc, May 2025](https://www.descubre.vc/noticia/belvo-impulsa-datos-alternativos-en-m-xico-pese-a-pausa-del-open-finance-2025-05-28)
- Belvo launched an IMSS formal-employment data aggregation product for lenders in Mexico. — [LatamFintech](https://www.latamfintech.co/articles/belvo-busca-incrementar-las-ofertas-de-credito-en-mexico-a-traves-de-los-datos-de-empleo)
- Belvo "institutions" include banks (e.g., Banamex retail, HSBC business), fiscal institutions (SAT in Mexico) and employment institutions (IMSS). — [Belvo developer docs – Institutions](https://developers.belvo.com/reference/institutions)
- Historical Mexico bank coverage: the 2020 private beta listed Banamex, Santander, Banorte, Scotiabank, BBVA Bancomer, HSBC and American Express (retail only) ([Belvo blog, beta](https://belvo.com/blog/belvo-launches-first-beta-live/)). A later post cited 12 Mexican banking institutions ([Belvo blog](https://belvo.com/blog/more-sdks-integrations-and-customisation-capabilities/)). In 2021 TechCrunch reported 40+ institutions covering >90% of LatAm personal/business accounts ([TechCrunch 2021](https://techcrunch.com/2021/06/01/belvo-latams-answer-to-plaid-raises-43m-series-a-to-scale-its-api-for-financial-services)). **Current coverage is contested.** Fintable lists 41 institutions ([Fintable](https://dashboard.fintable.io/coverage/providers/BELVO)). Open Banking Tracker lists only 3 bank integrations, including Citibanamex and Santander México ([Open Banking Tracker](https://www.openbankingtracker.com/api-aggregators/belvo)).
- **Belvo MCP (Aug 2026):** three MCP servers. Developer MCP and Data Access MCP are "live in Brazil and Mexico", and the Analytics MCP is "on our product roadmap". The FAQ says: "Your agent can access banking and employment sources in Brazil, and **employment and fiscal sources in Mexico**." Fiscal data is "tax returns and invoicing history". "The MCP servers carry no extra cost. You only pay for the underlying API calls". Data Access MCP: "Talk to our team to activate this feature." Developer MCP docs need no account, but live API calls require one. Belvo claims compatibility with Claude, ChatGPT, Copilot, Gemini and Cursor. It also offers a free public demo, "Panorama" (panorama.belvo.com), to "connect your personal accounts and ask the AI plain-language questions". — [Belvo MCPs page](https://belvo.com/resources/mcps/); [Belvo blog: MCPs, the new agentic open finance](https://belvo.com/blog/belvo-mcps-the-new-agentic-open-finance/); [LatamFintech coverage](https://www.latamfintech.co/articles/fintech-mexicana-belvo-lanza-mcp-su-infraestructura-para-conectar-agentes-de-ia-con-datos-de-open-finance-en-america-latina); [Open Banking Expo](https://www.openbankingexpo.com/news/belvo-launches-mcp-to-connect-ai-to-financial-data-in-latam/)
- Production access path (documented for Chile invoices): request access, then a sales meeting, then a certification review with an engineer, then production keys (sandbox at sandbox.belvo.com, production at api.belvo.com). — [Belvo docs – Invoices Chile](https://developers.belvo.com/apis/belvoopenapispec/invoices-chile)
- Belvo's pricing page URL (belvo.com/pricing) returned 404. A third-party directory labels Belvo "freemium", with no tier details. — [RankMyAI listing, Mar 2026](https://www.rankmyai.com/tools/cedbf8c8-247d-4197-9a1c-a8558f62162f/belvo)
- Belvo has a support article titled "Why is Belvo returning invoices with missing details?", which suggests that SAT invoice line details can come back empty or null. — [Belvo support](https://support.belvo.com/hc/en-us/articles/360012064617-I-m-receiving-invoices-with-empty-invoice-details-or-null-fields)
- Feb 2026: a secondary report says Belvo launched an AI suite for credit approval, payments and collections in Mexico. — [Descubre.vc, Feb 2026](https://www.descubre.vc/noticia/belvo-lanza-su-ecosistema-inteligente-de-open-finance-con-ia-en-m-xico-2026-02-12)

**Finerio Connect**
- Connects "con bancos, telcos y registros fiscales". Offers a transaction-categorization API claiming "+96% precisión". Calls to action are "Agenda una demo" and messages addressed to "tu institución financiera" (B2B). No public pricing, and the site does not say how it connects. — [finerioconnect.com](https://finerioconnect.com/)
- Works with 120+ institutions in several LatAm countries, reported >US$1M ARR and a US$6.5M round (Oct 2023). — [Descubre.vc – Finerio Connect](https://www.descubre.vc/e/Finerio-Connect)

**Syncfy**
- Claims access to 125+ banking institutions, wallets, tax authorities, utilities and crypto across 15+ countries, and "the widest banking coverage in Mexico". Clients include BBVA and Intuit. US$10M seed round in Dec 2022. — [LatamFintech](https://www.latamfintech.co/articles/syncfy-levanto-us-10m-para-construir-una-plataforma-de-ia-y-automatizacion-de-open-finance-para-latam); [Bloomberg Línea](https://www.bloomberglinea.com/2022/12/08/syncfy-cierra-ronda-semilla-por-us10-millones-para-su-negocio-de-open-finance/)

**Prometeo**
- Uruguayan open-banking infrastructure company (founded 2018). Launched account-to-account payments in Mexico (Mar 2024) and claims a direct connection to Banxico's network, giving access to "100% de los bancos mexicanos" (company claim, reprinted by the outlet). — [Portal ERP](https://portalerp.com/mx/noticia/prometeo-lanza-al-mercado-mexicano-la-solucion-tecnologica-pagos-cuenta-a-cuenta); [Descubre.vc – Prometeo](https://www.descubre.vc/e/prometeo)

**Plaid**
- Plaid's institutions page says it "supports over 10,000 institutions across the United States and Canada", plus a separate European coverage explorer. Mexico is not mentioned. — [Plaid docs – Institutions](https://plaid.com/docs/institutions/)
- Plaid's official MCP server is reportedly for diagnostics, not consumer financial data. Community Plaid MCP servers exist (self-hosted, need developer keys). — [Truto blog](https://truto.one/blog/how-to-connect-ai-agents-to-plaid-mcp-server-architecture-for-financial-data-access/) (vendor source, so treat with caution)

**Screen-scraping mechanics and risk**
- Almost all screen scraping requires customers to hand their usernames and passwords to a fintech or aggregator. — [BPI](https://bpi.com/screen-scraping-what-is-it-and-how-does-it-work/)
- There is no standardized consent mechanism, and scrapers break when banks change their websites. — [Open Banking Tracker](https://openbankingtracker.com/answers/what-is-screen-scraping-in-banking)
- API/OAuth flows instead route the user through their own bank's login and issue a revocable, scoped token. — [Stripe MX (vendor)](https://stripe.com/mx/resources/more/screen-scraping-vs-apis)

### Inferences
- **For an individual or open-source project:** aggregators require a company relationship, a sales call and certification, and charge per API call. Their ToS almost certainly forbid redistributing keys, so an open-source repo cannot ship working aggregator access. The realistic pattern is an optional adapter ("if you or your company have Belvo/Syncfy keys, plug them in"), never the default.
- Belvo's Mexico pivot toward SAT invoices and IMSS, and its MCP scope (fiscal, not banking, for Mexico), suggest that **bank-transaction aggregation in Mexico is commercially or technically weak in 2026**. This is consistent with screen scraping being fragile and with no regulated APIs. The aggregator data most useful for personal inflation in Mexico may actually be **SAT invoices (CFDI)**, which users can also get directly and for free (see section 3).
- Belvo's free "Panorama" demo shows the UX the user envisions (connect accounts, then ask the AI), but it is a demo, not a platform for third-party open-source apps.

### Gaps
- No public pricing for Belvo, Finerio, Syncfy or Prometeo. Belvo's pricing page is 404. Pricing for developers or individuals is unknown, and the market is "contact sales".
- I could not confirm the **connection method** (credential-based scraping vs. bank agreements) for any aggregator's current Mexican bank connectors, or the current list of Mexican banks each supports.
- I could not confirm whether Belvo still sells retail bank-transaction aggregation in Mexico (the MCP FAQ implies not via MCP, but the general product may still exist).
- Fintoc: I found no information on any Mexico aggregation product.
- I did not review aggregator ToS clauses (for example, end-user vs. developer restrictions).

---

## 3. Alternative data sources (CFDI, statements, CSV, email receipts, tickets OCR, questionnaires, ENIGH priors)

### Takeaway
The most promising **item-level** source is the user's own **SAT CFDI XMLs**. Every concepto line carries a mandatory UNSPSC-based **ClaveProdServ** code, and individuals can download received CFDIs free from the SAT portal (RFC + contraseña) or in bulk through the Descarga Masiva web service (e.firma, v1.5 since 30 May 2025). Mature open-source libraries exist (satcfdi, sat-ws, phpcfdi). The catch is **coverage bias**: everyday purchases (supermarket, street food, transport) usually end up in the merchant's **factura global** to "público en general" unless the consumer requests a nominative invoice. Individuals mostly request CFDIs for **deductible** spending (health, education, etc.). The practical design is therefore a **blend**: a declared monthly budget (questionnaire) plus ENIGH/INPC priors as the baseline, refined by bank statement/CSV parsing (merchant level) and CFDIs, email receipts and ticket OCR (item level) where available.

### Cited Findings
**SAT CFDI download**
- Portal route: log in to portalcfdi.facturaelectronica.sat.gob.mx with RFC + contraseña (or e.firma), choose "Consultar facturas recibidas", filter by month, then "Descargar seleccionados" to get a ZIP of XMLs. "Recuperar descargas de CFDI" shows bulk download requests. — [Yo-Facturo guide](https://yo-facturo.com/blog/como-descargar-facturas-del-sat-cfdi-xml-pdf/); [SATFácil ZIP guide](https://www.satfacil.com.mx/blog/como-descargar-cfdis-sat-zip-guia)
- **Descarga Masiva Web Service v1.5** has been in force since **30 May 2025**. Operations: SolicitaDescargaEmitidos (issued CFDIs, valid and cancelled); SolicitaDescargaRecibidos (full download of valid received CFDIs, but **only metadata for cancelled received CFDIs**); SolicitaDescargaFolio (a single CFDI by UUID); and status verification. Authentication uses e.firma. Up to 200,000 XMLs per request. Only the **last five years** (six fiscal years counting the current one) are downloadable. A reader comment says responses take ~24–72 h (anecdotal). — [ContadorMX](https://contadormx.com/nuevo-web-service-del-sat-1-5-descarga-masiva-de-xml/); [El Conta](https://elconta.mx/descarga-masiva-de-xml-web-service-sat-version-1-5-resumen/)
- El Conta reported widespread failures of SAT Descarga Masiva in late May 2025 (user reports, not official). — [El Conta](https://elconta.mx/descarga-masiva-de-xml-web-service-sat-version-1-5-resumen/)
- A 2026 guide gives approximate limits of 200,000 XML per package and up to one month per request (described as approximate). — [SATFácil](https://www.satfacil.com.mx/blog/como-descargar-cfdis-sat-zip-guia)
- **Open-source tooling:** `satcfdi` (Python) supports CFDI 3.2/3.3/4.0, Descarga Masiva, validation, the 69B list and DIOT, installs via `pip install satcfdi`, and handles .cer/.key signing ([GitHub SAT-CFDI/python-satcfdi](https://github.com/SAT-CFDI/python-satcfdi); [docs](https://satcfdi.readthedocs.io/en/4.5.1/generated/satcfdi.apis.html)). `sat-ws` (Python) is a Spanish-language Descarga Masiva client based on phpcfdi's ([PyPI sat-ws](https://pypi.org/project/sat-ws/)). phpCfdi (PHP) has Descarga Masiva and e.firma credential libraries ([github.com/phpcfdi](https://www.github.com/phpcfdi)).

**What a CFDI contains (granularity)**
- ClaveProdServ is a **required** element of each CFDI concepto, complementing the free-text description. — [Facturama](https://facturama.mx/blog/que-significa/catpys-catalogo-producto-servicios/)
- The SAT based the c_ClaveProdServ catalog on **UNSPSC**. — [IDC Online (2017, CFDI 3.3)](https://idconline.mx/fiscal-contable/2017/09/06/de-donde-viene-el-catalogo-para-el-llenado-de-cfdi-33); see also [Vertex: Mexico CFDI line-level commodity classification](https://developer.vertexinc.com/einvoicing/docs/mexico-cfdi-line-level-commodity-classification)
- Catalog size: Facturama reports **>52,000 keys**, but other figures conflict (≈18,000 UNSPSC categories in 2017). — [Facturama](https://facturama.mx/blog/que-significa/catpys-catalogo-producto-servicios/); [IDC Online](https://idconline.mx/fiscal-contable/2017/09/06/de-donde-viene-el-catalogo-para-el-llenado-de-cfdi-33)
- A fallback key "01010101" (no match in catalog) is reported by one blog but not confirmed against SAT guidance. — [Facturador Electrónico](https://facturadorelectronico.com/blog/?p=4537)

**Why CFDIs under-cover everyday purchases (factura global)**
- Sales to "público en general" use the generic RFC XAXX010101000, name "PUBLICO EN GENERAL", régimen 616 and uso S01. — [IDC Online 2023](https://idconline.mx/fiscal-contable/2023/04/28/cfdi-40-rfc-generico-ventas-al-publico-en-general)
- The CFDI global covers operations where customers did not request an invoice. RMF rule 2.7.1.21 allows a daily, weekly or monthly global CFDI, with ticket folio numbers in the conceptos. If a customer later requests a nominative invoice for a sale already in the global, the global must be cancelled and reissued without it. — [IDC Online 2022](https://idconline.mx/fiscal-contable/2022/06/29/cfdi-40-por-operaciones-con-publico-en-general); [SoyConta](https://www.soyconta.com/diferencia-entre-una-factura-nominativa-sin-rfc-y-una-factura-global/)
- Incentive pattern: medical fees count as a personal deduction only with a correct CFDI and payment by card, transfer or nominative check (cash disqualifies). — [SATFácil, declaración anual 2026](https://www.satfacil.com.mx/blog/declaracion-anual-personas-fisicas-2026)
- Belvo's SAT invoice data can come back with empty invoice details or null fields (support article title). — [Belvo support](https://support.belvo.com/hc/en-us/articles/360012064617-I-m-receiving-invoices-with-empty-invoice-details-or-null-fields)

**Bank statements / CSV**
- No BBVA **México**-specific open-source parser was found. `bbva2pandas` parses BBVA monthly PDFs into a DataFrame/CSV/SQLite via poppler `pdftotext`, but it targets bbva.es (Spain) ([PyPI bbva2pandas](https://pypi.org/project/bbva2pandas/)). `ofxstatement-bbva` (Spain) has experimental PDF support and notes the bank website exports XLSX only for the last year ([PyPI ofxstatement-bbva](https://pypi.org/project/ofxstatement-bbva)).
- Generic parsers that can be configured: Transtractor (Rust-backed Python library, custom JSON configs per bank, PRs welcome) ([Transtractor docs](https://transtractor-lib.readthedocs.io/)); AyonPal bank-statement-pdf-parser (stdlib Python + qpdf) ([GitHub](https://github.com/AyonPal/bank-statement-pdf-parser)).

**ENIGH / INPC weights as priors**
- INEGI updated INPC weights in **July 2024** (second fortnight) using **ENIGH Estacional 2022** spending data (773 concepts), with statistical adjustment for under-reported items (tequila, beer, brandy). The basket moved to **CCIF 2018**, genéricos fell **from 299 to 292** (259 unchanged, 20 split into 24, 20 merged into 9; items <0.01% of national spending folded into others), and the index switched to a **chained Laspeyres** with 2Q Jul 2018 = 100 and 2Q Jul 2024 as the splice period. Example: the weight of Salud went 3.08 → 4.13. — [México Cómo Vamos, Aug 2024](https://mexicocomovamos.mx/animal-politico/2024/08/inpc-2024-actualizacion-y-ajustes-en-ponderadores/); [INEGI presentation of 2024 results](https://inegi.org.mx/contenidos/programas/inpc/2018a/doc/present_resul_2024.pdf); [CONEVAL technical note, Nov 2024](https://www.coneval.org.mx/Medicion/Documents/Lineas_de_Pobreza_por_Ingresos/Nota_tecnica_ajuste_LPI_INPC_2024.pdf). (One SNIEG document shows "≈307" genéricos, so check the official list: [SNIEG](https://www.snieg.mx/Documentos/Economico/sesiones/doc_12023/8_actualizacion_inpc.pdf).)

### Inferences
- **Ranking of sources for a v1 open-source repo** (feasibility × granularity × privacy):
  1. **Declared budget questionnaire** (~15–40 lines such as rent, food at home, eating out, gasoline, public transport, electricity, gas LP, phone/internet, school, health, clothing), with ENIGH/INPC weights used to split each line into genéricos. Zero integration cost, works in a chat ("describe your monthly expenses"), and no PII beyond amounts. Accuracy is limited by recall.
  2. **Bank CSV/XLSX exports and statement PDFs**, parsed locally. Each Mexican bank needs its own parser; layouts change; merchant-level only.
  3. **SAT CFDI XMLs** (free, official, item-level ClaveProdServ). Best for health, education, utilities (CFE, telecom usually issue CFDIs), fuel, online retail and restaurants when the user requests an invoice. Weak for supermarkets and markets unless the user habitually invoices. e.firma handling is a security burden (see section 6), so the RFC + contraseña portal ZIP download done manually by the user is the safer default.
  4. **Email receipts** (Amazon, Mercado Libre, Uber, Rappi, DiDi, CFE, Telmex/Izzi/Totalplay, Netflix/Spotify). These are often item-level and can be read through an existing Gmail connector in Claude/ChatGPT (this session itself shows a Gmail MCP connector). No specific source on receipt formats was gathered.
  5. **Supermarket ticket OCR** (photo, then multimodal LLM). This is the only source with item-level grocery detail when no CFDI exists, but it needs the user to keep tickets and is high-friction.
- **ENIGH priors:** use INPC genérico weights (national or by income stratum/region if INEGI publishes them) as the default composition *within* each category, overwritten wherever the user has item-level data.
- **Coverage bias warning:** a CFDI-only index would over-weight deductible categories (health, education) relative to food. CFDIs should refine shares inside categories, not set the overall category weights unless total CFDI spending reconciles with bank outflows.

### Gaps
- No statistic found on the **share of retail purchases for which consumers request facturas**, or on the volume of CFDIs issued to individuals vs. the factura global. This is a key unknown for CFDI coverage.
- Not confirmed from SAT primary documents: the exact current limits of the portal download (per-day caps, max results per query) and the v1.5 web-service rules for personas físicas.
- No source gathered on which Mexican banks offer CSV/XLSX movement exports in their apps or web banking (BBVA México, Banorte, Santander, Banamex, Nu, Mercado Pago, Hey Banco), or on the standard fields they include (whether MCC or merchant category is ever exposed to consumers).
- Whether INEGI publishes ENIGH-based weights by **income decile or city** usable as personal priors (vs. a single national/plutocratic basket) was not verified here.

---

## 4. The categorization / granularity problem ("WALMART $1,500")

### Takeaway
Merchant-level data (bank transactions) can realistically be mapped to **CCIF divisions/groups or INPC subíndices** (roughly 10–40 buckets) with high accuracy, using MCC/rules plus an LLM with a fixed category enum and a per-merchant cache. Mapping to **~292 genéricos** is only meaningful with item-level data (CFDI ClaveProdServ, receipts, tickets) or by **imputing** within-merchant composition from ENIGH/INPC weights. No independent benchmark exists for LLM transaction categorization, and vendor claims (92–97%, "+96%") are self-reported. A tiered approach with explicit uncertainty is the honest design.

### Cited Findings
- No standardized independent benchmark for LLM merchant/MCC categorization was found. The available numbers are vendor blogs and self-reported results. — (synthesis of search results; see sources below)
- **TransactionGPT** (arXiv 2511.08939): a transaction foundation model (TGPT-2D, 56M params) beat the best fine-tuned LLM (Llama2-7B) at MCC prediction with 92% fewer parameters and ~300× faster inference (0.27 ms vs 84.9 ms). Fine-tuned LLMs also performed well. — [arXiv 2511.08939](https://arxiv.org/pdf/2511.08939)
- A 2026 EU-focused blog claims 92–97% accuracy on European bank feeds "out of the box", with no methodology. — [Freenance](https://freenance.io/financial-tools/ai-categorization-transactions-2026-europe-how-it-works-accuracy-banks-supported-vs-rules-comparison/)
- A lender found its third-party categorization wrong on ~25% of transactions, and accuracy fell to ~39% on the categories that mattered most (debt recognition). Aggregate accuracy hides weak categories. — [Uncapped](https://weareuncapped.com/blog/transaction-categorisation-model-lending-ecommerce)
- A small comparison on a synthetic + Kaggle dataset with 17 categories reported ~92% for an LLM-only approach (Llama 3.1 8B) vs ~96% for LightGBM. Self-reported, not real bank data. — [transaction-ai benchmarks](https://transaction-ai.readthedocs.io/en/latest/BENCHMARKS/)
- Practitioner advice: cache results per merchant string, force the LLM to choose from a fixed enum, and evaluate per category against a rules baseline. Multi-agent setups were reported to beat single-agent ones on financial classification. — [transaction-ai](https://transaction-ai.readthedocs.io/en/latest/1.4_Model_Selection_and_Performance_Targeting/); [Parafin blog](https://www.parafin.com/blog/why-two-llm-agents-beat-one-on-financial-classification)
- Finerio Connect markets a Mexico-relevant categorization API with a claimed "+96% precisión" (vendor claim). — [finerioconnect.com](https://finerioconnect.com/)
- The INPC basket follows **CCIF 2018** and has **292 genéricos** (2024 update), with items below 0.01% of spending merged. — [México Cómo Vamos](https://mexicocomovamos.mx/animal-politico/2024/08/inpc-2024-actualizacion-y-ajustes-en-ponderadores/)
- CFDI concepto lines carry UNSPSC-derived ClaveProdServ codes. — [Facturama](https://facturama.mx/blog/que-significa/catpys-catalogo-producto-servicios/); [IDC Online](https://idconline.mx/fiscal-contable/2017/09/06/de-donde-viene-el-catalogo-para-el-llenado-de-cfdi-33)

### Inferences
- **Proposed tiered approach:**
  - **Tier A (merchant → category, every transaction):** normalize the descriptor ("WAL MART SUC 1234 CDMX", "OXXO", "PEMEX", "UBER *TRIP", "CFE"). Resolve it with (1) a curated open-source **merchant dictionary for Mexico** (top ~500 chains: Walmart/Bodega Aurrerá/Sam's, Soriana, Chedraui, La Comer, OXXO, 7-Eleven, Pemex/G500/Shell, Liverpool, Coppel, Farmacias del Ahorro/Guadalajara/Similares, CFE, Telmex, Telcel, Izzi, Totalplay, Megacable, Uber, DiDi, Rappi, Netflix, Spotify, Amazon, Mercado Libre…), then (2) MCC when available, then (3) an LLM with a fixed enum of INPC/CCIF buckets, and (4) a per-merchant cache plus user corrections. Target: ~12 CCIF divisions and ~30–50 INPC groups, which is achievable with high accuracy because big merchants dominate spending.
  - **Tier B (category → genéricos, imputed):** for multi-category merchants (supermarkets, department stores, Amazon), split the amount across genéricos using INPC/ENIGH weights *conditional on the merchant type* (e.g., the supermarket basket = food at home + cleaning + personal care, normalized). Mark it as "imputed".
  - **Tier C (item-level → genérico, observed):** CFDI ClaveProdServ (UNSPSC → INPC genérico crosswalk, built once and published in the repo), email receipts and ticket OCR, with LLM mapping of product descriptions to the 292 genéricos. Replaces Tier B imputations for the covered share.
  - Report the **share of spending at each tier** alongside the personal index (e.g., "62% observed at genérico level, 38% imputed"). Also report a **group-level personal index**, which is more robust than a falsely precise genérico-level one.
- **The UNSPSC → genérico crosswalk is the key reusable open-source asset.** No public crosswalk between c_ClaveProdServ and INPC genéricos was found (see Gaps). Building and publishing one would be a differentiating contribution.
- Sensitivity insight: most of the difference between personal and official inflation comes from category *shares* (rent vs. owner, car vs. public transport, food-at-home share, education, health), not from genérico-level detail within food. Tier A + B probably captures most of the signal. This is an analytical judgement and should be tested by simulation.

### Gaps
- No public crosswalk found between SAT c_ClaveProdServ (UNSPSC) and INPC genéricos/CCIF. Not searched exhaustively; INEGI may hold internal concordances.
- No Mexico-specific benchmark of transaction categorization accuracy, and no evidence on whether Mexican bank exports expose MCC to consumers.
- No quantitative estimate found of how much accuracy is lost going from genérico-level to group-level weights for personal CPI.

---

## 5. AI delivery: MCP servers, Claude connectors/plugins, ChatGPT Apps SDK, local-first, monthly automation

### Takeaway
In 2026 both Claude and ChatGPT run on **MCP**. Claude supports remote connectors (web/desktop/mobile), local connectors packaged as **MCPB desktop extensions**, and **plugins** that bundle skills with connectors. ChatGPT's **Apps SDK** (Oct 2025) is MCP-based, fully supports the **MCP Apps** UI standard (Feb 2026), and has an app/plugin directory with strict submission rules. OpenAI **forbids collecting passwords/OTP and PCI data** and rejects "unofficial connectors to third-party services", which rules out bank scraping inside a ChatGPT app. Anthropic classes finance as **high-risk**, requiring human-in-the-loop and disclosure. The cleanest architecture is a **two-part design**:
1. A **public, stateless "INPC data + calculator" MCP server**, which receives only category weights or amounts and returns the personal index. It is listable in both directories.
2. A **local-first package/MCP server** that parses the user's statements and CFDIs on their machine.

GitHub Actions publishes the monthly INEGI dataset.

### Cited Findings
**Claude**
- Connectors work across apps: claude.ai web supports remote connectors "including MCP Apps that display interactive content"; the desktop app supports remote connectors "plus local connectors installed as desktop extensions"; mobile supports remote connectors; Claude Code can use connectors added in claude.ai; Cowork supports connectors and plugins. A local connector is "a desktop extension, packaged as an MCP Bundle (MCPB), that runs on your computer". Users can add an unlisted remote server by URL. Per-tool permissions are "Always allow / Needs approval / Blocked". — [Claude docs – Connectors overview](https://claude.com/docs/connectors/overview)
- Directory listings carry a Verified or Community label. — [Claude docs – Connectors overview](https://claude.com/docs/connectors/overview)
- Local MCP servers distributed via npm/PyPI cannot be listed directly in the Connectors Directory. They must be packaged as MCPB (Desktop Extensions) or bundled as a plugin. — [Claude docs](https://claude.com/docs/connectors) (via search summary); [Remote MCP server submission guide](https://support.claude.com/en/articles/12922490-remote-mcp-server-submission-guide)
- **Anthropic Software Directory Policy** (page shows "Updated this week"; a search snippet dates the current version 15 Apr 2026):
  - Finance is a "high-risk use case". High-risk software must use human-in-the-loop measures and direct consumer disclosure.
  - Software that "executes financial transactions autonomously on behalf of users, without human-in-the-loop safeguards" is excluded.
  - "Software must only collect data from the user's context that is necessary to perform their function." It must not store conversation content to build profiles.
  - Authenticated remote servers must use OAuth 2.0, and Streamable HTTP is preferred.
  - Listings require a privacy policy, a test account with sample data, ≥3 example prompts and verified contact information.
  - Plugins may connect to any approved directory connector.
  — [Anthropic Software Directory Policy](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy); [submission docs](https://claude.com/docs/connectors/building/submission)
- An older MCP Directory Policy said MCP servers may not transfer money or crypto or execute financial transactions for users. — [Anthropic MCP Directory Policy (older)](https://support.claude.com/en/articles/11697096-anthropic-mcp-directory-policy)
- Anthropic's MCP directory FAQ (per search summary) states that telemetry includes the parameters and data passed into tool calls and the server's responses. — [Anthropic MCP Directory FAQ](https://support.claude.com/en/articles/11596036-anthropic-mcp-directory-faq)

**ChatGPT / OpenAI**
- OpenAI introduced apps in ChatGPT and the Apps SDK on 6 Oct 2025. — [OpenAI blog](https://openai.com/blog/introducing-apps-in-chatgpt)
- A Nov 2025 help-center update said apps were in preview for Business/Enterprise/Edu. OpenAI accepts submissions to the ChatGPT app directory, and monetization details were to be "shared in the future". — [OpenAI Help – Build with the Apps SDK](https://help.openai.com/en/articles/12515353-build-with-the-apps-sdk)
- According to a third-party guide, OpenAI renamed "connectors" to "apps" on 17 Dec 2025. A ChatGPT app is an MCP-backed app, with the MCP server required and the UI optional. — [getdrio guide](https://www.getdrio.com/blog/what-are-chatgpt-apps)
- Changelog (the developers.openai.com Apps SDK changelog now redirects to a "plugins" changelog):
  - 2026-02-22: "ChatGPT is now fully compatible with the MCP Apps spec".
  - 2026-03-25: approved Apps SDK integrations can be distributed as **Codex plugins** ("At launch, plugins were available only in Codex").
  - 2026-05-27/28: MCP Apps tool lifecycle and host styling.
  - 2026-06-12: users choose when connected apps ask for permission.
  — [OpenAI plugins changelog](https://developers.openai.com/plugins/changelog)
- **OpenAI submission guidelines** (now phrased as "plugin submissions"):
  - "Do not collect, solicit, or process" PCI DSS data, PHI, government identifiers, or "access credentials and authentication secrets (such as API keys, MFA/OTP codes, or passwords)".
  - Sensitive data only if strictly necessary, with adequate consent and prominent disclosure.
  - A published privacy policy is required (categories, purposes, recipients, retention, controls). Data minimization: no "just in case" fields, no requesting the full chat log.
  - "We cannot approve plugins that primarily function as unofficial connectors to third-party services."
  - Prohibited: executing money transfers or trades. Commerce only for physical goods (no selling digital subscriptions). No ads.
  - Submitters must be verified individuals or organizations with support contacts, and must supply a demo account.
  — [OpenAI app/plugin submission guidelines](https://developers.openai.com/apps-sdk/app-submission-guidelines)

**MCP Apps standard**
- MCP Apps (SEP-1865) went live as the first official MCP extension on 26 Jan 2026, co-developed by Anthropic and OpenAI and built on MCP-UI and the OpenAI Apps SDK. Tools declare a UI served from `ui://` resources, rendered in sandboxed iframes with JSON-RPC messaging. Supported in Claude (web and desktop), ChatGPT, Goose and VS Code. — [MCP blog, 26 Jan 2026](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/); [WorkOS](https://workos.com/blog/2026-01-27-mcp-apps)

**Existing finance MCP servers**
- Belvo Developer MCP and Data Access MCP (Mexico: fiscal and employment only), launched Aug 2026. — [Belvo MCPs](https://belvo.com/resources/mcps/)
- Plaid's official MCP server is reportedly diagnostic only. Community Plaid MCP servers require developer keys. — [Truto](https://truto.one/blog/how-to-connect-ai-agents-to-plaid-mcp-server-architecture-for-financial-data-access/)
- Several MIT-licensed community MCP servers exist for **Actual Budget** (open-source YNAB-like budgeting), exposing accounts, transactions and spending insights. — [Glama – Actual Budget MCP servers](https://glama.ai/mcp/servers/integrations/actual-budget)

### Inferences
- **Recommended architecture (open source, local-first):**
  1. `inpc-data` (GitHub Actions cron): a monthly job (scheduled after INEGI's INPC release) fetches genérico indices and weights, validates them, and commits versioned CSV/Parquet + JSON to the repo/GitHub Pages/Releases. This gives a public, forkable dataset with no user data.
  2. `inflacion-personal` Python package + CLI:
     - parsers (bank CSV/XLSX/PDF per bank, CFDI XML via satcfdi, receipt JSON)
     - merchant dictionary
     - classifier (rules → LLM optional, BYO key or local model)
     - UNSPSC→genérico crosswalk
     - index engine (chained Laspeyres-style: personal weights × INPC genérico relatives)

     It runs entirely on the user's machine. SQLite stays local, and there are no credentials in the repo.
  3. **Local MCP server (stdio)** wrapping the package. Tools: `import_statement(path)`, `import_cfdi_zip(path)`, `classify_pending()`, `set_budget(lines)`, `personal_inflation(month)`, `explain_difference_vs_inpc()`. Distributed as a **Claude MCPB desktop extension** and a **Claude plugin** (skill + connector); it also works in Claude Code and other MCP clients. Tools should return **aggregates** (category shares, index values), not raw transaction lists, to minimize what reaches the model.
  4. **Public remote MCP server** (stateless, Streamable HTTP, no login needed or OAuth only if accounts are added). Tools: `get_inpc(generico|group, period)` and `personal_inflation_from_budget(lines)`, which takes declared monthly amounts per category in a chat and returns the index with an MCP Apps chart UI. This is the piece to submit to the **ChatGPT app directory** and the **Claude Connectors Directory**. Storing nothing keeps the privacy policy and LFPDPPP exposure minimal.
- **"Local-first" caveat:** even with a local MCP server, any transaction data a tool returns to Claude/ChatGPT is sent to the model provider as conversation content (and per Anthropic's FAQ, tool parameters and responses are part of telemetry). True "data never leaves my machine" requires computing locally and surfacing only aggregates, or using a local LLM. The docs should say this explicitly.
- **What not to build:** a ChatGPT or Claude app that asks for bank usernames/passwords or OTPs (explicitly prohibited by OpenAI; incompatible with Anthropic's OAuth/high-risk rules), or that acts as an "unofficial connector" to bank portals.
- The "what is my inflation?" UX maps best to the **remote budget-based tool** (questionnaire in chat, optionally pre-filled by the user pasting or uploading a statement). It also maps to a **Gmail-connector + skill** flow in Claude that reads receipts with the user's existing Gmail connector. That flow fits the Claude rule that plugins may connect to approved directory connectors.
- Monthly per-user automation can be a local scheduled task (cron/launchd), or a scheduled agent task in Claude/ChatGPT that calls the public server with stored weights. The weights would then live in the AI product's memory, which the user should be told about.

### Gaps
- I did not verify whether ChatGPT apps (in late 2026) can use **local** MCP servers, or only remote HTTPS servers. Similarly unverified: current plan and region availability of the ChatGPT directory for Mexico, and whether "apps" have been fully rebranded to "plugins" in ChatGPT (the changelog/guideline wording suggests so).
- The exact date of the current Anthropic Software Directory Policy is uncertain (page says "Updated this week"; snippet says 15 Apr 2026).
- I did not retrieve INEGI API details (token, endpoints for genéricos, release calendar) here. They are assumed to be covered by other researchers.
- No existing Mexico-focused personal-finance or INPC MCP server was found (not searched exhaustively on GitHub).

---

## 6. Privacy and legal in Mexico: the 2025 LFPDPPP, INAI's dissolution, obligations, scraping risks, security practices

### Takeaway
A new **LFPDPPP** has been in force since **21 March 2025**. INAI was dissolved (constitutional reform of Dec 2024), and its private-sector data-protection powers moved to the **Secretaría Anticorrupción y Buen Gobierno**. Any hosted service that stores or processes users' transactions becomes a "responsable": it needs an aviso de privacidad, consent, ARCO handling and security measures, and risks sanctions expressed in UMA. Transactional data under Ley Fintech requires express prior consent. The lowest-risk design keeps raw financial data local and makes any hosted component stateless (category-level inputs only). Credential-based scraping is legally grey, fragile and a security liability, and both AI platforms' policies effectively prohibit it.

### Cited Findings
- The new LFPDPPP was published in the DOF on **20 March 2025** and took effect **21 March 2025**, abrogating the 2010 law while keeping most of its content. — [Garrigues](https://www.garrigues.com/es_ES/noticia/mexico-nueva-ley-federal-proteccion-datos-personales-posesion-particulares-introduce); [GT Law](https://www.gtlaw.com/es/insights/2025/3/nueva-ley-general-proteccion-de-datos)
- INAI's functions over personal data held by private parties are transferred to the **Secretaría de Anticorrupción y Buen Gobierno**. — [EY Law Flash](https://www.ey.com/content/dam/ey-unified-site/ey-com/es-mx/technical/tax/documents/ey-law-flash-nueva-lfpdppp.pdf). INAI disappeared under the constitutional "simplificación orgánica" reform of December 2024. — [CDP](https://cdp.com/es/basics/international-u-s-data-privacy-laws-and-regulations-you-need-to-know/)
- The SCJN consolidated text shows a last DOF reform dated **14 Nov 2025**. — [SCJN LFPDPPP text](https://www.internet2.scjn.gob.mx/red/delitos/Word/27.%20LFPDPPP.docx)
- Key content of the 2025 law (per Garrigues):
  - Consent may be express or tacit, and tacit consent is the general rule unless a legal provision requires express consent.
  - The aviso de privacidad must list the data processed, flag sensitive data, and separate purposes that require consent. New purposes need new consent. Electronic collection requires a simplified notice linking to the full one.
  - The duty to disclose transfers was removed from the law but remains in the reglamento (still advisable).
  - Binding self-regulation schemes are allowed.
  - The scope of ARCO rights is clarified.
  - Challenges now go by **amparo** before specialized courts, replacing the TFJA nullity trial.
  - Sanctions are set in **UMA**, with a new infraction for negligent or intentional mishandling of ARCO requests.
  - Processing ("tratamiento") is defined broadly, from collection through disposal.

  — [Garrigues](https://www.garrigues.com/es_ES/noticia/mexico-nueva-ley-federal-proteccion-datos-personales-posesion-particulares-introduce)
- Ley Fintech Art. 76: transactional data sharing requires the customer's **prior express consent**. — [Fiskil](https://www.fiskil.com/es/open-finance-tracker/mexico)
- Screen scraping requires users to share usernames and passwords ([BPI](https://bpi.com/screen-scraping-what-is-it-and-how-does-it-work/)). It has no standardized consent and breaks with website changes ([Open Banking Tracker](https://openbankingtracker.com/answers/what-is-screen-scraping-in-banking)).
- OpenAI prohibits apps from collecting passwords, MFA/OTP codes, API keys, PCI data and government identifiers ([OpenAI guidelines](https://developers.openai.com/apps-sdk/app-submission-guidelines)). Anthropic requires OAuth 2.0 for authenticated remote servers, data minimization, and human-in-the-loop plus disclosure for finance ([Anthropic Software Directory Policy](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy)).
- Belvo's Data Access MCP claims "Every pull enforces strict user consent and leaves a complete audit trail" and "strict identity binding and least privilege on every call" (vendor claim). This is an example of the consent and audit expectations for hosted financial-data agents. — [Belvo MCPs](https://belvo.com/resources/mcps/)

### Inferences
- **Who is the "responsable"?** In a pure local-first repo, the user processes their own data, and the open-source maintainer is arguably not a responsable because they receive nothing. Once the project runs a hosted service that receives or stores spending data (even category totals tied to an account or email), it becomes a responsable under the LFPDPPP. It then needs: an aviso de privacidad (full + simplified), a defined purpose, consent (express is prudent for financial data), ARCO procedures, security measures, retention limits and transfer disclosures (e.g., to the LLM provider or cloud host). A stateless calculator that receives anonymous category amounts and logs nothing is the minimal-exposure option. (Legal inference, not legal advice.)
- **Security best practices for the repo:**
  - never handle bank passwords; never ask for e.firma .key/password in chat
  - if Descarga Masiva is supported, keep e.firma files local, encrypted at rest (OS keychain), with explicit warnings
  - prefer the manual portal ZIP download
  - local SQLite with optional encryption
  - redact account numbers and CLABE before anything reaches an LLM
  - send only aggregated outputs to the model
  - publish a threat model
  - sign releases and pin dependencies (also required by Anthropic for local servers)
- **e.firma risk:** the e.firma is a legally binding signature (it can sign tax filings and contracts). An agent with access to it is far riskier than read-only data access, so the default should be the RFC + contraseña portal ZIP that the user downloads, or the CFDI XMLs they already have.

### Gaps
- **Not verified:** whether the 2025 LFPDPPP keeps the 2010 law's explicit requirement of **express consent for financial or patrimonial data** (old Art. 8, from my recollection). Garrigues' summary does not address it. Check the DOF text (Arts. on consent) before relying on tacit consent.
- Not verified: the status of the **new reglamento** under the 2025 law, and any guidance from the Secretaría Anticorrupción y Buen Gobierno on cloud and AI processing or international transfers (e.g., to US-based LLM providers).
- No Mexican legal source was found on the legality of consumer-authorized screen scraping or on bank ToS prohibitions on sharing credentials. The Hogan Lovells 2018 note only confirms that it was in use.
- No sanction amounts (in UMA) were gathered.
