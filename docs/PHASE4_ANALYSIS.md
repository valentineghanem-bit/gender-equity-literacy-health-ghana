# Phase 4 — Spatial, Machine Learning & Ecological Mediation

**Project 16** · 2026-06-25 · Scripts: `phase4a_spatial.py`, `phase4b_ml_shap.py`, `phase4c_index_mediation.py`. Verified: `phase4_verify.py` (exit 0). Design: Refined Option C (Hybrid), all council R1–R11 controls applied.

## 4a. Spatial structure (261 districts) + MAUP
Centroid-KNN (k=6) weights from Master-Sheet lat/long — all **261 districts are full nodes** (incl. the 3 structural gaps), so the spatial frame is genuinely 261 units. Moran's I by 999-permutation inference.

| Scale | Variable | Moran's I | p |
|---|---|---|---|
| 261-district | Illiteracy (literacy proxy) | **0.759** | 0.001 |
| 261-district | Poverty incidence | **0.633** | 0.001 |
| 16-region (MAUP) | Illiteracy | 0.803 | 0.001 |
| 16-region (MAUP) | Poverty | 0.684 | 0.001 |

Strong, significant positive spatial autocorrelation. **MAUP check (council R4): conclusions are scale-robust** — 16-region and 261-district agree in direction and magnitude (mild upward smoothing at the coarser scale, as expected).

**LISA clusters (p<0.05):** Illiteracy — 56 High-High, 49 Low-Low, 4 spatial outliers (152 NS). Poverty — 44 HH, 44 LL, 8 outliers. HH clusters concentrate in the northern savannah belt, LL in the south (`outputs/data/lisa_districts_261.csv`).

## 4b. Descriptive interpretable ML (261 districts)
Council R1: **descriptive only, no inference.** Random Forest characterising which socioeconomic determinants structure district poverty incidence.
- 5-fold CV **R² = 0.876 ± 0.023** (descriptive fit).
- **Illiteracy is the dominant determinant by a wide margin** — mean|SHAP| 8.29 vs ≤1.43 for all others; permutation importance 1.05 vs ≤0.11. (`rf_district_importance.csv`, `shap_summary_district.png`).
- Reinforces the literacy–poverty co-clustering seen in the LISA maps. No causal claim.

## 4c. Gender-equity index + ecological mediation (16 regions)
**Index** (transparent standardized-mean, N=16-appropriate; higher = more equity): + own-decision, + final-say, − wife-beating-justified, − no-land, − IPV. **Cronbach α = 0.586** — modest, expected for a deliberately multi-dimensional equity construct (consistent with Abreha 2020 "dimension-specific"); reported honestly. Human-capital axis = women secondary+. RH service index = mean z of skilled delivery, modern CPR, FP-demand-satisfied (all in-scope; ANC4+/facility excluded — no region-level source within the 12 datasets).

**Mediation** (standardized, population-weighted WLS, 2000-rep bootstrap 95% CI, N=16 — hypothesis-generating, council R2):

| X | M | Y | a (X→M) | b (M→Y\|X) | c′ direct | c total | indirect a·b | 95% CI | mediated? |
|---|---|---|--:|--:|--:|--:|--:|---|:--:|
| Secondary+ | service | **U5MR** | 0.52 | 0.42 | −0.88 | −0.66 | 0.22 | [−0.25, 0.94] | no |
| Gender-equity | service | U5MR | 0.54 | 0.39 | −0.87 | −0.66 | 0.21 | [−0.48, 0.56] | no |
| Secondary+ | service | Child anaemia | 0.52 | 0.21 | −1.07 | −0.96 | 0.11 | [−0.19, 0.40] | no |
| Secondary+ | service | ASFR 15–19 | 0.52 | 0.13 | −0.69 | −0.62 | 0.07 | [−0.21, 0.63] | no |
| Gender-equity | service | ASFR 15–19 | 0.54 | 0.07 | −0.62 | −0.58 | 0.04 | [−0.48, 0.22] | no |

### Interpretation (honest, hypothesis-generating)
1. **Strong total ecological associations**: higher female education and gender equity track with **lower U5MR, child anaemia and adolescent fertility** (total effects ≈ −0.6 to −1.0 SD). Education/equity → more RH-service use is also strong (a ≈ 0.65).
2. **No supported mediation through measured RH-service use** — every indirect effect's bootstrap 95% CI spans 0 (point estimates small). The association operates mainly through the **direct path**, not service utilisation. Two plausible reasons, both pre-empted by the council's banked evidence: (a) a **ceiling effect** — skilled delivery already ≈ 89% nationally, leaving little between-region variance to mediate; (b) consistency with **CONTRASTING** findings (Chol Chol 2019 weak service links; Bliznashka 2021 null) that empowerment→health is not reliably service-mediated.
3. All wide CIs reflect the **N=16 ceiling** — these are exploratory, not confirmatory (stated up front).

## Verification (`phase4_verify.py`, exit 0)
LISA covers all 261; Moran's I ∈[−1,1] & significant; ML R² ∈(0,1), SHAP 261 rows; **mediation identity c = c′ + a·b holds for all 5 models**; α∈(0,1); index mean-centred.

## Outputs
`spatial_global_moran_261.csv`, `maup_sensitivity.csv`, `lisa_districts_261.csv`, `rf_district_performance.csv`, `rf_district_importance.csv`, `shap_values_district.csv`, `outputs/figures/shap_summary_district.png`, `gei_construction.csv`, `mediation_results.csv`, `data/processed/analytic_region_16_modeling.csv`.

## Deferred to Phase 5 (visualisation)
261-district choropleths + LISA cluster maps, mediation path diagram, forest plot of effects — figure/dashboard/poster rendering (bespoke HI-EI pipeline).
