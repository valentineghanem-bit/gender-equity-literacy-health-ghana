# Gender Equity, Literacy and Multi-Domain Health Outcomes: Spatial Machine-Learning Mediation Analysis in Ghana

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/valentineghanem-bit/gender-equity-literacy-health-ghana/actions/workflows/ci.yml/badge.svg)](.github/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11-blue) ![R](https://img.shields.io/badge/R-spdep-276DC3) ![Docker](https://img.shields.io/badge/Docker-reproducible-2496ED)
<!-- DOI badge to be added on Zenodo release: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX) -->

## 1. Overview
Ecological spatial machine-learning **mediation** study of how **gender equity and female literacy** relate to **multi-domain child and maternal health** (under-five mortality, anaemia, adolescent fertility) across Ghana, and whether **reproductive-health-service use mediates** the link. Inference is at the **16 regions** (2022 DHS); high-resolution spatial structure and mapping use **261 districts** (2021 Census).

## 2. Key findings
- Female illiteracy and poverty are **strongly spatially clustered** (Global Moran's I 0.76 and 0.63, both p=0.001), concentrating in the northern savannah; **scale-robust** (16-region 0.80/0.63 — MAUP-checked).
- Illiteracy is the **dominant structural correlate** of district poverty (descriptive Random Forest R²=0.88; mean|SHAP| 8.3).
- Higher female education/gender equity tracks **lower** under-five mortality (total standardized effect −0.66), child anaemia (−0.96) and adolescent fertility (−0.62) — but **service-mediation is not supported** (all indirect-effect 95% CIs span 0; service coverage already ~89%).
- *Associational, ecological, cross-sectional; inference N=16 (exploratory).*

## 3. Study design
Ecological cross-sectional, Refined Hybrid (Option C): 16-region DHS inference + 261-district Census spatial layer (3 structural-gap districts merged to parent polygons for rendering only — 261 frame retained).

## 4. Data sources
Twelve public datasets: 2022 Ghana DHS subnational indicators (gender, education, literacy, SDG, FP2020, anaemia, child mortality, HIV testing, HIV knowledge), the 2021 Ghana Census 261-district socioeconomic master sheet, the 260-polygon district GeoJSON, and the WHO GHO maternal-reproductive-health series (national context). See `docs/datalog_article16_corrected.md`.

## 5. Repository structure
```
data/{raw,processed}  analysis/  src/  outputs/{data,figures,tables}
docs/  qa/  tests/  dashboard/  poster/  evidence/  .github/workflows/
manuscript/  (LOCAL-ONLY — git-excluded, Tenet 20)   _archive/
```

## 6. Methods / pipeline
Region harmonisation + one-value-per-region extraction → 261-district frame + vetted crosswalk → cleaning/provenance → centroid-KNN Global/Local Moran's I (+MAUP sensitivity) → descriptive RF+SHAP → population-weighted bootstrap mediation. Each phase has a verification script (`phase{2,3,4}_verify.py`, all exit 0). R cross-check: `analysis/spatial_diagnostics.R` (spdep).

## 7. Reproducibility
```bash
pip install -r requirements.txt
bash run_all.sh          # runs phases 2–5 end-to-end
# or, containerised:
docker build -t gelh-ghana . && docker run --rm gelh-ghana
```

## 8. Outputs
`outputs/figures/` (choropleths, LISA maps, SHAP, mediation forest, Plotly supplementary), `outputs/tables/` (Table 1, spatial, mediation, importance), `outputs/data/` (LISA, MRH national context), `data/processed/` (master datasets + crosswalk).

## 9. Dashboard & poster
`dashboard/HI-EI_Dashboard.html` (interactive HI-EI; offline ECharts) and `poster/A0_Poster.html` (A0). Self-contained; colourblind-safe; associational caveat box. Open in any browser.

## 10. Data dictionary
`data/processed/variable_provenance.csv` — every variable → role → source file → indicator → survey → transform. District crosswalk: `docs/district_crosswalk_261_to_260.csv`.

## 11. Analytical verification
`qa/` holds phase verification reports and the QA badge. National population-weighted values reproduce published 2022 DHS Ghana figures.

## 12. Citation
See `CITATION.cff`. Please cite the dataset/code release (Zenodo DOI on release) and the associated article (in preparation).

## 13. License & ethics
Code under **MIT** (`LICENSE`). Secondary analysis of de-identified public aggregate data; Ghana Health Service Ethics Review Board exemption for ecological secondary analysis. **No manuscript files are committed** (kept local; Tenet 20).

## 14. Acknowledgements & contact
DHS Program; Ghana Statistical Service (2021 Census); WHO Global Health Observatory. **Valentine Golden Ghanem** — valentineghanem@gmail.com.
