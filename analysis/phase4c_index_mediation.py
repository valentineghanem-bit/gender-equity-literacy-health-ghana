"""
Phase 4c — Gender-equity index construction + ecological mediation (16 regions).
Council R2: hypothesis-generating, precision-weighted (by population), bootstrap CIs, with explicit
small-N (N=16) and sequential-ignorability caveats. NOT causal.
  Index: transparent standardized-mean (N=16-appropriate; factor analysis unstable at N=16) + Cronbach alpha.
  Mediation: X -> M(RH-service index) -> Y, WLS weighted by population; indirect = a*b; bootstrap 95% CI.
Outputs:
  data/processed/analytic_region_16_modeling.csv
  outputs/tables/gei_construction.csv
  outputs/tables/mediation_results.csv
"""
from pathlib import Path
import numpy as np, pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
PROC, OUTT = ROOT/"data"/"processed", ROOT/"outputs"/"tables"
RNG = np.random.default_rng(7)
reg = pd.read_csv(PROC/"analytic_region_16_clean.csv")
z = lambda s: (s - s.mean())/s.std(ddof=0)

# ---------- Gender-equity index (higher = more equity) ----------
# orientation: +autonomy, -harmful-attitudes/violence/asset-deprivation
items = {"x_own_decision_all3":+1,"x_final_say_women":+1,
         "x_wifebeating_justified_women":-1,"x_no_land_women":-1,"x_ipv_any":-1}
oriented = pd.DataFrame({k: sign*z(reg[k]) for k,sign in items.items()})
reg["gei"] = oriented.mean(axis=1)
reg["gei_z"] = z(reg["gei"])
# Cronbach alpha on oriented standardized items
k = oriented.shape[1]
alpha = k/(k-1) * (1 - oriented.var(axis=0,ddof=1).sum()/oriented.sum(axis=1).var(ddof=1))
gc = pd.DataFrame([{"item":it,"orientation":("+" if s>0 else "-"),
                    "item_total_corr":round(np.corrcoef(oriented[it], reg["gei"])[0,1],3)}
                   for it,s in items.items()])
gc["cronbach_alpha"]=round(alpha,3); gc["n_items"]=k
gc.to_csv(OUTT/"gei_construction.csv", index=False)
print(f"[4c] gender-equity index built; Cronbach alpha = {alpha:.3f}")

# ---------- human-capital axis (primary) + RH service index ----------
reg["human_capital_z"] = z(reg["x_women_secondary_plus"])
svc = ["m_skilled_delivery","m_modern_cpr_married","m_fp_demand_satisfied_modern"]
reg["service_index"] = pd.DataFrame({c: z(reg[c]) for c in svc}).mean(axis=1)
reg["service_index_z"] = z(reg["service_index"])
reg.to_csv(PROC/"analytic_region_16_modeling.csv", index=False)

# ---------- precision-weighted mediation ----------
W = reg["ctx_total_pop"].to_numpy()
def wls(yv, Xcols, df):
    Xm = sm.add_constant(df[Xcols].to_numpy())
    return sm.WLS(df[yv].to_numpy(), Xm, weights=W).fit()

def mediate(df, x, m, y, B=2000):
    d = df.copy()
    for v in (x,m,y): d[v+"_s"] = z(d[v])
    xs,ms,ys = x+"_s", m+"_s", y+"_s"
    a  = wls(ms,[xs],d).params[1]
    fb = wls(ys,[xs,ms],d); cp, b = fb.params[1], fb.params[2]
    c  = wls(ys,[xs],d).params[1]
    ind = a*b
    # bootstrap (resample regions with replacement)
    bs=[]
    n=len(d)
    for _ in range(B):
        idx = RNG.integers(0,n,n)
        s = d.iloc[idx].reset_index(drop=True)
        global W
        Wsav=W; W=s["ctx_total_pop"].to_numpy()
        try:
            aa=wls(ms,[xs],s).params[1]; bb=wls(ys,[xs,ms],s).params[2]; bs.append(aa*bb)
        except Exception: pass
        W=Wsav
    bs=np.array(bs); lo,hi=np.percentile(bs,[2.5,97.5])
    return {"X":x,"M":m,"Y":y,"a(X->M)":round(a,3),"b(M->Y|X)":round(b,3),
            "c'(direct)":round(cp,3),"c(total)":round(c,3),"indirect(a*b)":round(ind,3),
            "indirect_CI95":f"[{lo:.3f}, {hi:.3f}]","prop_mediated":round(ind/c,3) if c!=0 else np.nan,
            "CI_excludes_0":not(lo<=0<=hi)}

models=[
 ("x_women_secondary_plus","service_index","y_u5mr"),       # primary (human-capital axis)
 ("gei","service_index","y_u5mr"),
 ("x_women_secondary_plus","service_index","y_children_any_anemia"),
 ("x_women_secondary_plus","service_index","y_asfr_15_19"),
 ("gei","service_index","y_asfr_15_19"),
]
res=[mediate(reg,x,m,y) for x,m,y in models]
out=pd.DataFrame(res)
out.to_csv(OUTT/"mediation_results.csv", index=False)
print("[4c] mediation (standardized, population-weighted, bootstrap 95% CI, N=16 — exploratory):")
print(out.to_string(index=False))
print("\nDONE.")
