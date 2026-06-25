"""
Build the bespoke_gen.js region-data input for Project 16:
  [{name(UPPERCASE geojson), short, v(U5MR), lisa, x(women secondary+)}, ...]  (16 regions)
v = U5MR (primary outcome, high-bad); x = women secondary+ (gender/education driver);
lisa = 16-region Local Moran cluster on U5MR (centroid-KNN k=3, 999 perms, p<0.10 given N=16).
Writes to BOTH Temp (working) and _system/bespoke (durable).
"""
from pathlib import Path
import json, numpy as np, pandas as pd
from sklearn.neighbors import NearestNeighbors

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT/"data"/"processed"
TMP = Path("C:/Users/VGhanem/AppData/Local/Temp")
SYS = ROOT.parent/"_system"/"bespoke"
RNG = np.random.default_rng(11)

reg = pd.read_csv(PROC/"region_master_16_analytic.csv")
dm  = pd.read_csv(PROC/"district_master_261.csv")
cent = dm.groupby("region").apply(lambda g: pd.Series({
    "lat":np.average(g["lat"],weights=g["total_pop"]),"lon":np.average(g["lon"],weights=g["total_pop"])}),
    include_groups=False).reset_index()
reg = reg.merge(cent,on="region")

# 16-region KNN(k=3) row-standardized weights
rad=np.radians(reg[["lat","lon"]].to_numpy())
nn=NearestNeighbors(n_neighbors=4,metric="haversine").fit(rad); _,idx=nn.kneighbors(rad)
n=len(reg); W=np.zeros((n,n))
for i in range(n):
    nb=[j for j in idx[i] if j!=i][:3]; W[i,nb]=1/len(nb)

VVAR="x_women_cannot_read"  # choropleth/LISA variable: female illiteracy (on-theme, strong regional clustering)
x=reg[VVAR].to_numpy(); z=x-x.mean(); m2=(z@z)/n; lag=W@z; Ii=z*lag/m2
p=np.empty(n)
for i in range(n):
    nb=np.where(W[i]>0)[0]; k=len(nb); others=np.delete(z,i); sims=np.empty(999)
    for t in range(999):
        s=RNG.choice(others,k,replace=False); sims[t]=z[i]*(W[i,nb]@s)/m2
    p[i]=(np.sum(np.abs(sims)>=abs(Ii[i]))+1)/1000
quad=np.where((z>0)&(lag>0),"HH",np.where((z<0)&(lag<0),"LL",np.where((z>0)&(lag<0),"HL","LH")))
clust=np.where(p<0.10,quad,"NS")

SHORT={'GREATER ACCRA':'Gr.Accra','ASHANTI':'Ashanti','CENTRAL':'Central','EASTERN':'Eastern','WESTERN':'Western',
 'VOLTA':'Volta','BONO':'Bono','AHAFO':'Ahafo','BONO EAST':'Bono E','OTI':'Oti','WESTERN NORTH':'W.North',
 'UPPER EAST':'Upper East','UPPER WEST':'Upper West','NORTHERN':'Northern','SAVANNAH':'Savannah','NORTHERN EAST':'N.East'}
def up(r): return "NORTHERN EAST" if r=="North East" else r.upper()

out=[]
for i,r in reg.iterrows():
    nm=up(r["region"])
    out.append({"name":nm,"short":SHORT.get(nm,r["region"]),"v":round(float(r[VVAR]),1),
                "lisa":str(clust[i]),"x":round(float(r["y_u5mr"]),1)})
for d in (TMP,SYS):
    (d/"gender-equity-literacy_regions.json").write_text(json.dumps(out,indent=0), encoding="utf-8")
print("wrote gender-equity-literacy_regions.json (16 regions) to Temp + _system/bespoke")
print("LISA:", pd.Series(clust).value_counts().to_dict())
print(pd.DataFrame(out).to_string(index=False))
