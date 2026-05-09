---
layout: single
title: "Rajeev Jain"
permalink: /
author_profile: false
classes: wide
excerpt: "Principal Software Engineer | ML Infrastructure | HPC | Scientific Computing"
---

<div class="landing-shell">
  <section class="hero-card" id="about">
    <div class="hero-copy">
      <p class="eyebrow">Principal Software Engineer &middot; ML Infrastructure &middot; HPC &middot; Scientific Computing</p>
      <h1 class="hero-title">Rajeev Jain</h1>
      <p class="hero-role">I build and ship production software at the intersection of scientific computing, ML infrastructure, and high-performance systems at <a href="https://www.anl.gov/mcs">Argonne National Laboratory</a>, with a joint appointment at <a href="https://cs.uchicago.edu/">the University of Chicago</a>.</p>
      <p class="hero-summary">I focus on the gap between prototype and production: getting parallel training stable on new accelerator hardware, designing I/O that doesn't bottleneck at scale, building Python platforms that teams can actually extend and maintain. I've led multi-institution software efforts from architecture through delivery and stay in the picture until the system works.</p>

      <div class="hero-actions">
        <a class="button-link button-link--primary" href="#projects">View work</a>
        <a class="button-link" href="/blog/">Technical notes</a>
        <a class="button-link" href="/files/Rajeev_Jain_CV.pdf">Curriculum Vitae</a>
      </div>

      <p class="hero-documents">
        <a class="hero-documents__link" href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en">Google Scholar</a>
        <span>&middot;</span>
        <a class="hero-documents__link" href="https://orcid.org/0000-0002-1235-918X">ORCID</a>
      </p>

      <p class="hero-meta">Argonne National Laboratory <span>&middot;</span> University of Chicago <span>&middot;</span> Climate &middot; HPC &middot; AI systems</p>
    </div>

    <aside class="hero-panel">
      <img class="hero-portrait" src="/images/bio-photo.jpg" alt="Portrait of Rajeev Jain">
      <p class="hero-panel__eyebrow">Current focus</p>
      <ul class="panel-list">
        <li><a href="/blog/panguweather-aurora-climate-emulator/">Running AI weather models on Aurora's Intel GPU stack</a></li>
        <li><a href="https://github.com/UXARRAY/uxarray">Lead developer of UXarray for unstructured climate analysis</a></li>
        <li><a href="/blog/uxarray-mcp-improv-globus-compute/">Designing MCP/AI-agent workflows for HPC scientific datasets</a></li>
      </ul>

      <div class="mini-stats">
        <div class="mini-stat">
          <strong>16+</strong>
          <span>years in research software</span>
        </div>
        <div class="mini-stat">
          <strong>2&times;</strong>
          <span>R&amp;D 100 Award winner</span>
        </div>
        <div class="mini-stat">
          <strong>10k+</strong>
          <span>ML training runs coordinated</span>
        </div>
      </div>
    </aside>
  </section>

  <section class="focus-strip" aria-label="Current featured work">
    <article class="focus-card">
      <p class="card-meta">Exascale ML systems work</p>
      <h2><a href="/blog/panguweather-aurora-climate-emulator/">AI weather modeling on Aurora</a></h2>
      <p>Stable DDP-based training on 60,000+ Intel GPUs — portable PyTorch climate workflow across CUDA and Intel XPU, with checkpoint/restart contracts and queue-aware smoke tests.</p>
      <p class="focus-card__links"><a href="/blog/panguweather-aurora-climate-emulator/">Read note</a></p>
    </article>

    <article class="focus-card">
      <p class="card-meta">Open-source climate tooling</p>
      <h2><a href="https://github.com/UXARRAY/uxarray">UXarray</a></h2>
      <p>The standard Python library for DOE unstructured climate grid analysis — adopted by Argonne, NCAR, and universities. Conservative operators, multi-format I/O, full CI/release pipeline.</p>
      <p class="focus-card__links"><a href="https://uxarray.readthedocs.io">Documentation</a> &middot; <a href="https://github.com/UXARRAY/uxarray">Repository</a></p>
    </article>

    <article class="focus-card">
      <p class="card-meta">AI-agent HPC workflows</p>
      <h2><a href="/blog/uxarray-mcp-improv-globus-compute/">Scientific MCP server</a></h2>
      <p>Natural-language mesh discovery, subsetting, and visualization across laptop and HPC — production meshes stay on facility storage, only compact JSON and PNGs return.</p>
      <p class="focus-card__links"><a href="/blog/uxarray-mcp-improv-globus-compute/">Read note</a></p>
    </article>
  </section>

  <section class="content-section" id="projects">
    <div class="section-heading">
      <p class="section-kicker">Selected work</p>
      <h2 class="section-title">Systems I've shipped</h2>
      <p class="section-lead">Production software across exascale ML, climate analysis, cancer AI, and simulation infrastructure — with a clear problem, technical approach, and measurable outcome in each case.</p>
    </div>

    <div class="project-grid">
      <article class="project-card project-card--wide">
        <p class="card-meta">Lead developer | Open-source climate analysis | <a href="https://uxarray.readthedocs.io">Documentation</a></p>
        <h3><a href="https://github.com/UXARRAY/uxarray">UXarray</a></h3>
        <p>Python library for unstructured climate grid analysis — the standard tool for DOE labs, NCAR, and universities working with MPAS, ICON, SAM, and next-generation meshes.</p>
        <ul class="card-list">
          <li>Designed and shipped conservative analysis operators including zonal averaging via Gauss-Legendre quadrature — numerics that determine whether results are scientifically correct.</li>
          <li>Built grid I/O for ESMF, MPAS, SCRIP, and HEALPix formats, with repeatable releases and CI across multiple national labs.</li>
          <li><a href="/blog/uxarray-mcp-improv-globus-compute/">Extended with an MCP server and AI-agent workflow for natural-language dataset exploration across local and HPC execution.</a></li>
        </ul>
      </article>

      <article class="project-card">
        <p class="card-meta">Aurora exascale system | 60,000+ Intel GPUs | Argonne Leadership Computing Facility</p>
        <h3><a href="/blog/panguweather-aurora-climate-emulator/">Pangu-Weather on Aurora</a></h3>
        <p>PyTorch reimplementation of Pangu-Weather using the Spectral Fourier Neural Operator for DOE exascale Earth system modeling.</p>
        <ul class="card-list">
          <li>Established the first stable portable DDP baseline on Aurora — PMIX/PALS environment mapping, XPU/CUDA device branching, and checkpoint/restart as a hard contract.</li>
          <li>Identified the concrete next steps before any sharded-training complexity is warranted.</li>
        </ul>
        <p><a href="/blog/panguweather-aurora-climate-emulator/">Technical article</a></p>
      </article>

      <article class="project-card">
        <p class="card-meta">Core contributor | R&amp;D 100 Award 2023 | Cancer AI benchmarking</p>
        <h3><a href="https://github.com/JDACS4C-IMPROVE/IMPROVE">CANDLE / IMPROVE</a></h3>
        <p>HPO and benchmarking infrastructure for cancer drug response models — 15+ researcher collaboration across Argonne, LLNL, and ORNL.</p>
        <ul class="card-list">
          <li>Coordinated 10,000+ training experiments across Summit, Theta, and Cori using Parsl and Swift/T.</li>
          <li>Built GitHub Actions workflows for automated cross-study validation. Published in <a href="https://academic.oup.com/bib/article/27/1/bbaf667/7002013"><em>Briefings in Bioinformatics</em></a> 2025.</li>
        </ul>
      </article>

      <article class="project-card">
        <p class="card-meta">I/O and compression lead | R&amp;D 100 Award 2022 | Multiphysics simulation</p>
        <h3><a href="https://flash-x.org/">FLASH-X</a></h3>
        <p>Checkpoint and restart redesign for a million-line multiphysics engine used in astrophysics, combustion, and fluid dynamics.</p>
        <ul class="card-list">
          <li>Async HDF5 with Argobots plus SZ3/ZFP compression: 40–70% checkpoint overhead reduction and 50%+ storage savings on Summit.</li>
          <li>Enabled cross-checkpoint restart between AMReX and Paramesh — removing a hard constraint that forced full restarts when switching solvers.</li>
        </ul>
      </article>

      <article class="project-card">
        <p class="card-meta">PI and software lead | DOE NEAMS | Best Paper, IMR 2010</p>
        <h3><a href="https://bitbucket.org/fathomteam/meshkit">MeshKit</a></h3>
        <p>Open-source C++ toolkit for automated nuclear reactor core mesh generation — designed, led, and delivered through DOE NEAMS from 2009 to 2016.</p>
        <ul class="card-list">
          <li>Parallel CoreGen: 712 processors, 101 million hexahedral elements, 14 GB MONJU reactor mesh in under 7 minutes — a job the serial path couldn't run at all.</li>
        </ul>
        <p><a href="/blog/rgg-meshkit-moose-reactor-module/">RGG / MeshKit retrospective</a> &middot; <a href="https://bitbucket.org/fathomteam/meshkit">Source</a></p>
      </article>
    </div>
  </section>

  <section class="content-section" id="skills">
    <div class="section-heading">
      <p class="section-kicker">Technical depth</p>
      <h2 class="section-title">What I deliver</h2>
      <p class="section-lead">Full-stack technical depth from ML training to HPC I/O, with a track record of shipping software that teams adopt and extend.</p>
    </div>

    <div class="capability-grid">
      <article class="skill-card capability-card">
        <p class="card-meta">ML infrastructure</p>
        <h3>Training pipelines that reach production</h3>
        <ul class="card-list">
          <li>Distributed training across CUDA and Intel XPU — DDP baseline, launcher portability (MPI/PMIx/PALS/torchrun), mixed-precision policy, activation checkpointing.</li>
          <li>10,000+ HPO runs coordinated across Summit, Theta, and Cori through Parsl and Swift/T — reproducible experiment infrastructure, not ad-hoc scripts.</li>
        </ul>
      </article>

      <article class="skill-card capability-card">
        <p class="card-meta">HPC systems and I/O</p>
        <h3>Performance engineering on leadership machines</h3>
        <ul class="card-list">
          <li>Async HDF5 with Argobots, MPI-IO tuning, SZ3/ZFP compression, storage layout optimization — 40–70% checkpoint overhead reduction on Summit.</li>
          <li>Cross-checkpoint restart across solver stacks, runtime debugging on Argonne/ORNL/NERSC systems, Globus Compute for remote-execution workflows.</li>
        </ul>
      </article>

      <article class="skill-card capability-card">
        <p class="card-meta">Platform ownership</p>
        <h3>Open-source software that outlives the grant</h3>
        <ul class="card-list">
          <li>API design, grid I/O, conservative numerical operators, release engineering, CI, and packaging — led UXarray from initial design to adoption by DOE labs, NCAR, and universities.</li>
          <li>PI on DOE NEAMS MeshKit: full lifecycle from architecture through public release and community onboarding.</li>
        </ul>
      </article>

      <article class="skill-card capability-card">
        <p class="card-meta">Multi-institution delivery</p>
        <h3>Technical lead across labs and programs</h3>
        <ul class="card-list">
          <li>Led 15+ researcher cross-lab collaborations at Argonne, LLNL, and ORNL — architecture decisions, roadmap ownership, and delivery on DOE program timelines.</li>
          <li>Domains: climate and Earth system modeling, cancer pharmacogenomics AI, computational physics, exascale simulation, unstructured mesh analysis.</li>
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
            <span><a href="https://uxarray.readthedocs.io/">Tutorial: UXarray for Analysis of Unstructured Climate Data</a></span>
          </li>
          <li>
            <strong>SC24</strong>
            <span><a href="https://doi.org/10.1109/SCW63240.2024.00043">DRBSD-10: Enabling Data Reduction for FLASH-X Simulations</a></span>
          </li>
          <li>
            <strong>SC24</strong>
            <span><a href="https://sc24.conference-program.com/presentation/?id=ws_cafcw105&sess=sess764">CAFCW24: Cross-HPO for Cancer Drug Response</a></span>
          </li>
          <li>
            <strong>AMS 2024</strong>
            <span><a href="https://ams.confex.com/ams/104ANNUAL/meetingapp.cgi/Paper/434638">UXarray: Extending Xarray with Support for Unstructured Grids</a></span>
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
        <p>R&amp;D 100 Award for cancer AI infrastructure spanning Argonne, LLNL, and ORNL.</p>
      </article>

      <article class="detail-card">
        <p class="card-meta">R&amp;D 100 | 2022</p>
        <h3><a href="https://www.rdworldonline.com/rd-100-2022-winner/flash-x-a-multiphysics-simulation-software/">FLASH-X</a></h3>
        <p>R&amp;D 100 Award for the multiphysics simulation engine used in astrophysics and combustion research.</p>
      </article>

      <article class="detail-card">
        <p class="card-meta">Training and technical distinction</p>
        <h3>ATPESC Scholar</h3>
        <p>Selected in 2015 for Argonne's training program on extreme-scale computing methods.</p>
      </article>

      <article class="detail-card">
        <p class="card-meta">Best Paper | IMR 2010</p>
        <h3>International Meshing Roundtable</h3>
        <p>First-author paper on automated reactor core mesh generation with lattice hierarchy encoding.</p>
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
          <li><strong>Panelist</strong> Infraday Midwest on public infrastructure and AI.</li>
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
      <p class="section-lead">Research roles across labs and universities, centered on long-lived software and technical delivery in multi-institution programs.</p>
    </div>

    <div class="split-grid">
      <article class="detail-card">
        <p class="card-meta">Roles</p>
        <div class="timeline">
          <div class="timeline-item">
            <p class="timeline-item__range">2009-present</p>
            <div>
              <h3>Argonne National Laboratory</h3>
              <p>Principal Specialist in Research Software Engineering — technical lead across UXarray, FLASH-X, CANDLE/IMPROVE, Pangu-Weather on Aurora, MeshKit, and urban simulation software programs.</p>
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
