# Phase 1 — Literature Review & Six-Dimension Gap Analysis

**Project 16 — Gender Equity, Literacy and Multi-Domain Health Outcomes: Spatial ML Mediation Analysis in Ghana**
Author: Valentine Golden Ghanem · Date: 2026-06-24 · Design locked: **Refined Option C (Hybrid)** — 16-region inference + 261-district spatial/mapping.

**Quad-Connector status (Tenet 21):** Discovery = PubMed + Consensus ✓ · Synthesis = Consensus ✓ · Reliability = Scite ✓ (no retractions/EoC in the empowerment–maternal-health corpus; SUPPORTING-dominant with a CONTRASTING minority) · Validation = abstract-level for Phase 1; **full-body Truth-Check (Tenet 22) deferred to the Evidence Bank (epid-council Step 0 / Phase 6)** before any statistic enters the manuscript. Confidence labels are attached per claim.

---

## 1. Unified evidence table

One table, all sources merged. Quality signal = citation count + Scite/Consensus reliability where available. Prioritised to the last ~7 years; ecological/DHS designs flagged because they anchor our own design.

| # | Citation | Population / Setting | Design | Key finding | Quality signal |
|---|---|---|---|---|---|
| 1 | Yaya et al. 2018, *Reprod Health* | 474,622 women, 32 SSA countries (DHS) | Multilevel logistic | Women's empowerment dimensions positively predict contraceptive use; wide between-country variance (6.7%–72%) | 211 cites; SUPPORTING |
| 2 | Chol Chol et al. 2019, *BMJ Open* | 194,883 married women, 31 SSA (DHS) | Pooled multiple logistic | **Weak** autonomy→ANC4+/SBA links (aOR 1.07–1.15); paradoxical reversals (Senegal aOR 0.74) | 92 cites; **CONTRASTING/nuance** |
| 3 | Oduse et al. 2021, *Reprod Health* | 27 SSA countries (DHS) | Fairlie non-linear decomposition | Urban–rural maternal-care gap explained mostly by wealth, media exposure, women's & partners' education | 88 cites; SUPPORTING |
| 4 | Okyere et al. 2025, *Reprod Health* | 109,818 children, 22 SSA (DHS 2013–24) | Logistic + ordered logistic | Paternal education→ANC4+/SBA (AOR ~2.0); **no direct** link to child survival — **indirect via utilisation** | 3 cites; SUPPORTING (mediation) |
| 5 | Avelino et al. 2025, *Eur J Pediatr* | Africa, 39 studies | PRISMA systematic review | U5 mortality driven by poverty, **maternal education**, prenatal care; uses **Mosley–Chen** distal/intermediate/proximal framework | 17 cites; SUPPORTING (theory anchor) |
| 6 | Madichie et al. 2026, *PLOS One* | 10,820 women, Nigeria (MIS 2021) | Bivariate probit + PSM | Secondary education ↓U5 mortality (−2.08 ppt), ↑maternal care (+6.74 ppt); **literacy not independent of formal education** in adjusted models | new; SUPPORTING + collinearity caveat |
| 7 | Brinda et al. 2015, *BMC Public Health* | 138 countries | **Ecological**, robust regression | UNDP Gender Inequality Index positively associated with NMR/IMR/U5MR after confounders | 87 cites; **direct ecological design precedent** |
| 8 | Kennedy et al. 2020, *Lancet Glob Health* | 40 LMICs, first two decades of life | Indicator-framework analysis | Gender inequalities in health emerge in early adolescence; SRH disadvantage, child marriage, adolescent fertility | 122 cites; SUPPORTING |
| 9 | Sule et al. 2022, *BMJ Glob Health* | LMICs | Scoping review (17 studies) | Six gendered MNCH dimensions: financial access, agency, social norms, IPV, reproductive decision-making, partner support | 28 cites; SUPPORTING (theory) |
| 10 | Sen et al. 2023, *PLOS One* | 2,441 mothers, Bangladesh (DHS 2017-18) | **SEM mediation + bootstrap** | Multidimensional empowerment→essential newborn care; **indirect effect via skilled ANC > direct effect** | 8 cites; **mediation-method precedent** |
| 11 | Abreha et al. 2020, *PLoS One* | 10,641 women, Ethiopia (DHS 2016) | **MIMIC latent model** | Empowerment (socio-economic, decision-making) ↓stunting/wasting; decision-making→better child anaemia/pneumonia; **dimension-specific** | 51 cites; SUPPORTING + nuance |
| 12 | Petry et al. 2020, *Matern Child Nutr* | National survey, Ghana | Stratified multivariable regression | Anaemia risk factors (ID, malaria, inflammation) **differ by climate zone/belt** — Northern vs Middle vs Southern | 25 cites; SUPPORTING (spatial heterogeneity) |
| 13 | Wegmüller et al. 2020, *PLoS One* | 1,165 children + 973 women, Ghana (2017) | National cross-sectional | Child anaemia 35.6%, women 21.7%; higher in rural, poor, **Northern Belt** | 81 cites; SUPPORTING |
| 14 | Yakubu & Salisu 2018, *Reprod Health* | SSA, 24 studies | Systematic review | Adolescent pregnancy driven by poverty, unequal gender power, early marriage, lack of free education / staying in school | 464 cites; SUPPORTING (theory) |
| 15 | Melesse et al. 2020, *BMJ Glob Health* | 33 SSA countries (DHS) | Trend + inequality analysis | Large, persistent ASRH inequalities by **gender, education, residence, wealth** | 221 cites; SUPPORTING |
| 16 | Ahinkorah et al. 2021, *PLoS One* | 32 SSA countries (DHS 2010–18) | Multilevel logistic | First adolescent pregnancy patterned by education, wealth, early sexual debut; rural & West-Africa lower odds | 129 cites; SUPPORTING |
| 17 | Spatial LBW Ghana 2017 GMHS, *BMJ Open* (DOI 10.1136/bmjopen-2024-083904) | Ghana, Maternal Health Survey | **Spatial + multilevel** | Low-birth-weight clustering mapped; spatial + contextual predictors in Ghana | recent; Ghana spatial precedent |
| 18 | Petry/Wegmüller belt findings + Iodine XGBoost-SHAP 2025, *Adv Nutr* (DOI 10.1016/j.advnut.2025.100384) | Global nutrition | **XGBoost + SHAP** | Demonstrates SHAP for interpretable ML on nutrition/deficiency burden | recent; ML-method precedent |

