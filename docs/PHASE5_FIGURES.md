# Phase 5 — Publication Figures

**Project 16** · 2026-06-25 · `analysis/phase5_figures.py` (matplotlib only — raw-GeoJSON polygon renderer, no geopandas). 261-district frame. Anti-slop: colourblind-safe ramps, titles state the finding, labelled legends/colourbars, no chartjunk.

## Figures (`outputs/figures/`)
| File | Type | Finding |
|---|---|---|
| `fig_choropleth_illiteracy_261.png` | Choropleth (viridis) | Illiteracy concentrates in the northern districts (visually verified: N high / S low). |
| `fig_choropleth_poverty_261.png` | Choropleth (viridis) | Poverty incidence highest across the northern belt. |
| `fig_lisa_illiteracy_261.png` | LISA clusters (RdBu, CB-safe) | High-illiteracy hotspots (HH) blanket the north; low-illiteracy coldspots (LL) in the south. |
| `fig_lisa_poverty_261.png` | LISA clusters | High-poverty hotspots north; low coldspots south. |
| `fig_mediation_forest.png` | Forest plot | Strong negative total effects (education/equity → better outcomes); indirect (service-mediated) CIs all span 0. |
| `shap_summary_district.png` | SHAP beeswarm (Phase 4b) | Illiteracy dominates district poverty structure. |

## Rendering notes
- Choropleths colour the 260 GeoJSON polygons by the matched district value; the **3 structural-gap districts** (Guan/Sagnarigu/Awutu Senya West) are shown via their parent polygon (caption footnote) — data rows retained (261 frame). 2 legacy polygons with no Master-Sheet match render light grey (no-data).
- LISA palette: HH `#b2182b`, LL `#2166ac`, HL `#ef8a62`, LH `#67a9cf`, NS `#f7f7f7` (ColorBrewer RdBu, CB-distinguishable).
- All inputs trace to the 12-dataset scope + the Phase-4 outputs.

## Verification
Each map visually inspected: correct Ghana outline, expected north–south gradient, legend/colourbar present and labelled. Forest-plot labels corrected (clean X→Y mapping).

## Dashboard + poster (COMPLETE)
Built by `analysis/phase5_dashboard_poster.py` (self-contained; KPIs computed from verified CSVs; verified figures base64-embedded). `bespoke_gen.js` was not in the local tree, so a reproducible in-repo builder was used instead (vanilla JS + inline SVG + base64 PNGs).
- `dashboard/HI-EI_Dashboard.html` — KPI cards (N–S U5MR gap, Moran's I ×2, total edu→U5MR −0.66 SD, RF R²=0.88), inline-SVG belt chart, 6 embedded figures, sortable region table, persistent **caveat box**.
- `poster/A0_Poster.html` — finding banner, methods strip, spatial panels, association-not-mediation panel, **limitations box**, spatially-targeted implications.
- **Council-decided framing** (epid-council 2026-06-25, per standing order): associational headline; 261-district spatial result as quantitative anchor; null service-mediation shown honestly; mandatory caveat box on both.
- **Browser-verified** (preview server): dashboard 5 KPIs + 6 figs loaded + 16-row table + working sort, 0 console errors; poster finding/limitations/figures all present.

