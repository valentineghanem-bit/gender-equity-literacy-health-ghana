"""
Phase 4b — DESCRIPTIVE interpretable ML at 261 districts (council R1: descriptive only, no inference,
on the genuinely district-varying determinant layer). Characterises which socioeconomic determinants
structure district deprivation (poverty incidence). Random Forest + SHAP + permutation importance.
NO p-values / causal claims — this describes co-structure, complementing the LISA maps.
Outputs:
  outputs/tables/rf_district_performance.csv
  outputs/tables/rf_district_importance.csv
  outputs/data/shap_values_district.csv
  outputs/figures/shap_summary_district.png
"""
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, KFold
from sklearn.inspection import permutation_importance
import shap

ROOT = Path(__file__).resolve().parents[1]
PROC, OUTT, OUTD, OUTF = ROOT/"data"/"processed", ROOT/"outputs"/"tables", ROOT/"outputs"/"data", ROOT/"outputs"/"figures"
for d in (OUTT,OUTD,OUTF): d.mkdir(parents=True, exist_ok=True)

dm = pd.read_csv(PROC/"district_master_261.csv")
target = "poverty_incidence"
feats = ["illiteracy_rate","uninsured_rate","unemployment_rate","female_15_64_share","lat","lon"]
X, y = dm[feats].to_numpy(), dm[target].to_numpy()
labels = {"illiteracy_rate":"Illiteracy rate","uninsured_rate":"Uninsured rate","unemployment_rate":"Unemployment rate",
          "female_15_64_share":"Female 15-64 share","lat":"Latitude (northward)","lon":"Longitude"}

rf = RandomForestRegressor(n_estimators=600, max_depth=None, min_samples_leaf=3, random_state=42, n_jobs=-1)
cv = KFold(n_splits=5, shuffle=True, random_state=42)
r2 = cross_val_score(rf, X, y, cv=cv, scoring="r2")
rf.fit(X, y)
pd.DataFrame([{"target":target,"model":"RandomForest","n":len(dm),"n_features":len(feats),
              "cv_r2_mean":round(r2.mean(),3),"cv_r2_sd":round(r2.std(),3),
              "note":"DESCRIPTIVE structure characterisation; no inference / no causal claim"}]
            ).to_csv(OUTT/"rf_district_performance.csv", index=False)
print(f"[4b] RF descriptive 5-fold CV R2 = {r2.mean():.3f} ± {r2.std():.3f}")

# permutation importance + gini importance
pi = permutation_importance(rf, X, y, n_repeats=50, random_state=42, n_jobs=-1)
imp = pd.DataFrame({"feature":feats,"label":[labels[f] for f in feats],
                    "gini_importance":np.round(rf.feature_importances_,4),
                    "perm_importance":np.round(pi.importances_mean,4),
                    "perm_sd":np.round(pi.importances_std,4)}).sort_values("perm_importance",ascending=False)
imp.to_csv(OUTT/"rf_district_importance.csv", index=False)
print("[4b] importance:\n"+imp.to_string(index=False))

# SHAP
expl = shap.TreeExplainer(rf)
sv = expl.shap_values(X)
sdf = pd.DataFrame(sv, columns=[f"shap_{f}" for f in feats])
sdf.insert(0,"district_261",dm["district_261"]); sdf.insert(0,"region",dm["region"])
sdf.to_csv(OUTD/"shap_values_district.csv", index=False)
meanabs = pd.DataFrame({"feature":feats,"mean_abs_shap":np.round(np.abs(sv).mean(0),4)}).sort_values("mean_abs_shap",ascending=False)
print("[4b] mean|SHAP|:\n"+meanabs.to_string(index=False))

plt.figure()
shap.summary_plot(sv, pd.DataFrame(X,columns=[labels[f] for f in feats]), show=False, cmap=plt.get_cmap("viridis"))
plt.title("District determinants of poverty incidence (descriptive SHAP, n=261)", fontsize=10)
plt.tight_layout(); plt.savefig(OUTF/"shap_summary_district.png", dpi=200, bbox_inches="tight"); plt.close()
print("[4b] shap_summary_district.png written. DONE.")
