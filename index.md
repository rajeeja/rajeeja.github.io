---
layout: single
title: "Rajeev Jain"
permalink: /
author_profile: false
classes: wide
excerpt: "Engineer with 16+ years building scientific software across climate, data science, and high-performance computing."
---

<div class="page-intro content-section" id="about" style="--delay: 0s;">
  <div class="intro-grid">
    <div class="intro-media">
      <img class="intro-photo" src="/images/profile.png" alt="Rajeev Jain">
      <p class="intro-caption"><a href="https://www.anl.gov/profile/rajeev-jain">Principal Specialist, Research Software Engineering</a> &middot; Mathematics and Computer Science Division &middot; Argonne National Laboratory (Lemont, IL)</p>
    </div>
    <div class="intro-copy">
      <p class="lead">Research software engineer with 16+ years in scientific software and high-performance computing.</p>
      <p>Currently: Principal Specialist, Research Software Engineering at Argonne National Laboratory. Work includes climate, cancer data science, multiphysics simulation, urban systems, and nuclear engineering.</p>
      <p>Focus areas include parallel input/output, profiling and optimization, reproducibility, scalable pipelines, and Python programming, with emphasis on testing, continuous integration, and releases.</p>
      <p>I am an engineer who likes to solve problems. Outside of work, I play rapid chess and pickleball, enjoy cricket, a board of Catan, and biking.</p>
      <p class="compact-links"><a href="mailto:rajeeja@gmail.com">Email</a>  &middot;  <a href="https://github.com/rajeeja">GitHub</a>  &middot;  <a href="https://www.linkedin.com/in/rajeeja/">LinkedIn</a>  &middot;  <a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en">Scholar</a></p>
      <div class="hero-actions">
        <a class="btn btn--primary" href="/files/Rajeev_Jain_Resume.pdf">Resume (document)</a>
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
      <p><strong>Approach:</strong> Implemented conservative zonal averaging in UXarray using Gauss-Legendre quadrature, with validation tests and regular Python Package Index (PyPI) releases.</p>
      <p><strong>Outcome:</strong> Released as part of UXarray with validated accuracy and scalable analysis in Python.</p>
      <p class="case-links"><a href="https://eesm.science.energy.gov/presentations/uxarray-python-package-analysis-and-visualization-model-output-unstructured-climate">Paper</a>  &middot;  <a href="https://github.com/UXARRAY/uxarray/pull/1345">Pull request #1345</a></p>
    </article>
    <article class="case-study">
      <h3>FLASH-X: asynchronous input/output and compression</h3>
      <p><strong>Problem:</strong> Checkpoint input/output and restart overhead dominated runtime in large multiphysics simulations.</p>
      <p><strong>Approach:</strong> Added asynchronous Hierarchical Data Format 5 (HDF5) input/output with compression and a verification workflow with nightly baselines.</p>
      <p><strong>Outcome:</strong> Reduced input/output time in benchmarks (20%+ gains) and improved restart reliability.</p>
      <p class="case-links"><a href="https://arxiv.org/abs/2208.11630">Paper 1</a>  &middot;  <a href="https://ieeexplore.ieee.org/document/10026923">Paper 2</a></p>
    </article>
    <article class="case-study">
      <h3>Urban Exascale: boundary conditions for urban microclimate</h3>
      <p><strong>Problem:</strong> City-scale building energy models needed realistic urban microclimate boundary conditions.</p>
      <p><strong>Approach:</strong> Coupled urban weather boundary conditions into a city-scale workflow and ran multi-domain simulations.</p>
      <p><strong>Outcome:</strong> Improved boundary conditions for building energy modeling and published results.</p>
      <p class="case-links"><a href="https://eta-publications.lbl.gov/sites/default/files/17_-_urban_weather_boundary_conditions_-_tianzhen_hong.pdf">Paper</a></p>
    </article>
  </div>
</section>

<section class="content-section" id="experience" style="--delay: 0.1s;">
  <h2>Experience Snapshot</h2>
  <ul class="timeline">
    <li><strong>Argonne National Laboratory</strong> - Research software engineering roles (2009-present); current title: Principal Specialist, Research Software Engineering. Work across UXarray, FLASH-X, the Cancer Distributed Learning Environment (CANDLE), MeshKit, Reactor Geometry Generator, and urban simulation; ran large-scale hyperparameter optimization workflows for cancer data science projects.</li>
    <li><strong>The University of Chicago</strong> - Staff At-Large (2023-present). Joint appointment supporting cancer and earth science research.</li>
    <li><strong>Arizona State University</strong> - Research and Teaching Assistant (2007-2009).</li>
    <li><strong>Wipro Technologies</strong> - Project Engineer (2006-2007).</li>
  </ul>
</section>

<section class="content-section" id="publications" style="--delay: 0.2s;">
  <h2>Awards and Publications</h2>
  <ul class="pub-list">
    <li><strong>Awards:</strong> Research and Development 100 (R&amp;D 100) Awards for <a href="https://www.rdworldonline.com/rd-100-2022-winner/flash-x-a-multiphysics-simulation-software/">FLASH-X (2022)</a> and <a href="https://www.rdworldonline.com/candle-cancer-distributed-learning-environment-is-the-rd-100-winner-of-the-day/">CANDLE (2023)</a>; Best Paper (International Meshing Roundtable 2010); Arizona State University Graduate Fellowship (2007-2009).</li>
    <li><strong>MeshKit:</strong> Reactor core mesh generation. <a href="https://link.springer.com/article/10.1007/s00366-011-0221-4">Paper</a></li>
  </ul>
  <p class="more-links"><a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&amp;hl=en">Full publications list</a></p>
</section>

<section class="content-section" id="talks" style="--delay: 0.25s;">
  <h2>Selected Talks</h2>
  <ul class="talk-list">
    <li><a href="https://www.youtube.com/watch?v=qwqJeOO8m6A&amp;t=545s">UXarray for unstructured climate data (Scientific Python Conference 2023)</a></li>
    <li><a href="https://www.youtube.com/watch?v=MuifQ7lHRR8&amp;t=176s">Data reduction for FLASH-X simulations (Hierarchical Data Format User Group 2023)</a></li>
  </ul>
</section>

<section class="content-section" id="resume" style="--delay: 0.3s;">
  <h2>Resume and Curriculum Vitae</h2>
  <p>Short resume and full curriculum vitae (document).</p>
  <p>
    <a class="btn btn--primary" href="/files/Rajeev_Jain_Resume.pdf">Resume (document)</a>
    <a class="btn btn--ghost" href="/files/Rajeev_Jain_CV.pdf">Curriculum Vitae (document)</a>
  </p>
</section>

<section class="content-section" id="contact" style="--delay: 0.35s;">
  <h2>Contact</h2>
  <p><a href="mailto:rajeeja@gmail.com">rajeeja@gmail.com</a></p>
</section>
