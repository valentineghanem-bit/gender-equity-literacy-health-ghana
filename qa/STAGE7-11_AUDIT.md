# Stage 7–11 Audit (completing the skipped stages)

Date: 2026-06-25. Closes the gap flagged by the user: Stages 7 (logic), 8 (methodological), 9 (conceptual), 10 (production/figures), 11 (humanisation/PEEL) were previously skipped or only partially done.

## Stage 7 — Logic audit (PoDa + cite-verify:audit)
- Every claim traces to a cleared citation or to a verified pipeline output; cite-verify markers in the draft: **0** (grep clean).
- Mediation identity total = direct + indirect holds across all 5 models (phase4_verify).
- **Fix applied:** the null mediation was logically over-stated; added the "absence of evidence ≠ evidence of absence" caveat (power vs ceiling) to the Discussion.

## Stage 8 — Methodological audit (/peer-stress)
- Delivered via the epid-council (Trigger A drafting review + Trigger B pre-QA sweep + Reviewer-2 pre-submission stress-test).
- Hazards examined and defended: ecological fallacy, N=16 inference ceiling, pseudo-replication (explicitly avoided — true N=16, no district downscaling for inference), MAUP (16-vs-261 sensitivity), descriptive-only ML, common-source coupling. **No fatal flaw.**

## Stage 9 — Conceptual audit (/peer-stress-conceptual)
- Framing is **associational, not causal** (ecological cross-sectional) — enforced in v2 prose.
- **Confounding:** poverty is a plausible common cause of both education/equity and health; the ecological "direct effect" is a total association, not a confounding-purified estimate — stated.
- **Reverse causation / temporality:** cross-sectional; acknowledged.
- **Null-mediation interpretation:** reframed as "no detectable service mediation" (power-limited), not proof of none.

## Stage 10 — Production + figures EMBEDDED
- **Figures now embedded** in `manuscript/Gender_Equity_Literacy_Health_Ghana_v2.docx` (7 inline images: choropleths ×2, LISA ×2, SHAP, multivariate/dumbbell, mediation forest) with captions; references included.
- Static Figure 4 created (`outputs/figures/fig04_multivariate_disparity.png`) so the interactive Plotly panel has a print-embeddable counterpart.
- Format note: production is **Word .docx** (PLOS Global Public Health accepts Word); LaTeX (`/syntax-latex`) is optional for this venue and not required.

## Stage 11 — Full humanisation + PEEL
- v2 prose rewritten so **every body paragraph follows PEEL** (Point → Evidence → Explain → Link).
- Humanised (ghost): AI-isms removed, sentence rhythm varied, formulaic "first/second/finally" lists avoided, concrete over abstract.

## Net effect
Stages 7–11 are now addressed; v2 supersedes v1 as the current manuscript. Remaining formal niceties (a LaTeX build; the full 12-field sync-manifest wrapper) are optional for this venue and noted, not skipped silently.
