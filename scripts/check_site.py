#!/usr/bin/env python3
"""Check local targets, metadata, structured data, and publication consistency."""
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / 'dist'


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.h1s, self.canonicals, self.descriptions = [], set(), 0, [], []
        self.in_schema, self.schema_text = False, ''
        self.schemas = []
        self.publications = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate ID {attrs["id"]}'
            self.ids.add(attrs['id'])
        if tag == 'h1':
            self.h1s += 1
        if tag == 'article' and 'publication' in attrs.get('class', '').split():
            assert attrs.get('data-status') in ('published', 'unpublished', 'thesis')
            assert attrs.get('data-type') in ('journal', 'conference', 'preprint', 'thesis')
            self.publications.append(attrs['id'])
        for attr in ('href', 'src'):
            if attr in attrs:
                self.links.append(attrs[attr])
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonicals.append(attrs['href'])
        if tag == 'meta' and attrs.get('name') == 'description':
            self.descriptions.append(attrs['content'])
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.in_schema, self.schema_text = True, ''

    def handle_data(self, text):
        if self.in_schema:
            self.schema_text += text

    def handle_endtag(self, tag):
        if tag == 'script' and self.in_schema:
            self.schemas.append(json.loads(self.schema_text))
            self.in_schema = False


def main():
    checked = 0
    for path in [ROOT / 'index.html', ROOT / 'publications/index.html']:
        page = Page()
        source = path.read_text()
        page.feed(source)
        assert page.h1s == 1 and len(page.canonicals) == 1
        assert len(page.descriptions) == 1 and page.schemas
        assert 'noindex' not in source
        if path.parent.name == 'publications':
            assert len(page.publications) == len(json.loads((ROOT.parent / 'data/publications.json').read_text()))
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            destination = (ROOT / unquote(url.path).lstrip('/')) if url.path.startswith('/') else path.parent / unquote(url.path)
            if not url.path:
                destination = path
            if destination.is_dir():
                destination /= 'index.html'
            assert destination.exists(), f'{path.name}: broken target {link}'
            if url.fragment and destination.suffix == '.html':
                other = Page()
                other.feed(destination.read_text())
                assert unquote(url.fragment) in other.ids, f'Unknown fragment {link}'
            checked += 1
    records = json.loads((ROOT.parent / 'data/publications.json').read_text())
    assert len(records) == len({p['id'] for p in records})
    assert sum((ROOT / 'publications.bib').read_text().count('@' + kind + '{') for kind in ('misc', 'article', 'inproceedings', 'phdthesis')) == len(records)
    assert 'https://stuartah.github.io/sitemap.xml' in (ROOT / 'robots.txt').read_text()
    print(f'Site checks passed: two pages, {checked} local links/assets, {len(records)} unique publication records.')


if __name__ == '__main__':
    main()
