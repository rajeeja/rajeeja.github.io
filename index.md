---
layout: single
title: "Rajeev Jain"
permalink: /
author_profile: false
classes: wide
excerpt: "Principal Research Software Engineer · Argonne National Laboratory"
---

<div class="hero-section" id="about">
  <div class="hero-content">
    <div class="hero-image">
      <img src="/images/bio-photo.jpg" alt="Rajeev Jain">
    </div>
    <div class="hero-text">
      <h1 class="hero-title">Rajeev Jain</h1>
      <p class="hero-position"><strong>Principal Research Software Engineer</strong> · <a href="https://www.anl.gov/mcs">Argonne National Laboratory</a> · <a href="https://cs.uchicago.edu/">University of Chicago</a></p>
      <p class="hero-lead">I build and scale the software behind scientific breakthroughs — GPU-accelerated deep learning frameworks, million-line HPC simulation engines, and climate analysis libraries used worldwide. 16 years leading development on large, multi-institutional codebases. Two R&D 100 Awards, 22+ publications, and EB-1A recipient for extraordinary ability in sciences.</p>
      <p class="hero-links-line">
        <a href="mailto:rajeeja@gmail.com">Email</a> ·
        <a href="https://github.com/rajeeja">GitHub</a> ·
        <a href="https://www.linkedin.com/in/rajeeja/">LinkedIn</a> ·
        <a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en">Scholar</a> ·
        <a href="https://orcid.org/0000-0002-1235-918X">ORCID</a> ·
        <a href="/files/Rajeev_Jain_Resume.pdf">Resume</a> ·
        <a href="/files/Rajeev_Jain_CV.pdf">CV</a>
      </p>
    </div>
  </div>
</div>

<nav class="section-nav" id="section-nav">
  <div class="section-nav__inner">
    <a href="#about" class="section-nav__link">About</a>
    <span class="section-nav__dot">·</span>
    <a href="#projects" class="section-nav__link">Projects</a>
    <span class="section-nav__dot">·</span>
    <a href="#skills" class="section-nav__link">Skills</a>
    <span class="section-nav__dot">·</span>
    <a href="#publications" class="section-nav__link">Publications</a>
    <span class="section-nav__dot">·</span>
    <a href="#recognition" class="section-nav__link">Awards</a>
    <span class="section-nav__dot">·</span>
    <a href="#background" class="section-nav__link">Background</a>
  </div>
</nav>


<section class="content-section" id="projects">
  <h2>Projects</h2>
  <p class="section-lead">Large-scale open-source tools I lead or contribute to. Each built to serve research communities, handling codebases of 100K+ lines across multi-institutional teams.</p>

  <div class="entry">
    <h3 id="uxarray"><a href="https://github.com/UXARRAY/uxarray">UXarray</a></h3>
    <p class="entry-meta">Lead Developer · 205+ GitHub stars · <a href="https://uxarray.readthedocs.io">Docs</a></p>
    <p>Python library for unstructured climate grid analysis. Climate scientists working with next-generation grids (MPAS, ICON, SAM) lacked tools for conservative analysis that preserve integral quantities across non-uniform meshes — a gap blocking petabyte-scale research.</p>
    <p>I lead development since inception: core mathematical operators including conservative zonal averaging via Gauss-Legendre quadrature, Grid I/O for multiple formats (ESMF, MPAS, SCRIP, HEALPix), full CI pipeline, and regular PyPI releases. Currently building an <strong>MCP server and AI agent</strong> for natural-language interaction with climate datasets. Adopted by NCAR, DOE labs, and universities worldwide.</p>
  </div>

  <div class="entry">
    <h3 id="pangu-weather"><a href="https://www.anl.gov/aurora">Pangu-Weather on Aurora</a></h3>
    <p class="entry-meta">Aurora Exascale System · Argonne ALCF</p>
    <p>PyTorch-based reimplementation of the Pangu-Weather deep learning framework for climate modeling, using the <strong>Spectral Fourier Neural Operator (SFNO)</strong>. Ported and optimized for DOE's Aurora supercomputer — the first U.S. exascale system — with 60,000+ Intel GPUs. Demonstrates feasibility of AI-driven weather prediction beyond NVIDIA ecosystems, advancing DOE's mission for exascale Earth science.</p>
  </div>

  <div class="entry">
    <h3 id="candle"><a href="https://github.com/JDACS4C-IMPROVE/IMPROVE">CANDLE / IMPROVE</a></h3>
    <p class="entry-meta">Core Contributor · <a href="https://www.rdworldonline.com/candle-cancer-distributed-learning-environment-is-the-rd-100-winner-of-the-day/">R&D 100 Award 2023</a></p>
    <p>Hyperparameter optimization for cancer drug response prediction at supercomputer scale. Built the HPO infrastructure and ran <strong>10,000+ training experiments</strong> across Summit, Theta, and Cori. Developed GitHub Actions workflows for cross-study validation. The 15+ researcher multi-lab collaboration (Argonne, LLNL, ORNL) relied on my benchmarking framework. Published in <a href="https://academic.oup.com/bib/article/27/1/bbaf667/7002013"><em>Briefings in Bioinformatics</em></a> (2025). Additional papers: <a href="https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2508-4">CANDLE/Supervisor</a>, <a href="https://web.cels.anl.gov/~woz/papers/Counterfactuals_2021.pdf">Counterfactuals</a>.</p>
  </div>

  <div class="entry">
    <h3 id="flashx"><a href="https://flash-x.org/">FLASH-X</a></h3>
    <p class="entry-meta">I/O & Compression Lead · <a href="https://www.rdworldonline.com/rd-100-2022-winner/flash-x-a-multiphysics-simulation-software/">R&D 100 Award 2022</a> · <a href="https://arxiv.org/abs/2208.11630">Paper</a></p>
    <p>I/O optimization for a million-line exascale multiphysics simulation engine used by hundreds of researchers for astrophysics, combustion, and fluid dynamics. Checkpoint/restart was consuming 30–50% of runtime on leadership-class supercomputers. I implemented <strong>asynchronous HDF5 I/O</strong> with Argobots and integrated SZ3/ZFP compression — achieving 40–70% reduction in checkpoint times on Summit and 50%+ storage savings. Enabled cross-checkpoint restart between AMReX and Paramesh solvers (a first for FLASH). Published at <a href="https://ieeexplore.ieee.org/document/10026923">SC24 DRBSD-10</a>.</p>
  </div>

  <div class="entry">
    <h3 id="meshkit">MeshKit</h3>
    <p class="entry-meta">Principal Investigator · DOE NEAMS (2009–2016) · <a href="https://bitbucket.org/fathomteam/meshkit">Source</a></p>
    <p>Open-source C++ toolkit for automated nuclear reactor core mesh generation. As PI, led design and development of lattice hierarchy-based meshing, parallel generation capabilities, and multi-format I/O. Adopted by reactor simulation teams at Argonne. Won <strong>Best Paper Award</strong> at the International Meshing Roundtable (2010).</p>
  </div>
