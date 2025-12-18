---
layout: single
title: "Rajeev Jain"
permalink: /
author_profile: false
classes: wide
excerpt: "Engineer with 16+ years building scientific software across climate, data science, and HPC."
---

<div class="page-intro content-section" id="about" style="--delay: 0s;">
  <div class="intro-grid">
    <div class="intro-media">
      <img class="intro-photo" src="/images/profile.png" alt="Rajeev Jain">
    </div>
    <div class="intro-copy">
      <p class="lead">Research software engineer with 16+ years in scientific software.</p>
      <p>Currently: Principal Specialist, Research Software Engineering at Argonne National Laboratory. Work spans climate, cancer data science, multiphysics simulation, urban systems, and nuclear engineering.</p>
      <p><strong>Focus areas:</strong> parallel I/O, profiling/optimization, reproducibility, and scalable pipelines.</p>
      <p>I am an engineer who likes to solve problems. Outside of work, I play rapid chess, pickleball, and cricket, and I like a board of Catan and biking.</p>
      <p class="compact-links"><a href="mailto:rajeeja@gmail.com">Email</a>  &middot;  <a href="https://github.com/rajeeja">GitHub</a>  &middot;  <a href="https://www.linkedin.com/in/rajeeja/">LinkedIn</a>  &middot;  <a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en">Scholar</a></p>
      <div class="hero-actions">
        <a class="btn btn--primary" href="/files/Rajeev_Jain_Resume.pdf">Resume (PDF)</a>
        <a class="btn btn--ghost" href="#contact">Contact</a>
      </div>
    </div>
  </div>
</div>

<section class="content-section" id="impact" style="--delay: 0.05s;">
  <h2>Selected Impact</h2>
  <div class="case-studies">
    <article class="case-study">
      <h3>UXarray: conservative zonal averaging for unstructured grids</h3>
      <p><strong>Problem:</strong> Unstructured climate grids needed accurate, conservative zonal averages that preserve integrals and scale in Python.</p>
      <p><strong>Approach:</strong> Implemented conservative zonal averaging in UXarray using Gauss-Legendre quadrature, with validation tests and monthly PyPI releases.</p>
      <p><strong>Outcome:</strong> A scalable, accurate method for unstructured grid analysis in a pip-installable package.</p>
      <p class="case-links"><a href="https://eesm.science.energy.gov/presentations/uxarray-python-package-analysis-and-visualization-model-output-unstructured-climate">Paper</a>  &middot;  <a href="https://github.com/UXARRAY/uxarray/pull/1345">PR #1345</a></p>
    </article>
    <article class="case-study">
      <h3>FLASH-X: asynchronous I/O and compression</h3>
      <p><strong>Problem:</strong> Checkpoint I/O and restart overhead dominated runtime in large multiphysics simulations.</p>
      <p><strong>Approach:</strong> Added async HDF5 I/O with SZ3/ZFP compression and a verification workflow with nightly baselines.</p>
      <p><strong>Outcome:</strong> Reduced I/O time in benchmarks (20%+ gains) and improved restart reliability.</p>
      <p class="case-links"><a href="https://arxiv.org/abs/2208.11630">Paper 1</a>  &middot;  <a href="https://ieeexplore.ieee.org/document/10026923">Paper 2</a></p>
    </article>
    <article class="case-study">
      <h3>Urban Exascale: boundary conditions for urban microclimate</h3>
      <p><strong>Problem:</strong> City-scale building energy models needed realistic urban microclimate boundary conditions.</p>
      <p><strong>Approach:</strong> Coupled urban weather boundary conditions into a city-scale workflow and ran multi-domain simulations.</p>
      <p><strong>Outcome:</strong> Improved urban boundary conditions for building energy modeling and published results.</p>
      <p class="case-links"><a href="https://eta-publications.lbl.gov/sites/default/files/17_-_urban_weather_boundary_conditions_-_tianzhen_hong.pdf">Paper</a></p>
    </article>
  </div>
  <p class="skill-note"><strong>Core skills:</strong> Python, C++, Fortran; MPI, OpenMP, HDF5; PyTorch, Keras, NumPy, pandas; Git and CI/CD.</p>
