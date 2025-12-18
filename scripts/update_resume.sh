#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ "${SKIP_SCHOLAR:-}" != "1" ]]; then
  python3 "$repo_root/scripts/update_publications.py"
fi

if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error \
    -outdir="$repo_root/files" -jobname=Rajeev_Jain_Resume \
    "$repo_root/cv/Jain_CV.tex"
  latexmk -c -outdir="$repo_root/files" -jobname=Rajeev_Jain_Resume \
    "$repo_root/cv/Jain_CV.tex"
elif command -v pdflatex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory="$repo_root/files" -jobname=Rajeev_Jain_Resume \
    "$repo_root/cv/Jain_CV.tex"
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory="$repo_root/files" -jobname=Rajeev_Jain_Resume \
    "$repo_root/cv/Jain_CV.tex"
else
  echo "Error: latexmk or pdflatex is required to build the resume." >&2
  exit 1
fi

echo "Wrote files/Rajeev_Jain_Resume.pdf"
