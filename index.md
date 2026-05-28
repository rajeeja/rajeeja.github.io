---
layout: single
title: "Rajeev Jain"
permalink: /
author_profile: false
classes: wide
excerpt: "Principal Software Engineer | ML Infrastructure | HPC | Scientific Computing"
---

<div class="cv" id="about">

<header class="cv-head">
  <div class="cv-head__copy">
    <h1 class="cv-name">Rajeev Jain</h1>
    <p class="cv-tagline">Principal Software Engineer &middot; ML Infrastructure &middot; HPC &middot; Scientific Computing</p>
    <p class="cv-bio">The gap between prototype and production is where I work &mdash; ML training pipelines that scale on new accelerator hardware, I/O that doesn&rsquo;t bottleneck at exascale, Python platforms that research teams can actually maintain across institutions and years. Principal Specialist at <a href="https://www.anl.gov/mcs">Argonne National Laboratory</a>, with a joint appointment at <a href="https://cs.uchicago.edu/">the University of Chicago</a>.</p>
    <p class="cv-links">
      <a href="/files/Rajeev_Jain_CV.pdf">CV</a>
      <a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en">Google Scholar</a>
      <a href="https://github.com/rajeeja">GitHub</a>
      <a href="https://www.linkedin.com/in/rajeeja/">LinkedIn</a>
      <a href="https://orcid.org/0000-0002-1235-918X">ORCID</a>
    </p>
  </div>
  <img class="cv-portrait" src="/images/bio-photo.jpg" alt="Rajeev Jain">
</header>

<section class="cv-section" id="projects">
  <h2 class="cv-label">Work</h2>
  <ul class="cv-items">
    <li>
      <div class="item-head"><strong><a href="https://github.com/UXARRAY/uxarray">UXarray</a></strong><span class="item-role">Lead developer &middot; open-source climate analysis</span></div>
      Python library for unstructured climate grid analysis &mdash; the standard tool for DOE labs, NCAR, and universities working with MPAS, ICON, SAM, and next-generation meshes. Conservative zonal averaging via Gauss-Legendre quadrature; grid I/O for ESMF, MPAS, SCRIP, and HEALPix; MCP server for AI-agent dataset exploration across local and HPC execution.
      <span class="item-links"><a href="https://uxarray.readthedocs.io">Docs</a> &middot; <a href="https://github.com/UXARRAY/uxarray">GitHub</a> &middot; <a href="/blog/uxarray-mcp-improv-globus-compute/">MCP article</a></span>
    </li>
    <li>
      <div class="item-head"><strong><a href="/blog/panguweather-aurora-climate-emulator/">Pangu-Weather on Aurora</a></strong><span class="item-role">60,000+ Intel GPUs &middot; Argonne Leadership Computing Facility</span></div>
      PyTorch reimplementation of Pangu-Weather using the Spectral Fourier Neural Operator for DOE exascale Earth system modeling. First stable portable DDP baseline on Aurora: PMIX/PALS environment mapping, XPU/CUDA device branching, device-aware mixed precision with gradient scaling on CUDA and bf16 on Intel XPU.
      <span class="item-links"><a href="/blog/panguweather-aurora-climate-emulator/">Article</a></span>
    </li>
    <li>
      <div class="item-head"><strong><a href="https://github.com/JDACS4C-IMPROVE/IMPROVE">CANDLE / IMPROVE</a></strong><span class="item-role">Core contributor &middot; R&amp;D 100 Award 2023</span></div>
      HPO and benchmarking infrastructure for cancer drug response models &mdash; 15+ researchers across Argonne, LLNL, and ORNL. 10,000+ training experiments across Summit, Theta, and Cori using Swift/T. Published in <a href="https://academic.oup.com/bib/article/27/1/bbaf667/7002013"><em>Briefings in Bioinformatics</em></a>, 2025.
    </li>
    <li>
      <div class="item-head"><strong><a href="https://flash-x.org/">FLASH-X</a></strong><span class="item-role">I/O and compression lead &middot; R&amp;D 100 Award 2022</span></div>
      Checkpoint and restart redesign for a million-line multiphysics engine. Async HDF5 with Argobots plus SZ3/ZFP compression: 40&ndash;70% checkpoint overhead reduction and 50%+ storage savings on Summit. Cross-checkpoint restart between AMReX and Paramesh &mdash; removing a hard constraint that forced full restarts when switching solvers.
      <span class="item-links"><a href="https://doi.org/10.1109/SCW63240.2024.00043">SC24 paper</a></span>
    </li>
    <li>
      <div class="item-head"><strong><a href="https://bitbucket.org/fathomteam/meshkit">MeshKit</a></strong><span class="item-role">PI and software lead &middot; DOE NEAMS &middot; 2009&ndash;2016</span></div>
      Open-source C++ toolkit for automated nuclear reactor core mesh generation. Parallel CoreGen: 712 processors, 101 million hexahedral elements, 14 GB MONJU reactor mesh in under 7 minutes &mdash; a job the serial path couldn&rsquo;t run at all.
      <span class="item-links"><a href="/blog/rgg-meshkit-moose-reactor-module/">Blog post</a> &middot; <a href="https://bitbucket.org/fathomteam/meshkit">Source</a></span>
    </li>
  </ul>
