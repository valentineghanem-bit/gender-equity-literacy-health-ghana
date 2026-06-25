"""
Phase 3 — independent verification. Run before Phase 4. Exit non-zero on any hard failure.
Checks: (A) clean dataset integrity vs Phase-2 (no value corruption), (B) belt partition,
(C) z-score correctness, (D) provenance completeness, (E) Table 1 recomputation.
"""
import sys
from pathlib import Path
import pandas as pd, numpy as np

ROOT = Path(__file__).resolve().parents[1]
PROC, OUTT = ROOT/"data"/"processed", ROOT/"outputs"/"tables"
fail=[]

p2  = pd.read_csv(PROC/"region_master_16_analytic.csv").set_index("region")
cl  = pd.read_csv(PROC/"analytic_region_16_clean.csv").set_index("region")
pv  = pd.read_csv(PROC/"variable_provenance.csv")
t1  = pd.read_csv(OUTT/"table1_descriptives.csv")
bt  = pd.read_csv(OUTT/"table1_by_belt.csv").set_index("belt")

# ---- A. clean dataset preserves Phase-2 values exactly ----
if len(cl)!=16: fail.append(f"clean dataset rows={len(cl)} != 16")
if set(cl.index)!=set(p2.index): fail.append("region set changed between Phase-2 and clean")
shared=[c for c in p2.columns if c in cl.columns]
maxdiff=0.0
for c in shared:
    d=(cl.loc[p2.index,c]-p2[c]).abs().max()
    maxdiff=max(maxdiff, 0 if pd.isna(d) else d)
print(f"[A] clean dataset: rows={len(cl)} shared_cols={len(shared)} max|diff vs Phase2|={maxdiff:.2e}")
if maxdiff>1e-9: fail.append(f"clean dataset altered Phase-2 values (max diff {maxdiff})")

# ---- B. belt partition ----
if "belt" not in cl.columns: fail.append("belt column missing")
else:
    vc=cl["belt"].value_counts().to_dict()
    print(f"[B] belt counts={vc}  total={cl['belt'].notna().sum()}")
    if cl["belt"].isna().any(): fail.append("region(s) with no belt")
    if sum(vc.values())!=16: fail.append("belt partition != 16")
    if set(vc.keys())!={"Northern","Middle","Coastal/South"}: fail.append(f"unexpected belts {set(vc.keys())}")

# ---- C. z-score correctness ----
zc=[c for c in cl.columns if c.endswith("_z")]
print(f"[C] z-cols={len(zc)}")
bad=[]
for z in zc:
    base=z[:-2]
    if base not in cl.columns: fail.append(f"z col {z} has no base"); continue
    recomputed=(cl[base]-cl[base].mean())/cl[base].std(ddof=0)
    if cl[z].isna().any(): bad.append(f"{z} NaN")
    if abs(cl[z].mean())>1e-9: bad.append(f"{z} mean={cl[z].mean():.2e}")
    if abs(cl[z].std(ddof=0)-1)>1e-9: bad.append(f"{z} sd={cl[z].std(ddof=0):.4f}")
    if (cl[z]-recomputed).abs().max()>1e-9: bad.append(f"{z} mismatch")
print(f"[C] z-score issues: {bad if bad else 'none'}")
if bad: fail.append(f"z-score problems: {bad}")

# ---- D. provenance completeness ----
analytic_cols=[c for c in p2.columns]   # 29 region columns
prov_cols=set(pv["column"])
missing=[c for c in analytic_cols if c not in prov_cols]
extra=[c for c in prov_cols if c not in analytic_cols and c!="ctx_who_mrh_national"]
print(f"[D] provenance rows={len(pv)}  cols_missing_prov={missing}  prov_refs_nonexistent={extra}")
if missing: fail.append(f"columns lacking provenance: {missing}")
if extra: fail.append(f"provenance references nonexistent columns: {extra}")
if pv["column"].duplicated().any(): fail.append("duplicate provenance columns")

# ---- E. Table 1 recomputation ----
if len(t1)!=len(analytic_cols): fail.append(f"table1 rows={len(t1)} != {len(analytic_cols)} cols")
t1i=t1.set_index("variable")
chk=["x_women_secondary_plus","y_u5mr","m_skilled_delivery","y_children_any_anemia"]
for c in chk:
    for stat,fn in [("mean",lambda s:s.mean()),("sd",lambda s:s.std(ddof=1)),
                    ("min",lambda s:s.min()),("median",lambda s:s.median()),("max",lambda s:s.max())]:
        exp=round(float(fn(p2[c])),2); got=float(t1i.loc[c,stat])
        if abs(exp-got)>0.01: fail.append(f"table1 {c}.{stat}={got} != recomputed {exp}")
# national pop-weighted spot check
w=p2["ctx_total_pop"]
exp=round(float(np.average(p2["y_u5mr"],weights=w)),2)
got=float(t1i.loc["y_u5mr","national_popwt"])
print(f"[E] table1 recompute spot-checks done; U5MR national_popwt table={got} recomputed={exp}")
if abs(exp-got)>0.05: fail.append(f"table1 national_popwt U5MR {got} != {exp}")
# by-belt spot check
exp=round(float(p2.assign(belt=cl["belt"]).groupby("belt")["y_u5mr"].mean()["Northern"]),1)
got=round(float(bt.loc["Northern","y_u5mr"]),1)
if abs(exp-got)>0.1: fail.append(f"by-belt U5MR Northern {got} != {exp}")
print(f"[E] by-belt U5MR Northern table={got} recomputed={exp}")

print("\n"+"="*60)
if fail:
    print(f"VERIFY PHASE 3: {len(fail)} ISSUE(S):")
    for f in fail: print("  - "+f)
    sys.exit(1)
print("VERIFY PHASE 3: ALL CHECKS PASSED — Phase 3 clean.")
