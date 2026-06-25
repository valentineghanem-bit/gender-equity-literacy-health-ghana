"""
Phase 5 (cont.) — HI-EI dashboard + A0 poster, self-contained (vanilla JS + inline SVG +
base64-embedded verified figures). KPIs computed from verified CSVs (no hardcoding).
Council-mandated: associational headline; prominent caveat box; 261-district spatial result as
the quantitative anchor; null service-mediation shown honestly. Anti-slop, colourblind-safe.
Outputs: dashboard/HI-EI_Dashboard.html , poster/A0_Poster.html
"""
from pathlib import Path
import base64, pandas as pd, numpy as np

ROOT = Path(__file__).resolve().parents[1]
PROC, OUTT, OUTF = ROOT/"data"/"processed", ROOT/"outputs"/"tables", ROOT/"outputs"/"figures"
(ROOT/"dashboard").mkdir(exist_ok=True); (ROOT/"poster").mkdir(exist_ok=True)
PRIMARY = "#1a5276"  # spatial domain colour (CLAUDE §15)

reg  = pd.read_csv(PROC/"region_master_16_analytic.csv")
bt   = pd.read_csv(OUTT/"table1_by_belt.csv").set_index("belt")
mor  = pd.read_csv(OUTT/"spatial_global_moran_261.csv").set_index("variable")
med  = pd.read_csv(OUTT/"mediation_results.csv")
rfp  = pd.read_csv(OUTT/"rf_district_performance.csv").iloc[0]

def b64(p):
    return "data:image/png;base64,"+base64.b64encode((OUTF/p).read_bytes()).decode() if (OUTF/p).exists() else ""
IMG = {k:b64(v) for k,v in {
    "chor_il":"fig_choropleth_illiteracy_261.png","chor_pov":"fig_choropleth_poverty_261.png",
    "lisa_il":"fig_lisa_illiteracy_261.png","lisa_pov":"fig_lisa_poverty_261.png",
    "forest":"fig_mediation_forest.png","shap":"shap_summary_district.png"}.items()}

# KPIs
mi_il = mor.loc["illiteracy_rate","morans_I"]; mi_pov = mor.loc["poverty_incidence","morans_I"]
edu_u5 = med[(med.X=="x_women_secondary_plus")&(med.Y=="y_u5mr")].iloc[0]
u5_n, u5_s = bt.loc["Northern","y_u5mr"], bt.loc["Coastal/South","y_u5mr"]
an_n, an_s = bt.loc["Northern","y_children_any_anemia"], bt.loc["Coastal/South","y_children_any_anemia"]
KPIS = [
 ("North–South U5MR gap", f"{u5_n:.0f} vs {u5_s:.0f}", "per 1,000 — Northern belt vs Coastal/South"),
 ("Spatial clustering, illiteracy", f"Moran's I = {mi_il:.2f}", "261 districts, p&lt;0.001"),
 ("Spatial clustering, poverty", f"Moran's I = {mi_pov:.2f}", "261 districts, p&lt;0.001"),
 ("Education–U5MR association", f"{edu_u5['c(total)']:+.2f} SD", "total ecological effect (associational)"),
 ("Determinant model (descriptive)", f"R² = {rfp['cv_r2_mean']:.2f}", "illiteracy = top driver of poverty"),
]

