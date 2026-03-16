#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cv_dir="$repo_root/cv"
resume_tex="resume.tex"
cv_tex="cv.tex"
texmf_var="$repo_root/files/texmf-var"

mkdir -p "$texmf_var"
export TEXMFVAR="$texmf_var"
export TEXINPUTS="$cv_dir//:"
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1704067200}"
export TZ=UTC

if [[ "${SKIP_SCHOLAR:-}" != "1" ]]; then
  python3 "$repo_root/scripts/update_publications.py"
fi

cd "$cv_dir"

if command -v tectonic >/dev/null 2>&1; then
  rm -f \
    "$repo_root/files/resume.pdf" \
    "$repo_root/files/cv.pdf" \
    "$repo_root/files/Rajeev_Jain_Resume.pdf" \
    "$repo_root/files/Rajeev_Jain_CV.pdf"
  tectonic -Z search-path="$cv_dir" --outdir "$repo_root/files" "$resume_tex"
  mv "$repo_root/files/resume.pdf" "$repo_root/files/Rajeev_Jain_Resume.pdf"
  tectonic -Z search-path="$cv_dir" --outdir "$repo_root/files" "$cv_tex"
  mv "$repo_root/files/cv.pdf" "$repo_root/files/Rajeev_Jain_CV.pdf"
elif command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -g -interaction=nonstopmode -halt-on-error \
    -outdir="$repo_root/files" -jobname=Rajeev_Jain_Resume \
    "$resume_tex"
  latexmk -c -outdir="$repo_root/files" -jobname=Rajeev_Jain_Resume \
    "$resume_tex"
  latexmk -pdf -g -interaction=nonstopmode -halt-on-error \
    -outdir="$repo_root/files" -jobname=Rajeev_Jain_CV \
    "$cv_tex"
  latexmk -c -outdir="$repo_root/files" -jobname=Rajeev_Jain_CV \
    "$cv_tex"
elif command -v pdflatex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory="$repo_root/files" -jobname=Rajeev_Jain_Resume \
    "$resume_tex"
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory="$repo_root/files" -jobname=Rajeev_Jain_Resume \
    "$resume_tex"
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory="$repo_root/files" -jobname=Rajeev_Jain_CV \
    "$cv_tex"
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory="$repo_root/files" -jobname=Rajeev_Jain_CV \
    "$cv_tex"
else
  echo "Error: tectonic, latexmk, or pdflatex is required to build the resume." >&2
  exit 1
fi

echo "Wrote files/Rajeev_Jain_Resume.pdf"
echo "Wrote files/Rajeev_Jain_CV.pdf"
