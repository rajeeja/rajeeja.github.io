---
layout: single
title: "Blog"
permalink: /blog/
author_profile: false
classes: wide
---

<section class="content-section blog-hub">
  <div class="section-heading">
    <p class="section-kicker">Technical notes</p>
    <h2 class="section-title">Blog</h2>
    <p class="section-lead">Engineering notes on scientific software, AI-agent tooling, climate workflows, and HPC systems work.</p>
  </div>

  {% assign posts = site.posts | where_exp: "post", "post.categories contains 'blog'" %}
  {% assign featured = posts.first %}

  {% if featured %}
  <article class="project-card project-card--wide blog-card blog-card--featured">
    <p class="card-meta">{{ featured.date | date: "%B %-d, %Y" }} · Featured note</p>
    <h3><a href="{{ featured.url | relative_url }}">{{ featured.title }}</a></h3>
    <p>{{ featured.excerpt | strip_html }}</p>
  </article>
  {% endif %}

  <div class="project-grid blog-grid">
    {% for post in posts offset: 1 %}
    <article class="project-card blog-card">
      <p class="card-meta">{{ post.date | date: "%B %-d, %Y" }}</p>
      <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
      <p>{{ post.excerpt | strip_html }}</p>
    </article>
    {% endfor %}
  </div>
</section>
