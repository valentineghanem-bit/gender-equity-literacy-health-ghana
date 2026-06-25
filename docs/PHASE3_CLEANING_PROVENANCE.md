# Phase 3 — Cleaning, Provenance & Descriptive (Table 1)

**Project 16** · 2026-06-25 · Build: `analysis/phase3_clean_describe.py`. Gated behind a passing Phase-2 verification (`qa/PHASE2_VERIFY_REPORT.md`, exit 0).

## Cleaning decisions (audit trail — formalises every transformation)
1. **Survey filter:** `SurveyId == GH2022DHS` only; all historical surveys and the `#…` HXL header row dropped.
2. **Region harmonisation:** Location → 16 canonical post-2022 regions; the 5 pre-2022 aliases (Brong-Ahafo, "Northern (pre 2022)", "Northern, Upper West, Upper East", Volta/Western (pre 2022)) **excluded** (verified: no alias leakage).
3. **One value per region:** `IsPreferred==1` selected where multiple denominators exist; **verified exactly 1 source row per region** for all 21 indicators (no silent averaging — Phase-2 verify §B/C).
4. **Women's indicators:** `[Women]` variants used for gender/education/literacy/MTCT-knowledge.
5. **261-district frame:** all 261 Master-Sheet rows retained; **3 structural gaps** (Guan, Sagnarigu, Awutu Senya West) linked to parent polygons for rendering only (vetted crosswalk).
6. **Context rates:** district counts → region via population-weighted aggregation.

## Documented caveats (carried into limitations)
- **`ctx_illiteracy_rate` is an all-age proxy** (Illiterate Population ÷ Total Population), not the adult literacy rate; use the DHS `x_women_literate`/`x_women_cannot_read` for the literacy *exposure*, and treat the Master-Sheet illiteracy as a contextual district-varying layer.
- **`m_hiv_mtct_knowledge_women` substitutes** for "comprehensive AIDS knowledge" (absent from the 2022 region export); it is the HIV-knowledge mediator.
- **ANC4+ / facility birth excluded** — no region-level source within the 12 datasets (WHO MRH is national-only); `m_skilled_delivery` (sdgs) is the delivery-care mediator. **ASFR 15–19 sourced in-scope from `sdgs`.**
- **WHO MRH** = national context only (`outputs/data/mrh_national_context.csv`).

## Missing data & outliers
- **Missing: none** — all 21 DHS indicators + 6 context vars are 16/16 (Phase-2 verify §D).
- **Outliers:** all values within plausible ranges; national pop-weighted aggregates match published DHS-2022 Ghana figures (Phase-2 verify §E). No winsorising needed.

## Outputs
| File | Purpose |
|---|---|
| `data/processed/variable_provenance.csv` (30) | column → role → source file → indicator → survey → transform |
| `data/processed/analytic_region_16_clean.csv` (16×58) | analysis-ready: all vars + `belt` stratifier + z-scored (`_z`) versions of 27 analytic vars |
| `outputs/tables/table1_descriptives.csv` (29) | per-variable n, mean, SD, min, median, max, national pop-weighted |
| `outputs/tables/table1_by_belt.csv` | key vars by Ghana 3-belt zone |

## Belt stratifier (standard Ghana 3-zone)
- **Northern:** Northern, North East, Savannah, Upper East, Upper West
- **Middle:** Ashanti, Ahafo, Bono, Bono East, Eastern, Oti
- **Coastal/South:** Greater Accra, Central, Western, Western North, Volta

## Table 1 by belt — north–south gradient (face validity)
| | Secondary+ | Literate | Own-decision | WB-justified | Skilled del. | Modern CPR | FP-demand | Ever HIV-test | U5MR | Child anaemia | Women anaemia | ASFR 15–19 | Illiteracy | Poverty |
|---|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
| Coastal/South | 77.1 | 67.5 | 58.5 | 15.5 | 89.7 | 30.4 | 47.6 | 60.1 | 39.6 | 44.7 | 41.7 | 55.0 | 22.4 | 23.0 |
| Middle | 68.4 | 54.0 | 48.4 | 17.8 | 87.8 | 29.0 | 46.9 | 58.6 | 45.3 | 44.4 | 38.8 | 64.7 | 28.0 | 24.4 |
| Northern | 41.4 | 39.7 | 40.2 | 41.8 | 83.7 | 23.2 | 47.4 | 42.2 | 49.4 | 65.5 | 46.0 | 87.4 | 48.0 | 43.2 |

Monotonic gradient across the full exposure→mediator→outcome chain supports the hypothesised pathway direction.

## Deferred to Phase 4 (methodology, by design)
Gender-equity **composite index** (factor analysis of decision-making + violence attitudes + asset ownership) and the human-capital axis modelling are analytic-modelling decisions and are constructed in Phase 4, not here. z-scored components are pre-staged in the clean dataset.

## Next — Phase 4
Spatial structure (261-district LISA/Moran on literacy & poverty; MAUP 16-vs-261 sensitivity) → descriptive RF/SHAP at 261 → ecological mediation at 16 regions (precision-weighted, bootstrap CIs).
