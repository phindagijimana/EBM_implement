"""End-to-end KDE + MixtureSustain paths (small settings for CI)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from ebm_tle.demo import run_demo
from ebm_tle.fit import fit_from_csv


@pytest.mark.slow
def test_run_demo_writes_stages(tmp_path):
    out = run_demo(
        tmp_path / "demo_out",
        n_biomarkers=4,
        n_subjects=100,
        n_startpoints=5,
        n_mcmc=1500,
        seed=1,
        plot=False,
    )
    assert out.is_file()
    df = pd.read_csv(out)
    assert len(df) == 100
    assert {"subj_id", "ml_stage", "prob_ml_stage"}.issubset(df.columns)
    assert (tmp_path / "demo_out" / "pickle_files").is_dir()


def test_fit_from_csv(tmp_path):
    rng = np.random.default_rng(2)
    rows = []
    for i in range(40):
        rows.append(
            {
                "subject_id": f"c{i}",
                "group": 0,
                "a": float(rng.normal(0, 1)),
                "b": float(rng.normal(0, 1)),
                "c": float(rng.normal(0, 1)),
            }
        )
    for i in range(40):
        rows.append(
            {
                "subject_id": f"p{i}",
                "group": 1,
                "a": float(rng.normal(0.7, 1)),
                "b": float(rng.normal(0.5, 1)),
                "c": float(rng.normal(0.3, 1)),
            }
        )
    csv_path = tmp_path / "cohort.csv"
    pd.DataFrame(rows).to_csv(csv_path, index=False)

    out_csv = fit_from_csv(
        csv_path,
        tmp_path / "fit_out",
        n_startpoints=5,
        n_mcmc=2000,
        seed=3,
        plot=False,
    )
    assert out_csv.is_file()
    staged = pd.read_csv(out_csv)
    assert len(staged) == 80
    assert "ml_stage" in staged.columns
