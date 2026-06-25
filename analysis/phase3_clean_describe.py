"""
Phase 3 — Cleaning audit trail, provenance log, Table 1 descriptives, analysis-ready dataset.
Consumes Phase-2 outputs (region_master_16_analytic.csv, district_master_261.csv). No new raw reads.
Produces:
  data/processed/variable_provenance.csv
  outputs/tables/table1_descriptives.csv
  outputs/tables/table1_by_belt.csv
  data/processed/analytic_region_16_clean.csv   (adds belt stratifier + z-scored analytic vars)
Index construction (gender-equity factor index) and all inferential work are deferred to Phase 4.
"""
from pathlib import Path
import pandas as pd, numpy as np

ROOT = Path(__file__).resolve().parents[1]
PROC, OUTT = ROOT/"data"/"processed", ROOT/"outputs"/"tables"
OUTT.mkdir(parents=True, exist_ok=True)

reg = pd.read_csv(PROC/"region_master_16_analytic.csv")
dm  = pd.read_csv(PROC/"district_master_261.csv")

# ---------- 1. PROVENANCE (column -> source -> indicator -> survey -> transform) ----------
prov = [
 # col, role, source_file, dhs_indicator, survey, transform
 ("x_final_say_women","EXPOSURE","select-gender-indicators_subnational_gha.csv","Final say in all of the decisions [Women]","GH2022DHS","region value, IsPreferred"),
 ("x_wifebeating_justified_women","EXPOSURE","select-gender-indicators_subnational_gha.csv","Wife beating justified for at least one specific reason [Women]","GH2022DHS","region value, IsPreferred"),
 ("x_no_land_women","EXPOSURE","select-gender-indicators_subnational_gha.csv","Do not own land [Women]","GH2022DHS","region value, IsPreferred"),
 ("x_women_no_education","EXPOSURE","select-education-indicators_subnational_gha.csv","Women with no education","GH2022DHS","region value, IsPreferred"),
 ("x_women_secondary_plus","EXPOSURE (human-capital, PRIMARY)","select-education-indicators_subnational_gha.csv","Women with secondary or higher education","GH2022DHS","region value, IsPreferred"),
 ("x_women_literate","EXPOSURE (human-capital, SENSITIVITY)","literacy_subnational_gha.csv","Women who are literate","GH2022DHS","region value, IsPreferred; never modelled jointly with education"),
 ("x_women_cannot_read","EXPOSURE","literacy_subnational_gha.csv","Women who cannot read at all","GH2022DHS","region value, IsPreferred"),
 ("x_ipv_any","EXPOSURE","sdgs_subnational_gha.csv","Physical or sexual or emotional violence committed by husband/partner in last 12 months","GH2022DHS","region value, IsPreferred"),
 ("x_own_decision_all3","EXPOSURE","sdgs_subnational_gha.csv","Own decision making about all three decisions","GH2022DHS","region value, IsPreferred"),
 ("m_skilled_delivery","MEDIATOR","sdgs_subnational_gha.csv","Assistance during delivery from a skilled provider","GH2022DHS","region value, IsPreferred"),
 ("m_modern_cpr_married","MEDIATOR","fp2020_subnational_gha.csv","Married women currently using any modern method of contraception","GH2022DHS","region value, IsPreferred"),
 ("m_fp_demand_satisfied_modern","MEDIATOR","fp2020_subnational_gha.csv","Demand for family planning satisfied by modern methods","GH2022DHS","region value, IsPreferred"),
 ("m_ever_hiv_test","MEDIATOR","hiv-counseling-and-testing_subnational_gha.csv","Women ever receiving an HIV test","GH2022DHS","region value, IsPreferred"),
 ("m_anc_hiv_test","MEDIATOR","hiv-counseling-and-testing_subnational_gha.csv","Pregnant women tested for HIV during ANC or labor and receiving the results","GH2022DHS","region value, IsPreferred"),
 ("m_hiv_mtct_knowledge_women","MEDIATOR","hiv-knowledge_subnational_gha.csv","Knowledge of prevention of MTCT - special drugs during pregnancy [Women]","GH2022DHS","PROXY for HIV knowledge (no comprehensive-AIDS-knowledge in 2022 export)"),
 ("y_women_any_anemia","OUTCOME","anemia_subnational_gha.csv","Women with any anemia","GH2022DHS","region value, IsPreferred"),
 ("y_children_any_anemia","OUTCOME","anemia_subnational_gha.csv","Children with any anemia","GH2022DHS","region value, IsPreferred"),
 ("y_u5mr","OUTCOME (PRIMARY)","child-mortality-rates_subnational_gha.csv","Under-five mortality rate","GH2022DHS","region value; NMR/IMR = sensitivity"),
 ("y_nmr","OUTCOME (sensitivity)","child-mortality-rates_subnational_gha.csv","Neonatal mortality rate","GH2022DHS","region value"),
 ("y_imr","OUTCOME (sensitivity)","child-mortality-rates_subnational_gha.csv","Infant mortality rate","GH2022DHS","region value"),
 ("y_asfr_15_19","OUTCOME","sdgs_subnational_gha.csv","Age specific fertility rate: 15-19","GH2022DHS","adolescent birth rate per 1000 (in-scope source)"),
 ("ctx_total_pop","CONTEXT","Master Sheet.xlsx","Total Population","Census 2021","sum of district pop per region"),
 ("ctx_n_districts","CONTEXT","Master Sheet.xlsx","(count)","Census 2021","districts per region (261 frame)"),
 ("ctx_illiteracy_rate","CONTEXT","Master Sheet.xlsx","Illiterate Population / Total Population","Census 2021","pop-weighted; ALL-AGE PROXY (denominator=total pop)"),
 ("ctx_uninsured_rate","CONTEXT","Master Sheet.xlsx","Uninsured Population / Total Population","Census 2021","pop-weighted"),
 ("ctx_poverty_incidence","CONTEXT","Master Sheet.xlsx","Incidence of Poverty","Census/GLSS","pop-weighted"),
 ("ctx_female_15_64_share","CONTEXT","Master Sheet.xlsx","Female 15-64 / Total Population","Census 2021","pop-weighted"),
 ("ctx_who_mrh_national","CONTEXT-INTRO-ONLY","maternal_and_reproductive_health_indicators_gha.csv","WHO GHO national series","WHO GHO","outputs/data/mrh_national_context.csv; NOT a region mediator"),
]
pv = pd.DataFrame(prov, columns=["column","role","source_file","indicator","survey","transform"])
pv.to_csv(PROC/"variable_provenance.csv", index=False)
print(f"[1] variable_provenance.csv  rows={len(pv)}")

