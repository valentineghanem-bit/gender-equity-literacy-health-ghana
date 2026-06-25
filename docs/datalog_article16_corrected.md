# /datalog — Article 16 (CORRECTED)

**Gender Equity, Literacy and Multi-Domain Health Outcomes: Spatial ML Mediation Analysis in Ghana**
Supersedes the Phase 0 datalog. All corrections traced in `PHASE0_AUDIT_RECONCILIATION.md`.

| Field | Value |
|---|---|
| Dataset 1 | Ghana DHS 2022 (GH2022DHS) — subnational indicators, **16 post-2019 regions**, long format |
| Dataset 2 | WHO MRH Ghana — **national** longitudinal (Introduction/context only — NOT a regional mediator) |
| Dataset 3 | Ghana Master Sheet — **261-district** socioeconomic (Census 2021), 261 rows, 0 nulls |
| Primary inferential unit | **16 regions** (DHS) |
| High-resolution spatial/mapping unit | **261 districts** (Master Sheet); rendered on a 260-polygon GeoJSON with **Guan→Oti** merge |
| Extraction date | Per-dataset, to be logged in Phase 3 provenance (Phase 0 ambiguity flagged) |
| IRB | Ghana Health Service Ethics Review Board — secondary ecological analysis; no individual-level data |
| Design | Pending user lock — recommendation: Refined Option C (see audit) |

**Resolved from Phase 0:** 261-district frame enforced (C1); pseudo-replication rejected (C2); single design to be selected (C3); FGC→exposure, adolescent birth rate→outcome (C4); WHO MRH demoted to national context (C5); ANC4+/facility births excluded — no region-level source in the 12-dataset list, skilled delivery retained (2026-06-25 rescope, see DATA_USAGE_AUDIT.md); DHS `Location` cleaning incl. `#loc+name` HXL row (M1); gender-equity index for collinearity (M2); U5MR primary outcome (m3).

See `PHASE0_AUDIT_RECONCILIATION.md` for the full corrected X/M/Y mediation framework.

**Post-council finalised decisions (epid-council 2026-06-24 — see `PHASE1_LITERATURE_GAP_ANALYSIS.md` §6b):**
- **Human-capital axis:** women secondary+ (primary) and literacy (sensitivity) — never entered jointly (collinearity, Madichie 2026).
- **Gender-equity index:** decision-making + attitudes-to-violence + asset ownership. **FGC excluded** (near-constant at region level).
- **Outcomes:** U5MR primary; NMR/IMR + anaemia (women/children) + adolescent birth rate as sensitivity/secondary.
- **ML:** RF/SHAP at **261 districts, descriptive only** (determinant layer); region-level ML dropped. SAE = future upgrade.
- **Mediation:** 16 regions, precision-weighted, hypothesis-generating (bootstrap/Bayesian CIs).
- **Controls:** MAUP rezoning sensitivity (16 vs 261); ecological-fallacy + measurement-error limitations stated; causal language softened to "ecological associations / hypothesised pathway".
