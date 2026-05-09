---
title: "Probing Cancer Model Decision Boundaries: Counterfactual Analysis and Large-Scale HPO on Supercomputers"
date: 2026-05-09
permalink: /blog/candle-counterfactuals-hpo/
categories:
  - blog
tags:
  - machine-learning
  - hpc
  - cancer-research
  - candle
  - hyperparameter-optimization
  - scientific-computing
excerpt: "How CANDLE/Supervisor ran tens of thousands of HPO experiments on Summit and Theta — and what noise injection and counterfactual analysis revealed about where cancer drug response models break down."
author_profile: false
toc: true
toc_sticky: true
---

<div class="article-banner">
  <p class="eyebrow">Research retrospective &middot; May 2026</p>
  <h1 class="article-title">Probing Cancer Model Decision Boundaries: Counterfactual Analysis and Large-Scale HPO on Supercomputers</h1>
  <p class="article-dek">How CANDLE/Supervisor ran tens of thousands of HPO experiments on Summit and Theta — and what noise injection and counterfactual analysis revealed about where cancer drug response models break down.</p>
</div>

The CANDLE project (Cancer Distributed Learning Environment) was a DOE Exascale Computing Project effort to apply large-scale ML infrastructure to cancer drug response prediction. I was a core contributor from 2017 through 2023, working on the CANDLE/Supervisor workflow infrastructure and later on the cross-study analysis methodology that became the IMPROVE benchmark program.

This post covers two interconnected ideas: how we ran hyperparameter optimization at supercomputer scale using Supervisor, and what we learned when we probed cancer models with noise injection and counterfactual analysis to understand where they break down.

## The problem: predicting which drug will work for which cancer

Cancer drug response prediction is a supervised learning problem. You have a set of cell lines — tumor cells grown in a lab dish, each representing a particular cancer type with its own genetic profile — and a set of drugs. For each (cell line, drug) pair in your training dataset, you have a measured response: typically IC50 (the drug concentration that inhibits 50% of cell growth) or AUC (area under the dose-response curve, where higher values mean less sensitivity to the drug).

The model learns from this data: given the genomic features of a cell line (gene expression levels, mutation status, copy number variations) and the molecular features of a drug (chemical structure encoded as SMILES fingerprints, or physical-chemical properties), predict what the response will be for combinations the model has not seen.

If this works reliably, it has direct clinical relevance: given a patient's tumor genomic profile, rank the candidate drugs by predicted response and prioritize the most promising ones for treatment or clinical trial enrollment.

The challenge is that "works reliably" is harder to achieve than standard benchmark metrics suggest. Models can appear to perform well on held-out test data from the same dataset they were trained on, while failing badly when evaluated on data from a different lab with a different measurement protocol. And even within a dataset, models can be fragile near their decision boundaries in ways that aggregate accuracy metrics do not reveal.

## What hyperparameter optimization is

A machine learning model has two kinds of parameters. The *model weights* — the numbers learned during training that define what the model does — are optimized automatically by gradient descent. But before training starts, you must specify *hyperparameters*: the learning rate, the number and size of layers in the network, the type of activation function, the regularization strength, the optimizer, the batch size, and many others.

Hyperparameters cannot be learned by gradient descent because they control the training process itself. Choosing them poorly makes the difference between a model that converges to a good solution and one that diverges or underfits. The standard approaches are:

- **Grid search**: try every combination of a pre-specified set of values. Fine for 2–3 hyperparameters; explodes combinatorially with more.
- **Random search**: sample configurations randomly from a search space. Surprisingly competitive in practice because only a few hyperparameters tend to matter most.
- **Bayesian optimization**: build a probabilistic model (a *surrogate* — often a Gaussian process or random forest) of how performance varies as a function of hyperparameters, then use that model to choose the next configuration to evaluate. Sample-efficient because it uses information from all previous evaluations to guide the search.
- **Evolutionary/genetic algorithms**: maintain a population of configurations, evaluate them, and evolve better ones through mutation and crossover — mimicking natural selection on the hyperparameter space.

The right choice depends on the evaluation budget (how many configurations you can afford to train), the dimension of the search space, and whether the objective function is noisy.

## CANDLE/Supervisor: HPO as a workflow problem

The research question CANDLE set out to answer was: given access to DOE supercomputers with thousands of GPUs, can systematic HPO produce cancer drug response models that outperform what research groups achieve on their own? And can it do so at a scale and rigor that enables meaningful cross-model and cross-study comparison?

Running 10,000+ model training experiments is not primarily a modeling problem — it is a workflow problem. Each training run needs the right data, the right hyperparameter configuration, the right compute allocation, and a reliable way to log results so they can be compared across runs, datasets, and architectures. CANDLE/Supervisor, described in ["CANDLE/Supervisor: A workflow framework for machine learning applied to cancer research"](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2508-4) (Wozniak, Jain et al., *BMC Bioinformatics*, 2018), was built to solve that.

