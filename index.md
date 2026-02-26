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
      <p class="hero-position"><strong>Principal Research Software Engineer</strong> · Argonne National Laboratory · University of Chicago</p>
      <p class="hero-lead">I architect and scale scientific software that researchers depend on — from GPU-accelerated deep learning frameworks to million-line HPC simulation engines. Over 16 years at Argonne, I've led cross-institutional teams building open-source tools for climate analysis, cancer drug prediction, and exascale computing. Two R&D 100 Awards, 22+ publications, and a track record of shipping production-quality research software with real-world community impact.</p>
      <p class="hero-links">
        <a href="mailto:rajeeja@gmail.com" class="hero-link-item"><span class="link-icon">✉</span> Email</a>
        <a href="https://github.com/rajeeja" class="hero-link-item"><span class="link-icon">⌘</span> GitHub</a>
        <a href="https://www.linkedin.com/in/rajeeja/" class="hero-link-item"><span class="link-icon">in</span> LinkedIn</a>
        <a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en" class="hero-link-item"><span class="link-icon">◎</span> Scholar</a>
        <a href="https://orcid.org/0000-0002-1235-918X" class="hero-link-item"><span class="link-icon">⊙</span> ORCID</a>
      </p>
      <div class="hero-actions">
        <a class="btn btn--primary" href="/files/Rajeev_Jain_Resume.pdf">Resume</a>
        <a class="btn btn--outline" href="/files/Rajeev_Jain_CV.pdf">Full CV</a>
        <a class="btn btn--ghost" href="#projects">Projects ↓</a>
      </div>
    </div>
  </div>
  <div class="hero-stats">
    <div class="stat-item">
      <span class="stat-number">16+</span>
      <span class="stat-label">Years at Argonne</span>
    </div>
    <div class="stat-item">
      <span class="stat-number">2×</span>
      <span class="stat-label">R&D 100 Awards</span>
    </div>
    <div class="stat-item">
      <span class="stat-number">22+</span>
      <span class="stat-label">Publications</span>
    </div>
    <div class="stat-item">
      <span class="stat-number">205+</span>
      <span class="stat-label">GitHub Stars</span>
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


<section class="content-section" id="projects" style="--delay: 0.05s;">
  <h2>Projects</h2>
  <p class="section-subtitle">Large-scale open-source tools I lead or contribute to — each built to serve research communities, not just demos.</p>
</section>

<section class="project-section" id="uxarray" style="--delay: 0.1s;">
  <div class="project-header">
    <div class="project-label">Lead Developer · Active</div>
    <h3 class="project-title">UXarray</h3>
    <p class="project-tagline">Python library for unstructured climate grid analysis — 205+ GitHub stars</p>
  </div>
  <div class="project-body">
    <div class="project-detail">
      <h4>Challenge</h4>
      <p>Climate scientists working with next-generation unstructured grids (MPAS, ICON, SAM) lacked Python tools for conservative analysis that preserve integral quantities across non-uniform meshes — a gap blocking petabyte-scale climate research.</p>
    </div>
    <div class="project-detail">
      <h4>My Role</h4>
      <p>Lead developer since project inception. Implemented core mathematical operators including conservative zonal averaging using Gauss-Legendre quadrature, Grid I/O readers for multiple formats (ESMF, MPAS, SCRIP, HEALPix), and full testing infrastructure. Established continuous integration, regular PyPI releases, and grew the contributor community. Currently building an <strong>MCP server and AI agent</strong> for natural-language interaction with UXarray, enabling researchers to query climate datasets conversationally.</p>
    </div>
    <div class="project-detail">
      <h4>Impact</h4>
      <p>Adopted by researchers at NCAR, DOE labs, and universities worldwide. Enables analysis of multi-petabyte climate datasets on unstructured grids. Presented tutorials at SC24, AMS 2024, SciPy 2023, and ESDS Annual Event. Active open-source community with 205+ GitHub stars.</p>
    </div>
    <div class="project-links">
      <a href="https://github.com/UXARRAY/uxarray" class="project-link">GitHub</a>
      <a href="https://uxarray.readthedocs.io" class="project-link">Docs</a>
      <a href="https://github.com/UXARRAY/uxarray/pull/1345" class="project-link">Conservative Zonal Avg PR</a>
    </div>
  </div>
</section>

