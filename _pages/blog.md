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
    <h1 class="cv-name">Notes</h1>
    <p class="cv-bio">Write-ups of things I ran into at work, mostly numerical bugs and HPC plumbing.</p>
  </div>
</header>

{% assign posts = site.posts | where_exp: "post", "post.categories contains 'blog'" %}

<section class="cv-section">
  <ul class="cv-items cv-items--compact cv-items--posts">
    {% for post in posts %}
    <li><span class="item-venue">{{ post.date | date: "%Y-%m-%d" }}</span> <a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
</section>

<section class="cv-section">
  <h2 class="cv-label cv-label--sub">Something else</h2>
  <p class="cv-more"><a href="/atma_siddhi.html">Atma Siddhi Shastra</a> (<a href="/atma_siddhi_hindi.html">हिंदी</a>), an interactive guide to the text. Not about software.</p>
</section>

</div>
