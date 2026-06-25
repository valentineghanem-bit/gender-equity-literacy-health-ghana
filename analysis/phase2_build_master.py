"""
Phase 2 — Master dataset build for Project 16
Gender Equity, Literacy & Multi-Domain Health: Spatial ML Mediation, Ghana.

Design: Refined Option C (Hybrid) — 16-region DHS inference + 261-district Master-Sheet
spatial/mapping layer. 261-district frame ALWAYS (Guan->Oti merge for rendering only).

Inputs (data/raw/, canonical GH2022DHS STATcompiler exports + Census-2021 Master Sheet):
  Master Sheet.xlsx                              (261 districts, socioeconomic)
  Ghana_New_260_District.geojson                 (260 polygons / 16 regions)
  select-gender-indicators_subnational_gha.csv   (X)
  select-education-indicators_subnational_gha.csv (X)
  literacy_subnational_gha.csv                    (X)
  sdgs_subnational_gha.csv                        (X violence/decision + M skilled delivery)
  fp2020_subnational_gha.csv                      (M)
  anemia_subnational_gha.csv                      (Y)
  child-mortality-rates_subnational_gha.csv       (Y)
  fertility-rates_subnational_gha.csv             (Y adolescent birth rate) [optional]

Outputs:
  data/processed/district_master_261.csv
  docs/district_crosswalk_261_to_260.csv
  data/processed/region_master_16_dhs2022.csv
  data/processed/region_master_16_analytic.csv
  data/processed/phase2_indicator_manifest.csv
"""
import json, re, sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
DOCS = ROOT / "docs"
PROC.mkdir(parents=True, exist_ok=True)

# ---- 16 canonical post-2022 regions (Title Case = Master Sheet convention) ----
CANON = ["Ahafo","Ashanti","Bono","Bono East","Central","Eastern","Greater Accra",
         "North East","Northern","Oti","Savannah","Upper East","Upper West","Volta",
         "Western","Western North"]

def canon_region(x):
    """Map any of the 3 naming conventions (Master/GeoJSON/DHS) to canonical Title Case."""
    if x is None: return None
    s = str(x).strip()
    s = s.replace("..", "").strip()
    s = re.sub(r"\(post 2022\)", "", s, flags=re.I).strip()
    low = s.lower()
    m = {
        "northeast":"North East","north east":"North East","northern east":"North East",
        "northern(post 2022)":"Northern","northern":"Northern",
        "savannah":"Savannah","greater accra":"Greater Accra","bono east":"Bono East",
        "western north":"Western North","upper east":"Upper East","upper west":"Upper West",
    }
    if low in m: return m[low]
    # exclude pre-2022 aliases explicitly
    if any(k in low for k in ["pre 2022","brong","upper west, upper east"]): return None
    for c in CANON:
        if low == c.lower(): return c
    return None  # anything unmatched (aliases, HXL) is dropped

# ================================================================= 1. MASTER SHEET 261
ms = pd.read_excel(RAW / "Master Sheet.xlsx")
ms.columns = [c.strip() for c in ms.columns]
mmda_col = [c for c in ms.columns if "MMDA" in c or "Metropolitan" in c][0]
d = pd.DataFrame()
d["region"] = ms["Region"].map(canon_region)
d["district_261"] = ms[mmda_col].astype(str).str.strip()
d["class"] = ms.get("Class")
d["lat"] = ms.get("Latitude"); d["lon"] = ms.get("Longitude")
tot = ms["Total Population"].astype(float)
d["total_pop"] = tot
d["female_15_64"] = ms["Female Population 15-64"].astype(float)
d["female_15_64_share"] = 100 * d["female_15_64"] / tot
d["illiteracy_rate"] = 100 * ms["Illiterate Population"].astype(float) / tot   # all-age proxy
d["uninsured_rate"] = 100 * ms["Uninsured Population"].astype(float) / tot
d["poverty_incidence"] = ms["Incidence of Poverty"].astype(float)
d["poverty_intensity"] = ms["Intensity of Poverty"].astype(float)
emp = ms["Employed Population"].astype(float); unemp = ms["Unemployed Population"].astype(float)
d["unemployment_rate"] = 100 * unemp / (emp + unemp)
assert len(d) == 261, f"Master Sheet must be 261 rows, got {len(d)}"
assert d["region"].notna().all(), "Unmapped region in Master Sheet"
d.to_csv(PROC / "district_master_261.csv", index=False)
print(f"[1] district_master_261.csv  rows={len(d)}  regions={d['region'].nunique()}")

