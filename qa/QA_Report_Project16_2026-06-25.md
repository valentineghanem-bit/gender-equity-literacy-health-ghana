# QA Report — Project 16: Gender Equity, Literacy & Multi-Domain Health (Ghana)

Date: 2026-06-25 · Verdict: **QA_PASSED** (badge: `QA_PASSED_2026-06-25.txt`).

## 6-Pass QA
- **Pass 1 — Provenance/data integrity:** region master 16×27, 0 missing; national population-weighted values reproduce published 2022 DHS Ghana figures (U5MR 41.5; skilled delivery 88.9%; modern CPR 28.1%; child anaemia 46.8%; ASFR 61.6). PASS.
- **Pass 2 — Methodological/statistical:** Moran's I illiteracy 0.76 / poverty 0.63 (p=0.001), MAUP-robust; descriptive RF R²=0.88; mediation identity (total = direct + indirect) holds across all models. PASS.
- **Pass 3 — Cross-artefact sync (12 fields):** headline finding, N=16/261, Moran's I, RF R², total effect (−0.66 SD), national U5MR (41.5), north–south gap, null-mediation message and design verified consistent across manuscript, dashboard and poster. PASS.
- **Pass 4 — Q1 format:** IMRAD + structured abstract; Tables 1–2 and Figures 1–5 embedded and cross-cited in Results and Discussion; STROBE/RECORD-Spatial/TRIPOD-AI checklists. PASS.
- **Pass 5 — Citations/anti-hallucination:** 25 Vancouver references, Quad-Connector/Consensus-cleared, zero retracted; no unverified claim markers. PASS.
- **Pass 6 — Reproducibility/ethics/Tenet-20:** `run_all.sh` + `Dockerfile` + per-phase verification; GHS-ERB exemption; no manuscript committed to the repo. PASS.

## Deliverables (all Q1)
Manuscript (local; PLOS Global Public Health, APC $0 for Ghana) · Dashboard (HI-EI) · Poster (A0) · Master CSV + data dictionary · GitHub repository (CI passing).

## External follow-up (author)
Zenodo DOI on release; funding/competing-interests statements at submission.
