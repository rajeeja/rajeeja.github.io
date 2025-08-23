---
layout: single
title: "Rajeev Jain"
permalink: /
classes: wide
author_profile: false
---

<style>
/******* minimalist, readable, dark *******/
:root { --fg:#e8e8e8; --muted:#b6b6b6; --bg:#0b0b0c; --card:#111214; --accent:#8cc7ff; --border:#1b1b1f; --pill:#16171b; }
html.dark body { background: var(--bg); color: var(--fg); }
a { color: var(--accent); }
.section { margin: 2rem auto; max-width: 900px; padding: 0 1rem; }
.h1 { font-size: 2.2rem; font-weight: 700; letter-spacing:.2px; }
.lead { color: var(--muted); margin-top:.4rem; }
.row { display:grid; gap:1rem; grid-template-columns: repeat(auto-fit,minmax(240px,1fr)); }
.card { background: var(--card); border:1px solid var(--border); border-radius:10px; padding:1rem; }
.pills { display:flex; flex-wrap:wrap; gap:.5rem; margin-top:.5rem; }
.pill { background: var(--pill); border:1px solid var(--border); border-radius:999px; padding:.25rem .6rem; font-size:.9rem; color:var(--muted); }
.muted { color: var(--muted); }
blockquote { border-left:3px solid var(--border); padding-left:1rem; color: var(--muted); }
.pub-item { margin:.4rem 0; line-height:1.55; }
.pub-actions .btn { margin-left:.4rem; }
.hero { text-align:center; padding-top: 1.2rem; }
/* hide theme layout title to avoid duplicate name */
.page__title { display:none; }
</style>

<div class="section hero">
  <div class="h1">Rajeev Jain</div>
  <div class="lead">Principal Specialist, Research Software Engineering at Argonne National Laboratory</div>
  <div class="pills">
    <span class="pill">HPC & I/O</span>
    <span class="pill">Scientific Data & Visualization</span>
    <span class="pill">Applied ML for Science</span>
    <span class="pill">Exascale Software</span>
  </div>
</div>

<div class="section">
  <h2>Projects</h2>
  <div class="row">
    <div class="card"><h3>FLASH-X</h3><p class="muted">Problem: I/O bottlenecks at scale.<br>Approach: Async HDF5 I/O + compression; verification framework.<br>Impact: >20% speedup; R&D 100 (2022).</p><p><a href="https://flash-x.org/" target="_blank">Site</a> · <a href="https://ieeexplore.ieee.org/abstract/document/10026923" target="_blank">Paper</a></p></div>
    <div class="card"><h3>UXarray</h3><p class="muted">Problem: Analyze/visualize unstructured climate grids.<br>Approach: Python API design, vectorized cores, parallelism.<br>Impact: 60× speed-ups; DOE adoption.</p><p><a href="https://uxarray.readthedocs.io/" target="_blank">Docs</a> · <a href="https://climatemodeling.science.energy.gov/presentations/uxarray-python-package-analysis-and-visualization-model-output-unstructured-climate" target="_blank">Talk</a></p></div>
    <div class="card"><h3>CANDLE</h3><p class="muted">Problem: Scalable DL workflows for drug response.<br>Approach: Led CANDLE/Supervisor; HPO and reproducibility across systems.<br>Impact: R&D 100 (2023); widely cited.</p><p><a href="https://candle.cels.anl.gov/" target="_blank">Overview</a> · <a href="https://link.springer.com/article/10.1186/s12859-018-2056-3" target="_blank">Paper</a></p></div>
    <div class="card"><h3>Urban ECP</h3><p class="muted">Problem: Couple microclimate with building energy models.<br>Approach: Coupling + data pipelines; high-fidelity weather.<br>Impact: Published downtown Chicago boundary conditions.</p><p><a href="https://www.tandfonline.com/doi/abs/10.1080/19401493.2018.1534275" target="_blank">Paper</a></p></div>
  </div>
</div>

<div class="section">
  <h2>Selected Publications</h2>
  <ul>
    {% for p in site.data.selected_publications %}
    <li class="pub-item"><strong>{{ p.title }}</strong>. <em>{{ p.venue }}</em> ({{ p.year }}). {% if p.doi %}<a href="{{ p.doi }}">DOI</a>{% endif %}</li>
    {% endfor %}
  </ul>
  <h3>Full List</h3>
  {% include publications link=true limit=100 %}
</div>

<div class="section">
  <h2>Contact</h2>
  <p><a href="mailto:rajeeja@gmail.com">rajeeja@gmail.com</a> · <a href="https://scholar.google.com/citations?user=bC77n9MAAAAJ&hl=en" target="_blank">Google Scholar</a> · <a href="/files/Jain_CV.pdf" target="_blank">CV</a></p>
</div>

<blockquote class="section">
  <p>“Placeholder testimonial. Replace with collaborator quote.”</p>
  <p><em>— Name, Title, Affiliation</em></p>
</blockquote>