**Settled vs contested (Consensus synthesis):**
- *Settled (HIGH):* female education/literacy and women's empowerment are broadly protective for reproductive-health service use and child survival in SSA (#1,3,4,5,6,15,16).
- *Contested (MEDIUM):* the **magnitude** and **which empowerment dimension matters** are context-dependent — strong contraception effects (#1) vs weak/paradoxical maternal-care effects (#2), and dimension-specific child-health links (#11). Discussion must hold ≥2 CONTRASTING entries (#2, #11) — already banked.
- *Method gap (HIGH):* mediation evidence exists (#4,#10,#11) but almost always at **individual level**; ecological gender→child-mortality work exists (#7) but **without a formal mediator**, and **without spatial ML**. No SSA study combines (gender+literacy) → RH-service mediator → multi-domain outcome **in a spatial, ML-interpretable, ecological framework**.

---

## 2. Six-dimension gap matrix (6 × 2)

| Dimension | Gap present? | Our study addresses? | Detail |
|---|:--:|:--:|---|
| **1. Knowledge** — established evidence not applied to this context | **Y** | **Y** | Empowerment→MCH is established globally (#1,#7,#15) but rarely operationalised as a *spatial, multi-domain mediation* model for Ghana's 16-region / 261-district frame. |
| **2. Empirical** — missing data / conflicting findings | **Y** | **Y** | Conflicting magnitudes (#1 strong vs #2 weak; #11 dimension-specific). We test the pathway explicitly and quantify indirect vs direct effects rather than report a single adjusted OR. |
| **3. Methodological** — design / analytical gaps | **Y** | **Partial** | Mediation studies are individual-level (#4,#10,#11); ecological gender work lacks a mediator (#7); Ghana spatial work (#12,#17) lacks ML + mediation. We fuse spatial autocorrelation + interpretable ML (RF/SHAP) + mediation. **Caveat:** inference N=16 (regions) limits ML to exploratory; 261-district scale used for literacy/poverty spatial structure. |
| **4. Theoretical** — absent causal framework / DAG | **Y** | **Y** | We adopt **Mosley–Chen** (#5) + the gendered-MNCH dimensions (#9) to specify an explicit X→M→Y DAG (gender-equity/literacy → RH services → multi-domain health), pre-registered before analysis (`/anchor`). |
| **5. Population** — understudied groups (Ghana / LMIC / SSA) | **Y** | **Y** | Most multi-country DHS work pools SSA and obscures within-Ghana spatial inequity; belt-specific anaemia heterogeneity (#12,#13) shows Ghana-internal variation is real and under-mapped at district scale. |
| **6. Translational** — evidence-to-policy / practice failures in Ghana | **Y** | **Y** | District-level choropleths + LISA hotspots translate the pathway into a spatially targeted policy tool (SDG 3.1/3.2/3.7, 4, 5), addressing the "where to act" gap that pooled ORs cannot answer. |

**All six dimensions are addressed**, with Methodological only *partially* closed (the N=16 inference ceiling is a stated limitation, not a solved problem — see §4 self-critique).

---

## 3. Central thesis statement

> This study addresses the **knowledge, empirical, methodological, theoretical, population, and translational** gaps by modelling **gender equity and female literacy as ecological determinants of multi-domain health (child survival, anaemia, adolescent fertility) through reproductive-health-service mediators**, using **spatial autocorrelation, interpretable machine learning, and formal mediation** across **Ghana's 16 regions (inference) and 261 districts (spatial structure & mapping)**, to produce a **spatially targeted, SDG-aligned evidence tool** for sub-national health-equity policy — advancing beyond pooled, aspatial, single-outcome SSA analyses.

(`/anchor` set — no manuscript section proceeds until this thesis is fixed.)

---

## 4. Recommended design, data source & analytical approach

**Design:** Ecological cross-sectional, **Refined Option C (Hybrid)** — locked by user 2026-06-24.
**Data:** Ghana DHS 2022 subnational (16 regions; exposures, mediators, outcomes) + Master Sheet 261-district socioeconomic (Census 2021; literacy & poverty spatial layer) + WHO MRH national (Introduction context only). GeoJSON 260 polygons rendered at **261-district** frame (Guan→Oti merge).
**Analytical pipeline:**
1. Descriptive + regional inequality (Gini/ratios) across 16 regions.
2. **Spatial structure** — Global Moran's I + LISA on literacy & poverty at **261 districts**; Moran's I on DHS outcomes at 16 regions (descriptive, low power).
3. **Interpretable ML** — Random Forest + SHAP at 16 regions with **leave-one-out CV** and bootstrap CIs, reported as **exploratory** (N=16 ceiling stated up front); optional SAE noted as future upgrade.
4. **Mediation** — gender-equity/literacy index → RH-service mediator → outcome, via SEM/bootstrap (per #10) and MIMIC-style latent handling (per #11); report indirect vs direct effects.
5. **Outputs** — 261-district choropleths + LISA maps, SHAP plots, mediation path diagram; HI-EI dashboard + A0 poster.

**PRISMA flow:** not applicable (this is not a systematic review / meta-analysis).

---

## 5. Self-critique (mandatory)

- **Weakest assumption:** that 16-region DHS indicators carry enough signal for a *mediation* model. With N=16, indirect-effect CIs will be wide and ML importance is exploratory, not confirmatory. Mitigations: bootstrap/Bayesian CIs, LOOCV, pre-specified DAG, and SAE flagged as the upgrade path.
- **Most likely reviewer objection:** "ecological fallacy + pseudo-replication." Pre-empted by (a) keeping inference at the true unit (16 regions) and **never** treating downscaled districts as independent N (audit C2), (b) restricting the 261-district layer to variables that genuinely vary at district level (literacy, poverty) plus mapping, and (c) an explicit ecological-design limitation paragraph.
- **Second objection:** literacy and education collinearity (#6 shows literacy loses independence when education is included). Mitigation: enter a single composite or test them in separate models, not jointly.
- **Banked CONTRASTING evidence for Discussion:** #2 (weak/paradoxical autonomy effects) and #11 (dimension-specific, not universal) — satisfies the ≥2-CONTRASTING-per-major-claim rule for the empowerment→health claim.

---

## 6b. Council resolutions (epid-council, 2026-06-24) — Phase 1 issue closure

Phase 1 was peer-reviewed by the 5-advisor Epid Council. All flagged issues are resolved below; nothing carries forward unresolved into Phase 2.

| # | Council issue | Severity | Resolution (implemented) |
|---|---|---|---|
| R1 | **RF/SHAP at N=16 is uninterpretable** (p≫n) | FATAL | ML **moved to 261-district scale, descriptive only** (no p-values/inference) on the genuinely district-varying determinant layer (illiteracy rate, poverty, uninsured, female 15–64). Region-level RF/SHAP **dropped**. SAE flagged as the upgrade path for genuine district-level *outcome* ML. |
| R2 | Individual-level mediation precedents (Sen n=2,441; Abreha n=10,641) **don't license n=16 ecological mediation** | HIGH | Mediation stays at 16 regions but **reframed as hypothesis-generating**: bootstrap/Bayesian indirect-effect CIs, explicit small-N + sequential-ignorability caveat, precedents relabelled as *method templates* not *power justification*. |
| R3 | **Measurement error ignored** — DHS regional point estimates carry large sampling CIs (new small regions) | HIGH | Region rows **weighted by DHS denominator / carry CIs**; precision-weighted regression; small-region instability stated as a limitation. |
| R4 | **MAUP** — 16-region vs 261-district results can differ | HIGH | Mandatory **rezoning sensitivity analysis** (16-region vs 261-district) added to Methods (Fontanet 2023; Hogg 2025). |
| R5 | **Ecological fallacy** can flip coefficient signs / mis-target groups (Shih 2023) | HIGH | Explicit ecological-fallacy limitation; **no individual-level inference claimed**; causal language softened (see R8); district maps interpreted as *determinant clustering*, not outcome targeting. |
| R6 | **Temporal/boundary mismatch** — DHS 2022 vs Census 2021 vs 2019 region boundaries | MODERATE | Crosswalk harmonises vintages; contemporaneity assumption stated; 16 post-2022 regions ↔ 261 Census-2021 districts mapping documented. |
| R7 | **Common-source coupling** — facility births / SBA mediators overlap with outcomes | MODERATE | Mediator and outcome kept conceptually distinct; coupling flagged; SBA/facility-births treated as service-access mediators, not survival proxies. |
| R8 | **Causal language** from cross-sectional ecological data | MODERATE | "determinants / through mediators" → **"ecological associations / hypothesised pathway"** throughout. |
| R9 | **literacy/education collinearity** (Madichie 2026: literacy loses independence) | MODERATE | Single **human-capital axis**: *women secondary+* primary, *literacy* as sensitivity — **never entered jointly**. Gender-equity index (decision-making + violence attitudes + asset ownership) kept separate; **FGC excluded** (near-constant at region level). |
| R10 | **U5MR** vs NMR/IMR collinearity | LOW | **U5MR primary**; NMR/IMR sensitivity only. |
| R11 | **CONTRASTING insufficiency** on ecological/spatial design | HIGH | Banked: Shih 2023, Fontanet 2023, Hogg 2025 (design); Bliznashka 2021 (null), Christian 2023 (reversal) added for empowerment magnitude. **≥2 CONTRASTING per major claim now satisfied.** |

**Revised analytical pipeline (post-council, supersedes §4 step list):**
1. Descriptive + regional inequality (Gini) at 16 regions; precision-weighted by DHS denominator.
2. Spatial structure — Global Moran's I + LISA on literacy & poverty at **261 districts** (inferential, n=261, Guan→Oti adjacency); region-level outcome Moran's I descriptive only.
3. **Descriptive ML** — RF + SHAP at **261 districts** on the determinant layer (interpretation only, no inference). + **MAUP rezoning sensitivity** (16 vs 261).
4. **Ecological mediation** — human-capital + gender-equity index → RH-service mediator → outcome at 16 regions; bootstrap/Bayesian CIs; hypothesis-generating; sequential-ignorability caveat.
5. Outputs — 261-district choropleths + LISA, SHAP plots, mediation path diagram; HI-EI dashboard + A0 poster.

**Updated gap-matrix line:** Dimension 3 (Methodological) upgraded from *Partial* → **Addressed** — the N=16 ceiling is no longer carried by the ML component (now 261-district descriptive); the inference unit (16 regions) is used only where defensible, with MAUP + measurement-error + ecological-fallacy controls.

## 6. Evidence-bank handoff

This harvest seeds `evidence/lit-review/`, `evidence/intro/`, `evidence/methodology/`, and `evidence/discussion/` for the epid-council Step 0 stratification. Before any statistic is written into the manuscript, each quantitative figure must clear the full-body Truth-Check (Tenet 22). Citation links are recorded in `evidence/lit-review/evidence_bank_phase1.md`.
