# EBM_implement

Internal **research** CLI for **KDE event-based models** (MTLE-HS–style morphometry workflows): **`kde_ebm`** + **`MixtureSustain`** ([pySuStaIn](https://github.com/ucl-pond/pySuStaIn)), aligned with Lopez et al. *Epilepsia* 2022 ([10.1111/epi.17316](https://doi.org/10.1111/epi.17316)).

## Prerequisites

- **Python 3.9+** and network access for first install: **`pySuStaIn`**, **`kde_ebm`**, and **`awkde`** are installed from GitHub (see [requirements.txt](requirements.txt)), matching the [UCL POND](https://github.com/ucl-pond/pySuStaIn) stack.

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
| [USER_GUIDE.md](USER_GUIDE.md) | Usage, commands, limitations, generalization |
| [EBM_TLE_br.md](EBM_TLE_br.md) | Builder Review (Inzira-style): platform fit, reproducibility, clinical/integration notes |
| [EBM_TLE.md](EBM_TLE.md) | Short summary of the Lopez et al. paper |

There is **no** pretrained checkpoint from the paper in this repo; train on your features or see the user guide for reuse expectations.

## License / use

Tooling stack follows upstream **pySuStaIn** / **kde_ebm** terms. This wrapper is for **research** workflows, not a clinical product.
