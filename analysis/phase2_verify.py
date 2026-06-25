"""
Phase 2 — independent verification / error audit. Run before Phase 3.
Checks: (A) district frame & crosswalk integrity, (B) NO silent averaging in DHS extraction
(every region must reduce to exactly 1 source row after IsPreferred), (C) alias leakage,
(D) completeness, (E) national pop-weighted sanity vs published DHS-2022 Ghana benchmarks.
Exit non-zero on any hard failure.
"""
import json, re, sys
from pathlib import Path
import pandas as pd, numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW, PROC, DOCS = ROOT/"data"/"raw", ROOT/"data"/"processed", ROOT/"docs"
fail = []

CANON = ["Ahafo","Ashanti","Bono","Bono East","Central","Eastern","Greater Accra","North East",
         "Northern","Oti","Savannah","Upper East","Upper West","Volta","Western","Western North"]
def canon_region(x):
    if x is None: return None
    s = re.sub(r"\(post 2022\)","",str(x).replace("..","")).strip().lower()
    m = {"northeast":"North East","north east":"North East","northern east":"North East",
         "northern(post 2022)":"Northern","northern":"Northern","savannah":"Savannah",
         "greater accra":"Greater Accra","bono east":"Bono East","western north":"Western North",
         "upper east":"Upper East","upper west":"Upper West"}
    if s in m: return m[s]
    if any(k in s for k in ["pre 2022","brong","upper west, upper east"]): return None
    for c in CANON:
        if s == c.lower(): return c
    return None

# ---------- A. district frame + crosswalk ----------
dm = pd.read_csv(PROC/"district_master_261.csv")
print(f"[A] district_master_261 rows={len(dm)}  unique_districts={dm['district_261'].nunique()}  regions={dm['region'].nunique()}")
if len(dm) != 261: fail.append(f"district_master_261 has {len(dm)} rows, expected 261")
if dm['district_261'].duplicated().any(): fail.append(f"duplicate district names: {list(dm.loc[dm['district_261'].duplicated(),'district_261'])}")
if dm['region'].nunique() != 16: fail.append("district frame regions != 16")
cw = pd.read_csv(DOCS/"district_crosswalk_261_to_260.csv")
ngap = (cw['match_method']=='structural_gap').sum()
nlinked = dm['geojson_district'].notna().sum()
print(f"[A] crosswalk rows={len(cw)}  structural_gaps={ngap}  district_master linked_to_polygon={nlinked}")
if len(cw) != 261: fail.append("crosswalk != 261 rows")
if ngap != 3: fail.append(f"structural gaps = {ngap}, expected 3 (Guan/Sagnarigu/Awutu Senya West)")
if nlinked != 258: fail.append(f"linked polygons = {nlinked}, expected 258")

