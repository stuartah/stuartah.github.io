#!/usr/bin/env python3
"""Generate a small, accessible GitHub Pages site with Python's standard library."""
from html import escape as e
import json
from pathlib import Path
import shutil
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://stuartah.github.io'
SCHOLAR = 'https://scholar.google.com/citations?user=0zILLFkAAAAJ'
ORCID = 'https://orcid.org/0000-0002-4607-3921'
PAPERS = sorted(json.loads((ROOT / 'data/publications.json').read_text()), key=lambda p: (p['year'], p.get('date', ''), p['id']), reverse=True)
BY_ID = {p['id']: p for p in PAPERS}


def natural_name(name):
    if ',' in name:
        last, first = name.split(',', 1)
        return f'{first.strip()} {last.strip()}'
    return name


def authors(paper):
    names = [natural_name(name) for name in paper['authors']]
    if len(names) > 8:
        return e(names[0]) + ' et al. (including <strong>Stuart Hadfield</strong>)'
    return ', '.join(f'<strong>{e(n)}</strong>' if 'Stuart' in n and 'Hadfield' in n else e(n) for n in names)


def paper_url(paper):
    return f"https://arxiv.org/abs/{paper['arxiv']}"


def bibtex(paper):
    # Unicode is supported by modern BibTeX toolchains; braces protect title casing.
    title = paper['title'].replace('{', '').replace('}', '')
    fields = {'title': '{' + title + '}', 'author': ' and '.join(paper['authors']), 'year': str(paper['year']), 'eprint': paper['arxiv'], 'archivePrefix': 'arXiv', 'url': paper_url(paper)}
    if paper.get('doi'):
        fields['doi'] = paper['doi']
    key = 'Hadfield' + str(paper['year']) + '_' + paper['arxiv'].replace('.', '').replace('/', '')
    return '@misc{' + key + ',\n' + ''.join('  ' + k + ' = {' + v + '},\n' for k, v in fields.items()) + '}\n'


def shell(page, title, description, body):
    prefix = '../' if page else './'
    canonical = ORIGIN + ('/' + page + '/' if page else '/')
    person = {'@type': 'Person', '@id': ORIGIN + '/#person', 'name': 'Stuart Hadfield', 'alternateName': 'Stuart A. Hadfield', 'url': ORIGIN + '/', 'image': ORIGIN + '/SHprofile.jpg', 'jobTitle': 'Quantum computer scientist', 'affiliation': {'@type': 'Organization', 'name': 'USRA Research Institute for Advanced Computer Science'}, 'alumniOf': {'@type': 'CollegeOrUniversity', 'name': 'Columbia University'}, 'sameAs': [ORCID, SCHOLAR, 'https://arxiv.org/a/hadfield_s_1', 'https://github.com/stuartah'], 'knowsAbout': ['Quantum algorithms', 'Quantum optimization', 'Computational complexity', 'Quantum simulation']}
    schema = {'@context': 'https://schema.org', '@type': 'ProfilePage' if not page else 'CollectionPage', 'url': canonical, 'name': title, 'mainEntity': person if not page else {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': paper_url(p), 'name': p['title']} for i, p in enumerate(PAPERS)]}}
    active = ' aria-current="page"' if page == 'publications' else ''
    home_active = ' aria-current="page"' if not page else ''
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description, quote=True)}">
  <meta name="theme-color" content="#f6f4ee">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{prefix}assets/site.css">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title, quote=True)}">
  <meta property="og:description" content="{e(description, quote=True)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{ORIGIN}/SHprofile.jpg">
  <meta name="twitter:card" content="summary">
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False).replace('<', '&lt;')}</script>
  <script defer src="{prefix}assets/site.js"></script>
  <script defer src="{prefix}assets/analytics.js"></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header wrap">
  <a class="wordmark" href="{prefix}" aria-label="Stuart Hadfield, home"><span class="monogram" aria-hidden="true">s.</span><span class="wordmark-name">Stuart Hadfield</span></a>
  <button class="menu-toggle" aria-expanded="false" aria-controls="primary-nav" type="button">Menu</button>
  <nav id="primary-nav" aria-label="Main navigation">
    <a href="{prefix}"{home_active}>Home</a><a href="{prefix}#research">Research</a><a href="{prefix}publications/"{active}>Publications</a><a href="{prefix}#about">About</a><a class="nav-contact" href="{prefix}#contact">Contact <span aria-hidden="true">↗</span></a>
  </nav>
