# Data-Usage Audit — answer to "did you use data from these datasets?"

**Project 16** · 2026-06-25 · Scope locked to the user-specified 12-dataset list. Verified against `data/processed/variable_provenance.csv` and `data/raw/`.

## Yes — all 12 listed datasets were used, and (now) nothing else.

| # | Dataset (your list) | Used? | What it provided |
|---|---|:--:|---|
| 1 | select-gender-indicators_subnational_gha.csv | ✓ | x_final_say_women, x_wifebeating_justified_women, x_no_land_women |
| 2 | literacy_subnational_gha.csv | ✓ | x_women_literate, x_women_cannot_read |
| 3 | select-education-indicators_subnational_gha.csv | ✓ | x_women_no_education, x_women_secondary_plus |
| 4 | hiv-knowledge_subnational_gha.csv | ✓ | m_hiv_mtct_knowledge_women (MTCT-prevention knowledge [Women]) |
| 5 | hiv-counseling-and-testing_subnational_gha.csv | ✓ | m_ever_hiv_test, m_anc_hiv_test |
| 6 | fp2020_subnational_gha.csv | ✓ | m_modern_cpr_married, m_fp_demand_satisfied_modern |
| 7 | anemia_subnational_gha.csv | ✓ | y_women_any_anemia, y_children_any_anemia |
| 8 | maternal_and_reproductive_health_indicators_gha.csv | ✓ | National WHO-GHO context only → `outputs/data/mrh_national_context.csv` (Introduction); **not** a region variable (file is national, no region disaggregation) |
| 9 | child-mortality-rates_subnational_gha.csv | ✓ | y_u5mr (primary), y_nmr, y_imr |
| 10 | sdgs_subnational_gha.csv | ✓ | x_ipv_any, x_own_decision_all3, m_skilled_delivery, **y_asfr_15_19** |
| 11 | Master_Sheet.xlsx (actual file: `Master Sheet.xlsx`) | ✓ | 261-district frame; context (illiteracy, uninsured, poverty, female 15-64, population); centroids |
| 12 | Ghana_New_260_District.geojson | ✓ | 261↔260 crosswalk / polygon linkage; spatial frame |

## Inconsistency found and RESOLVED (this turn)
An earlier rebuild had also pulled from **3 datasets NOT on your list**:
- `fertility-rates_subnational_gha.csv` → adolescent fertility (ASFR 15–19)
- `mdgs_subnational_gha.csv` → ANC 4+ visits
- `mics-indicators_subnational_gha.csv` → facility births

**Resolution:**
- **ASFR 15–19 re-sourced from `sdgs`** (in-scope) — value-neutral (national 61.6 unchanged).
- **ANC4+ and facility births dropped** — they have **no region-level source within your 12 datasets** (the only candidate, the WHO MRH file, is national-only). `m_skilled_delivery` (sdgs) remains as the delivery-care mediator; the RH-service index = skilled delivery + modern CPR + FP-demand-satisfied (all in-scope).
- The 3 out-of-scope files were moved to `_archive/out-of-scope-datasets-2026-06-25/` (never deleted).
- Phases 2→4 were **rebuilt and re-verified** (all exit 0) on the in-scope data; a project-wide grep confirms no analytic output references the dropped datasets/columns.

**Current state:** every variable in `region_master_16_analytic.csv` (16×27) and `district_master_261.csv` traces to one of your 12 datasets. 0 pending, 0 out-of-scope.
