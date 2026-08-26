# rajeeja.github.io

Personal site of Rajeev Jain — profile, CV, and writing on scientific
computing, HPC, and AI tooling. Built with Jekyll and served by GitHub Pages
at <https://rajeeja.github.io>.

## Layout

| Path | Contents |
|---|---|
| `index.md` | Homepage: profile, selected work, publications |
| `_posts/` | Blog posts, published under `/blog/` |
| `_pages/` | Standalone pages (blog index, 404) |
| `_layouts/`, `_includes/`, `_sass/` | Theme |
| `assets/css/overrides.css` | Site-specific styling; edit this, not the SCSS |
| `cv/` | LaTeX sources for the CV and resume (not published) |
| `files/` | Built CV and resume PDFs |
| `scripts/` | CV build and publication-refresh helpers |

## Local build

```sh
bundle install
bundle exec jekyll serve
```

## CV

`cv/cv.tex` and `cv/resume.tex` are the sources. The
`.github/workflows/build-cv.yml` workflow compiles them with `tectonic` and
commits the PDFs to `files/`, so edit the `.tex` files and let CI produce the
PDFs rather than committing locally built ones.

## Credits

Forked from [academicpages](https://github.com/academicpages/academicpages.github.io),
itself a fork of the [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/)
Jekyll theme by Michael Rose. MIT licensed; see `LICENSE`.
