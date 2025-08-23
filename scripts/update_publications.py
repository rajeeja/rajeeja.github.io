#!/usr/bin/env python3
import csv
import os
import re
from typing import List, Dict, Any

try:
    import yaml
except ImportError:
    yaml = None


def load_scholar_user_id(config_path: str) -> str:
    # 1) ENV override
    env_id = os.getenv("SCHOLAR_USER_ID")
    if env_id:
        return env_id
    # 2) Try YAML parse
    if yaml:
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f)
            author = (cfg or {}).get("author", {}) or {}
            scholar_url = author.get("googlescholar", "")
            m = re.search(r"[?&]user=([A-Za-z0-9_-]+)", scholar_url)
            if m:
                return m.group(1)
        except Exception:
            pass
    # 3) Fallback: regex scan of raw text (tolerates tabs etc.)
    with open(config_path, "r", encoding="utf-8") as f:
        txt = f.read()
    m = re.search(r'googlescholar\s*:\s*"?https?://[^\n]*?[?&]user=([A-Za-z0-9_-]+)\b', txt)
    if m:
        return m.group(1)
    raise RuntimeError("Could not find Google Scholar user ID; set SCHOLAR_USER_ID env var or update _config.yml author.googlescholar")


def format_authors(bib_authors: Any) -> str:
    # scholarly returns a string of authors ("A B; C D" or "A B, C D") or list
    if isinstance(bib_authors, list):
        names = bib_authors
    elif isinstance(bib_authors, str):
        if ' and ' in bib_authors:
            names = [n.strip() for n in bib_authors.split(' and ') if n.strip()]
        elif ';' in bib_authors:
            names = [n.strip() for n in bib_authors.split(';') if n.strip()]
        else:
            names = [n.strip() for n in bib_authors.split(',') if n.strip()]
    else:
        names = []
    out: List[str] = []
    for name in names:
        parts = name.split()
        if not parts:
            continue
        last = parts[-1]
        first = " ".join(parts[:-1])
        out.append(f"{last}, {first}".strip())
    return ("; ".join(out) + ";") if out else ""


def to_int(s):
    try:
        return int(str(s).strip())
    except Exception:
        return -10**9


def fetch_from_scholar(user_id: str) -> List[Dict[str, str]]:
    from scholarly import scholarly

    author = scholarly.search_author_id(user_id)
    author = scholarly.fill(author, sections=['publications'])

    rows: List[Dict[str, str]] = []
    for pub in author.get('publications', []):
        try:
            pub = scholarly.fill(pub)
        except Exception:
            continue
        bib = pub.get('bib', {})
        title = (bib.get('title') or '').strip()
        year = str(bib.get('pub_year') or '').strip()
        venue = (bib.get('venue') or bib.get('journal') or bib.get('conference') or '').strip()
        authors = format_authors(bib.get('author', ''))
        volume = str(bib.get('volume') or '').strip()
        number = str(bib.get('number') or '').strip()
        pages = str(bib.get('pages') or '').strip()
        publisher = str(bib.get('publisher') or '').strip()

        if title and year:
            rows.append({
                'Authors': authors,
                'Title': title,
                'Publication': venue,
                'Volume': volume,
                'Number': number,
                'Pages': pages,
                'Year': year,
                'Publisher': publisher,
            })

    # Deduplicate by Title+Year
    seen = set()
    deduped = []
    for r in rows:
        key = (r['Title'].lower(), r['Year'])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(r)

    deduped.sort(key=lambda r: (to_int(r['Year']), r['Title'].lower()), reverse=True)
    return deduped


def write_citations_csv(path: str, rows: List[Dict[str, str]]):
    fieldnames = ['Authors', 'Title', 'Publication', 'Volume', 'Number', 'Pages', 'Year', 'Publisher']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    config_path = os.path.join(repo_root, '_config.yml')
    data_csv = os.path.join(repo_root, '_data', 'citations.csv')

    user_id = load_scholar_user_id(config_path)
    rows = fetch_from_scholar(user_id)

    y2025 = [r for r in rows if str(r['Year']).strip() == '2025']
    print(f"Fetched {len(rows)} publications from Scholar; {len(y2025)} entries for 2025.")

    new_csv = os.path.join(repo_root, '_data', 'citations.new.csv')
    write_citations_csv(new_csv, rows)

    old = ''
    if os.path.exists(data_csv):
        with open(data_csv, 'r', encoding='utf-8') as f:
            old = f.read()
    with open(new_csv, 'r', encoding='utf-8') as f:
        new = f.read()

    if new != old:
        os.replace(new_csv, data_csv)
        print(f"Updated {data_csv}")
    else:
        os.remove(new_csv)
        print("No changes to citations.csv")


if __name__ == '__main__':
    main()