**Swift/T** is the parallel workflow runtime Supervisor was built on. It is a dataflow language: you describe what computations need to happen and what data they depend on, and Swift/T executes them in parallel whenever their dependencies are satisfied. This made it natural to express HPO as a workflow — the HPO algorithm proposes a batch of configurations, Swift/T launches all those training runs simultaneously across GPU nodes on Summit or Theta, collects the results when they finish, and feeds them back to the algorithm to propose the next batch.

Supervisor supported three main HPO algorithms:

**mlrMBO** is a Bayesian optimization framework implemented in R. It builds a surrogate model (typically a Gaussian process) that approximates the relationship between hyperparameter settings and validation performance across all evaluations so far. It then uses an *acquisition function* (like expected improvement) to pick the next configuration to try — balancing exploration of untested regions against exploitation of regions that have already shown promise. mlrMBO is sample-efficient but requires fitting and querying the GP model at each iteration, which adds overhead as the number of evaluations grows.

**DEAP** (Distributed Evolutionary Algorithms in Python) provides genetic algorithm and evolutionary strategy implementations. The GA approach maintains a *population* of hyperparameter configurations, evaluates them in parallel, then selects the best performers and generates the next generation through mutation (randomly changing one or more values) and crossover (combining values from two parent configurations). Genetic algorithms are less sample-efficient than Bayesian methods but naturally parallel — an entire generation evaluates simultaneously — and robust to noisy objectives.

**Random search** served as a baseline. It has no memory of past evaluations and proposes configurations uniformly at random. For high-dimensional spaces where few hyperparameters matter, random search is competitive with more sophisticated methods because the sophisticated methods waste sample budget on irrelevant dimensions.

On Summit (IBM AC922 nodes, 6 V100 GPUs per node, 4,608 nodes total), a well-structured Supervisor run could launch thousands of concurrent training jobs, with the HPO algorithm running on a head node and Swift/T managing the parallel execution. A 500-iteration mlrMBO run with 20 configurations per iteration is 10,000 training jobs — feasible as a single multi-day allocation on a leadership-class machine.

## Probing decision boundaries: why aggregate accuracy is not enough

The counterfactuals paper — "Probing Decision Boundaries in Cancer Data Using Noise Injection and Counterfactual Analysis" (Jain et al., CAFCW at SC21, 2021) — came from a question that aggregate metrics do not answer: *how confident should you be in a specific prediction?*

A model that achieves 0.85 Pearson correlation between predicted and measured drug response across a held-out test set sounds good. But within that test set, some predictions are near the model's decision boundary — the surface in input space where the model changes its output from "sensitive" to "resistant" — and some are far from it. A prediction near the boundary is not the same as a prediction far from it, even if both happen to be correct on the test label.

Two techniques let us probe where those boundaries are.

**Noise injection** adds controlled random perturbations to the input features and measures how the model's prediction changes. If you take a cell line's gene expression profile and add small Gaussian noise to each value — noise within the range of typical measurement uncertainty — does the model's prediction stay stable? For a robust model, small perturbations produce small changes in the output. For a fragile model, small perturbations near the decision boundary flip the prediction entirely.

The practical significance: if a model predicts that Drug A will work for Tumor X, but a 5% perturbation to the gene expression values flips that prediction, the model is not providing a reliable clinical signal. It has learned a decision boundary that passes very close to the query point, and that boundary may not reflect true biology — it may reflect the way the training data was sampled or normalized.

**Counterfactual analysis** is the inverse problem. Instead of asking "what happens when I perturb this input randomly?", you ask: "what is the *smallest change* to this input that would flip the model's prediction?" This is a constrained optimization problem — find the point in input space nearest to the original that the model classifies differently.

Counterfactuals expose what the model has actually learned to distinguish. If the counterfactual for a cell line is found by changing the expression of three specific genes, those three genes are load-bearing for the model's prediction on that sample. Whether those genes are biologically meaningful — known to be relevant to drug response — or are statistical artifacts of the training data is the scientific question.

The findings from this work were practically significant. Models trained on drug response data could sometimes be moved across their decision boundaries with perturbations well within the measurement uncertainty of the underlying assay. Aggregate test-set metrics looked comparable across architectures; the noise injection analysis revealed which models were stable at the individual-sample level and which were not. This kind of per-sample robustness analysis is not standard in the field, but it is exactly what would matter for clinical deployment.

## What this enables

Running HPO at supercomputer scale, combined with principled analysis of model robustness, answers questions that neither approach can answer alone. HPO at scale finds model configurations that perform well in aggregate. Noise injection and counterfactual analysis reveal whether those configurations are actually trustworthy — or whether they are achieving good test-set metrics while making fragile predictions near the decision boundary.

For cancer drug response prediction to be clinically useful, both matter. A model that achieves high Pearson correlation on a benchmark dataset but flips predictions under measurement-level noise is not ready for clinical decision support. Understanding where models break down — and why — is as important as finding models that perform well on the metrics we currently measure.

---

*Paper: Wozniak, J. M., Jain, R., et al. ["CANDLE/Supervisor: A workflow framework for machine learning applied to cancer research."](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2508-4) BMC Bioinformatics, 2018.*

*Paper: Jain, R., et al. "Probing Decision Boundaries in Cancer Data Using Noise Injection and Counterfactual Analysis." CAFCW at SC21, 2021.*
