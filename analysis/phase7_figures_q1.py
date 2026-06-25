"""
Q1 figure regeneration (uniform Arial; decluttered; correct panel structure).
  fig01_choropleths.png  — 2-panel: (A) poverty, (B) illiteracy (clean; caption in manuscript)
  fig02_lisa.png         — 2-panel: (A) illiteracy LISA, (B) poverty LISA
  fig03_shap.png         — descriptive RF SHAP (re-fit)
  fig04_parallel_coordinates.png — standalone, decluttered (was Fig 4A)
  fig05_dumbbell.png     — standalone north-south gap (was Fig 4B)
  fig06_mediation_forest.png — total vs indirect effects + 95% CI
"""
import json, re
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams.update({"font.family":"sans-serif","font.sans-serif":["Arial","Helvetica","DejaVu Sans"],
                            "axes.titlesize":11,"axes.labelsize":10,"font.size":10})
from matplotlib.patches import Polygon as MplPoly, Patch
from matplotlib.collections import PatchCollection
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from pandas.plotting import parallel_coordinates

ROOT=Path(__file__).resolve().parents[1]; PROC=ROOT/"data"/"processed"; OUTF=ROOT/"outputs"/"figures"; RAW=ROOT/"data"/"raw"
dm=pd.read_csv(PROC/"district_master_261.csv"); lisa=pd.read_csv(ROOT/"outputs"/"data"/"lisa_districts_261.csv")
gj=json.loads((RAW/"Ghana_New_260_District.geojson").read_text(encoding="utf-8"))
val={c:dict(zip(dm.loc[dm.geojson_district.notna(),"geojson_district"],dm.loc[dm.geojson_district.notna(),c])) for c in ["illiteracy_rate","poverty_incidence"]}
g2d=dict(zip(dm.loc[dm.geojson_district.notna(),"geojson_district"],dm.loc[dm.geojson_district.notna(),"district_261"]))
licl={c:dict(zip(lisa.district_261,lisa[f"{c}_cluster"])) for c in ["illiteracy_rate","poverty_incidence"]}
def rings(g): return [g["coordinates"][0]] if g["type"]=="Polygon" else [p[0] for p in g["coordinates"]]

def choro(ax,vmap,label):
    arr=np.array(list(vmap.values())); norm=Normalize(arr.min(),arr.max()); cmap=plt.get_cmap("viridis")
    pats=[];cols=[]
    for f in gj["features"]:
        nm=str(f["properties"]["DISTRICT"]).strip(); c=cmap(norm(vmap[nm])) if nm in vmap else "#d9d9d9"
        for r in rings(f["geometry"]): pats.append(MplPoly(np.array(r),closed=True)); cols.append(c)
    ax.add_collection(PatchCollection(pats,facecolor=cols,edgecolor="white",linewidths=0.12))
    ax.autoscale_view(); ax.set_aspect("equal"); ax.axis("off")
    cb=plt.colorbar(ScalarMappable(norm=norm,cmap=cmap),ax=ax,fraction=0.035,pad=0.02); cb.set_label(label,fontsize=9)
LCOL={"HH":"#b2182b","LL":"#2166ac","HL":"#ef8a62","LH":"#67a9cf","NS":"#f7f7f7"}
def lisamap(ax,clus):
    pats=[];cols=[]
    for f in gj["features"]:
        nm=str(f["properties"]["DISTRICT"]).strip(); c=LCOL.get(clus.get(g2d.get(nm,""),"NS"),"#d9d9d9")
        for r in rings(f["geometry"]): pats.append(MplPoly(np.array(r),closed=True)); cols.append(c)
    ax.add_collection(PatchCollection(pats,facecolor=cols,edgecolor="white",linewidths=0.12))
    ax.autoscale_view(); ax.set_aspect("equal"); ax.axis("off")
def panel(ax,letter): ax.text(0.0,1.0,letter,transform=ax.transAxes,fontsize=15,fontweight="bold",va="top",ha="left")

# fig01 — choropleths (A poverty, B illiteracy)
fig,ax=plt.subplots(1,2,figsize=(11,6))
choro(ax[0],val["poverty_incidence"],"Poverty incidence (%)"); panel(ax[0],"A")
choro(ax[1],val["illiteracy_rate"],"Illiteracy rate (%)"); panel(ax[1],"B")
fig.tight_layout(); fig.savefig(OUTF/"fig01_choropleths.png",dpi=220,bbox_inches="tight"); plt.close(fig)

# fig02 — LISA (A illiteracy, B poverty)
fig,ax=plt.subplots(1,2,figsize=(11,6))
lisamap(ax[0],licl["illiteracy_rate"]); panel(ax[0],"A")
lisamap(ax[1],licl["poverty_incidence"]); panel(ax[1],"B")
fig.legend(handles=[Patch(facecolor=LCOL[k],edgecolor="grey",label=k) for k in ["HH","LL","HL","LH","NS"]],
           loc="lower center",ncol=5,frameon=False,fontsize=9)
fig.tight_layout(rect=[0,0.05,1,1]); fig.savefig(OUTF/"fig02_lisa.png",dpi=220,bbox_inches="tight"); plt.close(fig)

