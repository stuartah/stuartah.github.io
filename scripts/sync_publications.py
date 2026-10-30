#!/usr/bin/env python3
"""Refresh the static publication list from Stuart's identified arXiv author feed.

No scraping, API keys, browser-side requests, or third-party Python dependencies.
Existing records survive upstream failures; editorial overrides remain authoritative.
"""
import argparse
from datetime import date
import json
from pathlib import Path
import re
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FEED = 'https://arxiv.org/a/hadfield_s_1.atom'
NS = {'a': 'http://www.w3.org/2005/Atom', 'x': 'http://arxiv.org/schemas/atom'}


def clean_title(text):
    for old, new in [('\\"a', 'ä'), ('\\"o', 'ö'), ('\\"u', 'ü'), ("\\'e", 'é')]:
        text = text.replace(old, new)
    return re.sub(r'\s+', ' ', text.replace('$', '').replace('{', '').replace('}', '')).strip()


def infer_topics(title, categories):
    """Conservative browsing labels; per-paper overrides can refine these."""
    text = title.lower()
    topics = []
    rules = {
        'Optimization': ('optimization', 'qaoa', 'maxcut', 'max kxor', 'alternating operator', 'constraint programming'),
        'Complexity': ('complexity', 'barrier', 'counting optimal'),
        'Encodings': ('encoding', 'compression', 'compress', 'representation of boolean'),
        'Simulation': ('simulation', 'gauge', 'fourier transform', 'ground and excited', 'scientific computing'),
    }
    for topic, words in rules.items():
        if any(word in text for word in words):
            topics.append(topic)
    if any(c.startswith('hep-') for c in categories) and 'Simulation' not in topics:
        topics.append('Simulation')
    return topics


def parse_feed(raw):
    root = ET.fromstring(raw)
    entries = root.findall('a:entry', NS)
    if not entries:
        raise ValueError('No publication entries; refusing to replace the cached list.')
    records = []
    for entry in entries:
        url = entry.findtext('a:id', '', NS)
        match = re.fullmatch(r'https?://arxiv\.org/abs/((?:\d{4}\.\d{4,5}|[a-z-]+/\d{7}))(?:v\d+)?', url)
        authors = [a.findtext('a:name', '', NS).strip() for a in entry.findall('a:author', NS)]
        title = clean_title(entry.findtext('a:title', '', NS))
        published = entry.findtext('a:published', '', NS)[:10]
        if not match or not title or not authors or not published:
            raise ValueError('Incomplete or unrecognized arXiv publication metadata.')
        # This is an identified author's feed, with an additional per-entry identity check.
        if not any(re.fullmatch(r'Stuart(?:\s+A\.?)?\s+Hadfield', a) for a in authors):
            raise ValueError('Author identity mismatch; no changes have been written.')
        if date.fromisoformat(published) > date.today():
            continue
        journal = entry.findtext('x:journal_ref', '', NS).strip()
        journal_year = re.findall(r'\b(20\d{2})\b', journal)
        year = int(journal_year[-1]) if journal_year else int(published[:4])
        categories = [c.get('term', '') for c in entry.findall('a:category', NS)]
        records.append({
            'id': match[1], 'arxiv': match[1], 'title': title, 'authors': authors,
            'year': year, 'date': published, 'venue': journal or 'Preprint',
            'doi': entry.findtext('x:doi', '', NS).strip(),
            'topics': infer_topics(title, categories), 'summary': ''
        })
    if not records:
        raise ValueError('No eligible records; refusing an empty update.')
    return records


def merge_records(existing, imported, overrides):
    merged = {p['id']: dict(p) for p in existing}
    for paper in imported:
        old = merged.get(paper['id'], {})
        merged[paper['id']] = {**old, **paper}
        # Do not erase a locally supplied summary or useful subject labels.
        for field in ('summary',):
            if old.get(field):
                merged[paper['id']][field] = old[field]
    for ident, override in overrides.items():
        if ident not in merged:
            raise ValueError(f'An override has no underlying publication record: {ident}')
        merged[ident] = {**merged[ident], **override}
    # A DOI identifies a published work even if it has several arXiv identifiers.
    seen_doi, result = set(), []
    preferred = sorted(merged.values(), key=lambda p: p['id'] not in overrides)
    for paper in preferred:
        doi = paper.get('doi', '').lower().removeprefix('https://doi.org/').strip()
        if doi and doi in seen_doi:
            continue
        if doi:
            seen_doi.add(doi)
        result.append(paper)
    return sorted(result, key=lambda p: (p['year'], p.get('date', ''), p['id']), reverse=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--feed-file', type=Path, help='Use a previously downloaded Atom feed (offline validation).')
    args = parser.parse_args()
    if args.feed_file:
        raw = args.feed_file.read_bytes()
    else:
        request = urllib.request.Request(FEED, headers={'User-Agent': 'StuartHadfieldWebsite/1.0 (https://stuartah.github.io/)'} )
        with urllib.request.urlopen(request, timeout=45) as response:
            raw = response.read()
    imported = parse_feed(raw)
    target = ROOT / 'data/publications.json'
    records = merge_records(json.loads(target.read_text()), imported, json.loads((ROOT / 'data/overrides.json').read_text()))
    encoded = json.dumps(records, ensure_ascii=False, indent=2) + '\n'
    temporary = target.with_suffix('.tmp')
    temporary.write_text(encoded)
    temporary.replace(target)
    print(f'Publication import complete: {len(imported)} arXiv records; {len(records)} works after merging.')


if __name__ == '__main__':
    main()
