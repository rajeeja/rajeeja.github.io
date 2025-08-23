---
layout: single
title: "Rajeev Jain"
permalink: /
author_profile: true
excerpt: "Research software engineer developing fast, reliable tools for scientific discovery at scale."
---

<div class="page-intro" style="margin-top:.5rem">
  <p><strong>Principal Specialist, Research Software Engineering at Argonne National Laboratory.</strong> Since 2009, I’ve built high‑performance, reliable research software with domain scientists across cancer data science, climate computation, multiphysics simulation, urban systems, and nuclear reactor modeling.</p>
  <p>I work across fields and teams to turn complex problems into dependable software. I like clear goals, simple designs, and fast feedback: build, test, measure, improve. Most of my work sits at the boundary between research and production.</p>
  <ul>
    <li>Projects span cancer data science, climate tools, multiphysics codes, urban systems, and reactor modeling.</li>
    <li>Grateful to have worked with great people; I try to keep things simple, practical, and useful.</li>
    <li>Prefer small, steady steps over big promises; measure outcomes and improve.</li>
  </ul>
  
  <p style="margin-top:.4rem"><a href="/about/">Read more about my background →</a></p>
</div>

<hr/>

<h2>Projects</h2>
<ul>
  <li><strong>UXarray</strong> — Unstructured climate grids toolkit (Python), up to 60× faster on key workloads. <a href="/projects/#uxarray" class="small">Details →</a></li>
  <li><strong>CANDLE/Supervisor</strong> — Scalable DL workflows for drug response across supercomputers. <a href="/projects/#candle" class="small">Details →</a></li>
  <li><strong>FLASH‑X</strong> — Async HDF5 I/O and verification for multiphysics; >20% I/O speedups. <a href="/projects/#flashx" class="small">Details →</a></li>
  <li><strong>Urban ECP</strong> — Coupled microclimate + building energy modeling for city‑scale insights. <a href="/projects/#urban-ecp" class="small">Details →</a></li>
  <li><strong>NEAMS SIGMA/MeshKit/RGG</strong> — Reactor core mesh tools; cut modeling time from weeks to hours. <a href="/projects/#neams" class="small">Details →</a></li>
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