# fig03 — SHAP (re-fit descriptive RF)
from sklearn.ensemble import RandomForestRegressor
import shap
feats=["illiteracy_rate","uninsured_rate","unemployment_rate","female_15_64_share","lat","lon"]
lab=["Illiteracy rate","Uninsured rate","Unemployment rate","Female 15-64 share","Latitude","Longitude"]
X=dm[feats].to_numpy(); y=dm["poverty_incidence"].to_numpy()
rf=RandomForestRegressor(n_estimators=600,min_samples_leaf=3,random_state=42,n_jobs=-1).fit(X,y)
sv=shap.TreeExplainer(rf).shap_values(X)
plt.figure(); shap.summary_plot(sv,pd.DataFrame(X,columns=lab),show=False,cmap=plt.get_cmap("viridis"))
plt.tight_layout(); plt.savefig(OUTF/"fig03_shap.png",dpi=220,bbox_inches="tight"); plt.close()

# fig04 — parallel coordinates (standalone, decluttered)
reg=pd.read_csv(PROC/"analytic_region_16_clean.csv")
BELT={"Northern":["Northern","North East","Savannah","Upper East","Upper West"],"Middle":["Ashanti","Ahafo","Bono","Bono East","Eastern","Oti"],"Coastal/South":["Greater Accra","Central","Western","Western North","Volta"]}
reg["belt"]=reg["region"].map({r:b for b,rs in BELT.items() for r in rs}); BC={"Northern":"#b2182b","Middle":"#bdbdbd","Coastal/South":"#2166ac"}
cols=[("x_women_secondary_plus","Sec.+"),("x_women_literate","Literate"),("x_own_decision_all3","Decision"),("m_skilled_delivery","Skilled del."),("y_children_any_anemia","Child anaemia"),("y_u5mr","U5MR")]
pc=reg[["belt"]+[c for c,_ in cols]].copy()
for c,_ in cols: pc[c]=(pc[c]-pc[c].min())/(pc[c].max()-pc[c].min())
pc.columns=["belt"]+[l for _,l in cols]
fig,ax=plt.subplots(figsize=(8.5,4.6))
parallel_coordinates(pc,"belt",ax=ax,color=[BC[b] for b in pc["belt"].unique()],linewidth=1.1,alpha=0.55)
ax.set_ylabel("Normalised (0–1)",fontsize=10); ax.tick_params(axis="x",labelsize=9,rotation=15); ax.legend(fontsize=8,frameon=False,loc="upper right")
ax.grid(axis="y",color="#eee"); fig.tight_layout(); fig.savefig(OUTF/"fig04_parallel_coordinates.png",dpi=220,bbox_inches="tight"); plt.close(fig)

# fig05 — dumbbell (standalone)
pct=[("x_women_secondary_plus","Women secondary+"),("x_women_literate","Women literate"),("x_own_decision_all3","Own decision (all 3)"),("m_skilled_delivery","Skilled delivery"),("m_modern_cpr_married","Modern CPR"),("y_children_any_anemia","Child anaemia"),("y_women_any_anemia","Women anaemia")]
rows=[(l,reg[reg.belt=="Coastal/South"][c].mean(),reg[reg.belt=="Northern"][c].mean()) for c,l in pct]
dd=pd.DataFrame(rows,columns=["ind","coastal","northern"]).assign(gap=lambda d:d.coastal-d.northern).sort_values("gap")
yv=np.arange(len(dd)); fig,ax=plt.subplots(figsize=(8.5,4.6))
ax.hlines(yv,dd.northern,dd.coastal,color="#cccccc",lw=2.5,zorder=1)
ax.scatter(dd.northern,yv,color="#b2182b",s=60,zorder=2,label="Northern belt"); ax.scatter(dd.coastal,yv,color="#2166ac",s=60,zorder=2,label="Coastal/South belt")
ax.set_yticks(yv); ax.set_yticklabels(dd.ind,fontsize=9); ax.set_xlim(0,100); ax.set_xlabel("Regional belt mean (%)",fontsize=10)
ax.legend(fontsize=8,frameon=False,loc="lower right"); ax.grid(axis="x",color="#eee"); fig.tight_layout(); fig.savefig(OUTF/"fig05_dumbbell.png",dpi=220,bbox_inches="tight"); plt.close(fig)

# fig06 — mediation forest
med=pd.read_csv(ROOT/"outputs"/"tables"/"mediation_results.csv")
xm={"x_women_secondary_plus":"Secondary+","gei":"Gender-equity"}; ym={"y_u5mr":"U5MR","y_children_any_anemia":"child anaemia","y_asfr_15_19":"ASFR 15-19"}
fig,ax=plt.subplots(figsize=(8.5,4.6)); ylab=[]
for i,(_,r) in enumerate(med.iterrows()):
    ylab.append(f"{xm.get(r['X'],r['X'])} → {ym.get(r['Y'],r['Y'])}")
    lo,hi=[float(v) for v in r["indirect_CI95"].strip("[]").split(",")]
    ax.plot(r["c(total)"],i,"s",color="#1a5276",ms=8); ax.errorbar(r["indirect(a*b)"],i-0.18,xerr=[[r["indirect(a*b)"]-lo],[hi-r["indirect(a*b)"]]],fmt="o",color="#c0392b",capsize=3)
ax.axvline(0,color="grey",lw=0.8,ls="--"); ax.set_yticks(range(len(ylab))); ax.set_yticklabels(ylab,fontsize=9); ax.invert_yaxis()
ax.set_xlabel("Standardized effect (SD)",fontsize=10)
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([0],[0],marker="s",color="w",markerfacecolor="#1a5276",label="Total effect",ms=9),Line2D([0],[0],marker="o",color="#c0392b",label="Indirect (95% CI)")],fontsize=8,frameon=False,loc="lower right")
fig.tight_layout(); fig.savefig(OUTF/"fig06_mediation_forest.png",dpi=220,bbox_inches="tight"); plt.close(fig)
print("[Q1 figs] fig01..fig06 regenerated (Arial; Fig1 2-panel; Fig4/5 split)")
