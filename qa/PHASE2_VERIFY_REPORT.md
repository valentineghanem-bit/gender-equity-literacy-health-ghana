# Phase 2 — Verification Report (in-scope, pre-Phase-5 gate)

Run: `analysis/phase2_verify.py` · 2026-06-25 (12-dataset scope) · **Result: ALL CHECKS PASSED (exit 0).**

## A. District frame & crosswalk integrity
- `district_master_261.csv`: 261 rows, **261 unique districts**, 16 regions.
- Crosswalk: 261 rows, **3 structural gaps** (Guan, Sagnarigu, Awutu Senya West), **258 linked**. ✓

## B/C. DHS extraction integrity (key correctness test)
All **21 GH2022DHS indicators** (12-dataset scope): exactly **1 source row per region** after `IsPreferred` (`maxrows/reg=1`), **16 regions each**, **no silent averaging**, **no pre-2022 alias leakage**. ✓

## D. Completeness
Region table **16×27** (21 DHS + 6 context); **0 columns not 16/16**; **0 pending**. ✓

## E. National pop-weighted sanity vs published DHS-2022 Ghana
| Indicator | Weighted national | ~DHS-2022 |
|---|---|---|
| U5MR | 41.5 | ~40 |
| IMR | 28.8 | ~28 |
| NMR | 18.3 | ~17 |
| Skilled delivery | 88.9 | ~88 |
| Modern CPR (married) | 28.1 | ~28 |
| Children any anaemia | 46.8 | ~49 |
| Women any anaemia | 41.1 | ~45 |
| ASFR 15–19 (from sdgs) | 61.6 | ~66 |
| Illiteracy rate (proxy) | 25.7 | ~22 |

All within band; most near the point estimate — strong independent confirmation of correct extraction.

**Verdict:** Phase 2 has no outstanding errors or inconsistencies; scoped to the 12 datasets. Cleared to proceed.