# ---------- 2. BELT stratifier (standard Ghana 3-zone) ----------
BELT = {
 "Northern":["Northern","North East","Savannah","Upper East","Upper West"],
 "Middle":["Ashanti","Ahafo","Bono","Bono East","Eastern","Oti"],
 "Coastal/South":["Greater Accra","Central","Western","Western North","Volta"],
}
b2 = {r:b for b,rs in BELT.items() for r in rs}
reg["belt"] = reg["region"].map(b2)
assert reg["belt"].notna().all(), "unmapped region in belt"
assert len(reg)==16

# ---------- 3. analysis-ready clean dataset (+ z-scores; index deferred to Phase 4) ----------
analytic_cols = [c for c in reg.columns if c[:2] in ("x_","m_","y_") or c.startswith("ctx_") and c not in ("ctx_n_districts",)]
zcols = [c for c in reg.columns if c[:2] in ("x_","m_","y_") or c in
         ("ctx_illiteracy_rate","ctx_uninsured_rate","ctx_poverty_incidence","ctx_female_15_64_share")]
clean = reg.copy()
for c in zcols:
    clean[c+"_z"] = (clean[c]-clean[c].mean())/clean[c].std(ddof=0)
clean.to_csv(PROC/"analytic_region_16_clean.csv", index=False)
print(f"[3] analytic_region_16_clean.csv  rows={len(clean)}  cols={clean.shape[1]}  (z-scored {len(zcols)} vars)")

# ---------- 4. Table 1 descriptives ----------
desc_cols = [c for c in reg.columns if c[:2] in ("x_","m_","y_") or c.startswith("ctx_")]
w = reg["ctx_total_pop"]
rows=[]
for c in desc_cols:
    s = reg[c]
    natl = float(np.average(s, weights=w)) if c!="ctx_total_pop" else float(s.sum())
    rows.append({"variable":c,"n":int(s.notna().sum()),"mean":round(s.mean(),2),"sd":round(s.std(ddof=1),2),
                 "min":round(s.min(),2),"median":round(s.median(),2),"max":round(s.max(),2),
                 "national_popwt":round(natl,2)})
t1 = pd.DataFrame(rows)
t1.to_csv(OUTT/"table1_descriptives.csv", index=False)
print(f"[4] table1_descriptives.csv  rows={len(t1)}")

# by belt (means of key vars)
key = ["x_women_secondary_plus","x_women_literate","x_own_decision_all3","x_wifebeating_justified_women",
       "m_skilled_delivery","m_modern_cpr_married","m_fp_demand_satisfied_modern","m_ever_hiv_test",
       "y_u5mr","y_children_any_anemia","y_women_any_anemia","y_asfr_15_19",
       "ctx_illiteracy_rate","ctx_poverty_incidence"]
bt = reg.groupby("belt")[key].mean().round(1)
bt.to_csv(OUTT/"table1_by_belt.csv")
print(f"[4] table1_by_belt.csv\n{bt.to_string()}")
print("\nDONE.")
