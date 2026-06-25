# Data log — master dataset provenance

| Field | Value |
|---|---|
| Datasets | 2022 Ghana DHS subnational (gender, education, literacy, SDG, FP2020, anaemia, child-mortality, HIV testing, HIV knowledge); 2021 Census 261-district master sheet; Ghana 260-polygon GeoJSON; WHO GHO MRH (national context) |
| Spatial units | 16 post-2019 regions (inference); 261 districts (spatial structure/mapping; 3 structural gaps merged to parent polygon for rendering) |
| Extraction | DHS filtered to `SurveyId=GH2022DHS`; harmonised to 16 canonical regions (see `docs/region_harmonization_map.csv`); one preferred estimate per region |
| Cleaning | pre-2022 region aliases + HXL rows dropped; population-weighted aggregation of Census layer to region; national pop-weighted values reproduce published DHS figures |
| Outputs | `region_master_16_analytic.csv` (16×27), `district_master_261.csv` (261), `analytic_region_16_clean/modeling.csv` |
| Crosswalk | `docs/district_crosswalk_261_to_260.csv` (3 structural gaps: Guan, Sagnarigu, Awutu Senya West) |
| IRB | Ghana Health Service Ethics Review Board — exempt (secondary aggregate data) |
