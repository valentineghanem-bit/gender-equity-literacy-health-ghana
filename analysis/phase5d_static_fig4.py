"""
Stage 10 fix — static (matplotlib) version of Figure 4 (multivariate gradient + disparity)
so it can be EMBEDDED in the manuscript .docx (the Plotly version is interactive-only).
Two panels: (a) parallel-coordinates of regions by belt; (b) Coastal-vs-Northern dumbbell.
Colourblind-safe; titles state the finding. Output: outputs/figures/fig04_multivariate_disparity.png
"""
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates

ROOT = Path(__file__).resolve().parents[1]
PROC, OUTF = ROOT/"data"/"processed", ROOT/"outputs"/"figures"
reg = pd.read_csv(PROC/"analytic_region_16_clean.csv")
BELT = {"Northern":["Northern","North East","Savannah","Upper East","Upper West"],
        "Middle":["Ashanti","Ahafo","Bono","Bono East","Eastern","Oti"],
        "Coastal/South":["Greater Accra","Central","Western","Western North","Volta"]}
b2={r:b for b,rs in BELT.items() for r in rs}; reg["belt"]=reg["region"].map(b2)
BCOL={"Northern":"#b2182b","Middle":"#999999","Coastal/South":"#2166ac"}

fig,ax=plt.subplots(1,2,figsize=(13,5.2))
# (a) parallel coordinates (min-max normalised for comparability)
cols=[("x_women_secondary_plus","Sec.+"),("x_women_literate","Literate"),
      ("x_own_decision_all3","Own-decision"),("m_skilled_delivery","Skilled del."),
      ("y_children_any_anemia","Child anaemia"),("y_u5mr","U5MR")]
pc=reg[["belt"]+[c for c,_ in cols]].copy()
for c,_ in cols: pc[c]=(pc[c]-pc[c].min())/(pc[c].max()-pc[c].min())
pc.columns=["belt"]+[l for _,l in cols]
parallel_coordinates(pc,"belt",ax=ax[0],color=[BCOL[b] for b in pc["belt"].unique()],alpha=0.6)
ax[0].set_title("(a) Regions track together across every axis\n(min–max normalised; northern regions low on equity, high on mortality)",fontsize=9,loc="left")
ax[0].tick_params(axis="x",labelsize=8,rotation=20); ax[0].legend(fontsize=7,loc="upper right")
ax[0].set_ylabel("normalised (0–1)",fontsize=8)

# (b) dumbbell Coastal vs Northern
pct=[("x_women_secondary_plus","Women secondary+"),("x_women_literate","Women literate"),
     ("x_own_decision_all3","Own decision (all 3)"),("m_skilled_delivery","Skilled delivery"),
     ("m_modern_cpr_married","Modern CPR"),("y_children_any_anemia","Child anaemia"),
     ("y_women_any_anemia","Women anaemia")]
rows=[]
for c,l in pct:
    co=reg[reg.belt=="Coastal/South"][c].mean(); no=reg[reg.belt=="Northern"][c].mean()
    rows.append((l,co,no,co-no))
dd=pd.DataFrame(rows,columns=["ind","coastal","northern","gap"]).sort_values("gap")
y=np.arange(len(dd))
ax[1].hlines(y,dd.northern,dd.coastal,color="#cccccc",lw=3,zorder=1)
ax[1].scatter(dd.northern,y,color="#b2182b",s=70,zorder=2,label="Northern belt")
ax[1].scatter(dd.coastal,y,color="#2166ac",s=70,zorder=2,label="Coastal/South belt")
for yi,r in zip(y,dd.itertuples()):
    ax[1].text(r.northern-1,yi,f"{r.northern:.0f}",ha="right",va="center",fontsize=8)
    ax[1].text(r.coastal+1,yi,f"{r.coastal:.0f}",ha="left",va="center",fontsize=8)
ax[1].set_yticks(y); ax[1].set_yticklabels(dd.ind,fontsize=9); ax[1].set_xlim(0,100)
ax[1].set_xlabel("Regional belt mean (%)",fontsize=9)
ax[1].set_title("(b) The north–south divide (Coastal/South − Northern)\nfemale secondary education gap 35.8 pp; literacy 27.8 pp",fontsize=9,loc="left")
ax[1].legend(fontsize=8,loc="lower right"); ax[1].grid(axis="x",color="#eee")
fig.tight_layout(); fig.savefig(OUTF/"fig04_multivariate_disparity.png",dpi=200,bbox_inches="tight"); plt.close(fig)
print("[fig4] outputs/figures/fig04_multivariate_disparity.png written")
