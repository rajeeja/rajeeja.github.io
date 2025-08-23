---
layout: archive
title: "Projects"
permalink: /projects/
author_profile: true
redirect_from:
  - /projects
  - /current_projects
  - /current-projects
---

{% include base_path %}

After 2016, I started working on the three Exascale Compute Projects [ECP](https://www.exascaleproject.org/), two of which were R&D100 award winners: [CANDLE](https://candle.cels.anl.gov/), and [FLASH-X](https://flash-x.org/). The other exascale project was seed-funded, lasting for 2 years (2016-2018) [Urban ECP](https://www.anl.gov/exascale/multiscale-coupled-urban-systems). Prior to that, my work at Argonne revolved around managing different facets of the [NEAMS](https://www.anl.gov/article/using-supercomputers-to-explore-nuclear-energy) project under team [SIGMA/MeshKit/RGG](https://sigma.mcs.anl.gov/).

### IMPROVE/CANDLE (Cancer Data Science)
- Problem: Scaling deep learning workflows across DOE supercomputers for drug response prediction.
- My Approach: Led development of CANDLE/Supervisor workflow framework; standardized HPO/experiments; CI and reproducible runs across systems.
- Impact: Recognized with R&D 100 Award (2023); widely cited; enabled robust model comparisons.
- Key Publications:
  - [Probing decision boundaries in cancer data using noise injection and counterfactual analysis (SC'21 Workshop)](https://web.cels.anl.gov/~woz/papers/Counterfactuals_2021.pdf)
  - [CANDLE/Supervisor: A workflow framework for ML applied to cancer research (BMC Bioinformatics, 2018)](https://link.springer.com/article/10.1186/s12859-018-2508-4)

### UXARRAY (Climate Computation/Modeling)
- Problem: Efficiently analyze and visualize climate model output on unstructured grids.
- My Approach: Co-created UXarray (Python); designed APIs for mesh/topology, vectorized core routines, and parallelized heavy operations.
- Impact: 60× speed-ups on key workloads; adopted by DOE climate community; presented at SciPy/AMS/EGU.
- Key Presentations:
  - [UXarray: Python package for analysis and visualization on unstructured climate grids (EESM PI Meeting, 2024)](https://climatemodeling.science.energy.gov/presentations/uxarray-python-package-analysis-and-visualization-model-output-unstructured-climate)
  - [Extending Xarray with support for unstructured grids (AMS 2024)](https://ams.confex.com/ams/104ANNUAL/meetingapp.cgi/Paper/434638)

### FLASH-X (Multiphysics Simulation, Astrophysics)
- Problem: I/O bottlenecks and verification complexity in exascale multiphysics simulations.
- My Approach: Implemented async HDF5 I/O and compression (SZ3/ZFP); designed Jenkins-based nightly test framework with baselines.
- Impact: >20% performance improvements on I/O-bound workloads; R&D 100 award (2022); improved developer velocity.
- Key Publications:
  - [Framework and Methodology for Verification of Flash-X (2023)](https://ieeexplore.ieee.org/abstract/document/10487352)
  - [Accelerating Flash-X simulations with asynchronous I/O (2022)](https://ieeexplore.ieee.org/abstract/document/10026923)

### Urban ECP (Coupled Urban Simulations)
- Problem: Couple urban microclimate with building energy models for city-scale analysis.
- My Approach: Developed coupling and data pipelines; integrated high-fidelity weather with EnergyPlus-style models.
- Impact: Published methodology for urban boundary conditions in downtown Chicago; cross-institution collaboration.
- Publication: [Representation and evolution of urban weather boundary conditions (2020)](https://www.tandfonline.com/doi/abs/10.1080/19401493.2018.1534275)

### NEAMS SIGMA/MeshKit/RGG (Nuclear Reactor Simulations)
- Problem: Rapidly generate high-quality reactor core meshes for coupled physics at scale.
- My Approach: Led MeshKit/DAG and RGG tool development; advised Kitware on SBIR commercialization.
- Impact: Reduced core model generation from weeks to hours; enabled complex coupled simulations.
- Publications:
  - [Scalable Mesh Generation for HPC Applications (SC15 Poster)](https://sc15.supercomputing.org/sites/all/themes/SC15images/tech_poster/poster_files/post319s2-file3.pdf)
  - [Generating unstructured nuclear reactor core meshes in parallel (2014)](https://www.sciencedirect.com/science/article/pii/S1877705814016750)
