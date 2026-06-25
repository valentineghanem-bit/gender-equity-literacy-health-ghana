"""Smoke tests for the analysis pipeline outputs (read processed data only; fast)."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"


def test_region_master_shape():
    df = pd.read_csv(PROC / "region_master_16_analytic.csv")
    assert len(df) == 16, "region master must have 16 regions"
    assert df.drop(columns=["region"]).isna().sum().sum() == 0, "no missing values expected"


def test_district_frame_261():
    df = pd.read_csv(PROC / "district_master_261.csv")
    assert len(df) == 261, "district frame must retain all 261 districts"
    assert df["district_261"].nunique() == 261, "districts must be unique"


def test_national_u5mr_matches_dhs():
    df = pd.read_csv(PROC / "region_master_16_analytic.csv")
    natl = (df["y_u5mr"] * df["ctx_total_pop"]).sum() / df["ctx_total_pop"].sum()
    assert 35 < natl < 48, f"population-weighted national U5MR ({natl:.1f}) should approximate DHS 2022 (~41.5)"


def test_crosswalk_three_structural_gaps():
    cw = pd.read_csv(ROOT / "docs" / "district_crosswalk_261_to_260.csv")
    assert len(cw) == 261
    assert (cw["match_method"] == "structural_gap").sum() == 3
