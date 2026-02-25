---
layout: single
title: "Rajeev Jain"
permalink: /
author_profile: false
classes: wide
excerpt: "Research Software Engineer · Argonne National Laboratory"
---

<div class="hero-section" id="about">
  <div class="hero-content">
    <div class="hero-image">
      <img src="/images/bio-photo.jpg" alt="Rajeev Jain">
    </div>
    <div class="hero-text">
      <h1 class="hero-title">Rajeev Jain</h1>
      <p class="hero-position"><strong>Research Software Engineer</strong> · Argonne National Laboratory · University of Chicago</p>
      <p class="hero-lead">I build software tools for scientific research — climate data analysis, cancer drug response prediction, and high-performance computing. 16 years at Argonne, two R&D 100 Awards, and a passion for open-source scientific software.</p>
      <p class="hero-links">
        <a href="mailto:rajeeja@gmail.com" class="hero-link-item"><span class="link-icon">✉</span> Email</a>
        <a href="https://github.com/rajeeja" class="hero-link-item"><span class="link-icon">⌘</span> GitHub</a>
        <a href="https://www.linkedin.com/in/rajeeja/" class="hero-link-item"><span class="link-icon">in</span> LinkedIn</a>
        <a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en" class="hero-link-item"><span class="link-icon">◎</span> Scholar</a>
      </p>
      <div class="hero-actions">
        <a class="btn btn--primary" href="/files/Rajeev_Jain_Resume.pdf">Resume</a>
        <a class="btn btn--ghost" href="#projects">Projects ↓</a>
      </div>
    </div>
  </div>
</div>

<nav class="section-nav" id="section-nav">
  <div class="section-nav__inner">
    <a href="#about" class="section-nav__link">About</a>
    <span class="section-nav__dot">·</span>
    <a href="#uxarray" class="section-nav__link">UXarray</a>
    <span class="section-nav__dot">·</span>
    <a href="#candle" class="section-nav__link">CANDLE</a>
    <span class="section-nav__dot">·</span>
    <a href="#flashx" class="section-nav__link">FLASH-X</a>
    <span class="section-nav__dot">·</span>
    <a href="#recognition" class="section-nav__link">Awards</a>
    <span class="section-nav__dot">·</span>
    <a href="#background" class="section-nav__link">Background</a>
  </div>
</nav>


<section class="content-section" id="projects" style="--delay: 0.05s;">
  <h2>Projects</h2>
  <p class="section-subtitle">Open-source tools I lead or contribute to — each section is directly shareable.</p>
</section>

<section class="project-section" id="uxarray" style="--delay: 0.1s;">
  <div class="project-header">
    <div class="project-label">Project</div>
    <h3 class="project-title">UXarray</h3>
    <p class="project-tagline">Python library for unstructured climate grid analysis</p>
  </div>
  <div class="project-body">
    <div class="project-detail">
      <h4>Challenge</h4>
      <p>Climate scientists working with unstructured grids (MPAS, ICON, SAM) lacked Python tools for conservative analysis that preserve integral quantities across non-uniform meshes.</p>
    </div>
    <div class="project-detail">
      <h4>My Role</h4>
      <p>Lead developer since project inception. Implemented core mathematical operators including conservative zonal averaging using Gauss-Legendre quadrature, Grid I/O readers for multiple formats (ESMF, MPAS, SCRIP, HEALPix), and testing infrastructure. Established continuous integration and regular PyPI releases.</p>
    </div>
    <div class="project-detail">
      <h4>Impact</h4>
      <p>Used by researchers at NCAR, DOE labs, and universities worldwide (205+ GitHub stars). Enables analysis of multi-petabyte climate datasets. Presented tutorials at SC24, AMS 2024, and ESDS Annual Event.</p>
    </div>
    <div class="project-links">
      <a href="https://github.com/UXARRAY/uxarray" class="project-link">GitHub</a>
      <a href="https://uxarray.readthedocs.io" class="project-link">Docs</a>
      <a href="https://github.com/UXARRAY/uxarray/pull/1345" class="project-link">Conservative Zonal Avg PR</a>
    </div>
  </div>
</section>

<section class="project-section" id="candle" style="--delay: 0.15s;">
  <div class="project-header">
    <div class="project-label">Project · R&D 100 Award 2023</div>
    <h3 class="project-title">CANDLE / IMPROVE</h3>
    <p class="project-tagline">Hyperparameter optimization for cancer drug response models</p>
  </div>
  <div class="project-body">
    <div class="project-detail">
      <h4>Challenge</h4>
      <p>Cancer drug response prediction models showed poor generalization across different pharmacogenomic datasets, requiring systematic benchmarking and optimization.</p>
    </div>
    <div class="project-detail">
      <h4>My Role</h4>
      <p>Built hyperparameter optimization (HPO) infrastructure and ran 10,000+ training experiments across Summit, Theta, and Cori supercomputers. Developed GitHub Actions workflows for cross-study validation. Maintained benchmarking framework and co-authored standardization guidelines.</p>
    </div>
    <div class="project-detail">
      <h4>Impact</h4>
      <p>Benchmarking framework used by 15+ researchers across the project. Results published in Briefings in Bioinformatics (2025) and presented at 20th Workflows Workshop (2025). Contributed to R&D 100 Award (2023).</p>
    </div>
    <div class="project-links">
      <a href="https://github.com/JDACS4C-IMPROVE/IMPROVE" class="project-link">IMPROVE GitHub</a>
      <a href="https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2508-4" class="project-link">CANDLE/Supervisor Paper</a>
      <a href="https://academic.oup.com/bib/article/27/1/bbaf667/7002013" class="project-link">Benchmarking Paper</a>
      <a href="https://web.cels.anl.gov/~woz/papers/Counterfactuals_2021.pdf" class="project-link">Counterfactuals Paper</a>
    </div>
  </div>
