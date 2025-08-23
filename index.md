---
layout: single
title: "Rajeev Jain"
permalink: /
author_profile: true
excerpt: "Research software engineer developing fast, reliable tools for scientific discovery at scale."
---

<div class="page-intro" style="margin-top:.5rem">
  <p><strong>Principal Specialist, Research Software Engineering at Argonne National Laboratory.</strong> Since 2009, I’ve built high‑performance, reliable research software with domain scientists across cancer data science, climate computation, multiphysics simulation, urban systems, and nuclear reactor modeling.</p>
  <p>My work focuses on HPC I/O, unstructured data tooling, and applied ML for science. Recent efforts include <em>UXarray</em> (unstructured climate grids, Python), <em>FLASH‑X</em> (asynchronous HDF5 I/O with SZ3/ZFP, verification), and <em>CANDLE/Supervisor</em> (scalable deep‑learning workflows across supercomputers).</p>
  <ul>
    <li>Built and maintained production‑quality tools adopted by DOE projects and used at national facilities.</li>
    <li>Presented at venues including SciPy, AMS, and EGU; publications and software recognized by the community.</li>
    <li>Hands‑on with performance, testing, CI, and reproducibility to turn prototypes into dependable systems.</li>
  </ul>
  <div style="margin:.5rem 0;display:flex;gap:10px;flex-wrap:wrap;align-items:center;opacity:.95">
    <img alt="Argonne National Laboratory" src="{{ '/images/logos/anl.png' | relative_url }}" onerror="this.onerror=null;this.src='https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Argonne_National_Laboratory_logo.svg/240px-Argonne_National_Laboratory_logo.svg.png'" style="height:26px;background:#fff;border-radius:4px;padding:2px;border:1px solid #2a2a2a">
    <img alt="U.S. Department of Energy" src="{{ '/images/logos/doe.png' | relative_url }}" onerror="this.onerror=null;this.src='https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Seal_of_the_United_States_Department_of_Energy.svg/200px-Seal_of_the_United_States_Department_of_Energy.svg.png'" style="height:26px;background:#fff;border-radius:4px;padding:2px;border:1px solid #2a2a2a">
    <img alt="The University of Chicago" src="{{ '/images/logos/uchicago.png' | relative_url }}" onerror="this.onerror=null;this.src='https://upload.wikimedia.org/wikipedia/en/thumb/6/68/University_of_Chicago_shield.svg/200px-University_of_Chicago_shield.svg.png'" style="height:26px;background:#fff;border-radius:4px;padding:2px;border:1px solid #2a2a2a">
    <svg aria-label="R&D 100" viewBox="0 0 120 28" width="120" height="28" style="display:inline-block"><rect width="120" height="28" rx="14" fill="#111214" stroke="#1b1b1f"/><text x="60" y="18" fill="#e6e6e6" font-family="Arial, Helvetica, sans-serif" font-size="12" text-anchor="middle">R&amp;D 100 Winner</text></svg>
  </div>
  <p style="margin-top:.4rem"><a href="/about/">Read more about my background →</a></p>
</div>

<hr/>

<h2>Projects</h2>
<ul>
  <li><strong>UXarray</strong> — Unstructured climate grids toolkit (Python). Up to 60× speed‑ups on key workloads; adopted by DOE users. <a href="/projects/">Details →</a></li>
  <li><strong>CANDLE/Supervisor</strong> — Scalable DL workflows for drug response; standardized HPO/experiments across supercomputers. <a href="/projects/">Details →</a></li>
  <li><strong>FLASH‑X</strong> — Async HDF5 I/O + SZ3/ZFP; >20% speedup on I/O‑bound runs; verification framework. <a href="/projects/">Details →</a></li>
  <li><strong>Urban ECP</strong> — Coupled microclimate + building energy modeling for city‑scale analyses. <a href="/projects/">Details →</a></li>
</ul>

<hr/>

<h2>Selected Publications</h2>
<ul>
  {% for p in site.data.selected_publications limit:3 %}
    <li class="pub-item"><strong>{{ p.title }}</strong>. <em>{{ p.venue }}</em> ({{ p.year }}). {% if p.doi %}<a href="{{ p.doi }}" target="_blank">DOI</a>{% endif %}</li>
  {% endfor %}
</ul>
<p><a href="/publications/">View full list →</a></p>

<hr/>

<h2>Latest Posts</h2>
<ul>
  {% for post in site.posts limit:3 %}
    <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a> <span class="small">— {{ post.date | date: "%b %d, %Y" }}</span></li>
  {% endfor %}
</ul>
<p><a href="/year-archive/">All posts →</a></p>
