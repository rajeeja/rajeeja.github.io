---
layout: single
title: "Rajeev Jain"
permalink: /
author_profile: false
classes: wide
description: "Rajeev Jain, principal research software engineer at Argonne National Laboratory. Scientific software and AI agent tooling for HPC: SimBoard for E3SM, UXarray, and its MCP server."
excerpt: "Principal research software engineer at Argonne. SimBoard for E3SM, UXarray, and AI agent tooling for HPC."
---

<div class="cv" id="about">

<header class="cv-head">
  <div class="cv-head__copy">
    <h1 class="cv-name">Rajeev Jain</h1>
    <p class="cv-tagline">Principal research software engineer, <a href="https://www.anl.gov/mcs">Argonne National Laboratory</a></p>
    <p class="cv-bio">I build scientific software that runs on supercomputers, and lately the tooling that lets AI agents use it. I've been at Argonne since 2009. Most of my time now goes to SimBoard for <a href="https://e3sm.org/">E3SM</a> and to UXarray.</p>
    <p class="cv-links">
      <a href="/files/Rajeev_Jain_CV.pdf">CV (PDF)</a> &middot;
      <a href="mailto:jain@anl.gov">Email</a> &middot;
      <a href="https://github.com/rajeeja">GitHub</a> &middot;
      <a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en">Scholar</a> &middot;
      <a href="https://www.linkedin.com/in/rajeeja/">LinkedIn</a>
    </p>
  </div>
  <img class="cv-portrait" src="/images/bio-photo.jpg" alt="Rajeev Jain">
</header>

<section class="cv-section" id="projects">
  <h2 class="cv-label">Current work</h2>
  <ul class="cv-items">
    <li>
      <div class="item-head"><strong><a href="https://github.com/E3SM-Project/simboard">SimBoard</a></strong> <span class="item-role">contributor, E3SM</span></div>
      A web catalog of E3SM simulation runs: case metadata, provenance, and links to each run's diagnostics. FastAPI, PostgreSQL, and React, deployed at NERSC.
      <span class="item-links"><a href="https://simboard-dev.e3sm.org/">app</a> &middot; <a href="https://simboard.readthedocs.io/">docs</a> &middot; <a href="https://github.com/E3SM-Project/simboard">code</a></span>
    </li>
    <li>
      <div class="item-head"><strong><a href="https://github.com/UXARRAY/uxarray">UXarray</a></strong> <span class="item-role">lead developer</span></div>
      Python library for analysis on unstructured climate grids, used at DOE labs and NCAR. I wrote its MCP server, which lets AI agents run UXarray analyses on HPC systems through Globus Compute.
      <details class="item-more">
        <summary>Details</summary>
        <ul>
          <li>Made a 300-million-cell, 63 GB mesh loadable in 306 seconds by deduplicating coordinates before building the grid (<a href="/blog/scrip-dedup-63gb-mesh/">write-up</a>).</li>
          <li>Replaced a cross product in the spherical geometry kernels with error-free arithmetic after it drifted 0.68 m on a real Earth mesh (<a href="https://github.com/UXARRAY/uxarray/pull/1513">PR&nbsp;1513</a>).</li>
          <li>1.67&times; faster in a Numba hot path by removing hidden heap allocation (<a href="https://github.com/UXARRAY/uxarray/pull/1577">PR&nbsp;1577</a>, <a href="/blog/numba-heap-scalars-uxarray/">write-up</a>).</li>
        </ul>
      </details>
      <span class="item-links"><a href="https://uxarray.readthedocs.io">docs</a> &middot; <a href="https://github.com/UXARRAY/uxarray">code</a> &middot; <a href="/blog/uxarray-mcp-improv-globus-compute/">MCP write-up</a></span>
    </li>
    <li>
      <div class="item-head"><strong><a href="https://github.com/E3SM-Project/e3sm-ai-platform">E3SM AI platform</a></strong> <span class="item-role">contributor</span></div>
      An assistant for E3SM documentation that cites its sources or declines to answer. I added Argonne's Argo gateway as a model provider.
    </li>
    <li>
      <div class="item-head"><strong><a href="https://github.com/SEATStandards/ncvis">ncvis</a></strong> <span class="item-role">maintainer, DOE SEATS</span></div>
      A NetCDF viewer for structured and unstructured grids, written in C++.
    </li>
  </ul>