# ================================================================= 2. GEOJSON 260
gj = json.loads((RAW / "Ghana_New_260_District.geojson").read_text(encoding="utf-8"))
geo = pd.DataFrame([{"geo_region": canon_region(f["properties"].get("REGION")),
                     "geo_district": str(f["properties"].get("DISTRICT")).strip()}
                    for f in gj["features"]])
print(f"[2] GeoJSON polygons={len(geo)}  regions={geo['geo_region'].nunique()}")

# ================================================================= 3. CROSSWALK 261<->260
# Adopt the vetted, hand-reconciled crosswalk (same Master Sheet + GeoJSON as Project 15):
# all metro-composite / spelling / word-order variants resolved; exactly 3 structural gaps
# (Guan, Sagnarigu, Awutu Senya West) merged to their parent polygons for RENDERING only.
cw = pd.read_csv(DOCS / "district_crosswalk_261_to_260.csv")
cw["master_sheet_district"] = cw["master_sheet_district"].astype(str).str.strip()
assert len(cw) == 261, f"crosswalk must have 261 rows, got {len(cw)}"
gaps = cw[cw["match_method"] == "structural_gap"]
print(f"[3] crosswalk loaded: 261 districts; matched={261-len(gaps)}; structural_gaps={len(gaps)}")
for _, g in gaps.iterrows():
    print(f"      STRUCTURAL GAP: {g['master_sheet_district']} ({g['master_sheet_region']}) — {g['note']}")
# merge GeoJSON linkage into the district frame and re-write
d = d.merge(cw[["master_sheet_district","geojson_district","match_method"]],
            left_on="district_261", right_on="master_sheet_district", how="left").drop(columns=["master_sheet_district"])
unmatched = d[d["match_method"].isna()]
assert len(unmatched) == 0, f"{len(unmatched)} master districts absent from crosswalk: {list(unmatched['district_261'])[:5]}"
d.to_csv(PROC / "district_master_261.csv", index=False)
print(f"[3] district_master_261.csv re-written with GeoJSON linkage (unmatched={len(unmatched)})")

# ================================================================= 4. DHS 2022 REGION EXTRACTION
def extract(fname, indmap):
    """indmap: {exact DHS Indicator name: output column}. Returns wide df indexed by region."""
    fp = RAW / fname
    if not fp.exists():
        print(f"    [skip] {fname} not present"); return None, []
    df = pd.read_csv(fp, low_memory=False)
    df = df[df["SurveyId"] == "GH2022DHS"].copy()
    df["region"] = df["Location"].map(canon_region)
    df = df[df["region"].notna()]
    out = pd.DataFrame({"region": CANON}).set_index("region")
    got = []
    for ind, col in indmap.items():
        sub = df[df["Indicator"] == ind].copy()
        if len(sub) == 0:
            continue
        if "IsPreferred" in sub.columns and (sub["IsPreferred"] == 1).any():
            sub = sub[sub["IsPreferred"] == 1]
        sub["Value"] = pd.to_numeric(sub["Value"], errors="coerce")
        ser = sub.groupby("region")["Value"].mean()
        out[col] = ser
        got.append(col)
    return out, got

targets = [
 ("select-gender-indicators_subnational_gha.csv", {
    "Final say in all of the decisions [Women]":"x_final_say_women",
    "Wife beating justified for at least one specific reason [Women]":"x_wifebeating_justified_women",
    "Do not own land [Women]":"x_no_land_women"}),
 ("select-education-indicators_subnational_gha.csv", {
    "Women with no education":"x_women_no_education",
    "Women with secondary or higher education":"x_women_secondary_plus"}),
 ("literacy_subnational_gha.csv", {
    "Women who are literate":"x_women_literate",
    "Women who cannot read at all":"x_women_cannot_read"}),
 ("sdgs_subnational_gha.csv", {
    "Physical or sexual or emotional violence committed by husband/partner in last 12 months":"x_ipv_any",
    "Own decision making about all three decisions":"x_own_decision_all3",
    "Assistance during delivery from a skilled provider":"m_skilled_delivery",
    "Age specific fertility rate: 15-19":"y_asfr_15_19"}),
 ("fp2020_subnational_gha.csv", {
    "Married women currently using any modern method of contraception":"m_modern_cpr_married",
    "Demand for family planning satisfied by modern methods":"m_fp_demand_satisfied_modern"}),
 ("anemia_subnational_gha.csv", {
    "Women with any anemia":"y_women_any_anemia",
    "Children with any anemia":"y_children_any_anemia"}),
 ("child-mortality-rates_subnational_gha.csv", {
    "Under-five mortality rate":"y_u5mr",
    "Neonatal mortality rate":"y_nmr",
    "Infant mortality rate":"y_imr"}),
 # HIV mediators (in-scope)
 ("hiv-counseling-and-testing_subnational_gha.csv", {
    "Women ever receiving an HIV test":"m_ever_hiv_test",
    "Pregnant women tested for HIV during ANC or labor and receiving the results":"m_anc_hiv_test"}),
 ("hiv-knowledge_subnational_gha.csv", {
    "Knowledge of prevention of MTCT - Can be prevented by mother taking special drugs during pregnancy [Women]":"m_hiv_mtct_knowledge_women"}),
 # NOTE: ANC4+ and facility births have NO region-level source within the user's 12-dataset list
 # (WHO MRH file is national-only). Dropped to stay in-scope; skilled delivery (sdgs) covers delivery care.
]

