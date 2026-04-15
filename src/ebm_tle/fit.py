"""Fit KDE MixtureSustain from a cohort CSV (0=control, 1=case)."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from kde_ebm.mixture_model import fit_all_kde_models
from pySuStaIn.MixtureSustain import MixtureSustain


def fit_from_csv(
    csv_path: Path,
    output_dir: Path,
    *,
    group_col: str = "group",
    subject_col: str = "subject_id",
    biomarker_cols: list[str] | None = None,
    n_startpoints: int = 15,
    n_s_max: int = 1,
    n_mcmc: int = 50_000,
    seed: int = 42,
    plot: bool = False,
) -> Path:
    df = pd.read_csv(csv_path)
    if group_col not in df.columns:
        raise ValueError(f"Missing column {group_col!r}")
    if subject_col not in df.columns:
        raise ValueError(f"Missing column {subject_col!r}")
    df = df.loc[df[group_col].isin([0, 1])].reset_index(drop=True)
    if df.empty:
        raise ValueError("No rows with group in {0, 1}")
    if biomarker_cols is None:
        biomarker_cols = [
            c
            for c in df.columns
            if c not in (group_col, subject_col) and np.issubdtype(df[c].dtype, np.number)
        ]
    if len(biomarker_cols) < 2:
        raise ValueError("Need at least two numeric biomarker columns")

    labels = df[group_col].astype(int).values
    if set(np.unique(labels)) - {0, 1, 2}:
        raise ValueError("group column must be 0=control, 1=case (optional 2=unused)")
    data = df[biomarker_cols].astype(float).values

    mixtures = fit_all_kde_models(data, labels)
    L_yes = np.zeros(data.shape)
    L_no = np.zeros(data.shape)
    for i in range(data.shape[1]):
        L_no[:, i], L_yes[:, i] = mixtures[i].pdf(data[:, i].reshape(-1, 1))

    dataset_name = Path(csv_path).stem
    sustain = MixtureSustain(
        L_yes,
        L_no,
        biomarker_cols,
        n_startpoints,
        n_s_max,
        n_mcmc,
        str(output_dir),
        dataset_name,
        use_parallel_startpoints=False,
        seed=seed,
    )
    _a, _b, ml_subtype, prob_ml_subtype, ml_stage, prob_ml_stage, _c = sustain.run_sustain_algorithm(
        plot=plot, plot_format="png"
    )

    out = pd.DataFrame(
        {
            subject_col: df[subject_col].astype(str),
            "ml_subtype": np.asarray(ml_subtype).reshape(-1),
            "prob_ml_subtype": np.asarray(prob_ml_subtype).reshape(-1),
            "ml_stage": np.asarray(ml_stage).reshape(-1),
            "prob_ml_stage": np.asarray(prob_ml_stage).reshape(-1),
        }
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    out_csv = output_dir / f"{dataset_name}_stages.csv"
    out.to_csv(out_csv, index=False)
    (output_dir / "fit_meta.json").write_text(
        json.dumps(
            {
                "csv": str(csv_path),
                "biomarkers": biomarker_cols,
                "n_mcmc": n_mcmc,
                "n_subjects": int(len(df)),
            },
            indent=2,
        )
    )
    return out_csv