<section class="project-section" id="pangu-weather" style="--delay: 0.12s;">
  <div class="project-header">
    <div class="project-label">Project · Aurora Exascale System</div>
    <h3 class="project-title">Pangu-Weather on Aurora</h3>
    <p class="project-tagline">PyTorch reimplementation of AI weather prediction for DOE's exascale GPU system</p>
  </div>
  <div class="project-body">
    <div class="project-detail">
      <h4>Challenge</h4>
      <p>The Pangu-Weather deep learning model demonstrated breakthrough weather prediction accuracy, but the original implementation was architecture-specific and couldn't leverage DOE's next-generation Aurora supercomputer with Intel GPUs — the first U.S. exascale system.</p>
    </div>
    <div class="project-detail">
      <h4>My Role</h4>
      <p>Led the PyTorch-based reimplementation using the <strong>Spectral Fourier Neural Operator (SFNO)</strong> architecture. Ported and optimized the deep learning framework for Aurora's Intel Data Center GPU Max Series hardware. Coordinated with Argonne's ALCF team to enable large-scale training and inference on the exascale system.</p>
    </div>
    <div class="project-detail">
      <h4>Impact</h4>
      <p>Enables AI-driven global weather and climate prediction on Aurora — bridging cutting-edge deep learning frameworks with next-generation HPC hardware. Demonstrates feasibility of GPU-accelerated climate AI beyond NVIDIA ecosystems, advancing DOE's mission to leverage exascale computing for Earth science.</p>
    </div>
    <div class="project-links">
      <a href="https://www.anl.gov/aurora" class="project-link">Aurora</a>
      <a href="https://arxiv.org/abs/2211.02556" class="project-link">Pangu-Weather Paper</a>
    </div>
  </div>
</section>

<section class="project-section" id="candle" style="--delay: 0.15s;">
  <div class="project-header">
    <div class="project-label">Core Contributor · R&D 100 Award 2023</div>
    <h3 class="project-title">CANDLE / IMPROVE</h3>
    <p class="project-tagline">Hyperparameter optimization for cancer drug response prediction at scale</p>
  </div>
  <div class="project-body">
    <div class="project-detail">
      <h4>Challenge</h4>
      <p>Cancer drug response prediction models showed poor generalization across different pharmacogenomic datasets. The multi-lab, 15+ researcher collaboration needed systematic benchmarking infrastructure and hyperparameter optimization at supercomputer scale.</p>
    </div>
    <div class="project-detail">
      <h4>My Role</h4>
      <p>Built the hyperparameter optimization (HPO) infrastructure and ran <strong>10,000+ training experiments</strong> across Summit, Theta, and Cori supercomputers. Developed GitHub Actions workflows for cross-study validation and continuous benchmarking. Maintained the benchmarking framework, co-authored standardization guidelines, and coordinated with teams across Argonne, LLNL, and ORNL.</p>
    </div>
    <div class="project-detail">
      <h4>Impact</h4>
      <p>Benchmarking framework adopted by 15+ researchers across the multi-lab collaboration. Results published in <em>Briefings in Bioinformatics</em> (2025) and presented at 20th Workflows Workshop (SC25). Contributed to <strong>R&D 100 Award (2023)</strong> — the "Oscars of Innovation."</p>
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
    <div class="project-label">I/O & Compression Lead · R&D 100 Award 2022</div>
    <h3 class="project-title">FLASH-X</h3>
    <p class="project-tagline">I/O optimization for a million-line exascale multiphysics simulation engine</p>
  </div>
  <div class="project-body">
    <div class="project-detail">
      <h4>Challenge</h4>
      <p>Checkpoint and restart operations were consuming 30–50% of total runtime in billion-element FLASH-X simulations on leadership-class supercomputers — a million-line Fortran/C codebase used by hundreds of researchers for astrophysics, combustion, and fluid dynamics.</p>
    </div>
    <div class="project-detail">
      <h4>My Role</h4>
      <p>Implemented <strong>asynchronous HDF5 I/O</strong> with Argobots for non-blocking checkpoint operations and integrated SZ3/ZFP lossy compression. Built a verification workflow with nightly baseline testing to ensure scientific reproducibility. Enabled cross-checkpoint restart between AMReX and Paramesh solvers — a first for the FLASH codebase.</p>
    </div>
    <div class="project-detail">
      <h4>Impact</h4>
      <p>Achieved <strong>40–70% reduction</strong> in checkpoint write times on Summit supercomputer. Compression reduced storage requirements by 50%+ with minimal accuracy loss. Published at SC24 DRBSD-10 workshop. Contributed to <strong>R&D 100 Award (2022)</strong>.</p>
    </div>
    <div class="project-links">
      <a href="https://flash-x.org/" class="project-link">FLASH-X Project</a>
      <a href="https://arxiv.org/abs/2208.11630" class="project-link">FLASH-X Paper</a>
      <a href="https://ieeexplore.ieee.org/document/10026923" class="project-link">Compression Paper</a>
      <a href="https://flash-x.org/pages/source/" class="project-link">Source</a>
    </div>
  </div>
