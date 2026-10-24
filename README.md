# GRANDE-U · Groundwater-level reconstruction (two-step ML)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/VytautasSam/grande-u-gwl-reconstruction/blob/main/GRANDE_U_manuscript_reproducible_workflow.ipynb)

**Reproducibility repository** for the manuscript **“A Two-Step Machine-Learning Framework for Reconstructing Groundwater-Level Time Series in Transboundary Aquifers”**, developed within GRANDE-U.

The single Jupyter notebook reconstructs the manuscript's analytical sequence and exports Figures 1–9 and supporting tables. This is a method-preserving consolidation of the four original research notebooks; the scientific audit notes at the end of the notebook identify methodological limitations.

## Directory structure

```text
grande-u-gwl-reconstruction/
├── GRANDE_U_manuscript_reproducible_workflow.ipynb
├── data_inputs/
│   ├── static_wells.xlsx
│   ├── packed/             # compressed small-file parts of 3 original inputs
│   ├── manifest.json
│   └── README.md
├── scripts/
│   ├── verify_inputs.py
│   └── validate_notebook.py
├── .github/workflows/check-reproducibility.yml
├── requirements.txt
├── .gitignore
└── README.md
```


## Why datasets are stored as small compressed parts

GitHub’s web editor and some repository-writing interfaces can reject large files or large commits even below GitHub's normal Git push limit. To avoid this, **all three large inputs are stored as lossless gzip chunks smaller than 750 KiB each**. The fourth input, `static_wells.xlsx`, is stored normally. **These are not sampled, reduced-resolution, or simplified datasets.**

- The notebook downloads parts from this repository when run directly in Colab (no Drive mounting required).
- A local checkout uses the already-present parts offline.
- Exact original input bytes are reconstructed into ignored `data_inputs/` paths and checked against the manuscript's original SHA-256 hashes.
- `python scripts/verify_inputs.py` verifies every stored part and restored dataset byte-for-byte before a numerical analysis.
- For GitHub's web uploader, **extract the ZIP and upload the repository contents, not the ZIP itself**. Upload in several small batches if the website reports a total-commit-size limit. Running `git push` from a local clone remains the simplest reliable option.

## Run in Google Colab

**After publishing the repository as PUBLIC:** click **Open in Colab** above and choose **Runtime → Run all**. The notebook installs any missing Python packages and automatically downloads the small losslessly compressed data parts from `raw.githubusercontent.com`, restores the exact original four input files into Colab's `data_inputs/` folder, and checks their SHA-256 hashes. No Google Drive mounting and no manual file uploads are needed.

Colab loads notebooks directly from GitHub but does **not** clone their data files. The first input cell handles this for you. For full-model reproducibility use a runtime with sufficient RAM and uninterrupted CPU time; running per-well model ensembles, SHAP and high-DPI figure export may take substantial resources. Results are written under `manuscript_outputs/`, which is excluded from git. To retain outputs after a Colab session, download that directory or copy it to your own storage.

**Private repository alternative:** Anonymous GitHub raw-file downloads will fail for private repositories. Clone the private repo in an authenticated local environment or provide the four matching input files in `data_inputs/` before executing the notebook. Making datasets public requires checking redistribution permission first.

## Run locally

```bash
git clone https://github.com/VytautasSam/grande-u-gwl-reconstruction.git
cd grande-u-gwl-reconstruction
python -m pip install -r requirements.txt
python scripts/verify_inputs.py
jupyter lab GRANDE_U_manuscript_reproducible_workflow.ipynb
```

Then **Run All**. File paths are relative to the repository root.

## Analytical sequence

1. Record provenance and hashes, load the groundwater/climate, static well, processed TWS, and map inputs.
2. Join geospatial GRACE data, harmonize monthly records and audit data quality.
3. Examine missing records and exploratory statistics; create lagged and rolling climate/TWS predictors.
4. Perform chronological per-well cross-validation for Step 1 using baseline, ridge, random forest and gradient boosting.
5. Select area-specific reference wells and fit Step 2 with a transferred relative GWL predictor.
6. Export holdout predictions, diagnostics, clustering and SHAP outputs.
7. Produce manuscript figures **1–9** in manuscript order and supplementary plots/tables.

**Reproducibility controls:** byte-identical reconstruction from compressed parts, deterministic random seed, original documented fixed model hyperparameters, source-data SHA-256 digests, and software version manifest at notebook execution. On each GitHub push a lightweight GitHub Actions check verifies input hashes, source cell syntax, and the nine expected figure exports without rerunning the full ML models. The processed GRACE product is **not** the output of GRACE satellite gap-filling code stored in this repository. National well-source retrieval and climate data extraction were also conducted upstream and are not replicated.

## Publish to your GitHub account

The ZIP distribution is an **unpublished repository package**, not a new live repo. After extracting the folder, open a terminal *inside* `grande-u-gwl-reconstruction`:

```bash
git init -b main
git add .
git commit -m "Initial manuscript reproducibility repository"
# First log in to GitHub using GitHub CLI: gh auth login
# Choose ONE visibility option after reviewing the data access rights:
gh repo create VytautasSam/grande-u-gwl-reconstruction --private --source=. --remote=origin --push
# OR (only with permission to publish all supplied datasets):
# gh repo create VytautasSam/grande-u-gwl-reconstruction --public --source=. --remote=origin --push
```

On Windows, these commands can be run in **Git Bash**, with GitHub CLI (`gh`) installed. Alternatively, create an empty repository on GitHub and push with regular `git remote add origin ...` + `git push -u origin main`. The **Colab badge will only work once the named repository is published**, and fully automated anonymous input downloads require public visibility.

## Data availability, rights, citation

The archived original inputs (three stored as lossless gzip chunks under `data_inputs/packed/`) are processing-stage products supplied by the manuscript authors, with original links and SHA-256 hashes described in `data_inputs/manifest.json`. **No license is assigned automatically** to the source data or research code. Check collaborator approvals, source licenses and any well-location/data-release limitations before public redistribution. Add an appropriate `LICENSE` and an approved citation after author review. The manuscript paper's DOI is not assigned in this package.
