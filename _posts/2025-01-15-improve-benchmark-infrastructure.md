---
title: "IMPROVE: Building Rigorous Benchmark Infrastructure for Cancer Drug Response Prediction"
date: 2025-01-15
permalink: /blog/improve-benchmark-infrastructure/
categories:
  - blog
tags:
  - machine-learning
  - software-engineering
  - cancer-research
  - benchmarking
  - open-source
  - github-actions
excerpt: "After CANDLE: building the IMPROVE benchmark framework, improvelib, the UNO model, and the CI/CD infrastructure that made cross-study drug response evaluation reproducible for the community."
author_profile: false
toc: true
toc_sticky: true
---

<div class="article-banner">
  <p class="eyebrow">Benchmarking infrastructure &middot; 2025</p>
  <h1 class="article-title">IMPROVE: Building Rigorous Benchmark Infrastructure for Cancer Drug Response Prediction</h1>
  <p class="article-dek">After CANDLE: building the IMPROVE benchmark framework, improvelib, the UNO model, and the CI/CD infrastructure that made cross-study drug response evaluation reproducible across 15+ researchers at Argonne, LLNL, and ORNL.</p>
</div>

<div class="post-tags">
  <span class="post-tag post-tag--blue">benchmarking</span>
  <span class="post-tag post-tag--red">cancer research</span>
  <span class="post-tag post-tag--green">open source</span>
  <span class="post-tag post-tag--violet">neural networks</span>
  <span class="post-tag post-tag--amber">CI/CD</span>
</div>

<div class="stat-row">
  <div class="stat-card">
    <span class="stat-card__value">4</span>
    <span class="stat-card__label">public drug response datasets in cross-study analysis</span>
  </div>
  <div class="stat-card stat-card--green">
    <span class="stat-card__value">15+</span>
    <span class="stat-card__label">researchers across Argonne, LLNL, and ORNL</span>
  </div>
  <div class="stat-card stat-card--amber">
    <span class="stat-card__value">3</span>
    <span class="stat-card__label">GitHub Actions CI/CD workflows (unit, end-to-end, CSA)</span>
  </div>
</div>

The CANDLE project demonstrated that large-scale hyperparameter optimization on supercomputers could systematically improve cancer drug response models. But it exposed a deeper problem: different research groups, using different model architectures and different training splits of overlapping datasets, were reporting results that could not be directly compared. Was model A better than model B, or was it just trained on more favorable data splits?

