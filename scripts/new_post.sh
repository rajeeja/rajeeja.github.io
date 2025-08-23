#!/usr/bin/env bash
# Usage: scripts/new_post.sh "My Post Title" [category] [tags]
set -euo pipefail
TITLE=${1:-}
CATEGORY=${2:-blog}
TAGS=${3:-}
if [ -z "$TITLE" ]; then
  echo "Title required. Usage: scripts/new_post.sh \"My Post Title\" [category] [tags]" >&2
  exit 1
fi
# slugify: lowercase, spaces->-, strip non-alnum-
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed -e 's/ /-/g' -e 's/[^a-z0-9-]//g' -e 's/--*/-/g' -e 's/^-\