</section>


<section class="content-section" id="skills">
  <h2>Technical Expertise</h2>
  <p><strong>Languages:</strong> Python, C++, Fortran, R, Bash, SQL</p>
  <p><strong>ML & Data:</strong> PyTorch, TensorFlow, NumPy, Pandas, Xarray, Scikit-learn, Parsl, Swift/T</p>
  <p><strong>HPC & Systems:</strong> MPI, OpenMP, HDF5, NetCDF, MOAB, Docker, Singularity, GitHub Actions</p>
  <p><strong>Domains:</strong> Climate modeling, cancer pharmacogenomics, computational physics, mesh generation, AI/ML infrastructure, reproducible workflows</p>
</section>


<section class="content-section" id="publications">
  <h2>Selected Publications</h2>
  <p class="section-lead">22+ publications · <a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&hl=en">Full list on Google Scholar</a></p>

  <div class="pub-entry">
    <p class="pub-title"><a href="https://academic.oup.com/bib/article/27/1/bbaf667/7002013">Benchmarking community drug response prediction models</a></p>
    <p class="pub-detail">Partin, A., ..., <strong>Jain, R.</strong>, et al. · <em>Briefings in Bioinformatics</em>, 27(1), 2025</p>
  </div>

  <div class="pub-entry">
    <p class="pub-title">Enabling Data Reduction for Flash-X Simulations</p>
    <p class="pub-detail"><strong>Jain, R.</strong>, Tang, H., Dhruv, A., Byna, S. · <em>DRBSD-10 Workshop, SC24</em></p>
  </div>

  <div class="pub-entry">
    <p class="pub-title">Cross-HPO: Optimizing Neural Networks for Cancer Drug Response</p>
    <p class="pub-detail"><strong>Jain, R.</strong>, Wozniak, J.M., Partin, A., et al. · <em>CAFCW24 Workshop, SC24</em></p>
  </div>

  <div class="pub-entry">
    <p class="pub-title"><a href="https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2508-4">CANDLE/Supervisor: A workflow framework for machine learning applied to cancer research</a></p>
    <p class="pub-detail">Wozniak, J.M., ..., <strong>Jain, R.</strong>, et al. · <em>BMC Bioinformatics</em>, 19(S18), 2018</p>
  </div>

  <div class="pub-entry">
    <p class="pub-title">Creating Geometry and Mesh Models for Nuclear Reactor Core Geometries</p>
    <p class="pub-detail">Tautges, T.J., <strong>Jain, R.</strong> · <em>Journal of Engineering with Computers</em>, 2011</p>
  </div>
</section>


