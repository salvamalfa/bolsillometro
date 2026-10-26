# Business model, Mexican regulatory lines, go-to-market and naming for an open-source "personal inflation" project (status as of 2026-10-26)

Scope note: these notes cover (a) ethical monetization for an open-source-first project, including inside ChatGPT/Claude, (b) Mexican regulatory lines (CNBV investment advice, Ley Fintech, LFPDPPP 2025, PROFECO subscriptions, INEGI terms of use, IMPI trademarks), (c) financial education and distribution in Mexico, and (d) candidate names with domain, GitHub and meaning checks. Open-finance plumbing (Ley Fintech Art. 76 APIs, aggregators) is covered in depth in `02-datos-gasto-y-arquitectura-ia.md` and is only touched on here. **Nothing here is legal advice.** Items marked "LAWYER" should be confirmed by a Mexican lawyer (securities/fintech, data protection, consumer protection, IP). Many secondary sources are law-firm or vendor summaries; I flag this where it matters.

---

## 1. Which sustainable open-source business models fit, and how do comparable OSS personal-finance projects make money?

### Takeaway
OSS personal-finance tools that last are funded in one of four ways: a hosted/managed version of the same AGPL code (Ghostfolio Premium); donations to a stubborn solo maintainer (Firefly III); Open Collective plus a corporate backer (Actual Budget); or volunteers with a tip jar (GnuCash). The venture-funded B2C route failed twice at Maybe. Its 2025 farewell names automated bank sync costs and investor obligations, and it pivoted to B2B. Lunch Money, which is closed source but bootstrapped, shows that a pay-what-you-want subscription with no ads and no data sales can keep a small team going. For this project the best-supported order is: (1) a free OSS core plus a free hosted calculator, (2) sponsorships and grants (FLOSS/fund is the clearest open program), (3) a B2B API or white-label product for fintechs, payroll and HR, and media, and (4) at most a light, pay-what-you-want "monthly analysis" subscription. Selling individual-level data should be ruled out. Aggregate statistics are acceptable only if they are properly anonymized.

