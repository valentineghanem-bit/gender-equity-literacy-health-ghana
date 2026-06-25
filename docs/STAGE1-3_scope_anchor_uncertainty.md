# Stages 1–3 closure — Scope-lock · Anchor · Uncertainty register

Retro-documented 2026-06-25 to close the partially-done early stages (per the 14-stage workflow). Content was implicit in the design lock and limitations; this formalises it.

## Stage 1 — Strategy & Scope (`/scope-lock` + `/anchor`)
**Question.** Across Ghana, where does gender-equity/literacy disadvantage sit, how does it relate to multi-domain child/maternal health, and is the relationship mediated by reproductive-health-service use?

**In scope:** 12 named datasets; 16-region DHS-2022 inference; 261-district Census spatial/mapping; X (gender equity, education, literacy) → M (RH services) → Y (U5MR primary; anaemia; adolescent fertility); spatial autocorrelation, descriptive ML, ecological mediation.
**Out of scope (explicit):** individual-level/causal claims; district-level health *outcomes* (no SAE — flagged future work); datasets outside the 12-list; longitudinal/temporal modelling.
**Unit of inference:** 16 regions (mediation/ML inference); 261 districts (spatial structure + mapping only).

**Anchor / thesis (locked):** *Gender equity and female literacy are ecological determinants of multi-domain health that operate through hypothesised RH-service mediators; we quantify the spatial structure (261 districts) and the regional pathway (16 regions), producing a spatially-targeted, SDG-aligned tool.* No section proceeded before this was fixed.

## Stage 2 — Exhaustive Extraction + `/uq-flag` (uncertainty register)
Extraction: 21 DHS indicators + 6 Census context vars, 16/16 complete, one preferred row per region (verified). Literature: 25 Quad-Connector/Consensus-cleared sources.

**Uncertainty register (flag each key quantity):**
| Quantity | Uncertainty | Note |
|---|---|---|
| National pop-wt values | LOW | reproduce published DHS-2022 (validation) |
| Global/Local Moran's I (261) | LOW | significant, permutation p=0.001; MAUP-robust |
| RF R²=0.88 / SHAP | MODERATE | descriptive only; not inferential |
| DHS estimates for new small regions (Ahafo, Oti, North East, Savannah, Western North) | **HIGH** | wide sampling CIs; treated as fixed (limitation) |
| Gender-equity index α=0.586 | MODERATE | multidimensional construct, not single latent |
| Mediation effects (N=16) | **HIGH** | exploratory; wide bootstrap CIs; null may be power-limited |
| Region-level LISA on outcomes | **HIGH** | underpowered at N=16 (used descriptively) |

## Stage 3 — Distillation (`/compact`)
Distilled to the analysis-ready masters (`region_master_16_analytic.csv`, `district_master_261.csv`, `analytic_region_16_clean/modeling.csv`) with provenance + crosswalk. No raw bulk carried into modelling beyond what each step requires.