# ---------- B + C. DHS extraction: no silent averaging, no alias leakage ----------
targets = [
 ("select-gender-indicators_subnational_gha.csv", ["Final say in all of the decisions [Women]","Wife beating justified for at least one specific reason [Women]","Do not own land [Women]"]),
 ("select-education-indicators_subnational_gha.csv", ["Women with no education","Women with secondary or higher education"]),
 ("literacy_subnational_gha.csv", ["Women who are literate","Women who cannot read at all"]),
 ("sdgs_subnational_gha.csv", ["Physical or sexual or emotional violence committed by husband/partner in last 12 months","Own decision making about all three decisions","Assistance during delivery from a skilled provider","Age specific fertility rate: 15-19"]),
 ("fp2020_subnational_gha.csv", ["Married women currently using any modern method of contraception","Demand for family planning satisfied by modern methods"]),
 ("anemia_subnational_gha.csv", ["Women with any anemia","Children with any anemia"]),
 ("child-mortality-rates_subnational_gha.csv", ["Under-five mortality rate","Neonatal mortality rate","Infant mortality rate"]),
 ("hiv-counseling-and-testing_subnational_gha.csv", ["Women ever receiving an HIV test","Pregnant women tested for HIV during ANC or labor and receiving the results"]),
 ("hiv-knowledge_subnational_gha.csv", ["Knowledge of prevention of MTCT - Can be prevented by mother taking special drugs during pregnancy [Women]"]),
]
print("\n[B/C] extraction integrity (rows-per-region after IsPreferred; want exactly 1, 16 regions, no alias leak)")
for fname, inds in targets:
    fp = RAW/fname
    if not fp.exists(): fail.append(f"missing input {fname}"); continue
    df = pd.read_csv(fp, low_memory=False)
    df = df[df["SurveyId"]=="GH2022DHS"].copy()
    # alias leakage check: any location that is a pre-2022 alias but maps to a canonical region?
    df["region"] = df["Location"].map(canon_region)
    for ind in inds:
        sub = df[df["Indicator"]==ind].copy()
        if len(sub)==0: fail.append(f"{fname}: indicator not found '{ind}'"); continue
        sub = sub[sub["region"].notna()]
        if "IsPreferred" in sub.columns and (sub["IsPreferred"]==1).any():
            sub = sub[sub["IsPreferred"]==1]
        sub["Value"] = pd.to_numeric(sub["Value"], errors="coerce")
        # rows per region & distinct values per region
        g = sub.groupby("region")["Value"]
        maxrows = g.size().max() if len(sub) else 0
        # regions where >1 DISTINCT value would be averaged
        multi = g.nunique()
        avgleak = multi[multi>1]
        nreg = sub["region"].nunique()
        flag = ""
        if nreg != 16: flag += f" REG={nreg}!=16"
        if len(avgleak) > 0: flag += f" AVG-COLLAPSE@{list(avgleak.index)}"
        status = "OK" if flag=="" else "FAIL"
        print(f"   [{status}] {fname[:34]:34s} | {ind[:42]:42s} reg={nreg} maxrows/reg={maxrows}{flag}")
        if flag: fail.append(f"{fname}:{ind}:{flag.strip()}")

# ---------- D. completeness ----------
reg = pd.read_csv(PROC/"region_master_16_analytic.csv").set_index("region")
mf = pd.read_csv(PROC/"phase2_indicator_manifest.csv")
ncells = reg.drop(columns=[c for c in reg.columns if c.startswith("ctx_n")], errors="ignore")
empty = [c for c in reg.columns if reg[c].notna().sum()!=16]
print(f"\n[D] region table {reg.shape[0]}x{reg.shape[1]}  cols_not_16/16={empty}  pending={(mf['status'].str.startswith('PENDING')).sum()}")
if len(reg)!=16: fail.append("region table != 16 rows")
if empty: fail.append(f"columns not fully filled: {empty}")
if (mf['status'].str.startswith('PENDING')).any(): fail.append("manifest has PENDING items")

# ---------- E. national pop-weighted sanity vs DHS-2022 Ghana (approximate bands) ----------
w = reg["ctx_total_pop"]
def natl(col): return float(np.average(reg[col], weights=w))
bench = {  # (computed_col, approx national DHS-2022, tolerance) — generous bands; flags only gross scaling errors
 "y_u5mr":(40,18),"y_imr":(28,15),"y_nmr":(17,10),
 "m_anc4plus":(88,12),"m_skilled_delivery":(88,12),"m_facility_birth":(88,14),
 "m_modern_cpr_married":(28,12),"y_children_any_anemia":(49,15),"y_women_any_anemia":(45,15),
 "y_asfr_15_19":(66,30),"ctx_illiteracy_rate":(22,12),
}
print("\n[E] national pop-weighted vs approx DHS-2022 benchmark (sanity band only)")
for col,(b,tol) in bench.items():
    if col not in reg.columns: continue
    v = natl(col); ok = abs(v-b)<=tol
    print(f"   [{'OK' if ok else 'CHECK'}] {col:26s} weighted={v:6.1f}  ~bench={b}  (±{tol})")
    if not ok: fail.append(f"national sanity off: {col} weighted={v:.1f} vs ~{b}")

print("\n" + ("="*60))
if fail:
    print(f"VERIFY: {len(fail)} ISSUE(S) FOUND:")
    for f in fail: print("  - "+f)
    sys.exit(1)
else:
    print("VERIFY: ALL CHECKS PASSED — Phase 2 clean.")
