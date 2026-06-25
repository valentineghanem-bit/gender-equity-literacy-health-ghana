# Task Plan — Project 16: Gender Equity, Literacy & Multi-Domain Health (Spatial ML Mediation, Ghana)

**Goal:** Ecological spatial-ML mediation study — gender equity & literacy → reproductive-health services → multi-domain health outcomes, Ghana.

## Phase checklist
- [x] **Phase 0** — Session init, Learning Log, data profiling (done in Cowork)
- [x] **Phase 0.5 — Scaffold** (canonical tree + evidence/ subfolders) — built 2026-06-24
- [x] **Phase 0.5 — Audit & reconcile** all Phase 0 errors/inconsistencies → `docs/PHASE0_AUDIT_RECONCILIATION.md`
- [x] **Design lock** — user selected **Refined Option C (Hybrid)** on 2026-06-24
- [x] **Phase 1** — Literature Review & Six-Dimension Gap Analysis (Quad-Connector) → `docs/PHASE1_LITERATURE_GAP_ANALYSIS.md` + `evidence/lit-review/evidence_bank_phase1.md` → **STOPPED for review & approval**
- [x] **Phase 1 issues resolved** — epid-council run; R1–R11 closed (ML→261-district descriptive, mediation reframed, MAUP/measurement-error/ecological-fallacy controls, human-capital axis, U5MR primary, CONTRASTING banked) → `PHASE1_LITERATURE_GAP_ANALYSIS.md` §6b
- [x] **Phase 2** — master build, **scoped to the 12-dataset list** → `analysis/phase2_build_master.py`; 261-district frame + vetted crosswalk (3 structural gaps) + 16-region analytic table (**21 DHS indicators + 6 context = 16×27, all 16/16, 0 pending**); ASFR from sdgs; ANC4+/facility excluded (no in-scope source); MRH national context → `docs/PHASE2_DATA_BUILD.md`, `docs/DATA_USAGE_AUDIT.md`.
- [x] **Phase 2 VERIFIED** — `analysis/phase2_verify.py` all checks pass (exit 0): no silent averaging (1 row/region ×21), 261/3-gap frame, 16×27 0-pending, national pop-wt ≈ DHS-2022 benchmarks → `qa/PHASE2_VERIFY_REPORT.md`
- [x] **Phase 3** — cleaning audit trail + provenance + Table 1 + analysis-ready clean dataset (belt stratifier + z-scores) → `analysis/phase3_clean_describe.py`, `docs/PHASE3_CLEANING_PROVENANCE.md`
- [x] **Phase 3 VERIFIED** — `phase3_verify.py` exit 0 (no value corruption, belt partition, z-scores, provenance, Table 1 recompute)
- [x] **Phase 4** — spatial (261 Moran 0.76/0.63 p=.001 + LISA + MAUP scale-robust), descriptive RF/SHAP (R²=0.88, illiteracy dominant), gender-equity index (α=0.586), ecological mediation (strong total/direct effects; NO service-mediation, CIs span 0 at N=16) → `phase4a/b/c`, `docs/PHASE4_ANALYSIS.md`; VERIFIED `phase4_verify.py` exit 0 (incl. c=c'+a·b identity)
- [x] **Phase 5 — Visualisation COMPLETE:** 6 figures (2 choropleths, 2 LISA, forest, SHAP) + **HI-EI dashboard** + **A0 poster** (self-contained, base64 figures, council-framed associational headline + caveat box) → `analysis/phase5_figures.py`, `analysis/phase5_dashboard_poster.py`, `dashboard/HI-EI_Dashboard.html`, `poster/A0_Poster.html`, `docs/PHASE5_FIGURES.md`. Browser-verified (all figs loaded, layout sound, no console errors, sortable table works).
- [~] **Phase 6 — Q1 manuscript drafted (v1):** full IMRAD (Intro/Methods/Results/Discussion/Abstract) + 25 cleared Vancouver refs + council Trigger A → `manuscript/manuscript_draft_v1.md`. Journal DECIDED: **PLOS Global Public Health** (APC $0 for Ghana, verified). REMAINING: STROBE/RECORD-Spatial/TRIPOD-AI checklists; council Trigger B sweep; /qa (5 deliverables vs `_system/Q1_DELIVERABLE_STANDARDS.md`); .docx render; GitHub repo + Zenodo DOI + /github-publish (manuscript excluded).

## Current phase
Phase 0 fully reconciled. Awaiting design lock, then Phase 1.

## Hard rules in force
- 261-district frame ALWAYS (Guan→Oti merge for rendering only).
- No pseudo-replication (true N=16 for DHS-level analysis).
- Manuscripts never committed to git.
- Quad-Connector + cite-verify on every Phase 1 claim.
