# Phase 2 — Variable Extraction & Master Dataset Build (in-scope rebuild)

**Project 16** · rebuilt 2026-06-25 **strictly within the user's 12-dataset list**. Build: `analysis/phase2_build_master.py`; verified `analysis/phase2_verify.py` (exit 0). Design: Refined Option C (Hybrid).

## Provenance & scope
All inputs are the 12 user-specified datasets (`data/raw/`). DHS values are deterministic GH2022DHS STATcompiler exports. **0 pending, 0 out-of-scope.** See `DATA_USAGE_AUDIT.md`.

## Outputs
| File | Rows | Purpose |
|---|---|---|
| `data/processed/district_master_261.csv` | 261 | District socioeconomic frame + GeoJSON linkage |
| `docs/district_crosswalk_261_to_260.csv` | 261 | Vetted 261↔260 crosswalk (3 structural gaps) |
| `data/processed/region_master_16_dhs2022.csv` | 16 | DHS-2022 exposures/mediators/outcomes |
| `data/processed/region_master_16_analytic.csv` | 16 | **Primary analytic file** — 16×27 (21 DHS + 6 context), all 16/16 |
| `data/processed/phase2_indicator_manifest.csv` | 28 | Per-variable role/source/status |
| `outputs/data/mrh_national_context.csv` | 208 | WHO GHO national MRH series (Introduction context only) |

## 261-district frame integrity
261 rows retained; **exactly 3 structural gaps** merged to parent polygons for rendering only (Awutu Senya West→AWUTU SENYA, Sagnarigu→TAMALE METROPOLITAN, Guan→KRACHI EAST MUNICIPAL); 0 unmatched.

## Variable set (GH2022DHS, 16 regions — all 16/16 filled)
- **X exposures (9):** final-say, wife-beating-justified, no-land (gender); women no-education, secondary+ (education); literate, cannot-read (literacy); IPV-any, own-decision-all-3 (sdgs). Human-capital axis: secondary+ primary, literacy sensitivity (never joint). Gender-equity index = decision-making + violence attitudes + no-land. FGC dropped (absent from 2022 region export).
- **M mediators (6):** skilled delivery (sdgs); modern CPR married, FP demand satisfied modern (fp2020); ever-HIV-test, ANC-HIV-test (hiv-counseling-and-testing); MTCT-knowledge [Women] (hiv-knowledge).
- **Y outcomes (6):** women any-anaemia, children any-anaemia (anemia); **U5MR (primary)**, NMR, IMR (child-mortality-rates); ASFR 15–19 (sdgs).
- **Context (6, Master Sheet → region, pop-weighted):** total pop, n-districts, illiteracy rate, uninsured rate, poverty incidence, female-15-64 share.

### Source notes
- **ANC4+ and facility births are NOT included** — they have no region-level source within the 12 datasets (the WHO MRH file is national-only). `m_skilled_delivery` (sdgs) is the delivery-care mediator. (Earlier drafts sourced these from out-of-scope `mdgs`/`mics`; removed to honour the dataset list.)
- **Adolescent fertility (ASFR 15–19)** sourced in-scope from `sdgs`.
- **HIV knowledge:** the 2022 export carries only MTCT-prevention knowledge [Women]; used as the HIV-knowledge mediator (documented substitution).
- **WHO MRH** = national Introduction context only.

## QA (`phase2_verify.py`, exit 0)
- 21 DHS + 6 context columns: **16/16 filled**; every indicator reduces to exactly 1 source row per region (no silent averaging); no pre-2022 alias leakage.
- National pop-weighted ≈ DHS-2022 Ghana (U5MR 41.5, skilled delivery 88.9, modern CPR 28.1, child anaemia 46.8, ASFR 61.6, illiteracy 25.7).
- Crosswalk: 0 unmatched of 261; 3 structural gaps. **0 pending.**

## Next (Phase 3+)
Cleaning/provenance → spatial (261 LISA/Moran + MAUP) → descriptive RF/SHAP → ecological mediation.