</section>

<section class="project-section" id="meshkit" style="--delay: 0.25s;">
  <div class="project-header">
    <div class="project-label">Principal Investigator · DOE NEAMS (2009–2016)</div>
    <h3 class="project-title">MeshKit</h3>
    <p class="project-tagline">Automated mesh generation for nuclear reactor core simulations</p>
  </div>
  <div class="project-body">
    <div class="project-detail">
      <h4>Challenge</h4>
      <p>Nuclear reactor simulations required complex hexagonal and cylindrical mesh geometries that existing tools couldn't generate automatically with the precision and reproducibility needed for safety-critical analysis.</p>
    </div>
    <div class="project-detail">
      <h4>My Role</h4>
      <p><strong>Principal Investigator</strong> leading the design and development of MeshKit under DOE's NEAMS program. Implemented a lattice hierarchy-based approach for automated reactor core meshing, parallel mesh generation capabilities, and multi-format I/O. Managed the project roadmap, coordinated with the SIGMA team and reactor physics analysts at Argonne.</p>
    </div>
    <div class="project-detail">
      <h4>Impact</h4>
      <p>Adopted by reactor simulation teams at Argonne for safety analysis workflows. Published 5+ papers including a <strong>Best Paper Award</strong> at the International Meshing Roundtable (2010). Demonstrated that a lattice-based approach could automate what previously required weeks of manual meshing effort.</p>
    </div>
    <div class="project-links">
      <a href="https://bitbucket.org/fathomteam/meshkit" class="project-link">Source</a>
    </div>
  </div>
</section>


<section class="content-section" id="skills" style="--delay: 0.27s;">
  <h2>Technical Expertise</h2>
  <div class="skills-grid">
    <div class="skill-category">
      <h4>Languages</h4>
      <div class="skill-tags">
        <span class="skill-tag">Python</span>
        <span class="skill-tag">C++</span>
        <span class="skill-tag">Fortran</span>
        <span class="skill-tag">R</span>
        <span class="skill-tag">Bash</span>
        <span class="skill-tag">SQL</span>
      </div>
    </div>
    <div class="skill-category">
      <h4>ML & Data</h4>
      <div class="skill-tags">
        <span class="skill-tag">PyTorch</span>
        <span class="skill-tag">TensorFlow</span>
        <span class="skill-tag">NumPy</span>
        <span class="skill-tag">Pandas</span>
        <span class="skill-tag">Xarray</span>
        <span class="skill-tag">Scikit-learn</span>
        <span class="skill-tag">Parsl</span>
        <span class="skill-tag">Swift/T</span>
      </div>
    </div>
    <div class="skill-category">
      <h4>HPC & Systems</h4>
      <div class="skill-tags">
        <span class="skill-tag">MPI</span>
        <span class="skill-tag">OpenMP</span>
        <span class="skill-tag">HDF5</span>
        <span class="skill-tag">NetCDF</span>
        <span class="skill-tag">MOAB</span>
        <span class="skill-tag">Docker</span>
        <span class="skill-tag">Singularity</span>
        <span class="skill-tag">GitHub Actions</span>
      </div>
    </div>
    <div class="skill-category">
      <h4>Domains</h4>
      <div class="skill-tags">
        <span class="skill-tag tag-domain">Climate Modeling</span>
        <span class="skill-tag tag-domain">Cancer Pharmacogenomics</span>
        <span class="skill-tag tag-domain">Computational Physics</span>
        <span class="skill-tag tag-domain">Mesh Generation</span>
        <span class="skill-tag tag-domain">AI/ML Infrastructure</span>
        <span class="skill-tag tag-domain">Reproducible Workflows</span>
      </div>
    </div>
  </div>
</section>


