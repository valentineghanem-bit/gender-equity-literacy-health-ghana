"""
Build manuscript-ready Table 1 (descriptives by ecological belt) and Table 2 (mediation results)
as CSVs for embedding as real Word tables in the .docx.
National = population-weighted; belt columns = mean across the belt's regions (footnoted).
Outputs: outputs/tables/manuscript_table1.csv, manuscript_table2.csv
"""
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
PROC, OUTT = ROOT/"data"/"processed", ROOT/"outputs"/"tables"
reg = pd.read_csv(PROC/"analytic_region_16_clean.csv")
BELT = {"Northern":["Northern","North East","Savannah","Upper East","Upper West"],
        "Middle":["Ashanti","Ahafo","Bono","Bono East","Eastern","Oti"],
        "Coastal/South":["Greater Accra","Central","Western","Western North","Volta"]}
b2={r:b for b,rs in BELT.items() for r in rs}; reg["belt"]=reg["region"].map(b2)
w=reg["ctx_total_pop"]

rows=[("Women with secondary+ education, %","x_women_secondary_plus"),
      ("Women literate, %","x_women_literate"),
      ("Own decision-making (all three), %","x_own_decision_all3"),
      ("Wife-beating justified, %","x_wifebeating_justified_women"),
      ("Do not own land, %","x_no_land_women"),
      ("Intimate-partner violence, %","x_ipv_any"),
      ("Skilled birth attendance, %","m_skilled_delivery"),
      ("Modern contraceptive prevalence (married), %","m_modern_cpr_married"),
      ("FP demand satisfied, modern, %","m_fp_demand_satisfied_modern"),
      ("Ever HIV-tested (women), %","m_ever_hiv_test"),
      ("Under-five mortality, /1000","y_u5mr"),
      ("Neonatal mortality, /1000","y_nmr"),
      ("Infant mortality, /1000","y_imr"),
      ("Women with anaemia, %","y_women_any_anemia"),
      ("Children with anaemia, %","y_children_any_anemia"),
      ("Adolescent birth rate (15-19), /1000","y_asfr_15_19"),
      ("Female illiteracy rate, %","ctx_illiteracy_rate"),
      ("Poverty incidence, %","ctx_poverty_incidence"),
      ("Uninsured, %","ctx_uninsured_rate")]
def natl(c): return float(np.average(reg[c],weights=w))
T1=[]
for lab,c in rows:
    T1.append({"Characteristic":lab,
               "National":round(natl(c),1),
               "Coastal/South":round(reg[reg.belt=="Coastal/South"][c].mean(),1),
               "Middle":round(reg[reg.belt=="Middle"][c].mean(),1),
               "Northern":round(reg[reg.belt=="Northern"][c].mean(),1)})
# header counts row
T1.insert(0,{"Characteristic":"Regions (districts), n","National":"16 (261)",
             "Coastal/South":f"{(reg.belt=='Coastal/South').sum()}","Middle":f"{(reg.belt=='Middle').sum()}","Northern":f"{(reg.belt=='Northern').sum()}"})
pd.DataFrame(T1).to_csv(OUTT/"manuscript_table1.csv",index=False)
print("[T1] manuscript_table1.csv", len(T1),"rows")

# Table 2 — mediation
med=pd.read_csv(OUTT/"mediation_results.csv")
xmap={"x_women_secondary_plus":"Women secondary+ education","gei":"Gender-equity index"}
ymap={"y_u5mr":"Under-five mortality","y_children_any_anemia":"Child anaemia","y_asfr_15_19":"Adolescent birth rate"}
T2=[]
for _,r in med.iterrows():
    T2.append({"Exposure (X)":xmap.get(r["X"],r["X"]),
               "Mediator (M)":"RH-service index","Outcome (Y)":ymap.get(r["Y"],r["Y"]),
               "a (X→M)":r["a(X->M)"],"b (M→Y|X)":r["b(M->Y|X)"],
               "Direct c'":r["c'(direct)"],"Total c":r["c(total)"],
               "Indirect a·b":r["indirect(a*b)"],"95% CI":r["indirect_CI95"]})
pd.DataFrame(T2).to_csv(OUTT/"manuscript_table2.csv",index=False)
print("[T2] manuscript_table2.csv", len(T2),"rows")
