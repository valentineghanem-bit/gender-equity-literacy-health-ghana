# Project 16 — Council-selected chart plan

Per the standing policy (`memory/per-project-chart-selection`), the epid-council chose this **project-specific** set from `_system/bespoke/CHART_CATALOG.md`, mirroring the gender-equity / literacy / multi-domain-health / spatial-ML-mediation theme. It is deliberately **not** the generic 6-chart template.

| # | Question it answers | Chart | Engine | Status |
|---|---|---|---|---|
| 1 | Where is female illiteracy worst? | Choropleth (female illiteracy, roam/zoom) | ECharts | ✓ dashboard |
| 2 | Where are illiteracy hotspots? | LISA 5-class cluster map | ECharts | ✓ dashboard |
| 3 | Which regions rank worst? | Sorted bar, LISA-coloured, threshold line | ECharts | ✓ dashboard |
| 4 | Does literacy track child mortality? | Scatter + regression + what-if | ECharts | ✓ dashboard |
| 5 | How do regions compare across ALL equity/health axes? | **Parallel coordinates** | plotly.py | ✓ plotly_supplementary |
| 6 | How big is the north–south divide per indicator? | **Dumbbell** | plotly.py | ✓ plotly_supplementary |
| 7 | Is the pathway service-mediated? | Forest (total/direct/indirect + CI) | matplotlib | ✓ figure |
| 8 | What structures district deprivation? | SHAP beeswarm (descriptive) | matplotlib/SHAP | ✓ figure |
| 9 | Spatial determinant maps | Illiteracy + poverty choropleths, LISA maps (261) | matplotlib | ✓ figures |

**Why this set (story arc):** map the *literacy* exposure spatially (1–3) → link it to the *health* outcome (4) → show the *multivariate* equity gradient in one view (5) → quantify the *disparity* (6) → test the *mechanism* and find it is direct not service-mediated (7) → characterise the *determinant structure* (8) → ground it in the 261-district spatial frame (9). No pie/3D; colourblind-safe throughout; each panel answers a distinct question (no redundancy).

**Engines used:** ECharts (maps, dashboard) + plotly.py (parallel-coordinates, dumbbell) + matplotlib/SHAP (forest, SHAP, choropleths). plotly.js is available inline (`_system/bespoke/`) for future PJ-native dashboard panels.
