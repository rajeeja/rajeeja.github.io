---
layout: single
title: "Blog"
permalink: /blog/
author_profile: false
classes: wide
---

<section class="content-section blog-hub">
  <div class="article-hero blog-hero">
    <p class="eyebrow">Technical notes</p>
    <h1 class="article-title">Blog</h1>
    <p class="article-dek">Engineering notes on scientific software, AI-agent tooling, climate workflows, and HPC systems work. The emphasis here is on how systems behave in practice, not just what they are supposed to do on paper.</p>
  </div>

  {% assign posts = site.posts | where_exp: "post", "post.categories contains 'blog'" %}
  {% assign featured = posts.first %}

  {% if featured %}
  <div class="blog-lead-grid">
    <article class="project-card project-card--wide blog-card blog-card--featured">
      <p class="card-meta">{{ featured.date | date: "%B %-d, %Y" }} · Featured note</p>
      <h2><a href="{{ featured.url | relative_url }}">{{ featured.title }}</a></h2>
      <p>{{ featured.excerpt | strip_html }}</p>
      <p class="focus-card__links"><a href="{{ featured.url | relative_url }}">Read note</a></p>
    </article>

    <aside class="side-card blog-sidecard">
      <p class="card-meta">What you will find here</p>
      <ul class="clean-list">
        <li><strong>Scientific systems notes</strong> on runtime choices, portability, and workflow behavior.</li>
        <li><strong>Worked examples</strong> from climate analysis, ML infrastructure, and HPC tools.</li>
        <li><strong>Project context</strong> on why a tool matters, not only how it is implemented.</li>
      </ul>
    </aside>
  </div>
  {% endif %}

  <div class="note-river">
    {% for post in posts offset: 1 %}
    <article class="project-card blog-card note-row">
      <p class="card-meta">{{ post.date | date: "%B %-d, %Y" }}</p>
      <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
      <p>{{ post.excerpt | strip_html }}</p>
      <p class="focus-card__links"><a href="{{ post.url | relative_url }}">Read note</a></p>
    </article>
    {% endfor %}
  </div>
</section>
