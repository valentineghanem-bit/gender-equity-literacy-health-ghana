#!/usr/bin/env bash
# Reproduce the full analysis end-to-end (phases 2-5). Each phase is independently verified.
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8

echo "== Phase 2: build master datasets =="
python analysis/phase2_build_master.py
python analysis/phase2_verify.py

echo "== Phase 3: clean + provenance + Table 1 =="
python analysis/phase3_clean_describe.py
python analysis/phase3_verify.py

echo "== Phase 4: spatial + ML + mediation =="
python analysis/phase4a_spatial.py
python analysis/phase4b_ml_shap.py
python analysis/phase4c_index_mediation.py
python analysis/phase4_verify.py

echo "== Phase 5: figures + dashboard + poster =="
python analysis/phase5_figures.py
python analysis/phase5b_regions_json.py
python analysis/phase5c_plotly_figures.py
python analysis/phase5_dashboard_poster.py

echo "== Optional R spatial cross-check (requires R + spdep) =="
command -v Rscript >/dev/null 2>&1 && Rscript analysis/spatial_diagnostics.R || echo "  (Rscript not found; skipping R cross-check)"

echo "DONE."