region_tbl = pd.DataFrame({"region": CANON}).set_index("region")
extracted_cols = []
for fname, indmap in targets:
    o, got = extract(fname, indmap)
    if o is not None:
        for c in got:
            region_tbl[c] = o[c]
        extracted_cols += got
        print(f"[4] {fname:48s} -> {got}")

region_tbl.to_csv(PROC / "region_master_16_dhs2022.csv")
print(f"[4] region_master_16_dhs2022.csv  cols={len(region_tbl.columns)}  regions={len(region_tbl)}")

# ================================================================= 5. MASTER SHEET -> 16 REGIONS + MERGE
agg = d.groupby("region").apply(lambda g: pd.Series({
    "ctx_total_pop": g["total_pop"].sum(),
    "ctx_n_districts": len(g),
    "ctx_illiteracy_rate": 100*(g["illiteracy_rate"]/100*g["total_pop"]).sum()/g["total_pop"].sum(),
    "ctx_uninsured_rate": 100*(g["uninsured_rate"]/100*g["total_pop"]).sum()/g["total_pop"].sum(),
    "ctx_poverty_incidence": (g["poverty_incidence"]*g["total_pop"]).sum()/g["total_pop"].sum(),
    "ctx_female_15_64_share": 100*g["female_15_64"].sum()/g["total_pop"].sum(),
}), include_groups=False)
region_full = region_tbl.join(agg)
region_full.to_csv(PROC / "region_master_16_analytic.csv")
print(f"[5] region_master_16_analytic.csv  cols={len(region_full.columns)}")

# ================================================================= 6. MANIFEST
manifest = []
role = {"x":"EXPOSURE","m":"MEDIATOR","y":"OUTCOME","ctx":"CONTEXT"}
for c in region_full.columns:
    pre = c.split("_")[0]
    nonnull = region_full[c].notna().sum()
    manifest.append({"column": c, "role": role.get(pre,"?"),
                     "n_regions_filled": int(nonnull), "status": "extracted" if nonnull>0 else "EMPTY"})
# MRH = WHO GHO national file (no SurveyId; COUNTRY=Ghana) -> Introduction/national context ONLY (never a region mediator)
mrh_fp = RAW / "maternal_and_reproductive_health_indicators_gha.csv"
if mrh_fp.exists():
    mrh = pd.read_csv(mrh_fp, low_memory=False)
    mrh = mrh[mrh["YEAR (DISPLAY)"].astype(str).str.match(r"^\d{4}")].copy()  # drop HXL/non-year header rows
    keep = [c for c in ["GHO (DISPLAY)","YEAR (DISPLAY)","COUNTRY (DISPLAY)","DIMENSION (NAME)","Value","Numeric","Low","High"] if c in mrh.columns]
    (ROOT/"outputs"/"data").mkdir(parents=True, exist_ok=True)
    mrh[keep].to_csv(ROOT/"outputs"/"data"/"mrh_national_context.csv", index=False)
    print(f"[MRH] WHO GHO national context -> outputs/data/mrh_national_context.csv  rows={len(mrh)}  indicators={mrh['GHO (DISPLAY)'].nunique()}")
manifest.append({"column":"ctx_who_mrh_national","role":"CONTEXT-INTRO-ONLY","n_regions_filled":0,
                 "status":"WHO GHO national -> outputs/data/mrh_national_context.csv (Introduction context only; NOT a region mediator)"})
mf = pd.DataFrame(manifest)
mf.to_csv(PROC / "phase2_indicator_manifest.csv", index=False)
print(f"[6] phase2_indicator_manifest.csv  rows={len(mf)}  pending={sum(mf.status.str.startswith('PENDING'))}")
print("\nDONE.")
