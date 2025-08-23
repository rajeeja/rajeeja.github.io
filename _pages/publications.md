---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
redirect_from:
  - /publications
  - /pubs
  - /publication
---

If you would like PDFs of any of these papers, please email.

### Selected Publications
<ul>
{% for p in site.data.selected_publications %}
  <li class="pub-item"><strong>{{ p.title }}</strong>. <em>{{ p.venue }}</em> ({{ p.year }}). {% if p.doi %}<a href="{{ p.doi }}">DOI</a>{% endif %}</li>
{% endfor %}
</ul>

<div class="theme-toggle"><button id="theme-toggle-btn" aria-label="Toggle theme">Toggle theme</button></div>

### Full List
{% include publications link=true limit=100 %}

<!-- 
{% include base_path %}

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}

Under construction.. -->