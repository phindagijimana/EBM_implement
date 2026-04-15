"""Minimal KDE MixtureSustain demo (synthetic cohort) — same stack as Lopez-style EBM."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from kde_ebm.mixture_model import fit_all_kde_models
from pySuStaIn.MixtureSustain import MixtureSustain

from ebm_tle.synthetic import generate_data_mixture_sustain, generate_random_mixture_sustain_model


def run_demo(
    output_dir: Path,
    *,
    n_biomarkers: int = 5,
    n_subjects: int = 400,
    n_subtypes: int = 1,
    n_startpoints: int = 10,
    n_mcmc: int = 8000,
    seed: int = 42,
    plot: bool = False,
) -> Path:
    """Fit MixtureSustain with mixture_KDE on simulated data; write stages CSV and pickle dir."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    np.random.seed(seed)

    ground_truth_sequences = generate_random_mixture_sustain_model(n_biomarkers, n_subtypes)
    ground_truth_subtypes = rng.integers(0, n_subtypes, size=n_subjects).astype(int)

    n_stages = n_biomarkers
    n_ctrl = int(np.round(n_subjects * 0.25))
    ground_truth_stages = np.vstack(
        (
            np.zeros((n_ctrl, 1), dtype=int),
            rng.integers(1, n_stages + 1, size=(n_subjects - n_ctrl, 1)),
        )
    ).astype(int)

    data, _ = generate_data_mixture_sustain(
        ground_truth_subtypes, ground_truth_stages, ground_truth_sequences, "mixture_KDE"
    )

    min_case_stage = np.round((n_biomarkers + 1) * 0.8)
    index_case = np.where(ground_truth_stages >= min_case_stage)[0]
    index_control = np.where(ground_truth_stages == 0)[0]
    labels = 2 * np.ones(data.shape[0], dtype=int)
    labels[index_case] = 1
    labels[index_control] = 0

    mixtures = fit_all_kde_models(data, labels)
    L_yes = np.zeros(data.shape)
    L_no = np.zeros(data.shape)
    for i in range(n_biomarkers):
        L_no[:, i], L_yes[:, i] = mixtures[i].pdf(data[:, i].reshape(-1, 1))

    biomarker_labels = [f"bm{i}" for i in range(n_biomarkers)]
    dataset_name = "demo_synthetic"
    sustain = MixtureSustain(
        L_yes,
        L_no,
        biomarker_labels,
        n_startpoints,
        n_subtypes,
        n_mcmc,
        str(output_dir),
        dataset_name,
        use_parallel_startpoints=False,
        seed=seed,
    )

    _samples_seq, _samples_f, ml_subtype, prob_ml_subtype, ml_stage, prob_ml_stage, _prob_ss = (
        sustain.run_sustain_algorithm(plot=plot, plot_format="png")
    )

    subj_ids = [str(i + 1) for i in range(n_subjects)]
    df = pd.DataFrame(
        {
            "subj_id": subj_ids,
            "ml_subtype": np.asarray(ml_subtype).reshape(-1),
            "prob_ml_subtype": np.asarray(prob_ml_subtype).reshape(-1),
            "ml_stage": np.asarray(ml_stage).reshape(-1),
            "prob_ml_stage": np.asarray(prob_ml_stage).reshape(-1),
        }
    )
    out_csv = output_dir / "demo_stages.csv"
    df.to_csv(out_csv, index=False)

    meta = {
        "n_biomarkers": n_biomarkers,
        "n_subjects": n_subjects,
        "n_mcmc": n_mcmc,
        "ground_truth_sequence_row0": ground_truth_sequences[0].astype(int).tolist(),
    }
    import json

    (output_dir / "demo_meta.json").write_text(json.dumps(meta, indent=2))
    return out_csv