</section>

<section class="cv-section" id="writing">
  <h2 class="cv-label">Writing</h2>
  <ul class="cv-items cv-items--compact">
    <li>
      <span class="item-venue">2026</span>
      <a href="/blog/uxarray-mcp-improv-globus-compute/">UXarray MCP Server: AI-Agent Dataset Exploration with Globus Compute</a>
      <span class="item-dek">How the UXarray MCP server lets AI agents explore, analyze, and visualize unstructured climate grids — locally and on HPC via Globus Compute.</span>
    </li>
    <li>
      <span class="item-venue">2025</span>
      <a href="/blog/improve-benchmark-infrastructure/">IMPROVE: Building Rigorous Benchmark Infrastructure for Cancer Drug Response Prediction</a>
      <span class="item-dek">The improvelib package, cross-study analysis framework, GitHub Actions CI/CD, and the UNO dual-branch neural network for drug response prediction.</span>
    </li>
    <li>
      <span class="item-venue">2024</span>
      <a href="/blog/panguweather-aurora-climate-emulator/">Pangu-Weather on Aurora: Porting a Weather Foundation Model to 60,000 Intel GPUs</a>
      <span class="item-dek">Device abstraction, DDP setup, PMIX/PALS environment mapping, and mixed-precision on Intel XPU to get a stable training baseline on Aurora.</span>
    </li>
    <li>
      <span class="item-venue">2023</span>
      <a href="/blog/rgg-meshkit-moose-reactor-module/">From RGG and MeshKit to the MOOSE Reactor Module</a>
      <span class="item-dek">Parallel CoreGen generated a 101M-element MONJU reactor mesh on 712 processors in under 7 minutes — a job the serial path couldn't run at all.</span>
    </li>
    <li>
      <span class="item-venue">2022</span>
      <a href="/blog/candle-counterfactuals-hpo/">CANDLE/Supervisor: Running Cancer AI Research at Scale on DOE Supercomputers</a>
      <span class="item-dek">mlrMBO, DEAP, Hyperopt, and Swift/T ran 10,000+ experiments on Summit; noise injection and counterfactuals revealed which genes drive tumor classification.</span>
    </li>
    <li>
      <span class="item-venue">2020</span>
      <a href="/blog/urban-ecp-array-of-things/">Urban Microclimate at Scale: Array of Things, EnergyPlus, and CFD for Chicago</a>
      <span class="item-dek">Coupling Chicago's IoT sensor network, WRF mesoscale weather, EnergyPlus building simulation, and Nek5000 wall-resolved LES into a city-scale workflow.</span>
    </li>
  </ul>
</section>

<section class="cv-section" id="publications">
  <h2 class="cv-label">Selected papers</h2>
  <ul class="cv-items">
    <li>Partin, A., ..., <strong>Jain, R.</strong>, et al. <a href="https://academic.oup.com/bib/article/27/1/bbaf667/7002013">Benchmarking community drug response prediction models.</a> <em>Briefings in Bioinformatics</em>, 2025.</li>
    <li><strong>Jain, R.</strong>, Tang, H., Dhruv, A., Byna, S. <a href="https://doi.org/10.1109/SCW63240.2024.00043">Enabling Data Reduction for FLASH-X Simulations.</a> DRBSD-10 Workshop, SC24, 2024.</li>
    <li><strong>Jain, R.</strong>, Wozniak, J.M., Partin, A., et al. <a href="https://web.cels.anl.gov/~woz/papers/IMPROVE_HPO_2024.pdf">Cross-HPO: Optimizing Neural Networks for Cancer Drug Response.</a> CAFCW24, SC24, 2024.</li>
    <li>Wozniak, J.M., ..., <strong>Jain, R.</strong>, et al. <a href="https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2508-4">CANDLE/Supervisor: A workflow framework for machine learning applied to cancer research.</a> <em>BMC Bioinformatics</em>, 2018.</li>
    <li>Tautges, T.J., <strong>Jain, R.</strong> <a href="https://doi.org/10.1007/s00366-011-0236-8">Creating Geometry and Mesh Models for Nuclear Reactor Core Geometries.</a> <em>Engineering with Computers</em>, 2011.</li>
  </ul>
  <p class="cv-more"><a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en">Full list on Google Scholar</a> &middot; 22+ publications</p>

  <h2 class="cv-label cv-label--sub">Recent talks</h2>
  <ul class="cv-items cv-items--compact">
    <li><span class="item-venue">SciFM26</span> Presented UXarray MCP Server for agentic analysis of unstructured Earth-system meshes</li>
    <li><span class="item-venue">SC24</span> <a href="https://uxarray.readthedocs.io/">Tutorial: UXarray for Analysis of Unstructured Climate Data</a></li>
    <li><span class="item-venue">SC24</span> <a href="https://doi.org/10.1109/SCW63240.2024.00043">DRBSD-10: Enabling Data Reduction for FLASH-X</a></li>
    <li><span class="item-venue">SC24</span> <a href="https://sc24.conference-program.com/presentation/?id=ws_cafcw105&amp;sess=sess764">CAFCW24: Cross-HPO for Cancer Drug Response</a></li>
    <li><span class="item-venue">AMS 2024</span> <a href="https://ams.confex.com/ams/104ANNUAL/meetingapp.cgi/Paper/434638">UXarray: Extending Xarray with Support for Unstructured Grids</a></li>
    <li><span class="item-venue">SciPy 2023</span> <a href="https://www.youtube.com/watch?v=qwqJeOO8m6A">UXarray for Unstructured Climate Data</a></li>
  </ul>