</header>
<main id="main">{body}</main>
<footer class="site-footer wrap">
  <div class="footer-identity"><strong>Stuart A. Hadfield</strong><div class="footer-note">Quantum algorithms · Optimization · Complexity</div></div>
  <div class="footer-links"><a class="external" href="{SCHOLAR}">Google Scholar</a><a class="external" href="{ORCID}">ORCID</a><a class="external" href="https://arxiv.org/a/hadfield_s_1">arXiv</a></div>
</footer>
<!-- Clicky site 101117148 is reused from the Columbia homepage. The script
     runs only on the public production hostname, so previews are not counted. -->
</body>
</html>
'''


def reading_item(ident, label):
    paper = BY_ID[ident]
    return f'''<article class="reading-item"><div class="meta">{e(label)}<span class="separator">/</span>{paper['year']}</div><h3><a href="{paper_url(paper)}">{e(paper['title'])}</a></h3><p>{e(paper['summary'])}</p><a class="text-link" href="{paper_url(paper)}">Read the paper <span class="arrow" aria-hidden="true">↗</span></a></article>'''


def home():
    body = f'''
<div class="wrap">
  <section class="hero" aria-labelledby="home-title">
    <div class="hero-copy"><p class="eyebrow">Quantum algorithms &amp; complexity</p><h1 id="home-title">Stuart<span>Hadfield.</span></h1><p class="hero-role">Quantum computer scientist</p><p class="hero-description">I study how quantum computers can solve hard problems in optimization and simulation, and what limits their power.</p><div class="hero-actions"><a class="button" href="publications/">Publications <span aria-hidden="true">↗</span></a><a class="text-link" href="#research">Explore my research <span class="arrow" aria-hidden="true">↓</span></a></div></div>
    <figure class="portrait"><div class="portrait-label">QUANTUM MECHANIC</div><img src="SHprofile.jpg" width="196" height="260" alt="Portrait of Stuart Hadfield" fetchpriority="high"><figcaption class="portrait-caption"><span>Stuart A. Hadfield</span><span>hello.</span></figcaption></figure>
  </section>
  <div class="affiliation-bar"><div><strong><a href="https://riacs.usra.edu/quantum/">USRA · Research Institute for Advanced Computer Science</a></strong></div><div><a href="https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/nasa-quail/">NASA QuAIL · Ames Research Center</a></div></div>
  <section class="section" id="research" aria-labelledby="research-title">
    <div class="section-heading"><div class="label-group"><span class="section-number">01</span><h2 id="research-title">Research</h2></div><p>Algorithms, their applications, and the boundaries of quantum advantage.</p></div>
    <a class="research-row" href="publications/?topic=Optimization"><span class="row-number">01</span><h3>Quantum optimization</h3><p>Designing and understanding algorithms for hard combinatorial problems, including QAOA and the quantum alternating operator ansatz.</p><span class="row-arrow" aria-hidden="true">↗</span></a>
    <a class="research-row" href="publications/?topic=Complexity"><span class="row-number">02</span><h3>Computational complexity</h3><p>Understanding which approximation guarantees quantum computers can achieve, and the limits imposed by state preparation and quantum encodings.</p><span class="row-arrow" aria-hidden="true">↗</span></a>
    <a class="research-row" href="publications/?topic=Simulation"><span class="row-number">03</span><h3>Quantum simulation</h3><p>Developing algorithms and circuit primitives for scientific computing, physical systems, and lattice gauge theories.</p><span class="row-arrow" aria-hidden="true">↗</span></a>
  </section>
  <section class="section reading" aria-labelledby="reading-title"><div class="section-heading"><div class="label-group"><span class="section-number">02</span><h2 id="reading-title">Selected work</h2></div><p>A few starting points, from algorithm design to recent complexity results.</p></div><div class="reading-grid">{reading_item('1709.03489','Alternating operator ansatz')}{reading_item('2610.09584','Recent preprint')}{reading_item('2312.02279','Review · Nature Reviews Physics')}{reading_item('2609.07090','Quantum encodings')}</div><div class="reading-footer"><span>More papers, preprints, and open-access links.</span><a class="text-link" href="publications/">Browse publications <span class="arrow" aria-hidden="true">↗</span></a></div></section>
