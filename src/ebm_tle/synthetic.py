"""Synthetic mixture-style data (logic aligned with pySuStaIn sim/simfuncs.py)."""

from __future__ import annotations

import numpy as np


def generate_random_mixture_sustain_model(n_biomarkers: int, n_s: int) -> np.ndarray:
    s = np.zeros((n_s, n_biomarkers))
    matched_others = True
    for _ in range(30):
        matched_others = False
        for si in range(n_s):
            s[si, :] = np.random.permutation(n_biomarkers)
            for prev in range(si):
                if np.all(s[si, :] == s[prev, :]):
                    matched_others = True
        if not matched_others:
            break
    if matched_others:
        print("WARNING: could not find unique sequences for all subtypes.")
    return s


def generate_data_mixture_sustain(
    subtypes: np.ndarray,
    stages: np.ndarray,
    gt_ordering: np.ndarray,
    mixture_style: str,
) -> tuple[np.ndarray, np.ndarray]:
    n_biomarkers = gt_ordering.shape[1]
    n_subjects = len(subtypes)
    mean_controls = np.array([0] * n_biomarkers)
    std_controls = np.array([0.25] * n_biomarkers)
    if mixture_style == "mixture_GMM":
        mean_cases = np.array([1.5] * n_biomarkers)
        std_cases = np.random.uniform(0.25, 0.50, n_biomarkers)
    elif mixture_style == "mixture_KDE":
        mean_cases = np.array([0.5] * n_biomarkers)
        std_cases = np.random.uniform(0.2, 0.5, n_biomarkers)
    else:
        raise ValueError(mixture_style)

    data = np.zeros((n_subjects, n_biomarkers))
    data_denoised = np.zeros((n_subjects, n_biomarkers))
    stages = stages.astype(int)

    for i in range(n_subjects):
        s_i = gt_ordering[subtypes[i], :].astype(int)
        stage_i = stages[i].item()
        for j in range(stage_i):
            if mixture_style == "mixture_KDE":
                sample_j = np.random.lognormal(mean_cases[s_i[j]], std_cases[s_i[j]])
            else:
                sample_j = np.random.normal(mean_cases[s_i[j]], std_cases[s_i[j]])
            data[i, s_i[j]] = sample_j
            data_denoised[i, s_i[j]] = mean_cases[s_i[j]]
        for j in range(stage_i, n_biomarkers):
            data[i, s_i[j]] = np.random.normal(mean_controls[s_i[j]], std_controls[s_i[j]])
            data_denoised[i, s_i[j]] = mean_controls[s_i[j]]

    return data, data_denoised
