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

I work across DOE/ANL projects turning complex scientific problems into fast, reliable software. Below are concise case studies with the problem, my approach, and impact. For more details or demos, email me.

### UXARRAY (Climate Computation/Modeling)
- Problem: Analyze and visualize unstructured climate grids without bespoke scripts.
- My approach: Co-created UXarray; API design for mesh/topology; vectorized cores; parallelized heavy paths.
- Impact: Up to 60× faster on key workloads; adopted by DOE climate users; featured at SciPy/AMS/EGU.
- Key Presentations:
  - [UXarray: Python package for analysis and visualization on unstructured climate grids (EESM PI Meeting, 2024)](https://climatemodeling.science.energy.gov/presentations/uxarray-python-package-analysis-and-visualization-model-output-unstructured-climate)
  - [Extending Xarray with support for unstructured grids (AMS 2024)](https://ams.confex.com/ams/104ANNUAL/meetingapp.cgi/Paper/434638)

### IMPROVE/CANDLE (Cancer Data Science)
- Problem: Scale deep learning workflows for drug response prediction across DOE supercomputers.
- My approach: Led CANDLE/Supervisor; standardized experiments/HPO; added CI for reproducible multi-system runs.
- Impact: R&D 100 Award (2023); widely cited; enabled fair, apples-to-apples model comparison.
- Key Publications:
  - [Probing decision boundaries in cancer data using noise injection and counterfactual analysis (SC'21 Workshop)](https://web.cels.anl.gov/~woz/papers/Counterfactuals_2021.pdf)
  - [CANDLE/Supervisor: A workflow framework for ML applied to cancer research (BMC Bioinformatics, 2018)](https://link.springer.com/article/10.1186/s12859-018-2508-4)

### FLASH-X (Multiphysics Simulation, Astrophysics)
- Problem: I/O bottlenecks and verification complexity in exascale multiphysics simulations.
- My approach: Implemented async HDF5 I/O + SZ3/ZFP compression; built Jenkins nightly testing with baselines.
- Impact: >20% speedup on I/O-bound runs; R&D 100 (2022); faster iteration for developers.
- Key Publications:
  - [Framework and Methodology for Verification of Flash-X (2023)](https://ieeexplore.ieee.org/abstract/document/10487352)
  - [Accelerating Flash-X simulations with asynchronous I/O (2022)](https://ieeexplore.ieee.org/abstract/document/10026923)

### Urban ECP (Coupled Urban Simulations)
- Problem: Couple urban microclimate with building energy models for city-scale insight.
- My approach: Built coupling + data pipelines; integrated high-fidelity weather with EnergyPlus-style models.
- Impact: Published downtown Chicago boundary-condition methodology; multi-institution collaboration.
- Publication: [Representation and evolution of urban weather boundary conditions (2020)](https://www.tandfonline.com/doi/abs/10.1080/19401493.2018.1534275)

### NEAMS SIGMA/MeshKit/RGG (Nuclear Reactor Simulations)
- Problem: Generate high-quality reactor core meshes fast enough for coupled physics at scale.
- My approach: Led MeshKit/DAG and RGG tools; advised Kitware through SBIR commercialization.
- Impact: Reduced core-modeling time from weeks to hours; enabled complex coupled simulations.
- Publications:
  - [Scalable Mesh Generation for HPC Applications (SC15 Poster)](https://sc15.supercomputing.org/sites/all/themes/SC15images/tech_poster/poster_files/post319s2-file3.pdf)
  - [Generating unstructured nuclear reactor core meshes in parallel (2014)](https://www.sciencedirect.com/science/article/pii/S1877705814016750)