---
layout: single
title: "Rajeev Jain"
permalink: /
author_profile: true
excerpt: "Research software engineer developing fast, reliable tools for scientific discovery at scale."
---

<div class="page-intro" style="margin-top:.5rem">
  <p>I build and maintain high‑performance, reliable research software in collaboration with domain scientists. My focus areas include HPC I/O, unstructured data tooling, and applied ML for science.</p>
</div>

<hr/>

<h2>About</h2>
<p>Principal Specialist, Research Software Engineering at Argonne National Laboratory. Since 2009, I’ve worked across cancer data science, climate computation, multiphysics simulation, urban coupled systems, and nuclear reactor modeling. I enjoy building teams and mentoring, and I care about software that is fast, reproducible, and useful.</p>
<p><a href="/about/">Read more →</a></p>

<hr/>

<h2>Projects</h2>
<ul>
  <li><strong>UXarray</strong> — Unstructured climate grids toolkit (Python). 60× speed‑ups on key workloads; adopted by DOE users. <a href="/projects/">Details →</a></li>
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