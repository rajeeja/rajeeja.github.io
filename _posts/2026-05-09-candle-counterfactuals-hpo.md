---
title: "CANDLE/Supervisor: Running Cancer AI Research at Scale on DOE Supercomputers"
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
  <p class="eyebrow">Cancer AI infrastructure &middot; 2024</p>
  <h1 class="article-title">CANDLE/Supervisor: Running Cancer AI Research at Scale on DOE Supercomputers</h1>
  <p class="article-dek">How CANDLE/Supervisor orchestrated tens of thousands of HPO experiments across Summit, Theta, and Cori — and what noise injection and counterfactual analysis revealed about cancer model trust.</p>
</div>

<div class="post-tags">
  <span class="post-tag post-tag--blue">machine learning</span>
  <span class="post-tag post-tag--violet">hyperparameter optimization</span>
  <span class="post-tag post-tag--red">cancer research</span>
  <span class="post-tag post-tag--amber">HPC</span>
  <span class="post-tag post-tag--teal">Swift/T</span>
</div>

<div class="stat-row">
  <div class="stat-card">
    <span class="stat-card__value">10,000+</span>
    <span class="stat-card__label">training experiments across Summit, Theta, and Cori</span>
  </div>
  <div class="stat-card stat-card--amber">
    <span class="stat-card__value">3</span>
    <span class="stat-card__label">HPO algorithms: mlrMBO, DEAP, Hyperopt/TPE</span>
  </div>
  <div class="stat-card stat-card--violet">
    <span class="stat-card__value">PLOD2</span>
    <span class="stat-card__label">top gene identified by counterfactual analysis</span>
  </div>
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

<figure class="article-figure article-figure--wide">
  <img src="/images/blog/candle-hpo-pipeline.svg" alt="CANDLE/Supervisor HPO pipeline: algorithm → Swift/T runtime → analysis" />
  <figcaption>The CANDLE/Supervisor HPO loop. The algorithm proposes configurations; Swift/T launches them in parallel across thousands of GPUs; metrics flow back to update the surrogate model for the next batch.</figcaption>
</figure>

## CANDLE/Supervisor: HPO as a workflow problem

The research question CANDLE set out to answer was: given access to DOE supercomputers with thousands of GPUs, can systematic HPO produce cancer drug response models that outperform what research groups achieve on their own? And can it do so at a scale and rigor that enables meaningful cross-model and cross-study comparison?

Running 10,000+ model training experiments is not primarily a modeling problem — it is a workflow problem. Each training run needs the right data, the right hyperparameter configuration, the right compute allocation, and a reliable way to log results so they can be compared across runs, datasets, and architectures. CANDLE/Supervisor, described in ["CANDLE/Supervisor: A workflow framework for machine learning applied to cancer research"](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2508-4) (Wozniak, Jain et al., *BMC Bioinformatics*, 2018), was built to solve that.

**Swift/T** is the parallel workflow runtime Supervisor was built on. It is a dataflow language: you describe what computations need to happen and what data they depend on, and Swift/T executes them in parallel whenever their dependencies are satisfied. This made it natural to express HPO as a workflow — the HPO algorithm proposes a batch of configurations, Swift/T launches all those training runs simultaneously across GPU nodes on Summit or Theta, collects the results when they finish, and feeds them back to the algorithm to propose the next batch.

Supervisor supported three main HPO algorithms:

**mlrMBO** is a Bayesian optimization framework implemented in R. It builds a surrogate model (typically a Gaussian process) that approximates the relationship between hyperparameter settings and validation performance across all evaluations so far. It then uses an *acquisition function* (like expected improvement) to pick the next configuration to try — balancing exploration of untested regions against exploitation of regions that have already shown promise. mlrMBO is sample-efficient but requires fitting and querying the GP model at each iteration, which adds overhead as the number of evaluations grows.

**DEAP** (Distributed Evolutionary Algorithms in Python) provides genetic algorithm and evolutionary strategy implementations. The GA approach maintains a *population* of hyperparameter configurations, evaluates them in parallel, then selects the best performers and generates the next generation through mutation (randomly changing one or more values) and crossover (combining values from two parent configurations). Genetic algorithms are less sample-efficient than Bayesian methods but naturally parallel — an entire generation evaluates simultaneously — and robust to noisy objectives.

**Hyperopt** provided Tree-of-Parzen-Estimators (TPE)-based optimization — a Bayesian method that builds separate density models for promising and poor configurations and proposes new configurations from their ratio. It is effective when only a small number of hyperparameters dominate performance.

**Random search** served as a baseline. It has no memory of past evaluations and proposes configurations uniformly at random. For high-dimensional spaces where few hyperparameters matter, random search is competitive with more sophisticated methods because the sophisticated methods waste sample budget on irrelevant dimensions.

On Summit (IBM AC922 nodes, 6 V100 GPUs per node, 4,608 nodes total), a well-structured Supervisor run could launch thousands of concurrent training jobs, with the HPO algorithm running on a head node and Swift/T managing the parallel execution. A 500-iteration mlrMBO run with 20 configurations per iteration is 10,000 training jobs — feasible as a single multi-day allocation on a leadership-class machine.

## Probing decision boundaries: the NT3 benchmark