<section class="content-section" id="publications" style="--delay: 0.28s;">
  <h2>Selected Publications</h2>
  <p class="section-subtitle">22+ publications · <a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&hl=en">Full list on Google Scholar</a></p>

  <div class="publications-list">
    <div class="pub-item">
      <div class="pub-year">2025</div>
      <div class="pub-body">
        <p class="pub-title"><a href="https://academic.oup.com/bib/article/27/1/bbaf667/7002013">Benchmarking community drug response prediction models: datasets, models, tools, and metrics</a></p>
        <p class="pub-authors">Partin, A., Vasanthakumari, P., Narykov, O., ..., <strong>Jain, R.</strong>, et al.</p>
        <p class="pub-venue">Briefings in Bioinformatics, 27(1)</p>
      </div>
    </div>
    <div class="pub-item">
      <div class="pub-year">2024</div>
      <div class="pub-body">
        <p class="pub-title"><a href="#">Enabling Data Reduction for Flash-X Simulations</a></p>
        <p class="pub-authors"><strong>Jain, R.</strong>, Tang, H., Dhruv, A., Byna, S.</p>
        <p class="pub-venue">DRBSD-10 Workshop, SC24</p>
      </div>
    </div>
    <div class="pub-item">
      <div class="pub-year">2024</div>
      <div class="pub-body">
        <p class="pub-title"><a href="#">Cross-HPO: Optimizing Neural Networks for Cancer Drug Response</a></p>
        <p class="pub-authors"><strong>Jain, R.</strong>, Wozniak, J.M., Partin, A., et al.</p>
        <p class="pub-venue">CAFCW24 Workshop, SC24</p>
      </div>
    </div>
    <div class="pub-item">
      <div class="pub-year">2018</div>
      <div class="pub-body">
        <p class="pub-title"><a href="https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2508-4">CANDLE/Supervisor: A workflow framework for machine learning applied to cancer research</a></p>
        <p class="pub-authors">Wozniak, J.M., ..., <strong>Jain, R.</strong>, et al.</p>
        <p class="pub-venue">BMC Bioinformatics, 19(S18)</p>
      </div>
    </div>
    <div class="pub-item">
      <div class="pub-year">2011</div>
      <div class="pub-body">
        <p class="pub-title">Creating Geometry and Mesh Models for Nuclear Reactor Core Geometries Using a Lattice Hierarchy-Based Approach</p>
        <p class="pub-authors">Tautges, T.J., <strong>Jain, R.</strong></p>
        <p class="pub-venue">Journal of Engineering with Computers</p>
      </div>
    </div>
  </div>
</section>


<section class="content-section" id="presentations" style="--delay: 0.29s;">
  <h2>Selected Presentations</h2>
  <div class="presentations-list">
    <div class="pres-item">
      <span class="pres-year">2024</span>
      <span class="pres-body"><strong>SC24 Tutorial</strong> — UXarray for Analysis of Unstructured Climate Data</span>
    </div>
    <div class="pres-item">
      <span class="pres-year">2024</span>
      <span class="pres-body"><strong>SC24 DRBSD-10</strong> — Enabling Data Reduction for Flash-X Simulations</span>
    </div>
    <div class="pres-item">
      <span class="pres-year">2024</span>
      <span class="pres-body"><strong>SC24 CAFCW24</strong> — Cross-HPO for Cancer Drug Response</span>
    </div>
    <div class="pres-item">
      <span class="pres-year">2024</span>
      <span class="pres-body"><strong>AMS Annual Meeting</strong> — UXarray: Extending Xarray with Support for Unstructured Grids</span>
    </div>
    <div class="pres-item">
      <span class="pres-year">2023</span>
      <span class="pres-body"><strong>SciPy 2023</strong> — UXarray for Unstructured Climate Data</span>
    </div>
    <div class="pres-item">
      <span class="pres-year">2023</span>
      <span class="pres-body"><strong>HDF User Group</strong> — Data Reduction for FLASH-X Simulations</span>
    </div>
  </div>
</section>


<section class="content-section" id="recognition" style="--delay: 0.3s;">
  <h2>Recognition</h2>
  <div class="awards-grid">
    <div class="award-card award-card--highlight">
      <div class="award-year">EB-1A</div>
      <div class="award-body">
        <strong>Extraordinary Ability Classification</strong>
        <p>U.S. permanent residency granted under the EB-1A classification for extraordinary ability in sciences — reserved for individuals with sustained national or international acclaim</p>
      </div>
    </div>
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
      <div class="award-year">2015</div>
      <div class="award-body">
        <strong>ATPESC Scholar</strong>
        <p>Argonne Training Program on Extreme-Scale Computing — competitive program for HPC researchers</p>
      </div>
    </div>
    <div class="award-card">
      <div class="award-year">2010</div>
      <div class="award-body">
        <strong>Best Paper Award</strong>
        <p>International Meshing Roundtable — reactor core mesh generation</p>
      </div>
    </div>
    <div class="award-card">
      <div class="award-year">2007</div>
      <div class="award-body">
        <strong>Graduate Fellowship</strong>
        <p>Arizona State University — research assistantship in structural and computational mechanics</p>
      </div>
    </div>
  </div>
