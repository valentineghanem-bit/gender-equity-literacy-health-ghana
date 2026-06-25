# Phase 0 — Audit & Reconciliation

**Project 16 — Gender Equity, Literacy and Multi-Domain Health Outcomes: Spatial ML Mediation Analysis in Ghana**
Author: Valentine Golden Ghanem · Date: 2026-06-24 · Status: Phase 0 audit complete; design lock pending user sign-off

This document resolves every error and inconsistency in the Phase 0 `/datalog` before Phase 1 may begin (per user gate). Each item is `[VERIFIED]` against the actual files where checkable, or `[LOGIC]` where it is a design/consistency call.

---

## Data facts verified against the actual files

| Check | Claimed in Phase 0 | Verified | Verdict |
|---|---|---|---|
| Master Sheet rows | 261-district | **261 data rows, 0 nulls** | ✓ correct |
| Master Sheet contextual vars | Illiterate pop, poverty incidence/intensity, uninsured, total pop, female 15–64 | All present (+ lat/long centroids, employment, full age–sex) | ✓ correct |
| GeoJSON polygons | "260 districts" | **260 features, 16 distinct REGION values** | ✓ count correct, but framing wrong (see C1) |
| Guan/Oti | "Guan missing" | OTI present as region; Guan has no own polygon | ✓ rendering artefact, not a data gap |
| DHS export shape | long format, region-level | long; `Location` = 16 post-2022 regions + 5 pre-2022 aliases + 1 HXL row | ✓ + see M1 |

---

## CRITICAL — must be fixed before Phase 1

### C1 — "260-district" framing violates the hard 261 rule `[VERIFIED]`
Phase 0 uses "260 districts" in the geographic-unit line, Option B, Option C's secondary mapping, and the data-quality flag. **Ghana has 261 MMDAs; the analytical/reporting frame is always 261.** The GeoJSON's 260 polygons are a rendering artefact of the shapefile vintage (Guan, the 261st, has no own polygon).
**Resolution:** Keep all 261 Master-Sheet rows. For choropleth/LISA *rendering only*, merge Guan into its Oti parent polygon with a caption footnote. Report "261 districts" in every title, abstract, README, and table. Build `docs/district_crosswalk_261_to_260.csv`. Give Guan its parent's adjacency for spatial weights, or state explicitly that it shares Oti geometry.

