# User guide — EBM_implement (EBM_TLE)

Evaluation of the *Epilepsia* EBM/MTLE-HS methods paper and this repository’s implementation (usability, reproducibility, performance, generalization, clinical use, interpretability, integration, limitations). For a minimal overview see [README.md](README.md).

**Primary reference:** Lopez SM, Aksman LM, Oxtoby NP, et al. *Event-based modeling in temporal lobe epilepsy demonstrates progressive atrophy from cross-sectional data.* Epilepsia. 2022;63(8):2081–2095. https://doi.org/10.1111/epi.17316 (PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC9540015/)

**Typical layout:** this repo (`./ebm`, `src/ebm_tle/`, `requirements.txt`); **sibling** `predict_epi/vendor/pySuStaIn`; local `runs/`, `.ebm/logs/` (ignored by git); paper summary in `EBM_TLE.md`.

---

## Context

Lopez et al. use **cross-sectional** T1 morphometry from **ENIGMA-Epilepsy** to infer a **KDE event-based model (EBM)** sequence (hippocampus → neocortex → thalamus → ventricle) and per-subject **stages**, with clinical associations strongest for **Stage 0 vs non-0** on T1. The stack is the **UCL POND** lineage: **`kde_ebm`** (mixtures) + **`MixtureSustain`** in **pySuStaIn**.

This repository adds a **deployment shell**: venv + **`./ebm`** (`install`, `check`, `demo`, `fit`, `start`, `stop`, `logs`)—not ENIGMA extraction or the paper’s full mega-analysis.

| Piece | Location | Role |
|--------|-----------|------|
| CLI | `./ebm` | `install` creates `.venv`; other commands run `python -m ebm_tle`. |
| Package | `src/ebm_tle/` | `demo`, `fit`, lifecycle; `synthetic.py` avoids broken vendored `sim` imports. |
| Upstream | `../predict_epi/vendor/pySuStaIn` | Required for editable install unless you change `requirements.txt`. |
| Deps | `requirements.txt` | `kde_ebm`, `awkde`, numpy/scipy/sklearn, etc. |
| Run state | `.ebm/run/pid`, `.ebm/logs/fit.log` | `start` / `stop` / `logs`. |

---

## Commands (reference)

```bash
chmod +x ./ebm
./ebm install
./ebm check
./ebm demo --output runs/demo --mcmc 8000
./ebm fit cohort.csv --output runs/fit_out --group-col group --subject-col subject_id
./ebm start
./ebm logs -n 100
./ebm stop
```

**Outputs:** `demo_stages.csv` / `*_stages.csv`, `demo_meta.json` / `fit_meta.json`, **`pickle_files/`** under `--output`. Package version **0.1.0** (`pyproject.toml`).

**CSV `fit`:** rows must have `group` ∈ {0, 1} (0=control, 1=case); other codes are dropped. Biomarkers = numeric columns aside from ids.

---

## Platform fit and reproducibility

### Usability

**Published:** large multi-site cohort; feature screen (e.g. |Cohen’s *d*| ≥ 0.5); KDE + MCMC ordering + bootstrap; stages 0…*k*.

**Here:** one surface after `./ebm install`; **`demo`** is synthetic sanity; **`fit`** is your real table. **Friction:** first install clones GitHub deps; **MCMC** cost grows with `--mcmc` and pySuStaIn’s internal phases. **Gap:** no FreeSurfer/ENIGMA pipeline in-repo—build the CSV yourself.

### Reproducibility

No bundled **pretrained** model from the paper; **retrain** on your data or obtain artifacts from authors. Replication of paper figures needs **ENIGMA-Epilepsy** data and their protocols.

**Note:** `ebm_tle/synthetic.py` replaces broken `sim` package imports (`from simfuncs import *` when `sim` is installed as a package).

---

## Performance and generalization

**Performance:** raise `--mcmc` for research-grade runs; `./ebm check` does not benchmark MCMC.

**Generalization:** mixtures and ordering are **dataset-specific**. New sites usually need **harmonization** (e.g. ComBat, site covariates) or retraining; multi-site training (as in the paper) helps but does not guarantee a new scanner.

---

## Clinical relevance and integration

**Research:** staging supports cohort description and hypotheses; fine stages had **weak** clinical links vs **Stage 0 vs not** in the paper.

**Not** a clinical device: governance and validation are your institution’s responsibility.

**Integration:** natural downstream of BIDS + FreeSurfer/ENIGMA-style ROI tables → **`ebm fit`**.

---

## Limitations and failure modes

- No imaging pipeline; CSV QC is yours.
- Default **`start`** backgrounds the **synthetic demo**, not arbitrary jobs (change `cli.cmd_start` if needed).
- **`MPLBACKEND=Agg`** is set in `./ebm`; SuStaIn may still use matplotlib.
- NFS latency can slow venv and large pickles.

---

## Builder insight

This repo wires **`kde_ebm` + `MixtureSustain`** into a small CLI. The hard part is **feature construction and validation**, not `pip install`.

**Extensions:** example cohort CSV; Slurm wrapper; optional `ebm apply` to score new subjects from saved `pickle_files/` without full refit.

---

## References

- Lopez et al. 2022 *Epilepsia* (DOI above).
- `EBM_TLE.md` — short paper summary.
- pySuStaIn / kde_ebm — UCL POND (via `requirements.txt`).

---

*Last updated: 2026-04-14.*