# belt inline-SVG grouped bar (U5MR + child anaemia, bars from 0)
belts=["Coastal/South","Middle","Northern"]; metrics=[("y_u5mr","U5MR (/1000)","#1a5276"),("y_children_any_anemia","Child anaemia (%)","#117a65")]
def belt_svg():
    W,H,pad=520,260,46; gw=(W-2*pad)/len(belts); mx=max(bt[m[0]].max() for m in metrics)*1.15
    s=[f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Outcomes by belt">']
    s.append(f'<line x1="{pad}" y1="{H-pad}" x2="{W-pad}" y2="{H-pad}" stroke="#888"/>')
    for i,bn in enumerate(belts):
        x0=pad+i*gw; bw=gw/ (len(metrics)+1)
        for j,(col,lab,c) in enumerate(metrics):
            v=bt.loc[bn,col]; h=(v/mx)*(H-2*pad); x=x0+ (j+0.5)*bw
            s.append(f'<rect x="{x:.1f}" y="{H-pad-h:.1f}" width="{bw*0.8:.1f}" height="{h:.1f}" fill="{c}"><title>{bn} {lab}: {v:.1f}</title></rect>')
            s.append(f'<text x="{x+bw*0.4:.1f}" y="{H-pad-h-4:.1f}" font-size="10" text-anchor="middle" fill="#333">{v:.0f}</text>')
        s.append(f'<text x="{x0+gw/2:.1f}" y="{H-pad+16:.1f}" font-size="11" text-anchor="middle" fill="#333">{bn}</text>')
    leg=" ".join(f'<tspan fill="{c}">■</tspan> {lab}' for _,lab,c in metrics)
    s.append(f'<text x="{pad}" y="20" font-size="11">{leg}</text>')
    s.append('</svg>'); return "".join(s)

# region table rows
reg_sorted=reg.sort_values("y_u5mr",ascending=False)
rows="".join(f"<tr><td>{r.region}</td><td>{r.x_women_secondary_plus:.0f}</td><td>{r.x_women_literate:.0f}</td>"
             f"<td>{r.m_skilled_delivery:.0f}</td><td>{r.y_u5mr:.0f}</td><td>{r.y_children_any_anemia:.0f}</td>"
             f"<td>{r.y_asfr_15_19:.0f}</td><td>{r.ctx_poverty_incidence:.0f}</td></tr>" for r in reg_sorted.itertuples())

CAVEAT=("<b>Read as associations, not causes.</b> Ecological cross-sectional design; "
 "regional inference N=16 (exploratory); 261-district layer used for spatial structure &amp; mapping. "
 "Service-mediation was <b>not</b> supported (indirect-effect CIs span 0) — reproductive-health "
 "coverage is already ~89%, so it is not the missing link. Subject to ecological-fallacy &amp; MAUP limits "
 "(conclusions were scale-robust, 16-region vs 261-district).")

CSS="""
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#1c2833;background:#f4f6f7}
header{background:%P%;color:#fff;padding:20px 28px}header h1{margin:0;font-size:21px}header p{margin:6px 0 0;font-size:13px;opacity:.92;max-width:1100px}
.wrap{max-width:1180px;margin:0 auto;padding:18px}
.caveat{background:#fef9e7;border:1px solid #f1c40f;border-left:6px solid #f1c40f;padding:12px 16px;border-radius:6px;font-size:13px;margin:16px 0}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin:16px 0}
.kpi{background:#fff;border:1px solid #e5e8e8;border-radius:10px;padding:16px}
.kpi .v{font-size:26px;font-weight:700;color:%P%}.kpi .t{font-size:12px;color:#566573;margin-top:2px}.kpi .s{font-size:11px;color:#85929e;margin-top:6px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}@media(max-width:820px){.grid{grid-template-columns:1fr}}
.card{background:#fff;border:1px solid #e5e8e8;border-radius:10px;padding:16px;margin-bottom:18px}
.card h3{margin:0 0 8px;font-size:15px}.card .cap{font-size:12px;color:#566573;margin-top:6px}
img.fig{width:100%;height:auto;border-radius:6px}
table{width:100%;border-collapse:collapse;font-size:12.5px}th,td{padding:7px 9px;text-align:right;border-bottom:1px solid #eee}
th:first-child,td:first-child{text-align:left}th{cursor:pointer;background:#eaf2f8;position:sticky;top:0}tr:hover{background:#f8f9f9}
footer{font-size:12px;color:#566573;padding:18px 28px;border-top:1px solid #e5e8e8;margin-top:10px}
""".replace("%P%",PRIMARY)

def card(title, body, cap=""):
    return f'<div class="card"><h3>{title}</h3>{body}{f"<div class=cap>{cap}</div>" if cap else ""}</div>'

kpis_html="".join(f'<div class="kpi"><div class="v">{v}</div><div class="t">{t}</div><div class="s">{s}</div></div>' for t,v,s in KPIS)

dash=f"""<!DOCTYPE html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>HI-EI Dashboard — Gender Equity, Literacy &amp; Multi-Domain Health, Ghana</title><style>{CSS}</style></head><body>
<header><h1>Gender Equity, Literacy &amp; Multi-Domain Health — Ghana (HI-EI Dashboard)</h1>
<p>Where girls are less educated and women less empowered, children die younger and anaemia is higher — and these disadvantages cluster in northern Ghana. GH2022 DHS (16 regions) + Census-2021 (261 districts).</p></header>
<div class="wrap">
<div class="caveat">{CAVEAT}</div>
<div class="kpis">{kpis_html}</div>
{card("Outcomes by ecological belt","<div style='max-width:560px'>"+belt_svg()+"</div>","Bars from 0. Northern belt carries the highest under-five mortality and child anaemia.")}
<div class="grid">
{card("Illiteracy clusters in the north (261 districts)",f'<img class=fig src="{IMG["chor_il"]}">')}
{card("Poverty incidence (261 districts)",f'<img class=fig src="{IMG["chor_pov"]}">')}
{card("LISA hotspots — illiteracy",f'<img class=fig src="{IMG["lisa_il"]}">',"HH = high-illiteracy hotspots (north); LL = coldspots (south).")}
{card("LISA hotspots — poverty",f'<img class=fig src="{IMG["lisa_pov"]}">')}
{card("Strong total association, no supported service-mediation",f'<img class=fig src="{IMG["forest"]}">',"Total effects (squares) strongly negative; indirect effects (CIs) span 0.")}
{card("Determinant structure (descriptive ML)",f'<img class=fig src="{IMG["shap"]}">',"Descriptive only — no inference. Illiteracy dominates district poverty structure.")}
</div>
{card("Regional profile (sortable; ranked by U5MR)",'<div style="max-height:420px;overflow:auto"><table id=rt><thead><tr>'
 '<th onclick="sortT(0)">Region</th><th onclick="sortT(1)">Sec+ %</th><th onclick="sortT(2)">Literate %</th>'
 '<th onclick="sortT(3)">Skilled del. %</th><th onclick="sortT(4)">U5MR</th><th onclick="sortT(5)">Child anaemia %</th>'
 '<th onclick="sortT(6)">ASFR 15-19</th><th onclick="sortT(7)">Poverty %</th></tr></thead><tbody>'+rows+'</tbody></table></div>',
 "Click any column header to sort.")}
</div>
<footer>Design: Refined Option C (Hybrid). Data: 12 GH2022 DHS / Census-2021 datasets. Spatial: centroid-KNN Moran's I + LISA (261 districts). ML: Random Forest + SHAP (descriptive). Mediation: population-weighted, bootstrap 95% CI (N=16, exploratory). All figures reproducible from analysis/.</footer>
<script>
function sortT(c){{var t=document.getElementById('rt'),b=t.tBodies[0],r=[].slice.call(b.rows);
var asc=b.getAttribute('data-c')==c&&b.getAttribute('data-a')!='1';
r.sort(function(x,y){{var a=x.cells[c].innerText,z=y.cells[c].innerText;var na=parseFloat(a),nz=parseFloat(z);
if(!isNaN(na)&&!isNaN(nz)){{a=na;z=nz}};return (a>z?1:a<z?-1:0)*(asc?1:-1)}});
r.forEach(function(x){{b.appendChild(x)}});b.setAttribute('data-c',c);b.setAttribute('data-a',asc?'1':'0')}}
</script></body></html>"""
(ROOT/"dashboard"/"HI-EI_Dashboard.html").write_text(dash, encoding="utf-8")
kb=round(len(dash.encode())/1024); print(f"[dash] HI-EI_Dashboard.html  {kb} KB")

# ---------------- A0 poster ----------------
impl=("Target the northern HH clusters (high illiteracy + poverty + child anaemia) with girls' education and "
 "gender-equity programmes. Because reproductive-health service coverage is already near-universal (~89%), "
 "expanding services is unlikely to close the gap — the upstream levers are education and empowerment. "
 "Maps enable district-level GHS/MoE targeting (SDG 3.1/3.2/3.7, 4, 5).")
POSTER_CSS="""
@page{size:841mm 1189mm;margin:0}*{box-sizing:border-box}
body{margin:0;font-family:Segoe UI,Helvetica,Arial,sans-serif;color:#1c2833;width:841mm;height:1189mm;background:#fff}
.head{background:%P%;color:#fff;padding:26mm 28mm 18mm}.head h1{font-size:40pt;margin:0;line-height:1.1}
.head .auth{font-size:16pt;margin-top:8mm;opacity:.92}
.finding{background:#eaf2f8;border-left:10mm solid %P%;margin:10mm 28mm;padding:10mm 12mm;font-size:22pt;font-weight:600}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:12mm;padding:0 28mm}
.box{background:#fff;border:0.5mm solid #d5dbdb;border-radius:4mm;padding:8mm;margin-bottom:10mm}
.box h2{color:%P%;font-size:18pt;margin:0 0 5mm}.box p,.box li{font-size:13.5pt;line-height:1.4}
.kgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:8mm;padding:0 28mm;margin-bottom:8mm}
.k{background:#f4f6f7;border-radius:4mm;padding:7mm;text-align:center}.k .v{font-size:30pt;font-weight:700;color:%P%}.k .t{font-size:12pt;color:#566573}
img{width:100%;border-radius:3mm}.cap{font-size:11pt;color:#566573}
.lim{background:#fef9e7;border:0.5mm solid #f1c40f;border-radius:4mm;padding:8mm;font-size:13pt}
.foot{padding:8mm 28mm;font-size:11pt;color:#566573}
""".replace("%P%",PRIMARY)
kpis_p="".join(f'<div class="k"><div class="v">{v}</div><div class="t">{t}</div></div>' for t,v,s in KPIS[:3])
poster=f"""<!DOCTYPE html><html lang=en><head><meta charset=utf-8>
<title>Poster — Gender Equity, Literacy &amp; Multi-Domain Health, Ghana</title><style>{POSTER_CSS}</style></head><body>
<div class="head"><h1>Gender Equity, Literacy &amp; Multi-Domain Health Outcomes:<br>Spatial Machine-Learning Mediation Analysis in Ghana</h1>
<div class="auth">Valentine Golden Ghanem · GH2022 DHS (16 regions) + Census-2021 (261 districts)</div></div>
<div class="finding">Where girls are less educated and women less empowered, children die younger and anaemia is higher — and these disadvantages cluster spatially in northern Ghana.</div>
<div class="kgrid">{kpis_p}</div>
<div class="cols">
<div>
{f'<div class=box><h2>Background &amp; aim</h2><p>Gender inequality and low female literacy are linked to poorer maternal-child health across sub-Saharan Africa, but rarely mapped as a spatial, multi-domain pathway for Ghana. We test whether gender equity &amp; literacy track with child survival, anaemia and adolescent fertility — and whether reproductive-health service use mediates the link.</p></div>'}
{f'<div class=box><h2>Methods</h2><p>Ecological design (Refined Option C). 16-region DHS inference; 261-district Census layer for spatial structure &amp; mapping (3 structural-gap districts merged to parent polygons for rendering). Centroid-KNN Global/Local Moran’s I; descriptive Random Forest + SHAP; population-weighted bootstrap mediation. 12 datasets; full provenance audited.</p></div>'}
{f'<div class=box><h2>Spatial clustering (261 districts)</h2><img src="{IMG["chor_il"]}"><div class=cap>Illiteracy — strong north–south gradient.</div><img src="{IMG["lisa_il"]}" style="margin-top:6mm"><div class=cap>LISA: high-illiteracy hotspots (north).</div></div>'}
</div>
<div>
{f'<div class=box><h2>Outcomes by belt</h2><div>{belt_svg()}</div><div class=cap>Northern belt: highest U5MR &amp; child anaemia (bars from 0).</div></div>'}
{f'<div class=box><h2>Association, not mediation</h2><img src="{IMG["forest"]}"><div class=cap>Strong negative total effects; indirect (service-mediated) CIs span 0.</div></div>'}
{f'<div class=box><h2>Implications</h2><p>{impl}</p></div>'}
<div class="lim"><b>Limitations.</b> {CAVEAT}</div>
</div>
</div>
<div class="foot">Reproducible pipeline: analysis/phase2–5_*.py · every phase independently verified (exit 0) · manuscript kept local (not committed).</div>
</body></html>"""
(ROOT/"poster"/"A0_Poster.html").write_text(poster, encoding="utf-8")
print(f"[poster] A0_Poster.html  {round(len(poster.encode())/1024)} KB\nDONE.")
