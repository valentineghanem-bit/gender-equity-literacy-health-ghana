"""
Phase 4a — Spatial structure (the defensible high-resolution core) + MAUP sensitivity.
261-district Global Moran's I + Local Moran (LISA) for the determinant layer that genuinely
varies at district level: illiteracy (literacy proxy) and poverty. Centroid-KNN spatial weights
(k=6) from Master-Sheet lat/long — all 261 districts (incl. 3 structural gaps) are full nodes,
so the spatial frame is genuinely 261 units (hard rule). MAUP: repeat at 16 regions and compare.
Pure numpy/scipy/sklearn — no geopandas/GDAL.
Outputs:
  outputs/tables/spatial_global_moran_261.csv
  outputs/data/lisa_districts_261.csv
  outputs/tables/maup_sensitivity.csv
"""
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.neighbors import NearestNeighbors

ROOT = Path(__file__).resolve().parents[1]
PROC, OUTT, OUTD = ROOT/"data"/"processed", ROOT/"outputs"/"tables", ROOT/"outputs"/"data"
OUTT.mkdir(parents=True, exist_ok=True); OUTD.mkdir(parents=True, exist_ok=True)
RNG = np.random.default_rng(42)

def knn_W(coords, k):
    """Row-standardized KNN spatial weights (binary KNN, then row-standardize)."""
    n = len(coords)
    rad = np.radians(coords)
    nn = NearestNeighbors(n_neighbors=k+1, metric="haversine").fit(rad)
    _, idx = nn.kneighbors(rad)
    W = np.zeros((n, n))
    for i in range(n):
        nb = [j for j in idx[i] if j != i][:k]
        W[i, nb] = 1.0/len(nb)
    return W

def morans_I(x, W, perms=999):
    z = x - x.mean()
    lag = W @ z
    I = (z @ lag) / (z @ z)
    sims = np.empty(perms)
    for p in range(perms):
        zp = RNG.permutation(z)
        sims[p] = (zp @ (W @ zp)) / (zp @ zp)
    p_sim = (np.sum(sims >= I) + 1) / (perms + 1)        # one-sided (positive autocorr)
    return I, sims.mean(), p_sim

def local_moran(x, W, perms=999):
    z = x - x.mean()
    m2 = (z @ z) / len(z)
    lag = W @ z
    Ii = z * lag / m2
    n = len(z)
    p = np.empty(n)
    for i in range(n):
        nb = np.where(W[i] > 0)[0]
        k = len(nb)
        others = np.delete(z, i)
        sims = np.empty(perms)
        for t in range(perms):
            samp = RNG.choice(others, size=k, replace=False)
            sims[t] = z[i] * (W[i, nb] @ samp) / m2
        p[i] = (np.sum(np.abs(sims) >= abs(Ii[i])) + 1) / (perms + 1)
    # quadrant
    zl = lag
    quad = np.where((z > 0) & (zl > 0), "HH",
           np.where((z < 0) & (zl < 0), "LL",
           np.where((z > 0) & (zl < 0), "HL", "LH")))
    cluster = np.where(p < 0.05, quad, "NS")
    return Ii, zl, p, cluster

# ---------- load district frame ----------
dm = pd.read_csv(PROC/"district_master_261.csv")
assert len(dm) == 261
for c in ["lat","lon"]:
    assert dm[c].notna().all(), f"{c} has nulls — cannot build centroid weights"
assert dm["lat"].between(4,12).all() and dm["lon"].between(-4,2).all(), "centroids out of Ghana range"
coords = dm[["lat","lon"]].to_numpy()
W = knn_W(coords, k=6)
print(f"[4a] 261-district KNN(k=6) weights built; row-sums ok={np.allclose(W.sum(1),1)}")

# ---------- global Moran's I (261) ----------
rows = []
for col, label in [("illiteracy_rate","Illiteracy (literacy proxy)"), ("poverty_incidence","Poverty incidence")]:
    I, eI, p = morans_I(dm[col].to_numpy(), W)
    rows.append({"scale":"261-district","variable":col,"label":label,"morans_I":round(I,4),
                 "expected_I":round(-1/(len(dm)-1),4),"perm_mean":round(eI,4),"p_perm":round(p,4),"n":len(dm)})
    print(f"[4a] 261 Moran I  {col:18s} I={I:.3f}  p={p:.3f}")

# ---------- LISA (261) ----------
lisa = dm[["region","district_261","lat","lon","illiteracy_rate","poverty_incidence"]].copy()
for col in ["illiteracy_rate","poverty_incidence"]:
    Ii, lag, p, cl = local_moran(dm[col].to_numpy(), W)
    lisa[f"{col}_lisaI"] = np.round(Ii,4)
    lisa[f"{col}_lag"] = np.round(lag,4)
    lisa[f"{col}_p"] = np.round(p,4)
    lisa[f"{col}_cluster"] = cl
lisa.to_csv(OUTD/"lisa_districts_261.csv", index=False)
for col in ["illiteracy_rate","poverty_incidence"]:
    vc = lisa[f"{col}_cluster"].value_counts().to_dict()
    print(f"[4a] LISA {col}: {vc}")

# ---------- MAUP: 16-region Moran ----------
reg = pd.read_csv(PROC/"region_master_16_analytic.csv")
# region centroids = pop-weighted mean of district centroids
cent = dm.assign(w=dm["total_pop"]).groupby("region").apply(
    lambda g: pd.Series({"lat":np.average(g["lat"],weights=g["total_pop"]),
                         "lon":np.average(g["lon"],weights=g["total_pop"])}), include_groups=False).reset_index()
reg = reg.merge(cent, on="region")
Wr = knn_W(reg[["lat","lon"]].to_numpy(), k=3)
maup = []
for col in ["ctx_illiteracy_rate","ctx_poverty_incidence"]:
    I, eI, p = morans_I(reg[col].to_numpy(), Wr)
    maup.append({"scale":"16-region","variable":col,"morans_I":round(I,4),"p_perm":round(p,4),"n":16})
    print(f"[4a] 16-region Moran {col:22s} I={I:.3f} p={p:.3f}")
pd.DataFrame(rows).to_csv(OUTT/"spatial_global_moran_261.csv", index=False)
pd.concat([pd.DataFrame(rows)[["scale","variable","morans_I","p_perm","n"]], pd.DataFrame(maup)], ignore_index=True)\
  .to_csv(OUTT/"maup_sensitivity.csv", index=False)
print("[4a] MAUP sensitivity written. DONE.")
