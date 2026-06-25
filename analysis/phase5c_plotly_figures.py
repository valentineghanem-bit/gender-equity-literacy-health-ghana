"""
Phase 5c — Plotly (plotly.py) integration. Council-selected, topic-mirroring chart types for
Project 16 that ECharts/matplotlib did NOT provide — proving the Plotly integration and adding
multivariate data-storytelling. Self-contained offline HTML (plotly.js embedded once).
Charts (per the Project-16 chart plan):
  1) Parallel-coordinates — 16 regions across gender-equity/literacy/service/outcome axes (the
     multivariate north–south story in one view).
  2) Dumbbell — Coastal/South vs Northern belt gap per %-indicator (the disparity story).
Anti-slop: colourblind-safe (Cividis), titles state findings, no pie/3D/chartjunk.
Output: outputs/figures/plotly_supplementary.html
"""
from pathlib import Path
import pandas as pd, numpy as np
import plotly.graph_objects as go
import plotly.io as pio

ROOT = Path(__file__).resolve().parents[1]
PROC, OUTF = ROOT/"data"/"processed", ROOT/"outputs"/"figures"
reg = pd.read_csv(PROC/"analytic_region_16_clean.csv")

# ---------- 1) parallel coordinates ----------
dims = [("x_women_secondary_plus","Sec.+ %"),("x_women_literate","Literate %"),
        ("x_own_decision_all3","Own-decision %"),("m_skilled_delivery","Skilled del. %"),
        ("y_children_any_anemia","Child anaemia %"),("y_u5mr","U5MR /1k")]
pc = go.Figure(data=go.Parcoords(
    line=dict(color=reg["y_u5mr"], colorscale="Cividis",
              colorbar=dict(title="U5MR /1k"), showscale=True),
    dimensions=[dict(label=lab, values=reg[col]) for col,lab in dims]))
pc.update_layout(title="Northern regions track low on education/equity and high on child mortality across every axis (16 regions)",
                 font=dict(size=12), margin=dict(l=80,r=40,t=70,b=30), height=460)

# ---------- 2) dumbbell: Coastal/South vs Northern belt gap ----------
BELT = {"Northern":["Northern","North East","Savannah","Upper East","Upper West"],
        "Coastal/South":["Greater Accra","Central","Western","Western North","Volta"]}
b2 = {r:b for b,rs in BELT.items() for r in rs}
reg2 = reg.assign(belt=reg["region"].map(b2)).dropna(subset=["belt"])
pct = [("x_women_secondary_plus","Women secondary+"),("x_women_literate","Women literate"),
       ("x_own_decision_all3","Own decision (all 3)"),("m_skilled_delivery","Skilled delivery"),
       ("m_modern_cpr_married","Modern CPR"),("y_children_any_anemia","Child anaemia"),
       ("y_women_any_anemia","Women anaemia")]
rows=[]
for col,lab in pct:
    c=reg2[reg2.belt=="Coastal/South"][col].mean(); n=reg2[reg2.belt=="Northern"][col].mean()
    rows.append((lab,round(c,1),round(n,1),round(c-n,1)))
dd=pd.DataFrame(rows,columns=["ind","coastal","northern","gap"]).sort_values("gap")
db=go.Figure()
for _,r in dd.iterrows():
    db.add_trace(go.Scatter(x=[r.northern,r.coastal],y=[r.ind,r.ind],mode="lines",
                 line=dict(color="#bbb",width=3),showlegend=False,hoverinfo="skip"))
db.add_trace(go.Scatter(x=dd.northern,y=dd.ind,mode="markers+text",name="Northern belt",
             marker=dict(color="#b2182b",size=13),text=dd.northern,textposition="middle left"))
db.add_trace(go.Scatter(x=dd.coastal,y=dd.ind,mode="markers+text",name="Coastal/South belt",
             marker=dict(color="#2166ac",size=13),text=dd.coastal,textposition="middle right"))
db.update_layout(title="The north–south divide: Coastal/South vs Northern belt on key indicators (%)",
                 xaxis_title="Regional belt mean (%)", font=dict(size=12), height=430,
                 margin=dict(l=160,r=40,t=70,b=40), legend=dict(orientation="h",y=-0.18),
                 plot_bgcolor="white", xaxis=dict(gridcolor="#eee",rangemode="tozero"))

# ---------- assemble one self-contained offline HTML ----------
CAVEAT=("Ecological, cross-sectional, associational (inference N=16 regions). Charts selected by the "
        "AIPOCH epid-council for this project's gender-equity/literacy theme. Colourblind-safe.")
CFG = {"displaylogo": False, "responsive": True}  # white-label (no vendor logo)
div1 = pio.to_html(pc, include_plotlyjs=True, full_html=False, config=CFG)
div2 = pio.to_html(db, include_plotlyjs=False, full_html=False, config=CFG)
html = (f"<!DOCTYPE html><html lang=en><head><meta charset=utf-8>"
        f"<title>Plotly supplementary — Project 16</title>"
        f"<style>body{{font-family:Segoe UI,Arial,sans-serif;margin:0;background:#f4f6f7;color:#1c2833}}"
        f"header{{background:#1a5276;color:#fff;padding:16px 24px}}header h1{{margin:0;font-size:18px}}"
        f".cav{{background:#fef9e7;border:1px solid #f1c40f;border-left:6px solid #f1c40f;padding:10px 14px;margin:14px 24px;border-radius:6px;font-size:13px}}"
        f".card{{background:#fff;border:1px solid #e5e8e8;border-radius:10px;margin:16px 24px;padding:8px}}</style></head><body>"
        f"<header><h1>Project 16 — Plotly supplementary figures (council-selected chart plan)</h1></header>"
        f"<div class=cav>{CAVEAT}</div><div class=card>{div1}</div><div class=card>{div2}</div></body></html>")
OUTF.mkdir(parents=True, exist_ok=True)
(OUTF/"plotly_supplementary.html").write_text(html, encoding="utf-8")
print(f"[5c] outputs/figures/plotly_supplementary.html  {round(len(html.encode())/1024)} KB (offline, plotly.js embedded)")
print("Dumbbell gaps (Coastal − Northern):\n"+dd.to_string(index=False))
