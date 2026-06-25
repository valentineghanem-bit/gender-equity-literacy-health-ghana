# Progress — Project 16

**Done**
- Scaffold + evidence/ subfolders.
- Phase 0 audited/reconciled (5 critical + 5 moderate + 2 minor).
- Design LOCKED: Refined Option C (Hybrid).
- Phase 1 lit review & six-dimension gap analysis (Quad-Connector).
- **Phase 1 issues fully resolved via epid-council** (R1–R11): ML moved to 261-district descriptive; ecological mediation reframed (precision-weighted, bootstrap CIs); MAUP + measurement-error + ecological-fallacy controls added; human-capital axis (secondary+ primary, literacy sensitivity, never joint); FGC dropped; U5MR primary; CONTRASTING evidence banked (Bliznashka 2021, Christian 2023, Shih 2023, Fontanet 2023, Hogg 2025). Logged to AIPOCH_Learning_Log.md.
- **Phase 2 master build** (`analysis/phase2_build_master.py`): district_master_261 + vetted crosswalk (3 structural gaps, 0 unmatched) + region_master_16_analytic (**21 DHS indicators + 6 context = 16×27, all 16/16, 0 pending**, QA-passed). MRH → outputs/data/mrh_national_context.csv (Intro context).
- **RESCOPED to the 12-dataset list (2026-06-25):** ASFR 15–19 re-sourced from `sdgs`; ANC4+/facility dropped (no in-scope region source); `mdgs`/`mics`/`fertility-rates` archived. See `docs/DATA_USAGE_AUDIT.md`.

- **Phase 2 VERIFIED** (`analysis/phase2_verify.py`, exit 0): no silent averaging (exactly 1 row/region ×21), 261/3-gap frame intact, 16×27 0-pending, national pop-weighted ≈ DHS-2022 benchmarks → `qa/PHASE2_VERIFY_REPORT.md`.
- **Phase 3 complete** (`analysis/phase3_clean_describe.py`): cleaning audit trail + `variable_provenance.csv` (28) + `analytic_region_16_clean.csv` (16×54, belt + z-scores) + `table1_descriptives.csv` + `table1_by_belt.csv` (monotonic north–south gradient) → `docs/PHASE3_CLEANING_PROVENANCE.md`.

- **Phase 3 VERIFIED** (`phase3_verify.py`, exit 0).
- **Phase 4 complete + VERIFIED** (`phase4a/b/c_*.py`, `phase4_verify.py` exit 0; `docs/PHASE4_ANALYSIS.md`):
  - Spatial 261: Moran's I illiteracy 0.759 / poverty 0.633 (p=.001); LISA 56/44 HH clusters; MAUP scale-robust (16-region 0.80/0.68).
  - Descriptive RF/SHAP (261): CV R²=0.876; illiteracy dominant determinant of poverty (mean|SHAP| 8.3).
  - Gender-equity index built (Cronbach α=0.586); RH service index; human-capital axis.
  - Ecological mediation (16, pop-weighted, bootstrap, N=16 exploratory): strong total/direct effects (education/equity → lower U5MR/anaemia/ASFR, ~−0.6 SD); **NO supported service-mediation** (all indirect CIs span 0; ceiling effect + consistent with CONTRASTING evidence).

**In progress / blockers**
- None. Phases 0–4 complete and independently verified.

- **Data-usage audit + RESCOPE to 12 datasets (2026-06-25):** all 12 listed datasets used; 3 out-of-scope (mdgs/mics/fertility-rates) removed+archived; ASFR re-sourced from sdgs; ANC4+/facility dropped. Phases 2→4 rebuilt + re-verified green (P2/P3/P4 exit 0). All docs de-staled. → `docs/DATA_USAGE_AUDIT.md`.
- **Phase 5 COMPLETE + verified:** 6 figures + HI-EI dashboard + A0 poster (self-contained, base64; council-framed associational headline + caveat box; browser-verified, 0 console errors) → `analysis/phase5_figures.py`, `analysis/phase5_dashboard_poster.py`, `dashboard/HI-EI_Dashboard.html`, `poster/A0_Poster.html`.
- **Standing order saved:** decide via epid-council, never ask user (`memory/use-epid-council-to-decide.md`). Phase-5 framing decided by council.

- **Bespoke generator recovered + made permanent (2026-06-25):** full HI-EI toolkit (generator+templates+echarts+inliner+geojson) preserved at `_system/bespoke/`; Project-16 config added; **canonical bespoke dashboard+poster regenerated** (offline ECharts, browser-verified: 10 dashboard canvases / 4 poster charts, no vendor leak) replacing the custom fallback (archived).
- **Plotly integrated (council-decided):** plotly.py + plotly.min.js added to toolkit; `_system/bespoke/CHART_CATALOG.md` (selection menu) + per-project chart plan (`docs/PHASE5_CHART_PLAN.md`); new Project-16 Plotly figures (parallel-coordinates + dumbbell) → `outputs/figures/plotly_supplementary.html` (browser-verified). dash family = inspiration only (not a dep). Standing policy saved: council picks per-project chart set, varied, anti-slop (`memory/per-project-chart-selection`).

- **Phase 6 STARTED (2026-06-25):** Q1 IMRAD draft — Methods + Results drafted from verified pipeline; Intro/Discussion/Abstract scaffolded with banked Phase-1 citations + [CITE-VERIFY] markers → `manuscript/manuscript_draft_v0.md` + `manuscript/PHASE6_MANUSCRIPT_PLAN.md`. NOT complete.

- **Phase 6 manuscript v1 drafted** (`manuscript/manuscript_draft_v1.md`): full IMRAD + structured abstract + 25 cleared Vancouver refs; council Trigger A applied (associational; ≥2 CONTRASTING + Bessing 2026 same-data corroboration; SWPER-validated index). Journal DECIDED: **PLOS Global Public Health** (APC $0 for Ghana — R4L verified). New citations banked: Ewerling 2017, Bessing 2026, Cao 2026, Bai-Sesay 2025, Donkoh 2024.
- **Q1 standard hardcoded** for all 5 deliverables (`memory/q1-format-all-deliverables` + `_system/Q1_DELIVERABLE_STANDARDS.md`).

**Next (Phase 6 completion)**
- STROBE/RECORD-Spatial/TRIPOD-AI checklists → council Trigger B sweep → /qa (5 deliverables vs Q1 spec) → render .docx (docx skill, local only) → GitHub repo (Q1) + Zenodo DOI + /github-publish (manuscript excluded).

**Resume instruction**
Read this + task_plan.md + docs/PHASE1_*§6b + docs/PHASE2_DATA_BUILD.md. Re-run `analysis/phase2_build_master.py` after adding any Cowork files. Then Phase 3.
