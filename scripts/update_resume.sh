#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
resume_tex="$repo_root/cv/Rajeev_Jain_Resume.tex"
cv_tex="$repo_root/cv/Rajeev_Jain_CV.tex"
texmf_var="$repo_root/files/texmf-var"

mkdir -p "$texmf_var"
export TEXMFVAR="$texmf_var"

if [[ "${SKIP_SCHOLAR:-}" != "1" ]]; then
  python3 "$repo_root/scripts/update_publications.py"
fi

if command -v latexmk >/dev/null 2>&1; then
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
  echo "Error: latexmk or pdflatex is required to build the resume." >&2
  exit 1
fi

echo "Wrote files/Rajeev_Jain_Resume.pdf"
echo "Wrote files/Rajeev_Jain_CV.pdf"
