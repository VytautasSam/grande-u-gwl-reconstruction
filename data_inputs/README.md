# Archived inputs and provenance

These are the four **integrated and processed inputs** provided with the manuscript's Python notebooks, archived losslessly as small compressed files (except the static Excel file) to make the published notebook runnable in Colab without accessing private Drive links. The original source locations are retained in `manifest.json`. The notebook verifies their SHA-256 hashes before parsing to protect scientific reproducibility.

| File | Contents | Source notebook |
|---|---|---|
| `monthly_wells.csv` | Well-month groundwater levels, coordinates and harmonized climate covariates | `1_data_processing_and_validation` |
| `static_wells.xlsx` | Well-specific geologic and monitoring metadata | `1_data_processing_and_validation` |
| `processed_grace.parquet` | GRACE/GRACE-FO TWS time series already imputed and encoded spatially | `1_data_processing_and_validation` |
| `world_boundaries.geojson` | Country boundaries for map panels | `2_statistics_analytics_maps` |

**Important limitations:** The well-month table is an integration product; it is not a dump of raw records from national monitoring databases. The GRACE Parquet is **already imputed**; the steps preceding that imputation cannot be independently reconstructed from these inputs alone. See manuscript §3.1 for upstream source agencies (EELIS/KESE, LEGMC, PožVIS/LGS, PGI–NRI, NGWMN/USGS, Ukrainian agencies and operators; ERA5-Land; GRACE/GRACE-FO).

**Before setting the repository to public:** confirm redistributability/authorization for each integrated source (especially coordinates, national monitoring metadata and non-open Ukrainian partner-supplied records). No broad data-reuse license is asserted by this repository package. If datasets may not be public, keep the repository private and run it locally or stage data in an authenticated Colab runtime.

**Storage note:** Three large source datasets are represented by gzip parts under `packed/` (each under 750 KiB). The notebook restores the exact original CSV, Parquet and GeoJSON before parsing. Their SHA-256 digests and uncompressed sizes are unchanged. These are not approximated or simplified versions. Run `python scripts/verify_inputs.py` to confirm recovery from the tracked parts.