### Cited Findings
**Maybe Finance (what happened):**
- Maybe's README now says: "This repository is no longer actively maintained," and points to the v0.6.0 "final release." Forks are allowed under AGPLv3, but "'Maybe' is a trademark of Maybe Finance Inc. and therefore, use of it is NOT allowed in forked repositories (or the logo)." — [maybe-finance/maybe README via jsDelivr](https://cdn.jsdelivr.net/gh/maybe-finance/maybe@main/README.md)
- The v0.6.0 release came out on 24 July (2025); the repo's archive notice is dated Jul 27, 2025. The release says "Maybe is pivoting to B2B financial forecasting and scenario planning," "our obligation as a company is to our investors," "continuing to build this app is not our best chance at paying back our investors," "growing a B2C SaaS app is challenging," and "bootstrapping" a personal finance app with automated bank syncing "is an uphill battle." — [Maybe v0.6.0 release notes](https://github.com/maybe-finance/maybe/releases/tag/v0.6.0)
- An earlier collapse: the archived first codebase says the company shut the app down in mid-2023 after spending about $1,000,000 and then relaunched it as fully open source (AGPLv3). The archive was frozen on Feb 2, 2024. — [maybe-finance/maybe-archive](https://github.com/maybe-finance/maybe-archive) (via search summary)
- A community fork continues as "Sure" ("a community fork of the now-abandoned Maybe Finance project"). — [we-promise/sure README](https://cdn.jsdelivr.net/gh/we-promise/sure@main/README.md)

**Ghostfolio (hosted version of the OSS tool):**
- AGPLv3. "Our official Ghostfolio Premium cloud offering is the easiest way to get started… Revenue is used to cover operational costs for the hosting infrastructure and professional data providers, and to fund ongoing development." It also asks for GitHub Sponsors and "Buy me a coffee." — [Ghostfolio README](https://cdn.jsdelivr.net/gh/ghostfolio/ghostfolio@main/README.md)
- Sources disagree on price: AlternativeTo says "up to $40 per month," a Railway page says about €9/month. I could not read the official pricing page (it is a JS app). — [AlternativeTo](https://alternativeto.net/software/ghostfolio/about); [Railway](https://railway.com/deploy/ghostfolio)
- CVE-2026-47127: before v3.4.0, Ghostfolio's Stripe checkout callback let any authenticated user grant themselves a one-year Premium subscription without paying. This is a reminder that open-sourced billing code is attack surface. — [OSV CVE-2026-47127](https://osv.dev/vulnerability/CVE-2026-47127)

**Firefly III (donations, solo maintainer):**
- The official docs say the project is a side gig and that "Donations are the only form of compensation I receive." The money pays for hosting, domains and the maintainer's time. Channels are Patreon, GitHub Sponsors, ko-fi and Liberapay. The maintainer "will not be accepting VC money and capital injections from commercial organizations." — [Firefly III docs: Financial contributions](https://docs.firefly-iii.org/explanation/more-information/donations/) (via search summary; direct fetch returned 403)
- In a mid-2025 snapshot, the GitHub Sponsors profile showed 42 current and 189 total sponsors (minimum $5). — [GitHub JC5](https://GitHub.com/JC5) (via search summary; snapshot only)

**Actual Budget (Open Collective plus a corporate backer):**
- Recurring Open Collective tiers run from $5 to $100/month. The largest backer is a company, Peakford Ltd, with about $44,484 since Dec 2023. GitHub Sponsors brought in about $3,101 since Nov 2023. Top individual backers each gave about $1,000 or less. — [Open Collective: Actual](https://opencollective.com/actual)
- A small group of volunteers revived the project after the original push died down. — [Actual 2025 roadmap](https://actualbudget.org/blog/roadmap-for-2025)

**GnuCash (volunteers plus a tip jar):**
- Optional donations go through a SourceForge tip jar and mainly cover server costs. The project is run by "a handful of developers and other volunteers." — [GnuCash donate page](https://gnucash.org/donate.phtml)
- A developer wrote in 2018 that the project needs volunteers far more than money. In 2021 a developer said it had more funds than it spent and that past bug bounties had not worked well. — [gnucash-user 2018](https://lists.gnucash.org/pipermail/gnucash-user/2018-April/076418.html); [gnucash-user 2021](https://lists.gnucash.org/pipermail/gnucash-user/2021-May/096416.html)

**Lunch Money (closed source, bootstrapped; a model for an "ethical subscription"):**
- Founded in 2019, "100% bootstrapped," more than 13k paying members, and run by Jen Yip alone for its first five years. — [Lunch Money About](https://lunchmoney.app/about/)
- Pay-what-you-want pricing since 2023, from $60/year or $10/month. Revenue comes only from subscriptions. — [Lunch Money vs Monarch](https://lunchmoney.app/compare/monarch-alternative); [BadCredit.org](https://www.badcredit.org/news/lunch-money-app-offers-credit-and-financial-management/)
- Starter Story profiles growth to about $34K MRR (I did not see the details). — [Starter Story](https://www.starterstory.com/lunch-money-breakdown)

**Grants and sponsorship programs:**
- FLOSS/fund, run by Zerodha (an Indian brokerage): $1M a year for FOSS projects, in grants of $10k, $25k, $50k, $75k or $100k per project per year. You apply by publishing a `funding.json` file. It allocated $1M in 2025 across two tranches ($325k and $675k). — [Zerodha FLOSS/fund 2025 report](https://zerodha.com/open-source/2025-report/); [OpenSourceForU, Oct 2025](https://www.opensourceforu.com/2025/10/zerodha-announces-final-675000-tranche-for-global-open-source-projects-advocates-sovereign-foss-fund/); [The Register, Oct 2024](https://www.theregister.com/2024/10/17/zerodha_open_source_fund/)
- MetLife Foundation's Financial Health Innovation Fund (run by Village Capital) invested in Finerio Connect, a Mexican open-banking and PFM API company. This is investment, not a grant. — [LatamList](https://latamlist.com/village-capital-and-metlifes-financial-health-innovation-fund-makes-new-investment/)
- The UK FCDO / DAI "Mexico Financial Services Programme" (2019–2023) included young-adult financial education. It is closed. — [DAI](https://www.dai.com/our-work/projects/mexico-prosperity-fund-mexico-financial-services-programme)
- LHoFT "Catapult: Inclusion LAC" is a bootcamp, not a grant, for pre-seed to Series A fintechs, including financial-education solutions. — [TerraViva Grants](https://www.terravivagrants.org/lhoft-green-fintech-lac/)

**B2B demand signals (payroll/HR "employee-specific inflation," fintechs):**
- The 2026 general minimum wage rose 13% to 315.04 pesos/day (5% in the northern border zone, to 440.87). — [EY México bulletin](https://www.ey.com/es_mx/technical/tax/boletines-fiscales/incremento-salarios-minimos-2026) (figures via search summary)
- Nominal contractual raises in manufacturing ranged from 7.5% to 12.5% in 2022–2026, trending down since 2025 (PUED-UNAM using Banxico data). — [PUED-UNAM](https://pued.unam.mx/export/sites/default/archivos/SUCS/2026/SAET130526.pdf) (via search summary)
- Inflation is unequal, which is the core B2B and HR argument. IMCO (2022) found the poorest decile's basket rose 8.74% a year versus 7.48% for the richest. Food takes about 50% of decile-1 spending and about 28% of decile-10. — [IMCO](https://imco.org.mx/la-inflacion-afecta-mas-a-las-familias-que-menos-tienen/); [IMCO PDF](https://imco.org.mx/wp-content/uploads/2022/05/Inflación-de-los-hogares-en-México_IMCO_20220511-1.pdf)
- A UNAM study of 2015–2023 found poor, rural, indigenous and low-education households face more inflation, with cumulative inflation for poor households 6.5% above that for rich households. — [Revista de Investigación Económica (UNAM)](https://journals.unam.mx/index.php/rie/article/view/90415)
- April 2026: headline inflation was 4.45%, but fruits and vegetables were up 21.43% year on year. — [Expansión, May 7 2026](https://expansion.mx/economia/2026/05/07/inflacion-inegi-abril-2026-hogares-pobres-alimentos)

**Data products and privacy:**
- Under the 2025 LFPDPPP, using data for a new purpose requires new consent, and the privacy notice must separate purposes that need consent. — [Garrigues](https://www.garrigues.com/es_ES/noticia/mexico-nueva-ley-federal-proteccion-datos-personales-posesion-particulares-introduce)
- Littler notes that the new law's definition of personal data no longer requires the information to belong to a natural person, which widens its scope. — [Littler](https://www.littler.com/es/news-analysis/asap/mexico-tiene-nueva-ley-en-materia-de-proteccion-de-datos-personales)

### Inferences
- **Recommended monetization ladder (ethical, open-source-first):**
  1. *Core stays free forever:* the INPC-genérico weighting library, the CLI and the self-hostable web app (forkable). Use a trademark policy like Maybe's, so forks must rename and cannot pass themselves off as the original.
  2. *Free hosted calculator* in "declared basket" mode with no bank connection. This drives adoption and press, and costs almost nothing to run (INPC data is public and monthly).
  3. *Sponsorships and grants:* GitHub Sponsors and Open Collective for transparency, a `funding.json` for FLOSS/fund, and Mexican and LatAm financial-health funders (see Gaps).
  4. *B2B API / white-label (the most plausible revenue):* (a) fintechs, neobanks and brokers that want a "your inflation vs. your return" widget; (b) payroll and HR platforms and unions offering "inflation by employee profile" for raise negotiations. The IMCO/UNAM decile gaps and the 13% minimum-wage hike make a natural pitch. (c) Media and data journalism (licensed charts and an embeddable calculator); (d) Afores and asesores, as an educational tool. B2B clients carry their own regulatory obligations; the project sells only the computation.
  5. *Optional light subscription* ("monthly AI analysis of your inflation"): pay-what-you-want like Lunch Money, cancel in one click (legally required anyway, see §3d), no annual lock-in, no ads, no data sales. Its value is reminders, explanations and history, not investment picks.
  6. *Aggregate data products:* only k-anonymized, opt-in aggregates (e.g., "median personal inflation by decile/region"), published openly as a public good or licensed to researchers. Never individual-level data. LAWYER: confirm the anonymization standard under the 2025 LFPDPPP.
- **Maybe's lesson is cost structure.** Its B2C economics were sunk by bank sync. A personal-inflation calculator needs only *monthly category shares*, not real-time transactions. Statement or CSV upload, CFDI XML, or a declared basket avoid aggregator fees. Bank connection can be an opt-in premium or B2B feature through a licensed aggregator.
- **License trade-off:** AGPL (Maybe, Ghostfolio) blocks closed SaaS clones but can put off banks from embedding the code. Apache-2.0/MIT maximizes B2B embedding and forks. A common compromise is a permissive core library plus an AGPL hosted app, with a registered trademark either way.
- **Billing code in an OSS repo is attack surface** (Ghostfolio CVE). Keep payment handling in a separate private service, or use a hosted checkout.

### Gaps
- Ghostfolio's official current price: the pricing page is JS-rendered and sources conflict.
- No funding information found for Beancount or Fava.
- Firefly III's current sponsorship totals; the only counts are a 2025 snapshot.
- No open 2026 Mexican or LatAm grant call found specifically for open-source financial-education tools. Leads to check directly: Citi Foundation, Mastercard Center for Inclusive Growth, Fundación BBVA México, IDB Lab (BID Lab), Tinker Foundation (its listing had expired), and Finnovista/FINNOSUMMIT programs. These are unverified leads only.
- No public B2B price benchmarks for "personal inflation" APIs.
- An Aon 2026 salary-increase projection (6.4% unionized, 5.4% non-unionized) appeared in a search summary without a traceable URL, so it is not used as a finding.

---

## 2. Can developers charge for ChatGPT apps or Claude connectors/plugins in 2026? Rules and realities

### Takeaway
As of October 2026, **ChatGPT apps ("plugins" in OpenAI's renamed guidelines) cannot sell digital goods or subscriptions.** Commerce is allowed only for physical goods, through external checkout, and apps may not display plans or promote upgrades. Users may sign in to a paid account they already have. Instant Checkout was scaled back in March 2026. **The Claude directory** is free to list and "not pay-to-play." I found no native payment rails for connectors, and MCP servers may not move money. Both platforms restrict *personalized investment recommendations*. Anthropic's new Usage Policy (effective Nov 12, 2026) requires a qualified human reviewer and AI disclosure for "a personalized recommendation to buy, sell, hold, or allocate among specific investment products." The practical conclusion is to treat the AI plugins as a free distribution and education channel, charge (if at all) off-platform, and design the output as a benchmark and information, not a product recommendation.

### Cited Findings
**OpenAI / ChatGPT:**
- Monetization docs: "the **recommended** and **generally available** approach is to use **external checkout**"; "current approval is limited to plugins for physical goods purchases." Checkout with saved payment methods "can only display saved payment methods." The ChatGPT payment sheet "is limited to select marketplaces today." Merchants with PCI DSS Level 1 can receive raw payment methods through the Agentic Commerce Protocol Delegate Payment endpoint. — [OpenAI Apps SDK: Monetization](https://developers.openai.com/apps-sdk/build/monetization)
- Submission guidelines (now titled "Plugin guidelines"):
  - Commerce: "Currently, plugins may conduct commerce only for physical goods." "Selling digital products or services—including subscriptions, digital content, tokens, or credits—is not allowed." "Users may sign in to an existing paid account and access features already included in their subscription." "Plugins must not display subscription plans, initiate new subscriptions, or promote upgrades." An app may link to an informational plans page but not to a checkout.
  - No ChatGPT-specific surcharges and no degraded features. "Plugins must not serve advertisements."
  - Prohibited: "Unregulated, deceptive, or abusive financial services," "Execution of money transfers, crypto transfers, or investment trades," and "Negative-option billing…".
  - Data: a published privacy policy is required, plus data minimization. Do not collect PCI card data, government identifiers, or "access credentials" (passwords, API keys, MFA/OTP codes). No behavioral profiling unless disclosed and under user control, no precise location, and no reconstructing the chat log. — [OpenAI Plugin (app) submission guidelines](https://developers.openai.com/apps-sdk/app-submission-guidelines)
- OpenAI opened app submissions and launched the App Directory in December 2025. — [Novalogiq, Dec 18 2025](https://novalogiq.com/2025/12/18/openai-now-accepting-chatgpt-app-submissions-from-third-party-devs-launches-app-directory/)
- Developer-forum readings agree that monetizing any digital product or service in a submitted app is not allowed. — [OpenAI Developer Community](https://community.openai.com/t/chatgpt-app-monetization-apps-sdk/1372343)
- Instant Checkout launched in Sept 2025 with Stripe on the open-sourced Agentic Commerce Protocol. — [OpenAI "Buy it in ChatGPT"](https://openai.com/index/buy-it-in-chatgpt/); [Stripe newsroom](https://stripe.com/newsroom/news/stripe-openai-instant-checkout)
- In March 2026 OpenAI scaled it back. Modern Retail (Mar 27, 2026), citing The Information, reported that OpenAI would focus on checkouts inside specific partner apps, and an OpenAI spokesperson said Instant Checkout "is moving to Apps." Secondary reports say only about 12 Shopify stores were live. — [Modern Retail](https://www.modernretail.co/technology/what-went-wrong-with-chatgpts-instant-checkout/); [Forrester](https://www.forrester.com/blogs/what-it-means-that-the-leader-in-agentic-commerce-just-pulled-back); [EcomCrew](https://www.ecomcrew.com/openai-pulls-back-on-chatgpt-instant-checkout/)
- OpenAI Usage Policies (updated 2025-10-29) prohibit "provision of tailored advice that requires a license, such as legal or medical advice, without appropriate involvement by a licensed professional" and "automation of high-stakes decisions in sensitive areas without human review," including financial activities and credit. — [OpenAI Usage Policies](https://openai.com/policies/usage-policies/)

**Anthropic / Claude:**
- The MCP Directory Policy page (dated April 15, 2026) says it "has been consolidated into the Anthropic Software Directory Policy." — [Claude Help Center: MCP Directory Policy](https://support.claude.com/en/articles/11697096-anthropic-mcp-directory-policy)
- Earlier policy text: "MCP servers may not be used to transfer money, cryptocurrency, or other financial assets, or to execute financial transactions on behalf of users"; servers "should only collect data from the user's context that is necessary" and "should not collect extraneous conversation data, even for logging purposes." — [Anthropic MCP Directory Policy (search snippet)](https://support.anthropic.com/en/articles/11697096-anthropic-mcp-directory-policy)
- Directory inclusion is free, "not pay-to-play and never will be." Connector terms do not grant Anthropic training rights on partner data. — [Claude connectors partnership FAQ (search snippet; page returned 404 on fetch)](https://claude.com/docs/connectors/building/partnership-faq)
- Submission requirements include OAuth 2.0 for authenticated services, tool annotations, documentation and a privacy policy. Missing privacy policies lead to rejection. — [Claude connectors submission docs (search snippet)](https://claude.com/docs/connectors/building/submission)
- Finance-vertical connectors must not enable irreversible or high-consequence actions without explicit user confirmation. — [Claude connectors policies (search snippet; fetch 404)](https://claude.com/docs/connectors/policies)
- A developer submission portal for plugins and connectors opened Sept 25, 2026 for paid-plan users (third-party coverage). — [Unite.AI](https://www.unite.ai/anthropic-opens-directory-submission-portal-for-claude-plugins/); [Crypto Briefing](https://cryptobriefing.com/claude-plugin-mcp-connector-submission-portal/)
- Custom remote connectors work on Free (limited to one), Pro, Max, Team and Enterprise plans. — [Claude Help Center: custom connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) (via search summary)
- **Anthropic Usage Policy, effective Nov 12, 2026.** The financial high-risk area covers "a personalized recommendation to buy, sell, hold, or allocate among specific investment products" and individual tax advice or preparation. It excludes "General information or educational content" and "how investing works, without applying it to the individual's circumstances." Requirements: "A qualified person must meaningfully review a High-risk AI Recommendation, with the authority to change or modify it," and the individual "must be clearly told that AI was used to produce it." These apply "to anyone who uses our products to make a High-risk AI Recommendation," not only consumer-facing products. — [Anthropic Usage Policy](https://www.anthropic.com/aup); [Anthropic 2026 usage policy update](https://anthropic.com/news/2026-usage-policy-update)

### Inferences
- **The AI plugin is a free funnel, not a till.** In ChatGPT: build the free "¿cuál es mi inflación?" app. If a paid "monthly analysis" exists, the user buys it on the project's own website, then signs in from ChatGPT. The app itself must never show plans or upgrade prompts. In Claude: a remote MCP connector with OAuth to the project's service follows the same pattern. I found no explicit rule against paid-account gating in Claude, but also no in-product payments.
- **Design the output so it falls clearly outside "high-risk AI recommendation" and "asesoría de inversiones."** Safe framing: "Your personal inflation over the last 12 months was 6.1%; to preserve purchasing power your savings need a nominal return of at least 6.1%," plus general education on what real return means. Do not say "move your money to fund X / CETES / allocate 60/40." Comparing against a public reference rate (e.g., the published CETES rate or UDI) as *information* is probably fine but is borderline. LAWYER.
- **Do not collect bank credentials through ChatGPT** (explicitly prohibited). Collecting them through a Claude connector also runs against data minimization. Use statement or CSV upload, declared spending, or OAuth to the project's own service, which may use a licensed aggregator.
- Write the privacy policy once and reuse it for OpenAI, Anthropic and the LFPDPPP aviso de privacidad (§3c).

### Gaps
- The full current text of Anthropic's Software Directory Policy and Terms could not be retrieved (404s on claude.com docs pages). So there is no direct confirmation of rules on paid accounts, advertising or revenue share in the Claude directory.
- OpenAI has given no public timeline for allowing digital-goods or subscription monetization in ChatGPT apps.
- No revenue-share figures exist for either platform, because neither currently runs a developer payments program for digital goods.

---

## 3. Mexican regulatory lines (CNBV investment advice, Ley Fintech/ITF, LFPDPPP 2025, PROFECO subscriptions, INEGI terms, IMPI)

### Takeaway
- **Computing and explaining a person's inflation is not regulated financial activity.** Turning it into individualized recommendations about specific securities or financial products, offered habitually and professionally, is *asesoría de inversiones* under LMV Art. 225 and requires CNBV registration, certified staff and a conduct manual. Do not cross that line without registering.
- **Ley Fintech:** a calculator or PFM tool is not one of the ITF activities that need authorization (crowdfunding/IFC, e-money/IFPE, sandbox models). Regulated transactional open-finance APIs still do not exist, so bank data must come from the user (uploads) or a licensed or contracted aggregator.
- **LFPDPPP 2025** (in force since March 21, 2025): standard controller duties, a privacy notice, and new consent for new purposes. The supervising authority is now the Secretaría Anticorrupción y Buen Gobierno.
- **PROFECO:** the LFPC reform of December 2025 requires express consent for recurring charges, a renewal notice at least 5 days ahead, cancellation by the same channel, immediate and free cancellation, and no forced terms or penalties. Fines run up to about MXN 3 million.
- **INEGI:** commercial use of its data is explicitly allowed with attribution, but you may not imply INEGI endorsement.
- **IMPI:** descriptive names and names of government programs (e.g., "INPC") are not registrable as trademarks.

### Cited Findings
**3a. Asesoría de inversiones (CNBV / LMV):**
- LMV Art. 225 defines *asesores en inversiones* as people who, without being securities intermediaries, habitually and professionally provide portfolio management (making investment decisions on behalf of third parties) or *asesoría de inversión en valores*, which includes analysis and issuing "recomendaciones de inversión de manera individualizada." They must register with the CNBV. Individuals need good standing, a satisfactory credit history, and certification from a self-regulatory body recognized by the CNBV. Firms (S.C., S.A., S. de R.L.) need offices, shareholder disclosure and a conflicts-of-interest conduct manual. First paragraph amended by DOF 28-12-2023. — [mLey: LMV Art. 225](https://mley.mx/LMV/articulo/225/) (unofficial compilation; verify on diputados.gob.mx)
- The CNBV confirms that "para ser asesor en inversiones se requiere registrarse ante la Comisión." Advisers with no ties to financial groups add "independiente" to their name; otherwise they must disclose the ties. Registration can be cancelled for losing honorability or certification, or after six months without operations (Art. 227 Bis). — [CNBV: Asesores en inversiones (snippet)](https://cnbv.gob.mx/SECTORES-SUPERVISADOS/ASESORES_EN_INVERSIONES/Paginas/PreguntasFrecuentes.aspx) (direct fetch returned 503); [mLey LMV 227 Bis](https://mley.mx/LMV/articulo/227-bis/index.html.md)
- Requirements were tightened after the Black Wallstreet Capital fraud (2023 reform). — [El CEO](https://elceo.com/mercados/cnbv-elevara-requisitos-para-asesores-en-inversiones-tras-el-caso-de-bwc/)
- The CNBV's *Disposiciones de servicios de inversión*, as reproduced by banks, define asesoría as giving "recomendaciones o consejos personalizados… que le sugieran la toma de decisiones de inversión sobre uno o más productos financieros." A service is "no asesorado" when the entity only takes orders "o emite recomendaciones generalizadas." — [BBVA Guía de Servicios de Inversión](https://www.bbva.mx/content/dam/public-web/mexico/documents/18-sep/bpp/guia-de-servicios-de-inversion.pdf); [Banorte: Prácticas de venta](https://www.banorte.com/dam/jcr:91a793d2-5ecc-43ae-ac3a-7fd1469af2a0/15.%20Pr%C3%A1cticas%20de%20Venta%20y%20Perfilamiento%20de%20Clientes.pdf); [Vinci Compass Guía 2026](https://latam.vincicompass.com/wp-content/uploads/mexico/Operadora/Guía%20de%20Servicios%20de%20Inversión/SINV%20Guía%20de%20Servicios%20de%20Inversión%202026.pdf) (institutional paraphrases, not the official CNBV text)
- Regional precedent on "finfluencers": Chile's CMF said in June 2024 that influencers giving investment recommendations must register as advisers. Spain's CNMV found about 10% of roughly 100 finfluencer profiles broke the rules or possibly gave unauthorized personalized advice, and published a guide separating education from recommendation. — [Diario Financiero (Chile)](https://www.df.cl/mercados/banca-fintech/cmf-influencers-que-brinden-recomendaciones-financieras-deberan); [Forbes España](https://forbes.es/economia/902954/la-cnmv-detecta-que-un-10-de-los-finfluencers-incumplen-las-normas-sobre-recomendaciones-de-inversion/)

**3b. Ley Fintech / ITF / open finance:**
- The Ley Fintech (2018) regulates IFPE (e-money) and IFC (crowdfunding) and has a sandbox for "modelos novedosos." As of July 2026 the CNBV had authorized 89 ITFs. The sandbox had 9 applications, 5 rejected, 4 withdrawn and none approved. In Feb 2026 the CNBV announced a comprehensive regulatory review covering crypto and open finance, with no timeline. — [Facephi Observatory, Jul 2026](https://facephi.com/observatory/en/fintech-law-in-mexico-2026-competition-sandbox-and-new-financial-models/)
- Art. 76 requires standardized APIs for financial entities, ITFs, credit bureaus and others, so they can connect with "terceros especializados en tecnologías de la información." The CNBV published the open-data API rules in the DOF on June 4, 2020. Rules for aggregated and transactional data remain unpublished, and an amparo was filed in Jan 2026 over the omission. — [Holland & Knight, Jul 2020](https://www.hklaw.com/es/insights/publications/2020/07/open-banking-has-arrived-in-mexico); [Garrigues](https://www.garrigues.com/es_ES/garrigues-digital/fintech-mexico-aprueba-disposiciones-caracter-general-relativas-apis); [Facephi](https://facephi.com/observatory/en/fintech-law-in-mexico-2026-competition-sandbox-and-new-financial-models/)
- Example: aggregator Belvo obtained IFPE authorization for its *payments* business (Belvo Pagos). The license covers payments, not aggregation. — [LatamFintech](https://www.latamfintech.co/articles/belvo-fintech-de-open-banking-obtiene-la-autorizacion-de-la-cnbv-para-operar-como-ifpe-en-mexico)

**3c. Data protection, LFPDPPP 2025:**
- Published in the DOF on March 20, 2025 and in force since March 21, 2025. It abrogates the 2010 law. The Secretaría Anticorrupción y Buen Gobierno replaces the INAI. Consent may be express or tacit, and tacit consent is valid unless the law requires express consent. Using data for a new purpose needs new consent. The privacy notice must list the data processed, flag sensitive data and separate the purposes that need consent, with a simplified notice pointing to the full one for electronic collection. Sanctions are set in UMA. Amparo before specialized courts replaces nullity suits before the TFJA. The law also allows binding self-regulation schemes. — [Garrigues](https://www.garrigues.com/es_ES/noticia/mexico-nueva-ley-federal-proteccion-datos-personales-posesion-particulares-introduce)
- Sensitive data requires express written consent. The definition of personal data no longer requires it to belong to a natural person. — [Littler](https://www.littler.com/es/news-analysis/asap/mexico-tiene-nueva-ley-en-materia-de-proteccion-de-datos-personales); [GT Law](https://www.gtlaw.com/es/insights/2025/3/nueva-ley-general-proteccion-de-datos)
- The 2025 law keeps the same base principles and duties as the 2010 law. — [AMDA circular annex](https://www.amda.mx/wp-content/uploads/2025/04/anexo%201%20de%20circular%2023%20de%202025.pdf); [Basham](https://basham.com.mx/en/iniciativa-en-materia-de-transparencia-y-proteccion-de-datos-personales/)

**3d. Consumer protection for subscriptions (PROFECO / LFPC):**
- The Senate unanimously approved a reform requiring cancellation that is "inmediata, clara y gratuita" (online, by phone or in person). Recurring charges must be disclosed (frequency, amount, date) and require explicit consent. Automatic renewals must be notified at least 5 calendar days ahead. No forced terms or cancellation penalties are allowed, and PROFECO can fine up to MXN 3 million. — [El Informador, Nov 12 2025](https://www.informador.mx/mexico/prohiben-a-empresas-digitales-penalizar-por-cancelar-suscripciones-20251112-0009.html)
- The reform was published in the DOF on Dec 12, 2025 and took effect Dec 13, 2025. PROFECO says the new fractions of Art. 76 Bis ensure that any subscription can be cancelled through the same channel used to sign up. Subscriptions bought through Google Play or the App Store are cancelled through the store. — [El Imparcial, Dec 13 2025](https://www.elimparcial.com/mexico/2025/12/13/ya-esta-en-vigor-nueva-reforma-a-la-ley-federal-del-consumidor-te-protege-de-cobros-fantasma-en-plataformas-de-servicios-digitales/); [El Imparcial, Mar 17 2026](https://www.elimparcial.com/dinero/2026/03/17/profeco-obliga-a-plataformas-a-avisar-5-dias-antes-de-renovar-suscripciones-y-facilitar-cancelacion-sin-trabas-desde-2025/); [PROFECO on X](https://x.com/Profeco/status/2034003738483167527)

**3e. INEGI terms of free use:**
- Permitted: copying and distributing (without altering metadata), publishing, adapting, extracting, and "use it commercially, including as an input for other products or services." Obligations: credit INEGI as "Fuente: INEGI, nombre del producto de donde se extrae la información" (plus the update date where applicable); tell users when the data has been analyzed or transformed and do not present the result as INEGI's analysis; do not suggest INEGI endorses or sponsors the use. INEGI is not responsible for how results are interpreted. The terms are governed by the LSNIEG, with disputes before federal courts in CDMX. — [INEGI Términos de uso / libre uso](https://www.inegi.org.mx/inegi/terminos.html)

**3f. Trademarks (IMPI, LFPPI Art. 173):**
- Not registrable: generic and common-use terms (fr. I, I Bis); signs that are "descriptivos de los productos" or services (fr. IV); unauthorized "denominaciones, siglas, símbolos, emblemas, nombres de programas o proyectos" of governmental or international organizations (fr. VII); and signs confusingly similar to earlier marks (fr. XVIII). Acquired distinctiveness through use can overcome fr. I–VI. — [mLey: LFPPI Art. 173](https://mley.mx/LFPPI/articulo/173/) (unofficial; last reform 15-01-2026 per [SDV compendio](https://sdv.com.mx/compendio/ley-federal-de-proteccion-a-la-propiedad-industrial/articulo-173/))

### Inferences
- **Lines not to cross (absent a license or registration):**
  1. Individualized "buy, sell or allocate to product X" recommendations given habitually and for a fee. This triggers LMV 225 and also the Anthropic and OpenAI high-risk rules. The monthly AI agent should explain *your* inflation and general concepts (real return, UDIs, what "beating inflation" means), never pick products or suggest allocations for the individual. LAWYER: whether "your inflation is 6.1%; CETES at 28 days currently pays X%" counts as an individualized recommendation.
  2. Moving money, executing trades, or holding customer funds. That is IFPE or intermediary territory and is banned by both AI platforms anyway.
  3. Asking for or storing bank usernames and passwords. It conflicts with OpenAI's rules and with data minimization, and probably with bank contract terms (unverified). Use uploads or a licensed aggregator.
  4. Selling or sharing individual-level data, or reusing data for new purposes without new consent (LFPDPPP).
  5. Subscriptions with friction: anything other than one-click cancellation through the same channel, no 5-day renewal notice, annual lock-ins or cancellation fees (LFPC Art. 76 Bis).
  6. Branding that implies INEGI or Banxico endorsement. INEGI's terms prohibit it, and the user's Banxico past makes this extra sensitive. Use a disclaimer such as "Cálculos propios con datos del INPC (Fuente: INEGI, INPC). No es un producto oficial del INEGI ni de Banco de México."
- **Safe design pattern:** a "benchmark, not advice" disclaimer on every output; open methodology in the repo; a privacy notice compliant with the 2025 LFPDPPP; local-first or self-host option (the strongest privacy story, since the data never leaves the device); opt-in aggregate statistics only.
- **B2B contracts:** when a fintech or Afore embeds the widget, the contract should make clear that the client is the controller for its users' data and handles its own CNBV/CONSAR suitability duties. LAWYER.
- **Former Banxico staff:** check post-employment ethics rules for Banxico ex-staff (confidentiality, cooling-off periods for dealing with the institution) before pursuing Banxico or MIDE partnerships or using insider-sounding claims. Not researched here; LAWYER/HR.

### Gaps
- The official CNBV FAQ page was unavailable (HTTP 503), and the official text of the current *Disposiciones de servicios de inversión* was not read; only bank paraphrases were.
- No CNBV guidance specific to finfluencers or educational tools was found for Mexico.
- Whether the reglamento of the 2025 LFPDPPP has been published and what it says on anonymization or "disociación" and on profiling and automated decisions. Not verified.
- Whether financial or transactional data counts as "sensitive" under the 2025 LFPDPPP. It is not in the cited non-exhaustive list.
- The DOF text of the LFPC subscription reform was not read directly (only press and PROFECO statements). The voluntary e-commerce norm (NMX-COE-001-SCFI-2018) was not reviewed.
- Banxico post-employment restrictions for former staff were not researched.

---

## 4. Financial education and go-to-market in Mexico

### Takeaway
Mexico has broad access to financial products but weak financial habits. In ENIF 2024, 76.5% of adults have at least one product and 69.1% of account holders use a banking app. Yet only 23.9% of those who keep records budget, only 19.5% of them use apps or tools, the literacy score has been stuck at 58/100 since 2018, and about 6% have taken any financial course. Inflation hits poorer, food-heavy households harder. That argues for a "declared basket" mode with no bank connection, and for a message about *your* inflation versus the official figure. The established channels are CONDUSEF's Semana Nacional de Educación Financiera (every October, 75+ institutions in 2026), the MIDE (a museum created by Banxico and financial institutions), universities, podcasts (about 34M monthly listeners estimated for 2022) and TikTok/YouTube "FinTok," where trust is a known problem.

### Cited Findings
**ENIF 2024** (INEGI-CNBV, published Mar 13, 2025; ages 18–70 unless noted) — [INEGI Comunicado 49/25](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/enif/ENIF2024_CP.pdf):
- 76.5% have at least one formal financial product (68.4% in 2015): 80.9% of men and 72.8% of women. Lowest among indigenous-language speakers (58.2%) and in localities under 15k people (65.5%).
- Formal savings account: 63.0%. Formal credit: 37.3%. Insurance: 22.9%. Afore: 42.2% (51.4% of men vs 34.2% of women).
- Accounts opened via internet or non-bank apps rose 7.6 points since 2021. Among holders of formal savings accounts, mobile-app use for checking or moving money rose from 54.3% (2021) to 69.1% (2024).
- 2.1% had bought or invested in crypto. 38.0% knew CoDi (12.8% of them used it). 18.5% knew DiMo.
- For old age, 68.2% would rely on government support (up 11.0 points from 2021) and 67.3% on continuing to work.
- **Expense tracking:** 65.3% kept some record of their or their household's spending. Within that group, 51.8% separated money for payments and debts, 39.5% kept receipts or debt records, 24.8% wrote down expenses, **23.9% kept a budget** or a record of income and expenses, and **19.5% used direct debit, mobile apps or financial management tools.**
- **Literacy:** the score has been unchanged at **58/100 since 2018** (ENIF 2018/2021/2024). About 6% of adults took a course on saving, budgeting or responsible credit, and about 23% keep a budget. — [BBVA Research, Nov 13 2025](https://www.bbvaresearch.com/publicaciones/mexico-educar-para-incluir-rumbo-a-la-sostenibilidad-financiera/)
- A congressional document gives a knowledge score of 58.2% and a financial-behavior score of 48.2%. — [Gaceta Parlamentaria, Oct 21 2025](https://gaceta.diputados.gob.mx/Gaceta/66/2025/oct/20251021-II-5.html) (political source)
- The ENIF questionnaire includes items on simple and compound interest and the concept of inflation, but no 2024 breakdown of the inflation item was found. — [BBVA Research PDF (via search summary)](https://www.bbvaresearch.com/wp-content/uploads/2025/03/Tenencia-de-productos-financieros-y-acceso-a-cursos-basicos-para-finanzas-en-2024.pdf)
- The National Financial Education Strategy is to be folded into the 2025–2030 National Financial Inclusion Policy, which was still being drafted in Nov 2025. — [BBVA Research](https://www.bbvaresearch.com/publicaciones/mexico-educar-para-incluir-rumbo-a-la-sostenibilidad-financiera/)

**Who is most affected by inflation:**
- Poor, rural, indigenous and larger households face higher inflation; cumulatively about 6.5% more than rich households (2015–2023). — [UNAM RIE](https://journals.unam.mx/index.php/rie/article/view/90415)
- In 2022 the decile-1 basket rose 8.74% versus 7.48% for top-income households. Food is about 50% of spending for decile 1 versus about 28% for decile 10. — [IMCO](https://imco.org.mx/la-inflacion-afecta-mas-a-las-familias-que-menos-tienen/)
- April 2026: fruits and vegetables were up 21.43% year on year while headline inflation was 4.45%. Expansión frames this as eroding the purchasing power of low-income households. — [Expansión](https://expansion.mx/economia/2026/05/07/inflacion-inegi-abril-2026-hogares-pobres-alimentos)

**Channels and partners:**
- **SNEF 2026 (CONDUSEF):** main venue the Monumento a la Revolución, running until Oct 18, 2026, with more than 75 participating institutions (banks, insurers, Afores, public bodies, fintechs), 102 stands, and four pillars: security, resilience, control and financial freedom. — [Excélsior](https://www.excelsior.com.mx/finanzas/aprovecha-semana-educacion-financiera)
- SNEF 2025 (18th edition) ran in person in CDMX Oct 23–26, then online Oct 27–31. — [Expansión, Oct 15 2025](https://expansion.mx/finanzas-personales/2025/10/15/leva-invierte-semana-nacional-educacion-financiera)
- A BBVA article reports a SNEF edition reaching more than 92 thousand people nationwide (edition year unclear). — [BBVA México](https://www.bbva.com/es/mx/salud-financiera/la-trascendencia-de-la-educacion-financiera/)
- Universities take part in SNEF, for example UAEH and UdeG. — [UAEH](https://www.uaeh.edu.mx/noticias/600); [UdeG](https://comsoc.udg.mx/printpdf/94623)
- **MIDE:** created by Banco de México and several private financial institutions. The decree was issued in 2002 and the museum opened in 2006, billed as the first interactive economics museum in the world. More than 1.5M children and young people have visited. It has IDB recognition, a 2012 agreement with the Banque de France, and Global Money Week 2025 workshops on cognitive biases. Its founding director Silvia Singer describes an approach built on neuroeducation and behavioral economics. — [Expansión, Sep 3 2025](https://expansion.mx/finanzas-personales/2025/09/03/el-mide-revela-su-formula-asi-logro-que-la-economia-sea-un-juego-atractivo-para-sus-visitantes); [IPN repository](https://repositoriodigital.ipn.mx/bitstream/123456789/19704/1/MUSEO.pdf); [Global Money Week Mexico](https://www.globalmoneyweek.org/countries/109-mexico.html); [Museo Banco de México GMW press note](https://museobancodemexico.mx/documentos/GMW_NOTA_DE_PRENSA_FINAL.pdf)
- Banxico already publishes an official app with indicators, including inflation. — [Apple App Store: Banxico](https://apps.apple.com/mx/app/id727371545)
- **Podcasts:** monthly podcast listeners in Mexico were estimated at 22M (2020), 28M (2021) and 34M (2022, PwC). — [DPL News](https://dplnews.com/?p=133528)
- **Finfluencers:** they have grown on YouTube, TikTok and Instagram and earn from ads, courses, e-books and affiliations with banks and investment platforms. Only those with large audiences live off it. — [El Imparcial, Mar 21 2025](https://www.elimparcial.com/dinero/2025/03/21/influencers-financieros-ganan-dinero-compartiendo-educacion-financiera-en-redes-conoce-los-numeros/)
- Forbes México warns about fake finance influencers and "dinero rápido" investment scams. — [Forbes México](https://www.forbes.com.mx/esta-es-la-forma-de-detectar-a-falsos-influencers-de-finanzas-personales/)
- "FinTok" on TikTok has boosted creators offering investment tips (2023). — [Publimetro](https://www.publimetro.com.mx/noticias/2023/12/31/tiktok-fintok-catapulta-a-influencers-que-ofrecen-consejos-financieros/)

### Inferences
- **Positioning:** "El INPC es el promedio; tu inflación es la tuya." The message is a *measurement and education* tool, a "termómetro" for your pocket, which supports the non-advice regulatory framing in §3.
- **Priority audiences:**
  1. Salaried middle class negotiating raises or deciding whether a raise "le ganó a su inflación" (peaks around January wage revisions and the "cuesta de enero").
  2. New digital investors (69% app use, growth in non-bank accounts) who want a personal real-return benchmark.
  3. Lower-income, food-heavy households, who need the no-bank "declared basket" mode, simple language and WhatsApp-friendly sharing.
  4. Journalists and academics, an early-adopter and amplification channel, since the open methodology and data are citable.
- **Go-to-market sequence:** (1) publish the open-source repo plus a free web calculator alongside a data-journalism piece (personal inflation by decile or profile using public ENIGH weights) pitched to El Economista, El Financiero or Expansión around an INPC release; (2) launch the free ChatGPT app and Claude connector as "pregúntale a la IA cuál es tu inflación"; (3) apply for a stand or talk at SNEF 2027 (October) and approach MIDE for an exhibit or workshop tie-in; (4) university partnerships (economics and finance clubs, thesis datasets); (5) carefully chosen creators who do education, not stock picking, reviewed against the §3a lines. Each piece of content should carry the "no es asesoría de inversión" disclaimer.
- **The user's credibility asset** (ex-Banxico economist) is strong for trust, but needs strict separation from any implied official endorsement (§3 inference 6).

### Gaps
- No reliable, sourced ranking of Mexican personal-finance creators or podcasts with audience metrics was found. Named examples need direct checks on Spotify, YouTube or Rephonic.
- The official 2026 SNEF calendar and CONDUSEF's criteria for private participants were not retrieved.
- How MIDE or Banxico Educa partner with private or open-source projects is not documented in what I found.
- No 2024 breakdown of the ENIF inflation-concept question was found.

---

## 5. Naming: candidates and sanity checks

### Takeaway
The strongest options combine a playful, coined Mexican-flavored brand with a plain descriptive tagline ("tu inflación personal con datos del INPC/INEGI"). The best balance of memorability, no conflicts found, and free domains: **Bolsillómetro**, **Canastómetro**, **Inflacionómetro** and **¿Le Ganas?** (benchmark framing). **TuInflación** and **CuántoMeSube** work as descriptive secondary names. Avoid **MiINPC/INPCito** (INPC is INEGI's product name; LFPPI Art. 173 VII and INEGI's no-endorsement rule), **"IPC"** names (in Mexico "IPC" commonly means the BMV stock index), **MiInflación** (already used by several Argentine repos, and descriptive), **CuántoSubió** (used by Costa Rican and Paraguayan price trackers), and **Varómetro/Lanómetro** (.com already registered; lanometro.com only on 2026-10-20). IMPI's MARCia could not be queried automatically, so a manual trademark search there is a required next step.

### Cited Findings
**Method (run 2026-10-26):**
- *.com:* Verisign RDAP (404 means not registered, 200 means registered). *.app:* Google Registry RDAP (`pubapi.registry.google/rdap`), per the IANA RDAP bootstrap. *.mx / .com.mx:* NIC México has no RDAP in IANA's bootstrap and rdap.org returned 404, so I used DNS NS lookups through Cloudflare DNS-over-HTTPS. NXDOMAIN means probably unregistered; this is a signal only. Controls: google/inegi resolved as registered, and a random string came back free on all four.
- *GitHub:* repository and user search through the GitHub search API, because direct github.com page checks were blocked by the sandbox proxy.
- *IMPI MARCia (marcia.impi.gob.mx):* the page is a JS app ("Marcanet") and returned no searchable content, so **no trademark check was possible.**

**Candidate list (36 names; ASCII handle in parentheses):**
- "Mi inflación / IPC" family: MiInflación (miinflacion), TuInflación (tuinflacion), Inflación Propia (inflacionpropia), Mi Índice (miindice), Índice Propio (indicepropio), MiINPC (miinpc), INPCito (inpcito), TuIPC (tuipc), IPC Personal (ipcpersonal), IPCito (ipcito), Mi Deflactor (mideflactor), Mi Tasa Real (mitasareal).
- "-ómetro" family: Inflacionómetro (inflacionometro), Bolsillómetro (bolsillometro), Canastómetro (canastometro), Varómetro (varometro, a pun on barómetro plus "varo"), Lanómetro (lanometro), Chivómetro (chivometro), Preciómetro (preciometro), Tortillómetro (tortillometro), Mandadómetro (mandadometro), Pesómetro (pesometro).
- Colloquial and question names: ¿Cuánto Subió? (cuantosubio), ¿Ya Subió? (yasubio), ¿Cuánto Me Sube? (cuantomesube), ¿Le Ganas? / Le Ganas a la Inflación (leganas / leganasalainflacion / ganalealainflacion), Cuesta Arriba (cuestaarriba), El Gasto / Mi Gasto (elgasto / migasto), Carestía (carestia), Mi Poder de Compra (mipoderdecompra / poderdecompra), Mi Canasta / Canasta Personal (micanasta / canastapersonal), Mi Bolsillo (mibolsillo), InflaYo (inflayo), InflaMía (inflamia), Mi Precio (miprecio), Tianguis Index (tianguisindex).

**Domain signals (2026-10-26):**
- **Free on .com, .app, .mx and .com.mx:** miinflacion, tuinflacion, inflacionpersonal, inflacionometro, miinpc, inpcito, ipcpersonal, bolsillometro, canastometro, chivometro, cuantosubio, yasubio, mandadometro, inflayo, mideflactor, indicepropio, inflacionalamedida, inflaciontuya, tuipc, inflacionpropia, cuantomesube, mipoderdecompra, canastapersonal, leganas, mitasareal, ganalealainflacion, leganasalainflacion, tianguisindex.
- **.com already registered:**
  - varometro.com (registered 2023-05-10, Cloudflare NS)
  - lanometro.com (registered **2026-10-20**, parked); lanometro.com.mx also resolves
  - preciometro.com (2025-02-11)
  - tortillometro.com (2025-07-22, parked)
  - miipc.com (2012)
  - inflamia.com (2025-07-15)
  - micanasta.com (2006); micanasta.app also taken
  - mibolsillo (.com, .app, .mx and .com.mx all taken)
  - cuestaarriba (.com and .mx taken)
  - poderdecompra.com, elgasto.com, migasto.com and migasto.app, carestia.com, mindice.com, miindice.com, ipcito.com, pesometro.com, miprecio.com and miprecio.app
  - (RDAP lookups, Verisign/Google; registration dates from the Verisign RDAP "events" field.)

**GitHub conflicts (repo search, 2026-10-26):**
- "MiInflacion": LewanX/MiInflacion ("Calculadora de inflación Argentina en tiempo real. Datos oficiales del INDEC," Mar 2026); pironiagustin05-arch/miinflacion ("medir la inflación individual de cada persona/familia," Jun 2026); pironiagustin-arg/Miinflacion. — [GitHub search](https://github.com/search?q=miinflacion&type=repositories) (via GitHub API)
- "inflacion-personal": ariasmarianoo/inflacion-personal (Argentina 2026), LorenzoFerreyra/inflacion-personal-ar, adrianvalencia1/calculadora-inflacion. A Claude Code plugin for Argentine personal finance with inflation-adjusted spending also exists ("guita"). — [github.com/kvothesson/guita](https://github.com/kvothesson/guita); [github.com/ariasmarianoo/inflacion-personal](https://github.com/ariasmarianoo/inflacion-personal)
- "tu-ipc": jenarvaezg/tu-ipc ("Calculadora de IPC personal basada en datos del INE," Spain, 4 stars, updated Oct 2026); D1egoLopez/Calculadora-IPC-Personal and gonza2018/mi-propio-ipc (Argentina). — [github.com/jenarvaezg/tu-ipc](https://github.com/jenarvaezg/tu-ipc); [github.com/gonza2018/mi-propio-ipc](https://github.com/gonza2018/mi-propio-ipc)
- "cuantosubio": bbaltodanodev-lang/cuantosubio-cr (Costa Rica price and canasta tracker, Sep 2026); laguardiia/cuantosubiopy-scraper and cuantosubiopy-frontend (Paraguay, Aug 2026). — [github.com/bbaltodanodev-lang/cuantosubio-cr](https://github.com/bbaltodanodev-lang/cuantosubio-cr)
- "varometro": ppvaladez/varometro-api (Sep 2026, empty); MatiasIsaac/nat-ali4 (described "Varometro"); evilrender23/varometro-de-sarcasmo-r1. — [github.com/ppvaladez/varometro-api](https://github.com/ppvaladez/varometro-api)
- "leganas": only unrelated "legana" repos and mecmarketing26-cloud/leganastealdolar- (an Astro site, Apr 2026). — [GitHub search](https://github.com/search?q=leganas&type=repositories)
- **No repos or users found** for inflacionometro, bolsillometro, canastometro, chivometro, inpcito, tuinflacion, miinpc, mitasareal, cuantomesube, inflacionpropia, yasubio or mandadometro (GitHub repo and user search, 2026-10-26).
- Existing Mexican INPC repos (potential collaborators, not name conflicts): portfedh/Mexico_CPI (an INPC inflation calculator), nanisadw3/mcp-banxico (an MCP server for Banxico FX, INPC and UDIs, Sep 2026), alanvaa06/Inflation_Mexico. — [github.com/portfedh/Mexico_CPI](https://github.com/portfedh/Mexico_CPI); [github.com/nanisadw3/mcp-banxico](https://github.com/nanisadw3/mcp-banxico)

**Web and app-store conflicts:**
- No app named "Inflacionómetro/Inflaciómetro" was found in Mexico. Nearby names: Banxico's official app, an iOS app "InflaMate" (tracks prices of 12 basic goods), and the Argentine app "Infleta." — [Apple App Store: InflaMate](https://apps.apple.com/mx/app/inflamate/id6744309909); [Unidiversidad (Infleta)](https://www.unidiversidad.com.ar/infleta-la-app-para-cuidar-los-pesos-y-calcular-mejor-la-forma-de-pago26)
- No web results for "Bolsillómetro" or "Canastómetro." Results for "Varómetro" were dominated by "variómetro" (an aviation instrument). — (WebSearch, 2026-10-26; no relevant hits)
- Argentina's INDEC launched an official personal-inflation calculator, which is a precedent for the concept and for generic naming. — [Cadena 3](https://www.cadena3.com/noticia/informados-al-regreso/el-indec-lanzo-una-calculadora-de-inflacion-personal-como-funciona_402614)
- INEGI has an official "Calculadora de Inflación" (general INPC, between two dates). — [INEGI Calculadora de Inflación (PDF)](https://en.www.inegi.org.mx/app/indicesdeprecios/documentos/Calculadora_de_Inflacion.pdf)

**Meanings and connotations:**
- **"IPC" in Mexico** usually means the S&P/BMV IPC (Índice de Precios y Cotizaciones), the main BMV stock index of 35 companies, in use since 1978. Names like "TuIPC," "IPC Personal" or "IPCito" would be read as stock-market products and invite the very investment-advice confusion to avoid. — [S&P DJI: S&P/BMV IPC](https://www.spglobal.com/spdji/es/indices/equity/sp-bmv-ipc/); [Expansión](https://expansion.mx/dinero/2018/03/22/inversionista-primerizo-lo-que-debes-de-saber-del-indice-lider-de-la-bmv)
- **"INPC"** is INEGI's product name. LFPPI Art. 173 fr. VII bars unauthorized registration of governmental organizations' "siglas… nombres de programas o proyectos," and INEGI's terms bar implying endorsement. — [mLey LFPPI 173](https://mley.mx/LFPPI/articulo/173/); [INEGI Términos](https://www.inegi.org.mx/inegi/terminos.html)
- **"Chivo":** used colloquially for wages or money (anecdotal: "los abuelos llamaban 'chivo' a su salario," alongside "feria" and "lana"). It also means "chivo expiatorio" (scapegoat) and, per the RAE/ASALE for Mexico, a snitch. — [Chilango](https://www.chilango.com/general/formas-alternas-de-llamar-al-dinero/amp/); [RAE/ASALE via ClubMitsubishi FAQ](https://www.clubmitsubishiasx.com/faq/que-es-ser-un-chivo) (low-quality aggregator)
- **"Lana," "feria"** are colloquial Mexican words for money. — [Chilango](https://www.chilango.com/general/formas-alternas-de-llamar-al-dinero/amp/)
- **Descriptive names** ("Mi Inflación," "Tu Inflación," "Inflación Personal," "Mi Poder de Compra") face LFPPI Art. 173 fr. IV, which bars signs descriptive of the services, unless distinctiveness is acquired through use. — [mLey LFPPI 173](https://mley.mx/LFPPI/articulo/173/)

### Inferences
**Sanity-check summary of the top ~12** (domains: c = .com, a = .app, m = .mx; "free" means an RDAP 404 or DNS NXDOMAIN signal, not a guarantee):

| Name | Domains c/a/m | GitHub | Trademark registrability (IMPI, inferred) | Meaning / risk | Verdict |
|---|---|---|---|---|---|
| **Bolsillómetro** | free/free/free | none | Coined, likely distinctive | "Bolsillo" means pocket (spending), clear and friendly | **Top pick** |
| **Canastómetro** | free/free/free | none | Coined; "canasta" alone is generic | Evokes "canasta básica"/INPC basket; may sound food-only | **Top pick** |
| **Inflacionómetro** | free/free/free | none | Semi-descriptive; may draw fr. IV objection | Very clear; a bit long (15 letters) | Strong |
| **¿Le Ganas?** (leganas) | free/free/free | only unrelated "legana" | Distinctive (question form) | Matches the benchmark use case ("¿le ganas a tu inflación?"); might read as a betting or contest app | Strong (good for the AI plugin) |
| **Chivómetro** | free/free/free | none | Coined | Slang for pay is anecdotal; "chivo" also means scapegoat or snitch; possible association with El Salvador's government "Chivo" bitcoin wallet (not verified in this research) | Fun but risky |
| **Varómetro** | **.com taken (2023)**/free/free | 3 small repos | Coined; pun on "barómetro" | "Varo" is slang for money (not sourced here); repo conflicts | Second tier |
| **Lanómetro** | **.com taken 2026-10-20; .com.mx taken**/free/free | none | Coined | "Lana" means money | Avoid (just registered by someone) |
| **TuInflación** | free/free/free | none | Descriptive, hard to register | Clear Spanish product name | Use as tagline or secondary |
| **¿Cuánto Me Sube?** | free/free/free | none | Mildly distinctive | Conversational; maps to "what is my inflation?" | Good secondary / AI-plugin name |
| **MiInflación** | free/free/free | 3 Argentine repos | Descriptive | Already in use as an Argentine project name | Avoid as the main brand |
| **¿Cuánto Subió?** | free/free/free | Costa Rica and Paraguay price trackers | Mildly distinctive | Crowded in LatAm | Avoid |
| **MiINPC / INPCito** | free/free/free | none | Likely barred (fr. VII) or needs INEGI authorization | Implies official INEGI product | Avoid as brand; use "basado en el INPC" in the tagline |
| **TuIPC / IPC Personal / IPCito** | mostly free (ipcito.com taken) | Spain's tu-ipc; Argentine repos | Descriptive | In Mexico "IPC" means the BMV stock index | Avoid |

- **Recommended structure:** Brand = **Bolsillómetro** (or Canastómetro). Tagline = "Tu inflación personal, con datos del INPC (INEGI)." AI app name = "¿Cuál es mi inflación? — Bolsillómetro." Repo = `bolsillometro` and package = `bolsillometro`, since ASCII handles avoid accent problems. Register the .com, .mx and .app together. File at IMPI in class 9 (software) and class 36 or 42 (financial information / SaaS). Which Nice classes apply should be confirmed: LAWYER/IP agent.
- **ASCII vs. accents:** use unaccented handles for domains, packages and GitHub. Keep the accent in the logo and wordmark.
- Benchmark-oriented names ("¿Le Ganas?") fit the investment-benchmark use well, but slightly raise the "investment product" impression. Pair them with the education framing.

### Gaps
- **IMPI MARCia trademark search was not possible** (JS app). Every shortlisted name needs a manual search at marcia.impi.gob.mx (identical and phonetically similar marks, classes 9, 35, 36, 42).
- .mx and .com.mx availability is a DNS signal only. It should be confirmed at a registrar or with NIC México's whois.
- Google Play and App Store name searches were not done systematically beyond web search.
- The "Chivo" association with El Salvador's government bitcoin wallet, and "varo" as Mexican slang for money, are background knowledge not sourced in this research. Verify before using them in the final report.
- Whether "Inflacionómetro" would pass IMPI's descriptiveness test is my inference, not an IMPI ruling.
