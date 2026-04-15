# EBM_implement

Internal **research** CLI for **KDE event-based models** (MTLE-HS–style morphometry workflows): **`kde_ebm`** + **`MixtureSustain`** ([pySuStaIn](https://github.com/ucl-pond/pySuStaIn)), aligned with Lopez et al. *Epilepsia* 2022 ([10.1111/epi.17316](https://doi.org/10.1111/epi.17316)).

## Prerequisites

- **Python 3.9+** and network access for first install (`kde_ebm`, `awkde` from GitHub).
- **Sibling checkout:** this repo expects `predict_epi/vendor/pySuStaIn` next to it, e.g.
  - `Documents/predict_epi/vendor/pySuStaIn`
  - `Documents/EBM_TLE` (this project)  
  Adjust the `-e` line in `requirements.txt` if your layout differs.

## Quick start

```bash
chmod +x ./ebm
./ebm install
./ebm check
./ebm demo --output runs/demo
```

Cohort fit (CSV: `group` 0=control, 1=case; numeric biomarker columns):

```bash
./ebm fit your_cohort.csv --output runs/fit_out
```

Background demo, logs, stop:

```bash
./ebm start
./ebm logs -n 50
./ebm stop
```

## Documentation

| File | Contents |
|------|-----------|
| [USER_GUIDE.md](USER_GUIDE.md) | Full usage, design notes, limitations, generalization, references |
| [EBM_TLE.md](EBM_TLE.md) | Short summary of the Lopez et al. paper |

There is **no** pretrained checkpoint from the paper in this repo; train on your features or see the user guide for reuse expectations.

## License / use

Tooling stack follows upstream **pySuStaIn** / **kde_ebm** terms. This wrapper is for **research** workflows, not a clinical product.
