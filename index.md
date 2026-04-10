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
      <p class="hero-role">I build research software for climate analysis, AI workflows, and large simulation codes at <a href="https://www.anl.gov/mcs">Argonne National Laboratory</a>, with a joint appointment at <a href="https://cs.uchicago.edu/">the University of Chicago</a>.</p>
      <p class="hero-summary">My work sits where scientific computing meets usable engineering: climate and mesh analysis, machine-learning infrastructure, high-performance I/O, and tools that researchers can actually extend. I care most about software that survives beyond a single project cycle.</p>

      <div class="hero-actions">
        <a class="button-link button-link--primary" href="#projects">View work</a>
        <a class="button-link" href="/blog/">Read technical notes</a>
        <a class="button-link" href="/files/Rajeev_Jain_CV.pdf">Curriculum Vitae</a>
      </div>

      <p class="hero-documents">
        <a class="hero-documents__link" href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en">Google Scholar</a>
        <span>&middot;</span>
        <a class="hero-documents__link" href="https://orcid.org/0000-0002-1235-918X">ORCID</a>
      </p>

      <p class="hero-meta">Argonne National Laboratory <span>&middot;</span> University of Chicago <span>&middot;</span> Climate, HPC, and AI systems</p>
    </div>

    <aside class="hero-panel">
      <img class="hero-portrait" src="/images/bio-photo.jpg" alt="Portrait of Rajeev Jain">
      <p class="hero-panel__eyebrow">Current focus</p>
      <ul class="panel-list">
        <li><a href="/blog/panguweather-aurora-climate-emulator/">Running AI weather models on Aurora's Intel GPU stack</a></li>
        <li><a href="https://github.com/UXARRAY/uxarray">Building UXarray for unstructured climate analysis</a></li>
        <li><a href="/blog/uxarray-mcp-improv-globus-compute/">Designing MCP workflows for scientific dataset exploration</a></li>
      </ul>

      <div class="mini-stats">
        <div class="mini-stat">
          <strong>16+</strong>
          <span>years in research software</span>
        </div>
        <div class="mini-stat">
          <strong>22+</strong>
          <span>peer-reviewed papers</span>
        </div>
        <div class="mini-stat">
          <strong>10k+</strong>
          <span>benchmark and HPO runs</span>
        </div>
      </div>
    </aside>
  </section>

  <section class="focus-strip" aria-label="Current featured work">
    <article class="focus-card">
      <p class="card-meta">Featured systems work</p>
      <h2><a href="/blog/panguweather-aurora-climate-emulator/">AI weather modeling on Aurora</a></h2>
      <p>Porting and stabilizing large weather-model training workflows on Intel GPUs, with attention to portability, runtime behavior, and scientific throughput.</p>
      <p class="focus-card__links"><a href="/blog/panguweather-aurora-climate-emulator/">Read note</a></p>
    </article>

    <article class="focus-card">
      <p class="card-meta">Open-source climate tooling</p>
      <h2><a href="https://github.com/UXARRAY/uxarray">UXarray</a></h2>
      <p>Mesh-aware analysis for next-generation climate grids, built so scientific users can inspect, subset, and reason about unstructured datasets without bespoke code for each mesh.</p>
      <p class="focus-card__links"><a href="https://uxarray.readthedocs.io">Documentation</a> &middot; <a href="https://github.com/UXARRAY/uxarray">Repository</a></p>
    </article>

    <article class="focus-card">
      <p class="card-meta">AI-agent workflows</p>
      <h2><a href="/blog/uxarray-mcp-improv-globus-compute/">Scientific MCP workflows</a></h2>
      <p>Natural-language dataset discovery, plotting, workflows, and remote execution for scientific analysis across local machines and HPC systems.</p>
      <p class="focus-card__links"><a href="/blog/uxarray-mcp-improv-globus-compute/">Read note</a></p>
    </article>
  </section>

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
          <li><a href="/blog/uxarray-mcp-improv-globus-compute/">Extending the project with an MCP server and AI-agent workflow for natural-language dataset exploration across local and HPC execution.</a></li>
        </ul>
        <p><a href="/blog/uxarray-mcp-improv-globus-compute/">Technical article</a> &middot; <a href="https://github.com/UXARRAY/uxarray-mcp-server">UXarray MCP server</a></p>
      </article>

      <article class="project-card">
        <p class="card-meta">Aurora exascale system | Argonne Leadership Computing Facility</p>
        <h3><a href="/blog/panguweather-aurora-climate-emulator/">Pangu-Weather on Aurora</a></h3>
        <p>PyTorch-based reimplementation of Pangu-Weather using the Spectral Fourier Neural Operator for deployment on more than 60,000 Intel GPUs.</p>
        <ul class="card-list">
          <li>Ported the workflow to Intel GPUs and ran it at large scale on Aurora.</li>
          <li>Contributed to DOE exascale work in Earth system modeling and forecasting.</li>
        </ul>
        <p><a href="/blog/panguweather-aurora-climate-emulator/">Technical article</a></p>
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
      <h2 class="section-title">Capabilities across scientific software and systems</h2>
      <p class="section-lead">A compact view of the engineering areas I work in most often, from ML and analysis pipelines to HPC runtime and open-source delivery.</p>
    </div>

    <div class="capability-grid">
      <article class="skill-card capability-card">
        <p class="card-meta">Scientific Python and ML</p>
        <h3>Data, models, and analysis workflows</h3>
        <ul class="card-list">
          <li>PyTorch, TensorFlow, NumPy, Pandas, Xarray, and Scikit-learn for model development and scientific analysis.</li>
          <li>Parsl and Swift/T for large experiment campaigns and repeatable workflow execution.</li>
        </ul>
      </article>

      <article class="skill-card capability-card">
        <p class="card-meta">HPC systems and storage</p>
        <h3>Performance, portability, and I/O</h3>
        <ul class="card-list">
          <li>MPI, OpenMP, HDF5, NetCDF, MOAB, and storage-aware design for leadership-class machines.</li>
          <li>Intel GPUs, CUDA portability, asynchronous checkpoint workflows, and runtime debugging on shared systems.</li>
        </ul>
      </article>

      <article class="skill-card capability-card">
        <p class="card-meta">Open-source delivery</p>
        <h3>Software other researchers can extend</h3>
        <ul class="card-list">
          <li>Release engineering, CI pipelines, testing, and packaging for long-lived scientific projects.</li>
          <li>Roadmap ownership, collaboration across labs and universities, and mentoring around sustainable engineering practice.</li>
        </ul>
      </article>

      <article class="skill-card capability-card">
        <p class="card-meta">Scientific domains</p>
        <h3>Problem-driven engineering</h3>
        <ul class="card-list">
          <li>Climate modeling, unstructured mesh analysis, cancer pharmacogenomics, computational physics, and simulation software.</li>
          <li>AI infrastructure and reproducible workflows built around domain constraints rather than generic demos.</li>
        </ul>
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
          <p class="section-kicker">Links</p>
          <h2 class="section-title">Profiles and research links.</h2>
          <p class="section-lead">I keep the public site fairly minimal. LinkedIn is the best route for professional outreach.</p>
          <div class="hero-actions">
            <a class="button-link button-link--primary" href="https://www.linkedin.com/in/rajeeja/">LinkedIn</a>
            <a class="button-link" href="https://github.com/rajeeja">GitHub</a>
            <a class="button-link" href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en">Google Scholar</a>
            <a class="button-link" href="https://orcid.org/0000-0002-1235-918X">ORCID</a>
          </div>
        </article>
      </div>
    </div>
  </section>
</div>