</section>


<section class="content-section" id="funding" style="--delay: 0.32s;">
  <h2>Research Funding</h2>
  <div class="funding-grid">
    <div class="funding-item">
      <span class="funding-status status-active">Active</span>
      <div class="funding-body">
        <strong>DOE SEATS</strong> — Software Ecosystem for Advancing Climate Tools and Services
      </div>
    </div>
    <div class="funding-item">
      <span class="funding-status status-active">Active</span>
      <div class="funding-body">
        <strong>NSF Raijin</strong> — Collaborative Research in Climate Model Analysis
      </div>
    </div>
    <div class="funding-item">
      <span class="funding-status status-completed">Completed</span>
      <div class="funding-body">
        <strong>DOE ECP CANDLE</strong> — Core contributor to Exascale Computing Project (2017–2023)
      </div>
    </div>
    <div class="funding-item">
      <span class="funding-status status-completed">Completed</span>
      <div class="funding-body">
        <strong>DOE NEAMS</strong> — Principal Investigator for MeshKit (2009–2016)
      </div>
    </div>
  </div>
</section>


<section class="content-section" id="service" style="--delay: 0.34s;">
  <h2>Service & Mentorship</h2>
  <div class="service-grid">
    <div class="service-column">
      <h4>Professional Service</h4>
      <div class="service-list">
        <div class="service-item"><strong>SBIR/STTR Proposal Reviewer</strong> — U.S. Department of Energy</div>
        <div class="service-item"><strong>Panelist</strong> — 5th Infraday Midwest Event ("Revolutionizing Public Infrastructure with AI")</div>
        <div class="service-item"><strong>Reviewer</strong> — Journal of Open Research Software, NumGrid</div>
        <div class="service-item"><strong>Committee</strong> — NumGrid 2020 Program Committee Member</div>
      </div>
    </div>
    <div class="service-column">
      <h4>Mentorship</h4>
      <div class="service-list">
        <div class="service-item"><strong>Rylie Weaver</strong> — Research Aide (2022–2024) · IMPROVE project, HPO techniques</div>
        <div class="service-item"><strong>Aaron Zedwick</strong> — Student (2023–2024) · UXarray development</div>
        <div class="service-item"><strong>Mark Bartoszek</strong> — Systems Admin (2023) · Mentoring on systems administration</div>
      </div>
    </div>
  </div>
</section>


<section class="content-section" id="background" style="--delay: 0.36s;">
  <h2>Background</h2>
  <div class="timeline-grid">
    <div class="timeline-item">
      <div class="timeline-period">2009 – present</div>
      <div class="timeline-body">
        <strong>Argonne National Laboratory</strong> — Principal Specialist, Research Software Engineering
        <p>Lead developer for UXarray, FLASH-X, CANDLE/IMPROVE, MeshKit, and urban simulation projects. Division of Mathematics and Computer Science.</p>
      </div>
    </div>
    <div class="timeline-item">
      <div class="timeline-period">2023 – present</div>
      <div class="timeline-body">
        <strong>University of Chicago</strong> — Staff At-Large
        <p>Joint appointment supporting cancer pharmacogenomics and earth science research. Mentor graduate students and research associates.</p>
      </div>
    </div>
    <div class="timeline-item">
      <div class="timeline-period">2007 – 2009</div>
      <div class="timeline-body">
        <strong>Arizona State University</strong> — Research & Teaching Assistant
        <p>Structural and Computational Mechanics Lab. Research on blast mitigation via FEM-based design optimization. TA for Structural Analysis and Design.</p>
      </div>
    </div>
    <div class="timeline-item">
      <div class="timeline-period">2006 – 2007</div>
      <div class="timeline-body">
        <strong>Wipro Technologies</strong> — Project Engineer
        <p>Software development in Bangalore, India.</p>
      </div>
    </div>
    <div class="timeline-item">
      <div class="timeline-period">2005</div>
      <div class="timeline-body">
        <strong>Tata Motors</strong> — Engineering Intern
        <p>Engineering internship in Pune, India.</p>
      </div>
    </div>
    <div class="timeline-item timeline-item--education">
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

<section class="content-section" id="contact" style="--delay: 0.38s;">
  <h2>Contact</h2>
  <p>Open to collaborations in scientific computing, AI for health, climate modeling, and open-source software. Always interested in connecting with researchers working on large-scale computational challenges.</p>
  <p><a href="mailto:rajeeja@gmail.com">rajeeja@gmail.com</a></p>
</section>