</section>

<section class="cv-section" id="recognition">
  <h2 class="cv-label">Recognition</h2>
  <ul class="cv-items cv-items--compact">
    <li><span class="item-venue">R&amp;D 100, 2023</span> <a href="https://www.rdworldonline.com/candle-cancer-distributed-learning-environment-is-the-rd-100-winner-of-the-day/">CANDLE</a> &mdash; cancer AI infrastructure across Argonne, LLNL, and ORNL</li>
    <li><span class="item-venue">R&amp;D 100, 2022</span> <a href="https://www.rdworldonline.com/rd-100-2022-winner/flash-x-a-multiphysics-simulation-software/">FLASH-X</a> &mdash; multiphysics simulation engine</li>
    <li><span class="item-venue">IMR 2010</span> Best Paper &mdash; reactor core mesh generation with lattice hierarchy encoding</li>
    <li><span class="item-venue">ATPESC 2015</span> Scholar &mdash; Argonne training program on extreme-scale computing</li>
  </ul>

  <h2 class="cv-label cv-label--sub">Funding</h2>
  <ul class="cv-items cv-items--compact">
    <li><span class="item-venue">Active</span> DOE SEATS &mdash; Software Ecosystem for Advancing Climate Tools and Services</li>
    <li><span class="item-venue">Active</span> NSF Raijin &mdash; collaborative research in climate model analysis</li>
    <li><span class="item-venue">2017&ndash;2023</span> DOE ECP CANDLE &mdash; core contributor</li>
    <li><span class="item-venue">2009&ndash;2016</span> DOE NEAMS &mdash; principal investigator, MeshKit</li>
  </ul>
</section>

<section class="cv-section" id="background">
  <h2 class="cv-label">Roles</h2>
  <ul class="cv-items cv-items--compact">
    <li><span class="item-venue">2009&ndash;present</span> <strong>Argonne National Laboratory</strong> &mdash; Principal Specialist in Research Software Engineering</li>
    <li><span class="item-venue">2023&ndash;present</span> <strong>University of Chicago</strong> &mdash; Staff At-Large, cancer pharmacogenomics and Earth system science</li>
    <li><span class="item-venue">2007&ndash;2009</span> <strong>Arizona State University</strong> &mdash; Research and teaching assistant, structural and computational mechanics</li>
  </ul>

  <h2 class="cv-label cv-label--sub">Education</h2>
  <ul class="cv-items cv-items--compact">
    <li><span class="item-venue">2020</span> M.S. Computer Science &mdash; University of Chicago</li>
    <li><span class="item-venue">2009</span> M.S. Structural Engineering &mdash; Arizona State University</li>
    <li><span class="item-venue">2006</span> B.Tech. Mechanical Engineering &mdash; IIT ISM Dhanbad</li>
  </ul>
</section>

<footer class="cv-footer" id="contact">
  <p class="cv-connect">Happy to connect &mdash; <a href="mailto:jain@anl.gov">jain@anl.gov</a> &middot; <a href="mailto:rajeeja@gmail.com">rajeeja@gmail.com</a> &middot; <a href="https://www.linkedin.com/in/rajeeja/">LinkedIn</a></p>
  <p class="cv-links-secondary"><a href="https://github.com/rajeeja">GitHub</a> &middot; <a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en">Google Scholar</a> &middot; <a href="https://orcid.org/0000-0002-1235-918X">ORCID</a></p>
  <p class="cv-footnote">U.S. permanent resident &middot; EB-1A (extraordinary ability)</p>
</footer>

</div>
