---
layout: single
title: "Blog"
permalink: /blog/
author_profile: false
classes: wide
---

This page collects technical notes on scientific software, climate workflows, and HPC systems work.

{% assign posts = site.posts | where_exp: "post", "post.categories contains 'blog'" %}
{% for post in posts %}
<article class="archive__item" style="margin-bottom: 2.5rem;">
  <h2 class="archive__item-title" style="margin-bottom: 0.35rem;"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
  <p class="page__meta" style="margin-bottom: 0.6rem;">{{ post.date | date: "%B %-d, %Y" }}</p>
  <p style="margin-bottom: 0;">{{ post.excerpt | strip_html }}</p>
</article>
{% endfor %}
