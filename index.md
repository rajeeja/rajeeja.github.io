---
layout: single
title: "Rajeev Jain"
permalink: /
author_profile: false
classes: wide
excerpt: "Engineer with 16+ years building scientific software across climate, data science, and high-performance computing."
---

<div class="hero-section" id="about">
  <div class="hero-content">
    <div class="hero-image">
      <img src="/images/bio-photo.jpg" alt="Rajeev Jain">
    </div>
    <div class="hero-text">
      <h1 class="hero-title">Rajeev Jain</h1>
      <p class="hero-lead">Research software engineer building high-performance tools for climate science, cancer research, and exascale computing. Lead developer of <a href="https://github.com/UXARRAY/uxarray">UXarray</a> (205+ GitHub stars), 2× R&D 100 Award winner, with 16+ years optimizing scientific workflows at Argonne National Laboratory.</p>
      <p class="hero-position"><strong>Principal Specialist</strong> · Argonne MCS Division · Joint appointment at University of Chicago</p>
      <p class="hero-links">
        <a href="mailto:rajeeja@gmail.com">Email</a> · 
        <a href="https://github.com/rajeeja">GitHub</a> · 
        <a href="https://www.linkedin.com/in/rajeeja/">LinkedIn</a> · 
        <a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en">Scholar</a>
      </p>
      <div class="hero-actions">
        <a class="btn btn--primary" href="/files/Rajeev_Jain_Resume.pdf">Resume</a>
        <a class="btn btn--ghost" href="#work">Featured Work</a>
      </div>
    </div>
  </div>
</div>


<section class="content-section" id="work" style="--delay: 0.05s;">
  <h2>Featured Work</h2>
  <div class="case-studies">
    <article class="case-study">
      <h3>UXarray: Python library for unstructured climate grid analysis</h3>
      <p><strong>Challenge:</strong> Climate scientists working with unstructured grids (MPAS, ICON, SAM) lacked Python tools for conservative analysis that preserve integral quantities across non-uniform meshes.</p>
      <p><strong>Contribution:</strong> Lead developer since project inception, implementing core mathematical operators including conservative zonal averaging using Gauss-Legendre quadrature, Grid I/O readers for multiple formats (ESMF, MPAS, SCRIP, HEALPix), and testing infrastructure. Established continuous integration and regular PyPI releases.</p>
      <p><strong>Impact:</strong> UXarray is now used by researchers at NCAR, DOE labs, and universities worldwide (205+ GitHub stars). Enables analysis of multi-petabyte climate datasets with validated accuracy. Presented tutorials at SC24, AMS 2024, and ESDS Annual Event.</p>
      <p class="case-links"><a href="https://github.com/UXARRAY/uxarray">GitHub</a>  &middot;  <a href="https://uxarray.readthedocs.io">Documentation</a>  &middot;  <a href="https://github.com/UXARRAY/uxarray/pull/1345">Conservative zonal averaging PR</a></p>
    </article>
    <article class="case-study">
      <h3>CANDLE/IMPROVE: hyperparameter optimization for cancer drug response models</h3>
      <p><strong>Challenge:</strong> Cancer drug response prediction models showed poor generalization across different pharmacogenomic datasets, requiring systematic benchmarking and optimization.</p>
      <p><strong>Contribution:</strong> Built hyperparameter optimization (HPO) infrastructure and ran 10,000+ training experiments across Summit, Theta, and Cori supercomputers. Developed GitHub Actions workflows for cross-study validation. Maintained benchmarking framework and co-authored standardization guidelines.</p>
      <p><strong>Impact:</strong> Benchmarking framework used by 15+ researchers across the project. Results published in Briefings in Bioinformatics (2025) and presented at 20th Workflows Workshop (2025). Contributed to R&D 100 Award (2023).</p>
      <p class="case-links">
        <a href="https://github.com/JDACS4C-IMPROVE/IMPROVE">IMPROVE GitHub</a> &middot; 
        <a href="https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2508-4">CANDLE/Supervisor Paper</a> &middot; 
        <a href="https://academic.oup.com/bib/article/27/1/bbaf667/7002013">Benchmarking Paper</a> &middot; 
        Counterfactuals Paper (CAFCW 2021)
      </p>
    </article>
    <article class="case-study">
      <h3>FLASH-X: I/O optimization for exascale multiphysics simulations</h3>
      <p><strong>Challenge:</strong> Checkpoint and restart operations were taking 30-50% of total runtime in billion-element FLASH-X simulations on leadership-class supercomputers.</p>
      <p><strong>Contribution:</strong> Implemented asynchronous HDF5 I/O with Argobots for non-blocking checkpoint operations and integrated SZ3/ZFP compression. Built verification workflow with nightly baseline testing to ensure reproducibility. Enabled cross-checkpoint restart between AMReX and Paramesh solvers.</p>
      <p><strong>Impact:</strong> Achieved 40-70% reduction in checkpoint write times on Summit supercomputer. Compression reduced storage requirements by 50%+ with minimal accuracy loss. Published at SC24 workshop, contributed to R&D 100 Award (2022).</p>
      <p class="case-links"><a href="https://flash-x.org/">FLASH-X Project</a>  &middot;  <a href="https://arxiv.org/abs/2208.11630">FLASH-X Paper</a>  &middot;  <a href="https://ieeexplore.ieee.org/document/10026923">Compression Paper</a>  &middot;  <a href="https://github.com/Flash-X/Flash-X">GitHub</a></p>
    </article>
  </div>
</section>

<section class="content-section" id="recognition" style="--delay: 0.1s;">
  <h2>Recognition</h2>
  <ul class="recognition-list">
    <li><strong>R&D 100 Award 2023:</strong> <a href="https://www.rdworldonline.com/candle-cancer-distributed-learning-environment-is-the-rd-100-winner-of-the-day/">CANDLE</a> — Cancer Distributed Learning Environment for drug response prediction</li>
    <li><strong>R&D 100 Award 2022:</strong> <a href="https://www.rdworldonline.com/rd-100-2022-winner/flash-x-a-multiphysics-simulation-software/">FLASH-X</a> — Multiphysics simulation software for exascale computing</li>
    <li><strong>Best Paper Award:</strong> International Meshing Roundtable (2010) — Reactor core mesh generation</li>
  </ul>
</section>

<section class="content-section" id="background" style="--delay: 0.15s;">
  <h2>Background</h2>
  <p><strong>Argonne National Laboratory</strong> (2009–present) — Principal Specialist, Research Software Engineering. Lead developer for UXarray, FLASH-X, CANDLE/IMPROVE, MeshKit, and urban simulation projects.</p>
  <p><strong>University of Chicago</strong> (2023–present) — Staff At-Large. Joint appointment supporting cancer and earth science research.</p>
  <p><strong>Education:</strong> M.S. Computer Science (University of Chicago, 2020) · M.S. Structural Engineering (Arizona State University, 2009) · Arizona State University Graduate Fellowship (2007-2009)</p>
  <p class="more-links"><a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&hl=en">Full publications on Google Scholar</a> · <a href="/files/Rajeev_Jain_Resume.pdf">Resume PDF</a> · <a href="/files/Rajeev_Jain_CV.pdf">CV PDF</a></p>
</section>

<section class="content-section" id="contact" style="--delay: 0.2s;">
  <h2>Contact</h2>
  <p><a href="mailto:rajeeja@gmail.com">rajeeja@gmail.com</a></p>
</section>
