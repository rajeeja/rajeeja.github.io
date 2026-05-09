---
layout: single
title: "Blog"
permalink: /blog/
author_profile: false
classes: wide
---

<div class="cv">

<header class="cv-head cv-head--page">
  <div class="cv-head__copy">
    <p class="eyebrow">Technical notes</p>
    <h1 class="cv-name">Blog</h1>
    <p class="cv-bio">Engineering notes on scientific software, AI-agent tooling, climate workflows, and HPC systems work. The emphasis is on how systems behave in practice.</p>
  </div>
</header>

{% assign posts = site.posts | where_exp: "post", "post.categories contains 'blog'" %}

<section class="cv-section">
  <h2 class="cv-label">Posts</h2>
  <ul class="cv-items">
    {% for post in posts %}
    <li>
      <div class="item-head"><strong><a href="{{ post.url | relative_url }}">{{ post.title }}</a></strong><span class="item-role">{{ post.date | date: "%B %-d, %Y" }}</span></div>
      {{ post.excerpt | strip_html }}
    </li>
    {% endfor %}
  </ul>
</section>

</div>
