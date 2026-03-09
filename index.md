---
layout: single
title: "Rajeev Jain"
permalink: /
author_profile: false
classes: wide
excerpt: "Research Software Engineer | ML Infrastructure | Scientific Computing"
---

<div class="landing-shell">
  <section class="hero-card" id="about">
    <div class="hero-copy">
      <p class="eyebrow">Research Software Engineer | ML Infrastructure | Scientific Computing</p>
      <h1 class="hero-title">Rajeev Jain</h1>
      <p class="hero-role">Research software engineer at <a href="https://www.anl.gov/mcs">Argonne National Laboratory</a>, with a joint appointment at <a href="https://cs.uchicago.edu/">the University of Chicago</a>.</p>
      <p class="hero-summary">I work on research software for climate analysis, AI workflows, and large simulation codes. Over 16 years I have built software across national labs, universities, and multi-institutional collaborations, with an emphasis on reliable tools that other researchers can use and extend.</p>

      <div class="hero-actions">
        <a class="button-link button-link--primary" href="/files/Rajeev_Jain_Resume.pdf">Resume</a>
        <a class="button-link" href="/files/Rajeev_Jain_CV.pdf">Full CV</a>
        <a class="button-link" href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en">All papers</a>
      </div>

      <div class="hero-stat-grid">
        <div class="hero-stat">
          <span class="hero-stat__value">16+</span>
          <span class="hero-stat__label">Years building research software</span>
        </div>
        <div class="hero-stat">
          <span class="hero-stat__value">22+</span>
          <span class="hero-stat__label">Peer-reviewed publications</span>
        </div>
        <div class="hero-stat">
          <span class="hero-stat__value">10k+</span>
          <span class="hero-stat__label">Training runs in benchmarking and HPO studies</span>
        </div>
      </div>
    </div>

    <aside class="hero-panel">
      <img class="hero-portrait" src="/images/bio-photo.jpg" alt="Portrait of Rajeev Jain">
      <p class="hero-panel__eyebrow">Current focus</p>
      <ul class="panel-list">
        <li>AI weather modeling on Aurora's Intel GPU stack</li>
        <li>UXarray for unstructured climate analysis and scientific workflows</li>
        <li>Benchmarking and optimization for distributed cancer AI pipelines</li>
      </ul>
    </aside>
  </section>

  <nav class="section-nav" id="section-nav">
    <div class="section-nav__inner">
      <a href="#about" class="section-nav__link">About</a>
      <a href="#projects" class="section-nav__link">Projects</a>
      <a href="#skills" class="section-nav__link">Skills</a>
      <a href="#publications" class="section-nav__link">Publications</a>
      <a href="#recognition" class="section-nav__link">Recognition</a>
      <a href="#background" class="section-nav__link">Background</a>
      <a href="#contact" class="section-nav__link">Contact</a>
    </div>
  </nav>

  <section class="content-section" id="projects">
    <div class="section-heading">
      <p class="section-kicker">Selected work</p>
      <h2 class="section-title">Selected projects</h2>
      <p class="section-lead">Representative work across climate science, cancer AI, and simulation software.</p>
    </div>

    <div class="project-grid">
      <article class="project-card project-card--wide">
        <p class="card-meta">Lead developer | Open-source climate analysis | <a href="https://uxarray.readthedocs.io">Documentation</a></p>
        <h3><a href="https://github.com/UXARRAY/uxarray">UXarray</a></h3>
        <p>Python library for unstructured climate grid analysis used by DOE labs, NCAR, and universities working with MPAS, ICON, SAM, and other next-generation meshes.</p>
        <ul class="card-list">
          <li>Built conservative analysis operators, including zonal averaging via Gauss-Legendre quadrature.</li>
          <li>Shipped support for ESMF, MPAS, SCRIP, and HEALPix grid formats, with repeatable releases and CI.</li>
          <li>Currently extending the project with an MCP server and AI-agent workflow for natural-language dataset exploration.</li>
        </ul>
      </article>

      <article class="project-card">
        <p class="card-meta">Aurora exascale system | Argonne Leadership Computing Facility</p>
        <h3><a href="https://www.anl.gov/aurora">Pangu-Weather on Aurora</a></h3>
        <p>PyTorch-based reimplementation of Pangu-Weather using the Spectral Fourier Neural Operator for deployment on more than 60,000 Intel GPUs.</p>
        <ul class="card-list">
          <li>Ported the workflow to Intel GPUs and ran it at large scale on Aurora.</li>
          <li>Contributed to DOE exascale work in Earth system modeling and forecasting.</li>
        </ul>
      </article>

      <article class="project-card">
        <p class="card-meta">Core contributor | Cancer AI benchmarking infrastructure</p>
        <h3><a href="https://github.com/JDACS4C-IMPROVE/IMPROVE">CANDLE / IMPROVE</a></h3>
        <p>Hyperparameter optimization and benchmarking infrastructure for cancer drug response models at supercomputer scale.</p>
        <ul class="card-list">
          <li>Ran more than 10,000 training experiments across Summit, Theta, and Cori.</li>
          <li>Built GitHub Actions workflows for cross-study validation in a 15+ researcher collaboration.</li>
          <li>Published in <a href="https://academic.oup.com/bib/article/27/1/bbaf667/7002013"><em>Briefings in Bioinformatics</em></a> in 2025.</li>
        </ul>
      </article>

      <article class="project-card">
        <p class="card-meta">I/O and compression work for multiphysics simulation</p>
        <h3><a href="https://flash-x.org/">FLASH-X</a></h3>
        <p>Optimization of checkpoint and restart workflows for a million-line multiphysics simulation engine used in astrophysics, combustion, and fluid dynamics.</p>
        <ul class="card-list">
          <li>Implemented asynchronous HDF5 I/O with Argobots plus SZ3 and ZFP compression.</li>
          <li>Reduced checkpoint overhead by 40-70% on Summit and delivered 50%+ storage savings.</li>
          <li>Enabled cross-checkpoint restart between AMReX and Paramesh solvers.</li>
        </ul>
      </article>

      <article class="project-card">
        <p class="card-meta">DOE NEAMS, 2009-2016</p>
        <h3><a href="https://bitbucket.org/fathomteam/meshkit">MeshKit</a></h3>
        <p>Open-source C++ toolkit for automated nuclear reactor core mesh generation and lattice hierarchy modeling.</p>
        <ul class="card-list">
          <li>Led the design of parallel meshing and multi-format I/O for reactor simulation teams at Argonne.</li>
          <li>Won Best Paper Award at the International Meshing Roundtable in 2010.</li>
        </ul>
      </article>
    </div>
  </section>

  <section class="content-section" id="skills">
    <div class="section-heading">
      <p class="section-kicker">Technical expertise</p>
      <h2 class="section-title">Breadth across research software and systems</h2>
      <p class="section-lead">Tools and systems I work with most often across research software, data, and HPC.</p>
    </div>

    <div class="skill-grid">
      <article class="skill-card">
        <p class="card-meta">Languages</p>
        <h3>Python to Fortran</h3>
        <p>Python, C++, Fortran, R, Bash, and SQL for analysis pipelines, simulation code, build systems, and automation.</p>
      </article>

      <article class="skill-card">
        <p class="card-meta">ML and data</p>
        <h3>Framework and workflow depth</h3>
        <p>PyTorch, TensorFlow, NumPy, Pandas, Xarray, Scikit-learn, Parsl, and Swift/T for model development and large experiment campaigns.</p>
      </article>

      <article class="skill-card">
        <p class="card-meta">HPC and systems</p>
        <h3>Performance and portability</h3>
        <p>MPI, OpenMP, HDF5, NetCDF, MOAB, Docker, Singularity, GitHub Actions, and storage-aware I/O design for leadership-class machines.</p>
      </article>

      <article class="skill-card">
        <p class="card-meta">Domains</p>
        <h3>Science-driven software</h3>
        <p>Climate modeling, cancer pharmacogenomics, computational physics, mesh generation, AI infrastructure, and reproducible workflows.</p>
      </article>

      <article class="skill-card">
        <p class="card-meta">Leadership and delivery</p>
        <h3>Software that lasts</h3>
        <p>Release engineering, CI pipelines, open-source governance, multi-institution coordination, mentoring, and roadmap ownership.</p>
      </article>
    </div>
  </section>

  <section class="content-section" id="publications">
    <div class="section-heading">
      <p class="section-kicker">Publications and talks</p>
      <h2 class="section-title">Selected papers, workshops, and presentations</h2>
      <p class="section-lead">More than 22 publications across HPC, machine learning, and computational science.</p>
    </div>

    <div class="split-grid">
      <div class="publication-list">
        <article class="publication-card">
          <p class="card-meta">Briefings in Bioinformatics | 2025</p>
          <h3><a href="https://academic.oup.com/bib/article/27/1/bbaf667/7002013">Benchmarking community drug response prediction models</a></h3>
          <p>Partin, A., ..., <strong>Jain, R.</strong>, et al.</p>
        </article>

        <article class="publication-card">
          <p class="card-meta">DRBSD-10 Workshop, SC24</p>
          <h3><a href="https://doi.org/10.1109/SCW63240.2024.00043">Enabling Data Reduction for FLASH-X Simulations</a></h3>
          <p><strong>Jain, R.</strong>, Tang, H., Dhruv, A., Byna, S.</p>
        </article>

        <article class="publication-card">
          <p class="card-meta">CAFCW24 Workshop, SC24</p>
          <h3><a href="https://web.cels.anl.gov/~woz/papers/IMPROVE_HPO_2024.pdf">Cross-HPO: Optimizing Neural Networks for Cancer Drug Response</a></h3>
          <p><strong>Jain, R.</strong>, Wozniak, J.M., Partin, A., et al.</p>
        </article>

        <article class="publication-card">
          <p class="card-meta">BMC Bioinformatics | 2018</p>
          <h3><a href="https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2508-4">CANDLE/Supervisor: A workflow framework for machine learning applied to cancer research</a></h3>
          <p>Wozniak, J.M., ..., <strong>Jain, R.</strong>, et al.</p>
        </article>

        <article class="publication-card">
          <p class="card-meta">Engineering with Computers | 2011</p>
          <h3><a href="https://doi.org/10.1007/s00366-011-0236-8">Creating Geometry and Mesh Models for Nuclear Reactor Core Geometries</a></h3>
          <p>Tautges, T.J., <strong>Jain, R.</strong></p>
        </article>
      </div>

      <aside class="side-card">
        <p class="card-meta">Recent presentations</p>
        <ul class="timeline-list">
          <li>
            <strong>SC24</strong>
            <span>Tutorial: UXarray for Analysis of Unstructured Climate Data</span>
          </li>
          <li>
            <strong>SC24</strong>
            <span>DRBSD-10: Enabling Data Reduction for FLASH-X Simulations</span>
          </li>
          <li>
            <strong>SC24</strong>
            <span>CAFCW24: Cross-HPO for Cancer Drug Response</span>
          </li>
          <li>
            <strong>AMS 2024</strong>
            <span>UXarray: Extending Xarray with Support for Unstructured Grids</span>
          </li>
          <li>
            <strong>SciPy 2023</strong>
            <span><a href="https://www.youtube.com/watch?v=qwqJeOO8m6A">UXarray for Unstructured Climate Data</a></span>
          </li>
          <li>
            <strong>HDF User Group 2023</strong>
            <span><a href="https://www.youtube.com/watch?v=MuifQ7lHRR8">Data Reduction for FLASH-X Simulations</a></span>
          </li>
        </ul>

        <p class="side-card__copy">For the full publication record, citations, and profile links, use the sources below.</p>
        <div class="stacked-links">
          <a class="button-link" href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en">Google Scholar</a>
          <a class="button-link" href="https://orcid.org/0000-0002-1235-918X">ORCID</a>
        </div>
      </aside>
    </div>
  </section>

  <section class="content-section" id="recognition">
    <div class="section-heading">
      <p class="section-kicker">Recognition</p>
      <h2 class="section-title">Recognition and service</h2>
      <p class="section-lead">Awards, funding, and community work related to the software and collaborations above.</p>
    </div>

    <div class="recognition-grid">
      <article class="detail-card">
        <p class="card-meta">Work authorization</p>
        <h3>U.S. Permanent Resident</h3>
        <p>Authorized to work in the United States without sponsorship.</p>
      </article>

      <article class="detail-card">
        <p class="card-meta">R&amp;D 100 | 2023</p>
        <h3><a href="https://www.rdworldonline.com/candle-cancer-distributed-learning-environment-is-the-rd-100-winner-of-the-day/">CANDLE</a></h3>
        <p>Project recognized by R&amp;D World in 2023.</p>
      </article>

      <article class="detail-card">
        <p class="card-meta">R&amp;D 100 | 2022</p>
        <h3><a href="https://www.rdworldonline.com/rd-100-2022-winner/flash-x-a-multiphysics-simulation-software/">FLASH-X</a></h3>
        <p>Project recognized by R&amp;D World in 2022.</p>
      </article>

      <article class="detail-card">
        <p class="card-meta">Training and technical distinction</p>
        <h3>ATPESC Scholar</h3>
        <p>Selected in 2015 for Argonne's training program on extreme-scale computing.</p>
      </article>

      <article class="detail-card">
        <p class="card-meta">Research publication</p>
        <h3>Best Paper Award</h3>
        <p>International Meshing Roundtable, 2010, for automated reactor core mesh generation research.</p>
      </article>
    </div>

    <div class="split-grid split-grid--compact">
      <article class="detail-card">
        <p class="card-meta">Research funding</p>
        <ul class="clean-list">
          <li><strong>DOE SEATS</strong> <span class="status-pill">Active</span> Software Ecosystem for Advancing Climate Tools and Services.</li>
          <li><strong>NSF Raijin</strong> <span class="status-pill">Active</span> Collaborative research in climate model analysis.</li>
          <li><strong>DOE ECP CANDLE</strong> Core contributor from 2017 to 2023.</li>
          <li><strong>DOE NEAMS</strong> Principal investigator for MeshKit from 2009 to 2016.</li>
        </ul>
      </article>

      <article class="detail-card">
        <p class="card-meta">Service and mentorship</p>
        <ul class="clean-list">
          <li><strong>SBIR/STTR Proposal Reviewer</strong> U.S. Department of Energy.</li>
          <li><strong>Panelist</strong> 5th Infraday Midwest Event on public infrastructure and AI.</li>
          <li><strong>Reviewer</strong> Journal of Open Research Software and NumGrid.</li>
          <li><strong>Committee Member</strong> NumGrid 2020 Program Committee.</li>
        </ul>
        <p>Mentored students and doctoral researchers on scientific Python, HPC techniques, and open-source development practices.</p>
      </article>
    </div>
  </section>

  <section class="content-section" id="background">
    <div class="section-heading">
      <p class="section-kicker">Background</p>
      <h2 class="section-title">Roles, education, and collaboration style</h2>
      <p class="section-lead">Research roles across labs and universities, centered on long-lived software and collaborative delivery.</p>
    </div>

    <div class="split-grid">
      <article class="detail-card">
        <p class="card-meta">Roles</p>
        <div class="timeline">
          <div class="timeline-item">
            <p class="timeline-item__range">2009-present</p>
            <div>
              <h3>Argonne National Laboratory</h3>
              <p>Principal Specialist in Research Software Engineering, working across UXarray, FLASH-X, CANDLE/IMPROVE, MeshKit, and urban simulation software efforts.</p>
            </div>
          </div>

          <div class="timeline-item">
            <p class="timeline-item__range">2023-present</p>
            <div>
              <h3>University of Chicago</h3>
              <p>Staff At-Large with joint research activity spanning cancer pharmacogenomics and Earth system science.</p>
            </div>
          </div>

          <div class="timeline-item">
            <p class="timeline-item__range">2007-2009</p>
            <div>
              <h3>Arizona State University</h3>
              <p>Research and teaching assistant in structural and computational mechanics, focused on blast mitigation and FEM-based design optimization.</p>
            </div>
          </div>
        </div>
      </article>

      <div class="stacked-column">
        <article class="detail-card">
          <p class="card-meta">Education</p>
          <ul class="timeline-list">
            <li>
              <strong>M.S. Computer Science</strong>
              <span>University of Chicago, 2020</span>
            </li>
            <li>
              <strong>M.S. Structural Engineering</strong>
              <span>Arizona State University, 2009</span>
            </li>
            <li>
              <strong>B.Tech. Mechanical Engineering</strong>
              <span>IIT ISM Dhanbad, 2006</span>
            </li>
          </ul>
        </article>

        <article class="contact-card" id="contact">
          <p class="section-kicker">Contact</p>
          <h2 class="section-title">Available for conversations about research software and scientific computing.</h2>
          <p class="section-lead">I am interested in work across scientific computing, AI for health, climate modeling, reproducible workflows, and long-lived open-source systems.</p>
          <div class="hero-actions">
            <a class="button-link" href="mailto:rajeeja@gmail.com">rajeeja@gmail.com</a>
            <a class="button-link" href="https://www.linkedin.com/in/rajeeja/">LinkedIn</a>
            <a class="button-link" href="https://github.com/rajeeja">GitHub</a>
            <a class="button-link" href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en">Google Scholar</a>
            <a class="button-link" href="https://orcid.org/0000-0002-1235-918X">ORCID</a>
          </div>
        </article>
      </div>
    </div>
  </section>
</div>