### C2 — Option B "more powerful statistically" is a statistical error `[LOGIC]`
Assigning a region's DHS value to all its districts and then analysing 261 rows as independent observations is **pseudo-replication**: it does not add information, it understates standard errors and inflates Type-I error. The true analytical N for any DHS exposure/mediator/outcome is **16**, regardless of how the values are mapped onto polygons.
**Resolution:** District downscaling is legitimate **only** for (a) spatial autocorrelation of variables that genuinely vary at district level (the Master Sheet's literacy and poverty) and (b) descriptive mapping. It is **not** valid for inferential mediation/ML treating 261 as independent N. The Phase 0 "more powerful" claim is struck.

### C3 — Two conflicting "preferred" design options `[LOGIC]`
Option A is tagged "(Recommended)" while Option C is tagged "(Most Defensible)". Exactly one design must be selected.
**Resolution:** Recommendation below (Refined Option C); final choice is the one decision requiring user sign-off before Phase 1.

### C4 — Variables double-classified across roles `[LOGIC]`
A variable cannot be both exposure and outcome (or mediator and outcome) in one mediation model.
- **"Women circumcised / FGC (%)"** appears under EXPOSURES (gender) **and** OUTCOMES (sdgs). → Resolve to **EXPOSURE** (gender-inequity / harmful-practice marker). *Caveat m2: FGC in Ghana is low and concentrated in Upper East/West & Savannah; at 16-region level it is near-zero in most regions and will behave as a near-constant northern marker — consider dropping or recoding.*
- **"Adolescent birth rate 15–19"** appears under MEDIATORS (sdgs) **and** OUTCOMES (sdgs). → Resolve to **OUTCOME** (SDG 3.7 demographic-health outcome).
(Both resolutions are overridable at the Phase 1 review gate.)

### C5 — WHO MRH national variables masquerading as region-level mediators `[LOGIC]`
"ANC 4+ visits (%)" and "Facility births (%)" are listed as MEDIATORS but sourced from the WHO MRH **national** file (one value for Ghana) — they cannot vary across 16 regions.
**Resolution:** Source ANC 4+, skilled birth attendance, and facility delivery as mediators from the **DHS regional** files (sdgs carries "Assistance during delivery from skilled provider"; DHS subnational carries ANC 4+ and facility delivery by region). Reserve the WHO MRH national longitudinal series for **Introduction / national-context** only.

---

## MODERATE — fix during extraction (Phase 2/3)

- **M1 — DHS `Location` cleaning `[VERIFIED]`.** The export carries 16 canonical post-2022 regions + 5 pre-2022 aliases (Brong-Ahafo; Northern (pre 2022); "Northern, Upper West, Upper East"; Volta (pre 2022); Western (pre 2022)) **+ one HXL artefact row `#loc+name`** that Phase 0 did not flag. Drop the aliases AND the HXL row; strip the `..` prefixes (`..Northeast`→North East, `..Northern(post 2022)`→Northern, `..Savannah`→Savannah). Keep only `IsPreferred`/total rows per indicator.
- **M2 — Empowerment-variable collinearity.** "Final say in all decisions" (gender) and "Own decision making about all 3 decisions" (sdgs) measure near-identical constructs. With N=16, build a single **gender-equity index** (decision-making + attitudes-to-violence + asset ownership) rather than entering each separately, to preserve degrees of freedom.
- **M3 — Geographic-unit statement internally inconsistent.** Header mixes "16 regions (primary)", "260-district GeoJSON", and "261-District". Standardise: **primary inferential unit = 16 regions (DHS); high-resolution spatial/mapping unit = 261 districts (Master Sheet; 260 polygons rendered, Guan→Oti).**
- **M4 — Extraction date ambiguous** ("Dec 2024 / Jun 2025"). Record per-dataset extraction dates in the Phase 3 provenance log.
- **M5 — N=16 power not addressed for ML.** RF + SHAP on N=16 overfit; GWR on 16 units is unstable; Moran's I on 16 units has low power. "Standard for region-level Ghana DHS spatial studies" needs a citation or softening. Resolution is bound to the design choice (see below).

## MINOR
- **m1** — Standardise the North East region display label (GeoJSON "NORTHERN EAST" / DHS "..Northeast" → **North East**).
- **m3** — U5MR, NMR, IMR are highly collinear; with N=16 pick **U5MR as primary**, treat NMR/IMR as sensitivity.

---

## Corrected mediation framework (working — overridable at Phase 1 gate)

**X — Gender equity & literacy** (DHS 16-region; Master-Sheet contextual aggregated to region)
- Education: women no education %; women secondary+ %
- Literacy: women literate % (primary); cannot-read % (mirror)
- Gender-equity index: final-say-in-decisions %; wife-beating-justified %; do-not-own-land %; partner violence % (sdgs); FGC % (flagged m2)
- Contextual (Master Sheet → region): illiteracy rate, poverty incidence/intensity, uninsured rate

**M — Reproductive-health services** (DHS regional only)
- modern CPR %; demand for FP satisfied by modern methods %
- skilled birth attendance % (sdgs); modern CPR % + FP demand satisfied % (fp2020)  [NOTE 2026-06-25: ANC4+ / facility births have no region-level source in the 12-dataset list → excluded; see DATA_USAGE_AUDIT.md]
- ever-HIV-tested % + ANC HIV testing % (hiv-counseling-and-testing); MTCT-prevention knowledge % (hiv-knowledge; proxy for comprehensive HIV knowledge)

**Y — Multi-domain health** (DHS regional)
- Child survival: **U5MR (primary)**; NMR, IMR (sensitivity)
- Anemia: women any anemia %; children any anemia %
- Adolescent birth rate 15–19 (SDG 3.7)

**Spatial frame** — 261 districts (Master Sheet) for LISA/Moran of literacy & poverty + all choropleths (Guan→Oti merge); 16 regions for DHS-outcome Moran (descriptive).

---

## Design recommendation (the one item needing user sign-off)

**Refined Option C (Hybrid) — recommended.** Mediation + ML at **16 regions** (leave-one-out CV, bootstrap/Bayesian CIs, reported as exploratory given N=16); LISA/Moran of literacy & poverty at **261 districts**; all choropleths at 261 (Guan→Oti). Rejects Option B's pseudo-replication. Honest, defensible, delivers the title.

**Ambitious upgrade — Small-Area Estimation (SAE).** Model district-level DHS outcomes from Master-Sheet covariates (as Project 10 did) → genuine N=261 for spatial ML + mediation with uncertainty. Strongest district-level claims; adds modelling assumptions and effort.

See the question posed to the user for the four mutually-exclusive options.