The counterfactuals paper — "Probing Decision Boundaries in Cancer Data Using Noise Injection and Counterfactual Analysis" ([Jain, Shah, Mohd-Yusof, Wozniak, Brettin, Xia, Stevens, CAFCW at SC21, 2021](https://sc21.supercomputing.org/proceedings/workshops/workshop_pages/ws_cafcw125.html)) — used the CANDLE **NT3 benchmark** as its test case. NT3 is a classification problem: given RNA expression data from a tissue sample, predict whether it is normal or tumor tissue. The input is a high-dimensional gene expression vector; the output is a binary label.

This is a deliberately clean setup. Unlike drug response regression, where the output is continuous and the ground truth is noisy, NT3 has clear ground truth labels. That makes it ideal for studying what happens when you *corrupt* the data — injecting noise — and measuring how the model degrades.

### Label noise and feature noise

The paper tested two kinds of corruption:

**Label noise**: flip a fraction of the training labels — mark some tumor samples as normal and vice versa. This simulates mislabeled training data, which happens in real clinical datasets due to biopsy error, pathology disagreement, or sample handling mistakes. As the fraction of flipped labels increases, the model gets trained on contradictory signal.

**Feature noise**: add random perturbations to gene expression values. This simulates measurement noise in RNA-seq assays, batch effects between sequencing runs, or biological variability between samples from the same tissue type.

The baseline NT3 model is a deep neural network trained by standard supervised learning. Under heavy label noise, its validation accuracy degrades substantially — it cannot tell which labels to trust, so it fits the corrupted training signal.

### The abstaining classifier

The key comparison in the paper is against an **abstaining classifier** — a model variant that learns not just to predict a label, but to predict *when the input is too uncertain to classify reliably*. Instead of forcing a binary output on every sample, the abstaining classifier can output "I don't know" when the evidence is ambiguous.

At high noise levels, the abstaining classifier significantly outperforms the standard model on the samples it does classify — because it has learned to withhold predictions on the corrupted or ambiguous cases rather than making overconfident wrong ones. For clinical applications, this matters: a model that says "I'm uncertain, refer for additional testing" is more useful than one that confidently gives the wrong answer.

### Counterfactual analysis as a tool for gene discovery

The second contribution of the paper uses counterfactual examples as an **explainability tool** — not just to probe model robustness but to identify which genes the model is actually using to distinguish normal from tumor tissue.

A counterfactual for a given sample is the smallest change to that sample's gene expression vector that would flip the model's prediction. To find it, you solve a constrained optimization problem: minimize the distance from the original point while crossing the decision boundary. The genes that change most in the counterfactual are the ones the model is most sensitive to — the features that are "load-bearing" for that classification.

We computed counterfactual perturbation vectors for a set of samples and clustered them to find genes that consistently appear in the perturbation direction. The top gene the analysis identified was **PLOD2** (Procollagen-Lysine, 2-Oxoglutarate 5-Dioxygenase 2), which has been described in the literature as associated with cancer cell migration and metastasis. Other genes the analysis flagged — **LRTM1**, **RGS5**, **TP53I13**, **MAN1B1**, **TRRAP** — have documented connections to urothelial, lung, renal, bladder, ovarian, and bone cancers.

The significance: the model learned to distinguish normal from tumor tissue using signal in these genes, and the counterfactual analysis surfaced that signal in an interpretable form. Rather than just knowing the model achieves 90% accuracy, you now know *which biological features* it is using — and whether those features make biological sense.

A further experiment confirmed the specificity of this result: injecting noise specifically into the genes identified by counterfactual analysis caused steeper accuracy degradation than injecting the same amount of noise into randomly selected genes. The model is genuinely more sensitive near the counterfactual direction, confirming that those genes are load-bearing features rather than artifacts of the analysis method.

### Why aggregate accuracy is not enough

The broader point the paper makes is that aggregate test-set accuracy is an incomplete description of a model. Two models can achieve identical accuracy while having very different decision boundaries — one might be stable and biologically grounded, the other fragile and fitting statistical artifacts. Noise injection and counterfactual analysis provide tools to probe that difference. For cancer AI to be clinically useful, understanding where and why models are uncertain is as important as knowing their aggregate performance.

## What this enables

Running HPO at supercomputer scale, combined with principled analysis of model robustness, answers questions that neither approach can answer alone. HPO at scale finds model configurations that perform well in aggregate. Noise injection and counterfactual analysis reveal whether those configurations are actually trustworthy — or whether they are achieving good test-set metrics while making fragile predictions near the decision boundary.

For cancer drug response prediction to be clinically useful, both matter. A model that achieves high Pearson correlation on a benchmark dataset but flips predictions under measurement-level noise is not ready for clinical decision support. Understanding where models break down — and why — is as important as finding models that perform well on the metrics we currently measure.

---

*Paper: Wozniak, J. M., Jain, R., et al. ["CANDLE/Supervisor: A workflow framework for machine learning applied to cancer research."](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2508-4) BMC Bioinformatics, 2018.*

*Paper: Jain, R., et al. "Probing Decision Boundaries in Cancer Data Using Noise Injection and Counterfactual Analysis." CAFCW at SC21, 2021.*