IMPROVE — the [Innovative Methods and Metrics for Prediction and Evaluation of Cancer Drug Response](https://github.com/JDACS4C-IMPROVE/IMPROVE) effort within the JDACS4C (Joint Design of Advanced Computing Solutions for Cancer) collaboration — was built to solve that. I led the software engineering side: the `improvelib` Python package, the CI/CD infrastructure, the GitHub Actions workflows, and the [UNO model](https://github.com/JDACS4C-IMPROVE/UNO).

## Background: what cancer drug response datasets look like

To understand why systematic comparison is hard, it helps to know what the data looks like.

A drug response dataset contains rows of the form: (cell line, drug, response). A *cell line* is a tumor cell population grown in a laboratory — the HCT116 colon cancer cell line, for instance, or the MCF7 breast cancer cell line. Each cell line has a distinct genomic profile: its gene expression levels (which genes are turned up or down compared to normal tissue), mutations, copy number variations, and other molecular features measured by high-throughput genomics assays.

A *drug* is characterized by its molecular structure — often encoded as a SMILES string (a text representation of the chemical graph) and converted to numerical fingerprints or graph features. The *response* is measured experimentally: expose the cell line to a range of drug concentrations and fit a dose-response curve. IC50 is the concentration that kills 50% of cells. AUC (area under the dose-response curve) captures the shape of the entire curve and is often more stable than IC50.

The major public datasets — GDSC (Genomics of Drug Sensitivity in Cancer), CCLE (Cancer Cell Line Encyclopedia), CTRPv2 (Cancer Therapeutics Response Portal), NCI60, gCSI — all contain this structure. They share some drugs and some cell lines, but they were collected by different labs using different assay protocols, different growth conditions, and different drug concentrations. The same cell line measured in GDSC and CCLE will not have identical response values, because the experimental conditions differ.

<figure class="article-figure article-figure--wide">
  <img loading="lazy" decoding="async" src="/images/blog/improve-csa-matrix.svg" alt="Cross-Study Analysis matrix: train on one dataset, test on another" />
  <figcaption>The CSA evaluation matrix. Diagonal cells are within-dataset evaluations; off-diagonal cells are the cross-study tests that reveal whether a model generalizes across labs and protocols.</figcaption>
</figure>

## The benchmark comparison problem

Suppose you train a neural network on GDSC data and achieve 0.85 Pearson correlation between predicted and measured AUC on a held-out test set from GDSC. Your colleague trains a different architecture on CCLE data and achieves 0.82. Is your model better?

You cannot tell. The two numbers are not comparable because the datasets have different distributions, different drugs, different noise levels, and different train/test split protocols. To make a fair comparison, both models need to be trained and evaluated under identical conditions: the same data preprocessing, the same train/validation/test splits, and — crucially — the same evaluation held-out data.

*Cross-study analysis* (CSA) makes the comparison even stricter: train a model on dataset A and evaluate it on dataset B. This tests whether the model has learned something generalizable about drug-cell line biology, or whether it has learned to fit the particular characteristics of one dataset — its noise structure, its cell line composition, its concentration range. A model that generalizes across datasets is more likely to capture real biology than one that only works within the dataset it was trained on.

Running CSA systematically — every combination of train-dataset and test-dataset, multiple model architectures, multiple random seeds — requires infrastructure. That infrastructure is what IMPROVE provides.

## improvelib: a shared Python package for the benchmarking community

The [IMPROVE Python package](https://github.com/JDACS4C-IMPROVE/IMPROVE) (`improvelib`) provides the shared building blocks every model in the benchmark uses.

**Standardized data loading.** The package provides loaders for each supported drug response dataset. When you call `improvelib.load_response_data("GDSC2")`, you get the same preprocessed dataframe regardless of which model code is calling it. Normalization, filtering of missing values, and alignment of cell line identifiers are done consistently. Without this, two groups using the same GDSC2 source files can end up with subtly different feature matrices, making their results incomparable even if everything else is identical.

**Consistent train/validation/test splits.** The benchmark defines canonical splits for each dataset — the same rows in train, the same rows in test, every time. Models are not allowed to choose their own splits. This removes one of the most common sources of inflated benchmark performance: selecting a favorable split and reporting results on it.

**Evaluation metrics.** The package computes Pearson correlation, Spearman correlation, RMSE, and MAE against the standardized test set. Everyone uses the same metric implementations, so differences in reported numbers reflect differences in model quality, not differences in how metrics were computed.

**Model interface templates.** Every model that participates in the IMPROVE benchmark must implement three entry points: `preprocess`, `train`, and `infer`. These take standardized arguments and write standardized output files. This interface is what makes cross-model comparison automatic — you can swap models in and out of the CSA evaluation pipeline without modifying the pipeline itself.

## GitHub Actions: CI/CD for scientific software

Scientific software has historically been underserved by software engineering practice. Code is often written to run once on one machine, with no automated tests and no reproducibility guarantees. A major part of my contribution to IMPROVE was applying production software engineering discipline to a research codebase.

**Continuous integration** means running tests automatically on every change to the codebase. If a developer modifies the data loading code and accidentally changes how normalization works, the tests should catch that before the change is merged — not three months later when someone notices that results have shifted.

The [GitHub Actions workflows](https://github.com/JDACS4C-IMPROVE/IMPROVE/actions) I wrote for IMPROVE cover three scenarios:

**Unit tests.** The `IMPROVE UnitTest GitHub Actions` workflow runs the `improvelib` test suite on every pull request. It validates that data loaders return the expected shapes and statistics, that metric computations are correct on known inputs, and that the model interface contract is satisfied. For a benchmark library, correctness of preprocessing and evaluation is the highest-stakes concern — a silent bug in normalization or metric computation invalidates every result produced with that version of the library.

**End-to-end model workflows.** The `Docker GraphDRP LCA workflow` runs a full preprocess-train-infer pipeline on a reference model (GraphDRP, a graph neural network for drug response prediction) inside a Docker container. Docker packaging ensures that the workflow runs identically regardless of the host machine's software environment — every dependency is pinned, the runtime is isolated, and the result is reproducible. If the pipeline produces different output than the reference, something has broken.

**Parsl-based parallel CSA workflows.** The `Docker Parsl GraphDRP CSA workflow` runs the full cross-study analysis: all combinations of train/test datasets for GraphDRP, orchestrated by Parsl for parallel execution. Parsl is a Python-based parallel workflow library developed at Argonne that can execute tasks on laptops, clusters, and supercomputers using the same workflow description. Using Parsl in the CI workflow means the same code that runs the CSA benchmark in GitHub Actions can be scaled up to run on Argonne computing systems without changing the workflow logic.

Setting up CI/CD for scientific software is harder than it sounds. The test artifacts are large datasets. The compute is sometimes only available on specific HPC configurations. Getting workflows that involve real model training to run reliably in GitHub Actions — which provides standard Linux containers with no access to Argonne compute — required careful decisions about what to validate in CI versus what to validate on dedicated hardware.

## The UNO model

[UNO](https://github.com/JDACS4C-IMPROVE/UNO) (Unified Neural Optimizer) is the cancer drug response model I led within the IMPROVE framework. UNO takes the two-branch architecture approach: drug features and cell-line features are embedded through separate fully connected neural networks, then the two embeddings are concatenated and passed through a third network that predicts drug response (AUC).

The two-branch design reflects a scientific choice, not just an architectural one. Drugs and cell lines are fundamentally different kinds of objects — one is a chemical structure, the other is a biological system. Learning separate representations before combining them gives the model a chance to capture the structure of each space independently before modeling the interaction. In practice this also enables better transfer: a drug embedding learned on GDSC may generalize to CCLE because drug molecular features are physical properties that do not change across labs.

UNO is packaged as an IMPROVE model: it implements the preprocess/train/infer interface, consumes standardized CSA benchmark data from `improvelib`, and writes standardized evaluation output. This packaging is what makes UNO comparable to other models in the benchmark — not just a model that achieves good numbers, but a model that participates in a shared, reproducible evaluation.

## From CANDLE to IMPROVE: what the shift meant

CANDLE and IMPROVE share the same scientific goal — better cancer drug response models — but the emphasis changed.

CANDLE was about *scale*: run more HPO experiments than anyone had run before, on the largest machines available, to find model configurations that worked. The Supervisor workflow was built for throughput — thousands of concurrent training jobs across Summit, Theta, and Cori. The science it enabled was primarily about what systematic HPO at scale could achieve.

IMPROVE is about *rigor*: make the comparisons meaningful. It matters less how many experiments were run than whether the conclusions from those experiments generalize — across datasets, across labs, across model architectures. The CSA benchmark and `improvelib` are infrastructure for producing claims that hold up under scrutiny.

That shift from scale to rigor reflects where the field had to go. Early cancer AI benchmarking showed that larger models with more compute performed better on within-dataset splits. IMPROVE was built to ask whether those improvements were real — whether a model that won on GDSC would win on CCLE, or whether the leaderboard was measuring overfitting to dataset-specific artifacts as much as biological signal.

The benchmark analysis contributed to ["Benchmarking community drug response prediction models"](https://academic.oup.com/bib/article/27/1/bbaf667/7002013) (Partin, Jain et al., *Briefings in Bioinformatics*, 2025) — the published cross-study analysis of what systematic evaluation reveals about where the field actually stands.

---

*Repository: [JDACS4C-IMPROVE/IMPROVE](https://github.com/JDACS4C-IMPROVE/IMPROVE)*

*UNO model: [JDACS4C-IMPROVE/UNO](https://github.com/JDACS4C-IMPROVE/UNO)*

*Paper: Partin, A., ..., Jain, R., et al. ["Benchmarking community drug response prediction models."](https://academic.oup.com/bib/article/27/1/bbaf667/7002013) Briefings in Bioinformatics, 2025.*