</section>

<section class="cv-section" id="earlier">
  <h2 class="cv-label">Earlier</h2>
  <ul class="cv-items cv-items--compact">
    <li><span class="item-venue">2025&ndash;26</span> <a href="/blog/sfno-aurora-climate-emulator/">SFNO on Aurora</a>. Ported a PyTorch climate emulator to Aurora's Intel GPUs and set up distributed training.</li>
    <li><span class="item-venue">2017&ndash;25</span> <a href="https://github.com/JDACS4C-IMPROVE/IMPROVE">CANDLE and IMPROVE</a>. Hyperparameter search for cancer drug-response models, 10,000+ training runs on Summit, Theta, and Cori. R&amp;D 100, 2023.</li>
    <li><span class="item-venue">2019&ndash;24</span> <a href="https://flash-x.org/">FLASH-X</a>. Asynchronous checkpointing with compression, cutting checkpoint overhead 40&ndash;70% on Summit. R&amp;D 100, 2022.</li>
    <li><span class="item-venue">2016&ndash;19</span> Urban ECP. A weather-to-building-to-CFD workflow for downtown Chicago.</li>
    <li><span class="item-venue">2009&ndash;16</span> <a href="https://bitbucket.org/fathomteam/meshkit">MeshKit</a>. Reactor core mesh generation, as PI. A 101-million-element core mesh in about 7 minutes on 712 cores.</li>
  </ul>
</section>

<section class="cv-section" id="skills">
  <h2 class="cv-label">Tools</h2>
  <dl class="cv-skills">
    <dt>Languages</dt><dd>Python, C++, Fortran, Bash</dd>
    <dt>Scientific Python</dt><dd>NumPy, Xarray, Numba, Dask, Polars, PyTorch</dd>
    <dt>AI systems</dt><dd>MCP servers, agent evaluation, distributed training, hyperparameter search</dd>
    <dt>HPC</dt><dd>MPI, HDF5, NetCDF, SZ3 and ZFP compression, Intel and NVIDIA GPUs, PBS, Slurm</dd>
    <dt>Engineering</dt><dd>CMake, CI/CD, packaging (conda-forge, PyPI), Globus Compute, code review</dd>
  </dl>
</section>

