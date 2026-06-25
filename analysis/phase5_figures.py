"""
Phase 5 — publication figures (matplotlib only; no geopandas). 261-district frame.
  fig_choropleth_illiteracy_261.png, fig_choropleth_poverty_261.png  (sequential viridis)
  fig_lisa_illiteracy_261.png,       fig_lisa_poverty_261.png         (ColorBrewer RdBu CB-safe)
  fig_mediation_forest.png  (total/direct/indirect effects + 95% CI across models)
Anti-slop: sequential CB-safe ramp, titles state the finding, legends labelled, no chartjunk.
"""
from pathlib import Path
import json, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPoly
from matplotlib.collections import PatchCollection
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

ROOT = Path(__file__).resolve().parents[1]
PROC, OUTD, OUTF = ROOT/"data"/"processed", ROOT/"outputs"/"data", ROOT/"outputs"/"figures"
OUTF.mkdir(parents=True, exist_ok=True)
RAW = ROOT/"data"/"raw"

dm   = pd.read_csv(PROC/"district_master_261.csv")
lisa = pd.read_csv(OUTD/"lisa_districts_261.csv")
gj   = json.loads((RAW/"Ghana_New_260_District.geojson").read_text(encoding="utf-8"))

# value lookups keyed by GeoJSON district name (direct-matched rows only; gaps share parent polygon)
val_illit = dict(zip(dm.loc[dm["geojson_district"].notna(),"geojson_district"], dm.loc[dm["geojson_district"].notna(),"illiteracy_rate"]))
val_pov   = dict(zip(dm.loc[dm["geojson_district"].notna(),"geojson_district"], dm.loc[dm["geojson_district"].notna(),"poverty_incidence"]))
gj2d      = dict(zip(dm.loc[dm["geojson_district"].notna(),"geojson_district"], dm.loc[dm["geojson_district"].notna(),"district_261"]))
lisa_illit = dict(zip(lisa["district_261"], lisa["illiteracy_rate_cluster"]))
lisa_pov   = dict(zip(lisa["district_261"], lisa["poverty_incidence_cluster"]))

def rings(geom):
    if geom["type"]=="Polygon": return [geom["coordinates"][0]]
    if geom["type"]=="MultiPolygon": return [p[0] for p in geom["coordinates"]]
    return []

def draw(ax, color_fn, title):
    patches, colors = [], []
    for f in gj["features"]:
        name = str(f["properties"].get("DISTRICT")).strip()
        c = color_fn(name)
        for ring in rings(f["geometry"]):
            patches.append(MplPoly(np.array(ring), closed=True)); colors.append(c)
    pc = PatchCollection(patches, facecolor=colors, edgecolor="white", linewidths=0.15)
    ax.add_collection(pc)
    ax.autoscale_view(); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, fontsize=11, loc="left")
    return ax

# ---- choropleths (sequential viridis) ----
for vals, label, fname, finding in [
    (val_illit,"Illiteracy rate (%)","fig_choropleth_illiteracy_261","Illiteracy concentrates in Ghana's northern districts"),
    (val_pov,"Poverty incidence (%)","fig_choropleth_poverty_261","Poverty incidence is highest across the northern belt")]:
    arr = np.array(list(vals.values())); norm = Normalize(arr.min(), arr.max()); cmap = plt.get_cmap("viridis")
    fig, ax = plt.subplots(figsize=(7,7.6))
    draw(ax, lambda n: cmap(norm(vals[n])) if n in vals else "#d9d9d9", f"{finding}\n261 districts (Guan/Sagnarigu/Awutu Senya West shown via parent polygon)")
    sm = ScalarMappable(norm=norm, cmap=cmap); sm.set_array([])
    cb = fig.colorbar(sm, ax=ax, fraction=0.035, pad=0.02); cb.set_label(label, fontsize=9)
    fig.tight_layout(); fig.savefig(OUTF/f"{fname}.png", dpi=200, bbox_inches="tight"); plt.close(fig)
    print(f"[5] {fname}.png")

# ---- LISA cluster maps (CB-safe RdBu categorical) ----
LCOL = {"HH":"#b2182b","LL":"#2166ac","HL":"#ef8a62","LH":"#67a9cf","NS":"#f7f7f7"}
for clus, fname, var in [(lisa_illit,"fig_lisa_illiteracy_261","illiteracy"),(lisa_pov,"fig_lisa_poverty_261","poverty")]:
    fig, ax = plt.subplots(figsize=(7,7.6))
    draw(ax, lambda n: LCOL.get(clus.get(gj2d.get(n,""),"NS"),"#d9d9d9"),
         f"LISA clusters of {var} (261 districts, p<0.05)\nHH = high-{var} hotspots; LL = low-{var} coldspots")
    from matplotlib.patches import Patch
    leg=[Patch(facecolor=LCOL[k],edgecolor="grey",label=k) for k in ["HH","LL","HL","LH","NS"]]
    ax.legend(handles=leg, loc="lower left", fontsize=8, frameon=False, title="Cluster")
    fig.tight_layout(); fig.savefig(OUTF/f"{fname}.png", dpi=200, bbox_inches="tight"); plt.close(fig)
    print(f"[5] {fname}.png")

# ---- mediation forest plot ----
med = pd.read_csv(ROOT/"outputs"/"tables"/"mediation_results.csv")
fig, ax = plt.subplots(figsize=(8.5,5))
xmap={"x_women_secondary_plus":"Secondary+","gei":"Gender-equity"}
ymap={"y_u5mr":"U5MR","y_children_any_anemia":"child anaemia","y_asfr_15_19":"ASFR 15-19"}
ylabs=[]; y=0
for _,r in med.iterrows():
    lab=f"{xmap.get(r['X'],r['X'])} → {ymap.get(r['Y'],r['Y'])}"
    ylabs.append(lab)
    lo,hi=[float(v) for v in r["indirect_CI95"].strip("[]").split(",")]
    ax.plot([r["c(total)"]],[y],"s",color="#1a5276",ms=8)          # total (direct ecological assoc)
    ax.errorbar(r["indirect(a*b)"],y-0.18,xerr=[[r["indirect(a*b)"]-lo],[hi-r["indirect(a*b)"]]],fmt="o",color="#c0392b",capsize=3)  # indirect+CI
    y+=1
ax.axvline(0,color="grey",lw=0.8,ls="--")
ax.set_yticks(range(len(ylabs))); ax.set_yticklabels(ylabs, fontsize=9); ax.invert_yaxis()
ax.set_xlabel("Standardized effect (SD)", fontsize=10)
ax.set_title("Strong total ecological associations; no supported service-mediation (indirect CIs span 0, N=16)", fontsize=10, loc="left")
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([0],[0],marker="s",color="w",markerfacecolor="#1a5276",label="Total effect (c)",ms=9),
                   Line2D([0],[0],marker="o",color="#c0392b",label="Indirect a·b (95% CI)")],
          loc="lower right", fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig(OUTF/"fig_mediation_forest.png", dpi=200, bbox_inches="tight"); plt.close(fig)
print("[5] fig_mediation_forest.png\nDONE.")
