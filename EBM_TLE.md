# Summary: Event-based modeling in MTLE-HS (Lopez et al., *Epilepsia* 2022)

**Citation:** Lopez SM, Aksman LM, Oxtoby NP, et al. Event-based modeling in temporal lobe epilepsy demonstrates progressive atrophy from cross-sectional data. *Epilepsia*. 2022;63(8):2081–2095. doi:[10.1111/epi.17316](https://doi.org/10.1111/epi.17316) (PMC:[PMC9540015](https://pmc.ncbi.nlm.nih.gov/articles/PMC9540015/))

---

## Research question

From a large **cross-sectional** T1-weighted MRI cohort, the authors ask whether mesial temporal lobe epilepsy with hippocampal sclerosis (MTLE-HS) shows a **characteristic order** of regional morphometric abnormalities, and whether **event-based model (EBM) stage** relates to illness duration, age at onset, and antiseizure medication (ASM) resistance.

## Why event-based modeling (EBM)?

Longitudinal imaging in epilepsy is scarce. EBM is a **data-driven** approach that infers a **most likely sequence** of biomarker abnormalities from snapshots of many patients at different points, under assumptions that markers become abnormal **sequentially** and change **monotonically** (no reversion to “normal”). It uses mixture modeling (kernel density estimation) to separate case-like vs control-like distributions per region, then searches for the best ordering (e.g., MCMC with bootstrapping for uncertainty).

The paper also uses **brain asymmetry indices (BASI)** so that, for unilateral pathology, contralateral structure acts as a within-subject reference—often improving sensitivity for early change.

## Data and features

- **ENIGMA-Epilepsy:** 804 people with MTLE-HS and 1625 healthy controls across **25 centers**.
- Features: regional **cortical thickness**, **surface area**, and **subcortical volumes** from T1w MRI.
- **Feature selection:** biomarkers with moderate case–control effect (**Cohen’s |d| ≥ 0.5**; sensitivity analysis at **|d| ≥ 0.4** with more markers but similar ordering).

## Inferred progression sequence (high level)

With seven robust features, the bootstrapped EBM ordering was broadly:

1. **Ipsilateral hippocampal volume loss** and **increased hippocampal asymmetry** (early events).
2. Then **neocortical thinning** (e.g., bilateral superior parietal regions, ipsilateral precuneus in the primary seven-feature model).
3. Then **ipsilateral thalamic volume reduction**.
4. Finally **ipsilateral lateral ventricle enlargement**.

**Left vs right** MTLE-HS showed **similar** progression patterns. A **richer** model (|d| ≥ 0.4) added detail but kept the same overall story: spread from mesial temporal structures toward **bilateral** neocortex and thalamus.

## Staging of participants

Stages **0–7** correspond to how many of the selected regional measures are classified as abnormal for that person. Notable distributions:

- **~29%** of MTLE-HS patients were **Stage 0** (no statistically detectable T1w abnormality under the model)—consistent with known **overlap** between radiologic HS and “normal-range” hippocampal volume on T1 in a substantial minority of cases, and with HS being a **multisequence** diagnosis.
- **~71%** were Stage 1 or higher; many cluster in early stages reflecting hippocampal volume/asymmetry changes.

## Clinical associations (important nuance)

- **EBM stage (0–7)** correlated with **duration of illness**, **age at onset**, and showed a modest effect for **ASM resistance** (AUC ≈ 0.59, *p* = 0.043).
- The authors stress that these associations were **largely driven by Stage 0 vs non-0**: Stage 0 cases had **shorter** disease duration and **later** age at onset on average; within **Stages 1–7**, correlations with duration/onset were **weak or absent**.
- Interpretation: the model’s **continuous accumulation of imaging burden (Stages 1–7)** did **not** strongly track the available clinical severity proxies in this cohort; the **clearest** clinical contrast was between “T1-subtle” (Stage 0) and “T1-detectable” MTLE-HS.

## Main conclusions and context

- Cross-sectional ENIGMA data support an **ordered cascade** of structural changes **originating ipsilateral hippocampus** and extending to neocortex, thalamus, and ventricle—**qualitatively aligned** with prior **longitudinal** atrophy literature in TLE/MTLE-HS.
- The authors separate **possible genetic / predisposition** signals (hippocampal volume/asymmetry also seen in relatives) from **disease-related** cortical thinning (less attributed to healthy siblings).
- **Limitation / forward look:** better linkage to progression may require **other clinical variables** (e.g., seizure burden, detailed ASM exposure) and acknowledges **center heterogeneity** in Stage 0 rates (diagnostic practice/capability).

---

*Summary notes derived from the published paper; for exact statistics, figures, and supplementary analyses, refer to the original article and its supplements.*