<section class="cv-section" id="publications">
  <h2 class="cv-label">Selected papers</h2>
  <ul class="cv-items cv-items--refs">
    <li><strong>Jain, R.</strong>, Jacob, R. <a href="https://agent4sc.github.io/">Beyond Tool Execution: Evaluating Scientific MCP Interfaces with UXarray.</a> AGENT4SC at IEEE eScience, 2026.</li>
    <li>Partin, A., &hellip;, <strong>Jain, R.</strong>, et al. <a href="https://academic.oup.com/bib/article/27/1/bbaf667/7002013">Benchmarking community drug response prediction models.</a> <em>Briefings in Bioinformatics</em>, 2026.</li>
    <li><strong>Jain, R.</strong>, Tang, H., Dhruv, A., Byna, S. <a href="https://doi.org/10.1109/SCW63240.2024.00043">Enabling Data Reduction for FLASH-X Simulations.</a> DRBSD-10 at SC24, 2024.</li>
    <li><strong>Jain, R.</strong>, Wozniak, J.M., Partin, A., et al. <a href="https://web.cels.anl.gov/~woz/papers/IMPROVE_HPO_2024.pdf">Cross-HPO: Optimizing Neural Networks for Cancer Drug Response.</a> CAFCW at SC24, 2024.</li>
    <li>Wozniak, J.M., &hellip;, <strong>Jain, R.</strong>, et al. <a href="https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2508-4">CANDLE/Supervisor: A workflow framework for machine learning applied to cancer research.</a> <em>BMC Bioinformatics</em>, 2018.</li>
    <li>Tautges, T.J., <strong>Jain, R.</strong> <a href="https://doi.org/10.1007/s00366-011-0236-8">Creating Geometry and Mesh Models for Nuclear Reactor Core Geometries.</a> <em>Engineering with Computers</em>, 2012.</li>
  </ul>
  <p class="cv-more">Everything else is on <a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en">Google Scholar</a>.</p>

  <h2 class="cv-label cv-label--sub">Recent talks</h2>
  <ul class="cv-items cv-items--compact">
    <li><span class="item-venue">AMS 2027</span> Conservative zonal averaging on unstructured Earth-system grids</li>
    <li><span class="item-venue">SC26</span> Poster: Refuse to Guess, a declared precondition in the UXarray MCP server</li>
    <li><span class="item-venue">eScience 26</span> <a href="https://agent4sc.github.io/">Evaluating scientific MCP interfaces with UXarray</a></li>
    <li><span class="item-venue">SciFM26</span> <a href="/blog/uxarray-mcp-improv-globus-compute/">A UXarray MCP server for unstructured Earth-system meshes</a></li>
    <li><span class="item-venue">SC24</span> Tutorial: UXarray for unstructured climate data</li>
    <li><span class="item-venue">SciPy 2023</span> <a href="https://www.youtube.com/watch?v=qwqJeOO8m6A">UXarray for unstructured climate data</a></li>
  </ul>
</section>

<section class="cv-section" id="recognition">
  <h2 class="cv-label">Recognition</h2>
  <ul class="cv-items cv-items--compact">
    <li><span class="item-venue">2023</span> R&amp;D 100 Award, <a href="https://www.rdworldonline.com/candle-cancer-distributed-learning-environment-is-the-rd-100-winner-of-the-day/">CANDLE</a></li>
    <li><span class="item-venue">2022</span> R&amp;D 100 Award, <a href="https://www.rdworldonline.com/rd-100-2022-winner/flash-x-a-multiphysics-simulation-software/">FLASH-X</a></li>
    <li><span class="item-venue">2015</span> ATPESC scholar</li>
    <li><span class="item-venue">2010</span> Best paper, International Meshing Roundtable</li>
    <li><span class="item-venue">2004</span> First prize, low-budget car design contest, IIT Kharagpur</li>
  </ul>

  <h2 class="cv-label cv-label--sub">Service</h2>
  <ul class="cv-items cv-items--compact">
    <li><span class="item-venue">2026</span> Program committee, <a href="https://ornl.github.io/events/agenticai4hpc2026/">AgenticAI4HPC</a> at SC26 and <a href="https://agent4sc.github.io/">AGENT4SC</a> at eScience</li>
    <li><span class="item-venue">Ongoing</span> DOE SBIR/STTR proposal reviewer</li>
  </ul>
</section>

<section class="cv-section" id="background">
  <h2 class="cv-label">Background</h2>
  <ul class="cv-items cv-items--compact">
    <li><span class="item-venue">2009&ndash;</span> Argonne National Laboratory, Principal Specialist in Research Software Engineering</li>
    <li><span class="item-venue">2023&ndash;</span> University of Chicago, CASE, staff at-large</li>
    <li><span class="item-venue">2020</span> M.S. Computer Science, University of Chicago</li>
    <li><span class="item-venue">2009</span> M.S. Structural Engineering, Arizona State University</li>
    <li><span class="item-venue">2006</span> B.Tech. Mechanical Engineering, IIT (ISM) Dhanbad</li>
  </ul>
</section>

<footer class="cv-footer" id="contact">
  <p>Email is the best way to reach me: <a href="mailto:jain@anl.gov">jain@anl.gov</a>. Also <a href="https://orcid.org/0000-0002-1235-918X">ORCID</a> and <a href="/feed.xml">RSS</a>.</p>
</footer>

</div>