</div>
<section class="about-strip" id="about" aria-labelledby="about-title"><div class="wrap"><div><p class="eyebrow">A little background</p><h2 id="about-title">Computer science.<br>Quantum physics.<br>Hard questions.</h2></div><div><p>I am a quantum scientist with USRA’s Research Institute for Advanced Computer Science, working with NASA’s QuAIL collaboration at Ames Research Center.</p><p>I received my Ph.D. in computer science from Columbia University in 2018. My research brings together algorithms, computational complexity, and physics, with applications in optimization and scientific computing.</p><a class="text-link" href="https://arxiv.org/abs/1805.03265">My Ph.D. dissertation <span class="arrow" aria-hidden="true">↗</span></a></div></div></section>
<section class="contact wrap" id="contact" aria-labelledby="contact-title"><div class="contact-top"><div><p class="eyebrow">Get in touch</p><h2 id="contact-title">Let’s talk research.</h2><p>For research questions, collaboration, or a conversation about quantum computing.</p></div><a class="contact-email" href="mailto:shadfield@usra.edu">shadfield@usra.edu <span aria-hidden="true">↗</span></a></div></section>
'''
    return shell('', 'Stuart Hadfield | Quantum Algorithms, Optimization & Complexity', 'Stuart Hadfield is a quantum computer scientist at USRA/RIACS and NASA QuAIL. Research in quantum algorithms, optimization, complexity, and simulation.', body)


def publication(paper):
    topics = paper.get('topics') or ['Other']
    searchable = ' '.join([paper['title'], *paper['authors'], paper.get('venue', ''), str(paper['year']), *topics, paper.get('summary', ''), paper['arxiv']])
    journal = paper.get('journal_url') or ('https://doi.org/' + paper['doi'] if paper.get('doi') else '')
    journal_link = f'<a class="external" href="{e(journal, quote=True)}">Journal</a>' if journal else ''
    summary = f'<details><summary>Summary</summary><div>{e(paper["summary"])}</div></details>' if paper.get('summary') else ''
    citation = e(bibtex(paper))
    return f'''<article class="publication" id="paper-{paper['id'].replace('/', '-')}" data-year="{paper['year']}" data-topics="{e('|'.join(topics), quote=True)}" data-search="{e(searchable, quote=True)}"><div class="pub-year">{paper['year']}</div><div><h2><a href="{paper_url(paper)}">{e(paper['title'])}</a></h2><div class="pub-authors">{authors(paper)}</div><p class="pub-venue">{e(paper['venue'])}</p><div class="pub-links"><a class="external" href="{paper_url(paper)}">arXiv</a><a class="external" href="https://arxiv.org/pdf/{paper['arxiv']}">PDF</a>{journal_link}{summary}<details class="citation"><summary>BibTeX</summary><div><pre><code>{citation}</code></pre><button class="copy-citation" type="button" aria-label="Copy citation for {e(paper['title'], quote=True)}">Copy citation</button></div></details></div></div></article>'''


def publications():
    years = sorted({p['year'] for p in PAPERS}, reverse=True)
    topics = sorted({t for p in PAPERS for t in p.get('topics', [])})
    options = ''.join(f'<option value="{e(t)}">{e(t)}</option>' for t in topics)
    year_options = ''.join(f'<option value="{y}">{y}</option>' for y in years)
    body = f'''<div class="wrap"><section class="page-intro"><p class="eyebrow">Papers &amp; preprints</p><h1>Publications.</h1><p>Work on quantum algorithms, optimization, simulation, and computational complexity.</p><div class="intro-links"><a class="external" href="{SCHOLAR}">Google Scholar</a><a class="external" href="https://arxiv.org/a/hadfield_s_1">arXiv author page</a><a href="../publications.bib" download>Download BibTeX ↓</a></div></section><section aria-label="Publication list"><div class="publication-tools" hidden><div class="filter-fields"><div class="field"><label for="publication-search">Search publications</label><input id="publication-search" type="search" placeholder="Title, author, keyword…" autocomplete="off"></div><div class="field"><label for="publication-topic">Topic</label><select id="publication-topic"><option value="">All topics</option>{options}</select></div><div class="field"><label for="publication-year">Year</label><select id="publication-year"><option value="">All years</option>{year_options}</select></div></div><div class="filter-status"><span id="publication-count" role="status" aria-live="polite">{len(PAPERS)} works</span><button class="reset-filters" type="button" hidden>Clear filters</button></div></div><div class="pub-list">{''.join(publication(p) for p in PAPERS)}</div><div class="empty-state" id="empty-state" hidden><h2>No matching publications.</h2><p>Try a different title, author, or keyword.</p></div><p class="pub-note">This list combines my arXiv author record with selected publication details. For my broader publication record, see <a href="{SCHOLAR}">Google Scholar</a>.</p></section></div><section class="contact wrap"><div class="contact-top"><div><h2>A question about the work?</h2><p>I’m happy to hear from fellow researchers.</p></div><a class="contact-email" href="mailto:shadfield@usra.edu">Get in touch <span aria-hidden="true">↗</span></a></div></section>'''
    return shell('publications', 'Publications | Stuart Hadfield', 'Papers and preprints by Stuart Hadfield on quantum optimization, QAOA, computational complexity, quantum encodings, and simulation. Open-access links and citations.', body)


def main():
    (ROOT / 'index.html').write_text(home())
    (ROOT / 'publications').mkdir(exist_ok=True)
    (ROOT / 'publications/index.html').write_text(publications())
    (ROOT / 'publications.bib').write_text('\n'.join(bibtex(p) for p in PAPERS))
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n')
    (ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{ORIGIN}/</loc></url><url><loc>{ORIGIN}/publications/</loc></url></urlset>\n')
    not_found = '<section class="error-page wrap"><p class="eyebrow">404 · Page not found</p><h1>A different path.</h1><p>The page you’re looking for isn’t here.</p><a class="button" href="/">Return home <span aria-hidden="true">↗</span></a></section>'
    error = shell('', 'Page not found | Stuart Hadfield', 'Return to Stuart Hadfield’s research website.', not_found).replace('<head>', '<head>\n  <meta name="robots" content="noindex">').replace('href="./', 'href="/').replace('src="./', 'src="/')
    (ROOT / '404.html').write_text(error)
    # Preview uses the identical built bytes that are committed for GitHub Pages.
    dist = ROOT / 'dist'
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir()
    for name in ['index.html', '404.html', 'publications.bib', 'robots.txt', 'sitemap.xml', 'SHprofile.jpg', '.nojekyll']:
        shutil.copy2(ROOT / name, dist / name)
    for name in ['assets', 'publications']:
        shutil.copytree(ROOT / name, dist / name, dirs_exist_ok=True)
    print(f'Built two pages and bibliography for {len(PAPERS)} works.')


if __name__ == '__main__':
    main()