</section>

<section class="project-section" id="flashx" style="--delay: 0.2s;">
  <div class="project-header">
    <div class="project-label">Project · R&D 100 Award 2022</div>
    <h3 class="project-title">FLASH-X</h3>
    <p class="project-tagline">I/O optimization for exascale multiphysics simulations</p>
  </div>
  <div class="project-body">
    <div class="project-detail">
      <h4>Challenge</h4>
      <p>Checkpoint and restart operations were taking 30–50% of total runtime in billion-element FLASH-X simulations on leadership-class supercomputers.</p>
    </div>
    <div class="project-detail">
      <h4>My Role</h4>
      <p>Implemented asynchronous HDF5 I/O with Argobots for non-blocking checkpoint operations and integrated SZ3/ZFP compression. Built verification workflow with nightly baseline testing to ensure reproducibility. Enabled cross-checkpoint restart between AMReX and Paramesh solvers.</p>
    </div>
    <div class="project-detail">
      <h4>Impact</h4>
      <p>Achieved 40–70% reduction in checkpoint write times on Summit supercomputer. Compression reduced storage requirements by 50%+ with minimal accuracy loss. Published at SC24 workshop, contributed to R&D 100 Award (2022).</p>
    </div>
    <div class="project-links">
      <a href="https://flash-x.org/" class="project-link">FLASH-X Project</a>
      <a href="https://arxiv.org/abs/2208.11630" class="project-link">FLASH-X Paper</a>
      <a href="https://ieeexplore.ieee.org/document/10026923" class="project-link">Compression Paper</a>
      <a href="https://flash-x.org/pages/source/" class="project-link">Source</a>
    </div>
  </div>
</section>

<section class="content-section" id="recognition" style="--delay: 0.25s;">
  <h2>Recognition</h2>
  <div class="awards-grid">
    <div class="award-card">
      <div class="award-year">2023</div>
      <div class="award-body">
        <strong><a href="https://www.rdworldonline.com/candle-cancer-distributed-learning-environment-is-the-rd-100-winner-of-the-day/">R&D 100 Award</a></strong>
        <p>CANDLE — Cancer Distributed Learning Environment for drug response prediction</p>
      </div>
    </div>
    <div class="award-card">
      <div class="award-year">2022</div>
      <div class="award-body">
        <strong><a href="https://www.rdworldonline.com/rd-100-2022-winner/flash-x-a-multiphysics-simulation-software/">R&D 100 Award</a></strong>
        <p>FLASH-X — Multiphysics simulation software for exascale computing</p>
      </div>
    </div>
    <div class="award-card">
      <div class="award-year">2010</div>
      <div class="award-body">
        <strong>Best Paper Award</strong>
        <p>International Meshing Roundtable — Reactor core mesh generation</p>
      </div>
    </div>
  </div>
</section>

<section class="content-section" id="background" style="--delay: 0.3s;">
  <h2>Background</h2>
  <div class="timeline-grid">
    <div class="timeline-item">
      <div class="timeline-period">2009 – present</div>
      <div class="timeline-body">
        <strong>Argonne National Laboratory</strong> — Principal Specialist, Research Software Engineering
        <p>Lead developer for UXarray, FLASH-X, CANDLE/IMPROVE, MeshKit, and urban simulation projects.</p>
      </div>
    </div>
    <div class="timeline-item">
      <div class="timeline-period">2023 – present</div>
      <div class="timeline-body">
        <strong>University of Chicago</strong> — Staff At-Large
        <p>Joint appointment supporting cancer and earth science research.</p>
      </div>
    </div>
    <div class="timeline-item">
      <div class="timeline-period">Education</div>
      <div class="timeline-body">
        <p>M.S. Computer Science — University of Chicago (2020)<br>
        M.S. Structural Engineering — Arizona State University (2009)<br>
        B.Tech Mechanical Engineering — IIT ISM Dhanbad (2006)</p>
      </div>
    </div>
  </div>
  <p class="more-links"><a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&hl=en">Publications on Google Scholar</a> · <a href="/files/Rajeev_Jain_Resume.pdf">Resume PDF</a> · <a href="/files/Rajeev_Jain_CV.pdf">CV PDF</a></p>
</section>

<section class="content-section" id="contact" style="--delay: 0.35s;">
  <h2>Contact</h2>
  <p>Open to collaborations in scientific computing, AI for health, and open-source software.</p>
  <p><a href="mailto:rajeeja@gmail.com">rajeeja@gmail.com</a></p>
</section>