</section>

<section class="content-section" id="experience" style="--delay: 0.1s;">
  <h2>Experience Snapshot</h2>
  <ul class="timeline">
    <li><strong>Argonne National Laboratory</strong> - Principal Specialist, Research Software Engineering (2009-present). Work across UXarray, FLASH-X, CANDLE/IMPROVE, MeshKit/RGG, and urban simulation; ran large-scale HPO workflows for CANDLE/IMPROVE; runs span exascale-class systems including the Aurora Accessory system.</li>
    <li><strong>The University of Chicago</strong> - CASE Staff At-Large (2023-present). Joint appointment supporting computational cancer research.</li>
    <li><strong>Arizona State University</strong> - Research and Teaching Assistant (2007-2009).</li>
    <li><strong>Wipro Technologies</strong> - Project Engineer (2006-2007).</li>
  </ul>
</section>

<section class="content-section" id="publications" style="--delay: 0.2s;">
  <h2>Selected Publications and Awards</h2>
  <ul class="pub-list">
    <li><strong>Awards:</strong> R&amp;D 100 Awards (FLASH-X 2022, CANDLE/Supervisor 2023); Best Paper (International Meshing Roundtable 2010); ASU University Graduate Fellowship (2007-2009).</li>
    <li><strong>UXarray:</strong> UXarray: Python package for analysis and visualization of unstructured climate grids. <a href="https://eesm.science.energy.gov/presentations/uxarray-python-package-analysis-and-visualization-model-output-unstructured-climate">Link</a></li>
    <li><strong>FLASH-X:</strong> Data reduction and verification for multiphysics simulations. <a href="https://arxiv.org/abs/2208.11630">Paper 1</a>  &middot;  <a href="https://ieeexplore.ieee.org/document/10026923">Paper 2</a></li>
    <li><strong>CANDLE:</strong> Workflow tooling and counterfactual analysis for cancer data. <a href="https://pubmed.ncbi.nlm.nih.gov/30577736/">Paper 1</a>  &middot;  <a href="https://web.cels.anl.gov/~woz/papers/Counterfactuals_2021.pdf">Paper 2</a></li>
    <li><strong>Urban microclimate:</strong> Boundary conditions for urban weather simulations. <a href="https://eta-publications.lbl.gov/sites/default/files/17_-_urban_weather_boundary_conditions_-_tianzhen_hong.pdf">Paper</a></li>
    <li><strong>MeshKit:</strong> Reactor core mesh generation. <a href="https://doi.org/10.1007/s00366-011-0221-4">DOI</a></li>
  </ul>
  <p class="more-links"><a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en">Full publications list</a></p>
</section>

<section class="content-section" id="talks" style="--delay: 0.25s;">
  <h2>Selected Talks</h2>
  <ul class="talk-list">
    <li><a href="https://www.youtube.com/watch?v=qwqJeOO8m6A&amp;t=545s">UXarray for unstructured climate data (SciPy 2023)</a></li>
    <li><a href="https://www.youtube.com/watch?v=MuifQ7lHRR8&amp;t=176s">Data reduction for FLASH-X simulations (HDF5 User Group 2023)</a></li>
  </ul>
</section>

<section class="content-section" id="resume" style="--delay: 0.3s;">
  <h2>Resume and CV</h2>
  <p>Short resume and full CV (PDF).</p>
  <p>
    <a class="btn btn--primary" href="/files/Rajeev_Jain_Resume.pdf">Resume (PDF)</a>
    <a class="btn btn--ghost" href="/files/Rajeev_Jain_CV.pdf">Full CV (PDF)</a>
  </p>
</section>

<section class="content-section" id="contact" style="--delay: 0.35s;">
  <h2>Contact</h2>
  <p><a href="mailto:rajeeja@gmail.com">rajeeja@gmail.com</a></p>
</section>