<section class="content-section" id="presentations">
  <h2>Selected Presentations</h2>
  <ul class="clean-list">
    <li><strong>SC24</strong> — Tutorial: UXarray for Analysis of Unstructured Climate Data</li>
    <li><strong>SC24</strong> — DRBSD-10: Enabling Data Reduction for Flash-X Simulations</li>
    <li><strong>SC24</strong> — CAFCW24: Cross-HPO for Cancer Drug Response</li>
    <li><strong>AMS 2024</strong> — UXarray: Extending Xarray with Support for Unstructured Grids</li>
    <li><strong>SciPy 2023</strong> — UXarray for Unstructured Climate Data</li>
    <li><strong>HDF User Group 2023</strong> — Data Reduction for FLASH-X Simulations</li>
  </ul>
</section>


<section class="content-section" id="recognition">
  <h2>Recognition</h2>

  <div class="entry">
    <h4>EB-1A Extraordinary Ability</h4>
    <p>U.S. permanent residency granted under the EB-1A classification for extraordinary ability in sciences — reserved for individuals with sustained national or international acclaim.</p>
  </div>

  <div class="entry">
    <h4><a href="https://www.rdworldonline.com/candle-cancer-distributed-learning-environment-is-the-rd-100-winner-of-the-day/">R&D 100 Award, 2023</a></h4>
    <p>CANDLE — Cancer Distributed Learning Environment for drug response prediction. The "Oscars of Innovation."</p>
  </div>

  <div class="entry">
    <h4><a href="https://www.rdworldonline.com/rd-100-2022-winner/flash-x-a-multiphysics-simulation-software/">R&D 100 Award, 2022</a></h4>
    <p>FLASH-X — Multiphysics simulation software for exascale computing.</p>
  </div>

  <div class="entry">
    <h4>ATPESC Scholar, 2015</h4>
    <p>Argonne Training Program on Extreme-Scale Computing — competitive program for HPC researchers.</p>
  </div>

  <div class="entry">
    <h4>Best Paper Award, 2010</h4>
    <p>International Meshing Roundtable — reactor core mesh generation.</p>
  </div>

  <div class="entry">
    <h4>Graduate Fellowship, 2007</h4>
    <p>Arizona State University — research assistantship in structural and computational mechanics.</p>
  </div>
</section>


<section class="content-section" id="funding">
  <h2>Research Funding</h2>
  <ul class="clean-list">
    <li><strong>DOE SEATS</strong> <span class="tag-active">Active</span> — Software Ecosystem for Advancing Climate Tools and Services</li>
    <li><strong>NSF Raijin</strong> <span class="tag-active">Active</span> — Collaborative Research in Climate Model Analysis</li>
    <li><strong>DOE ECP CANDLE</strong> — Core contributor (2017–2023)</li>
    <li><strong>DOE NEAMS</strong> — Principal Investigator for MeshKit (2009–2016)</li>
  </ul>
</section>


<section class="content-section" id="service">
  <h2>Service & Mentorship</h2>
  <ul class="clean-list">
    <li><strong>SBIR/STTR Proposal Reviewer</strong> — U.S. Department of Energy</li>
    <li><strong>Panelist</strong> — 5th Infraday Midwest Event ("Revolutionizing Public Infrastructure with AI")</li>
    <li><strong>Reviewer</strong> — Journal of Open Research Software, NumGrid</li>
    <li><strong>Committee</strong> — NumGrid 2020 Program Committee Member</li>
  </ul>
  <p>Mentored several students and doctoral candidates over the years on research software engineering, HPC techniques, and open-source development practices.</p>
</section>


<section class="content-section" id="background">
  <h2>Background</h2>

  <div class="entry">
    <h4>Argonne National Laboratory <span class="entry-date">2009 – present</span></h4>
    <p>Principal Specialist, Research Software Engineering. Lead developer for UXarray, FLASH-X, CANDLE/IMPROVE, MeshKit, and urban simulation projects. Division of Mathematics and Computer Science.</p>
  </div>

  <div class="entry">
    <h4>University of Chicago <span class="entry-date">2023 – present</span></h4>
    <p>Staff At-Large. Joint appointment supporting cancer pharmacogenomics and earth science research.</p>
  </div>

  <div class="entry">
    <h4>Arizona State University <span class="entry-date">2007 – 2009</span></h4>
    <p>Research & Teaching Assistant. Structural and Computational Mechanics Lab. Research on blast mitigation via FEM-based design optimization.</p>
  </div>

  <div class="entry entry--education">
    <h4>Education</h4>
    <p>M.S. Computer Science — University of Chicago (2020)<br>
    M.S. Structural Engineering — Arizona State University (2009)<br>
    B.Tech Mechanical Engineering — IIT ISM Dhanbad (2006)</p>
  </div>

  <p class="more-links"><a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&hl=en">Google Scholar</a> · <a href="/files/Rajeev_Jain_Resume.pdf">Resume</a> · <a href="/files/Rajeev_Jain_CV.pdf">Full CV</a></p>
</section>

<section class="content-section" id="contact">
  <h2>Contact</h2>
  <p>Open to collaborations in scientific computing, AI for health, climate modeling, and open-source software.</p>
  <p><a href="mailto:rajeeja@gmail.com">rajeeja@gmail.com</a></p>
</section>
