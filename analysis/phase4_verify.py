"""
Phase 4 — independent verification. Exit non-zero on any hard failure.
(A) spatial: LISA clusters cover all 261; p in [0,1]; global Moran in [-1,1] & significant.
(B) ML: shap file = 261 rows; importances finite; CV R2 in (0,1).
(C) mediation identity: total c == direct c' + indirect a*b (linear-model invariant); CI lo<=hi.
(D) index: alpha in (0,1); gei mean ~ 0.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
PROC, OUTT, OUTD = ROOT/"data"/"processed", ROOT/"outputs"/"tables", ROOT/"outputs"/"data"
fail=[]

# A spatial
gm = pd.read_csv(OUTT/"spatial_global_moran_261.csv")
lisa = pd.read_csv(OUTD/"lisa_districts_261.csv")
print(f"[A] global Moran rows={len(gm)}; lisa rows={len(lisa)}")
if len(lisa)!=261: fail.append(f"LISA rows {len(lisa)}!=261")
for c in ["illiteracy_rate","poverty_incidence"]:
    tot = lisa[f"{c}_cluster"].value_counts().sum()
    if tot!=261: fail.append(f"LISA {c} clusters cover {tot}!=261")
    if not lisa[f"{c}_p"].between(0,1).all(): fail.append(f"LISA {c} p out of [0,1]")
if not gm["morans_I"].between(-1,1).all(): fail.append("global Moran out of [-1,1]")
if not (gm["p_perm"]<0.05).all(): fail.append("a global Moran not significant (expected sig)")

# B ML
perf = pd.read_csv(OUTT/"rf_district_performance.csv")
sv = pd.read_csv(OUTD/"shap_values_district.csv")
imp = pd.read_csv(OUTT/"rf_district_importance.csv")
r2 = float(perf["cv_r2_mean"][0])
print(f"[B] RF CV R2={r2}; shap rows={len(sv)}; top feature={imp.iloc[0]['feature']}")
if len(sv)!=261: fail.append(f"shap rows {len(sv)}!=261")
if not (0<r2<1): fail.append(f"CV R2 {r2} not in (0,1)")
if not np.isfinite(imp["perm_importance"]).all(): fail.append("non-finite importance")

# C mediation identity
med = pd.read_csv(OUTT/"mediation_results.csv")
print("[C] mediation identity check (c == c' + a*b):")
for _,r in med.iterrows():
    lhs=r["c(total)"]; rhs=r["c'(direct)"]+r["indirect(a*b)"]
    ok=abs(lhs-rhs)<=0.02
    print(f"    {r['X'][:22]:22s}->{r['Y']:22s} c={lhs:.3f} c'+ab={rhs:.3f} {'OK' if ok else 'FAIL'}")
    if not ok: fail.append(f"mediation identity off: {r['X']}->{r['Y']} {lhs} vs {rhs}")
    lo,hi=[float(v) for v in r["indirect_CI95"].strip("[]").split(",")]
    if lo>hi: fail.append(f"CI inverted {r['X']}->{r['Y']}")

# D index
gc = pd.read_csv(OUTT/"gei_construction.csv")
mod = pd.read_csv(PROC/"analytic_region_16_modeling.csv")
alpha=float(gc["cronbach_alpha"][0])
print(f"[D] Cronbach alpha={alpha}; gei mean={mod['gei'].mean():.2e}; rows={len(mod)}")
if not (0<alpha<1): fail.append(f"alpha {alpha} not in (0,1)")
if abs(mod['gei'].mean())>1e-9: fail.append("gei not mean-centred")
if len(mod)!=16: fail.append("modeling table != 16 rows")

print("\n"+"="*60)
if fail:
    print(f"VERIFY PHASE 4: {len(fail)} ISSUE(S):")
    for f in fail: print("  - "+f);
    sys.exit(1)
print("VERIFY PHASE 4: ALL CHECKS PASSED — Phase 4 clean.")
