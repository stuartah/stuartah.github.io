#!/usr/bin/env python3
"""Generate Stuart Hadfield's static GitHub Pages site."""
from html import escape as e
import json
from pathlib import Path
import shutil

from news import homepage_news, news_items, ordered_news
from publication_metadata import is_to_appear, publication_status, publication_type, publication_venue

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://stuarthadfield.me'
SCHOLAR = 'https://scholar.google.com/citations?user=0zILLFkAAAAJ'
ORCID = 'https://orcid.org/0000-0002-4607-3921'
PHOTO = 'assets/stuart-hadfield.jpg'
PAPERS = sorted(json.loads((ROOT / 'data/publications.json').read_text()), key=lambda p: (p['year'], p.get('date', ''), p['id']), reverse=True)
BY_ID = {p['id']: p for p in PAPERS}
NEWS = ordered_news(json.loads((ROOT / 'data/news.json').read_text()))
MUSIC = json.loads((ROOT / 'data/music.json').read_text())


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
    return f"https://arxiv.org/abs/{paper['arxiv']}" if paper.get('arxiv') else paper['publication_url']


def bibtex(paper):
    title = paper['title'].replace('{', '').replace('}', '')
    fields = {'title': '{' + title + '}', 'author': ' and '.join(paper['authors']), 'year': str(paper['year']), 'url': paper_url(paper)}
    if paper.get('arxiv'):
        fields.update(eprint=paper['arxiv'], archivePrefix='arXiv')
    kind = publication_type(paper)
    entry_type = {'journal': 'article', 'conference': 'inproceedings', 'thesis': 'phdthesis'}.get(kind, 'misc')
    if kind == 'thesis' and paper.get('thesis_type') == 'honours':
        entry_type = 'misc'
    if paper.get('bibtex_entry_type') == 'incollection':
        entry_type = 'incollection'
        fields['booktitle'] = paper['booktitle']
        for field in ('series', 'volume', 'pages', 'publisher'):
            if paper.get(field):
                fields[field] = paper[field]
    elif kind in ('journal', 'conference'):
        fields['journal' if kind == 'journal' else 'booktitle'] = paper['venue']
    elif kind == 'thesis':
        if paper.get('thesis_type') == 'honours':
            fields['howpublished'] = paper['venue']
        else:
            fields['school'] = paper.get('school', 'Columbia University')
    if is_to_appear(paper):
        fields['note'] = 'To appear'
    if paper.get('doi'):
        fields['doi'] = paper['doi']
    key = 'Hadfield' + str(paper['year']) + '_' + paper['id'].replace('.', '').replace('/', '')
    return '@' + entry_type + '{' + key + ',\n' + ''.join('  ' + k + ' = {' + v + '},\n' for k, v in fields.items()) + '}\n'


def shell(page, title, description, body, collection=None):
    prefix = '../' if page else './'
    canonical = ORIGIN + ('/' + page + '/' if page else '/')
    person = {
        '@type': 'Person', '@id': ORIGIN + '/#person', 'name': 'Stuart Hadfield',
        'alternateName': 'Stuart A. Hadfield', 'url': ORIGIN + '/',
        'image': ORIGIN + '/' + PHOTO, 'jobTitle': 'Quantum computer scientist',
        'affiliation': {'@type': 'Organization', 'name': 'USRA Research Institute for Advanced Computer Science'},
        'alumniOf': {'@type': 'CollegeOrUniversity', 'name': 'Columbia University'},
        'sameAs': [ORCID, SCHOLAR, 'https://arxiv.org/a/hadfield_s_1', 'https://github.com/stuartah'],
        'knowsAbout': ['Quantum algorithms', 'Quantum optimization', 'Computational complexity', 'Quantum simulation']
    }
    schema = {
        '@context': 'https://schema.org', '@type': 'ProfilePage' if not page else 'CollectionPage',
        'url': canonical, 'name': title,
        'mainEntity': person if not page else {
            '@type': 'ItemList', 'itemListElement': collection if collection is not None else [
                {'@type': 'ListItem', 'position': i + 1, 'url': paper_url(p), 'name': p['title']}
                for i, p in enumerate(PAPERS)
            ]
        }
    }
    active = ' aria-current="page"' if page == 'publications' else ''
    news_active = ' aria-current="page"' if page == 'news' else ''
    music_active = ' aria-current="page"' if page == 'music' else ''
    structured = json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c')
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description, quote=True)}">
  <meta name="theme-color" content="#ffffff">
  <meta name="color-scheme" content="light">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{prefix}assets/site.css">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title, quote=True)}">
  <meta property="og:description" content="{e(description, quote=True)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{ORIGIN}/{PHOTO}">
  <meta property="og:image:alt" content="Stuart Hadfield">
  <meta name="twitter:card" content="summary">
  <script type="application/ld+json">{structured}</script>
  <script defer src="{prefix}assets/site.js"></script>
  <script defer src="{prefix}assets/analytics.js"></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header wrap">
  <a class="wordmark" href="{prefix}" aria-label="Stuart Hadfield, home">Stuart Hadfield</a>
  <button class="menu-toggle" aria-expanded="false" aria-controls="primary-nav" type="button">Menu</button>
  <nav id="primary-nav" aria-label="Main navigation">
    <a href="{prefix}#research">Research</a>
    <a href="{prefix}publications/"{active}>Publications</a>
    <a href="{prefix}news/"{news_active}>News</a>
    <a href="{prefix}music/"{music_active}>Music</a>
    <a href="{prefix}#contact">Contact</a>
  </nav>
</header>
<main id="main">{body}</main>
<footer class="site-footer wrap">
  <span>Stuart Hadfield</span>
  <div class="footer-links"><a href="{SCHOLAR}">Google Scholar</a><a href="{ORCID}">ORCID</a><a href="https://arxiv.org/a/hadfield_s_1">arXiv</a><a href="{prefix}music/"{music_active}>Music</a></div>
</footer>
<!-- Existing Clicky tracker runs only on the public production hostname. -->
</body>
</html>
'''


def selected_paper(ident):
    p = BY_ID[ident]
    venue = publication_venue(p)
    if str(p['year']) not in venue:
        venue += f", {p['year']}"
    return f'''<li class="selected-paper">
  <h3><a href="{paper_url(p)}">{e(p['title'])}</a></h3>
  <p class="paper-meta">{authors(p)} · {e(venue)}</p>
</li>'''


def recent_updates():
    entries = homepage_news(NEWS)
    if not entries:
        return ''
    return '<section class="recent-updates" id="news" aria-labelledby="news-title"><h2 id="news-title">Recent &amp; upcoming</h2>' + news_items(entries) + '<a class="all-news" href="news/">All news →</a></section>'


def news_archive():
    years = sorted({entry['date'][:4] for entry in NEWS}, reverse=True)
    groups = ''.join(
        f'<section class="news-year" aria-labelledby="year-{year}"><h2 id="year-{year}">{year}</h2>'
        + news_items([entry for entry in NEWS if entry['date'].startswith(year)]) + '</section>'
        for year in years
    )
    body = '<div class="wrap"><section class="page-intro"><h1>News</h1><p>Publications, talks, and other research news.</p></section><div class="news-archive">' + groups + '</div></div>'
    collection = [
        {'@type': 'ListItem', 'position': i + 1, 'url': ORIGIN + '/news/#news-' + entry['id'],
         'name': ''.join(part['text'] for part in entry['segments'])}
        for i, entry in enumerate(NEWS)
    ]
    return shell('news', 'News | Stuart Hadfield', 'News from Stuart Hadfield: papers, publications, and talks.', body, collection)


def music():
    sections = []
    collection = []
    for position, album in enumerate(MUSIC['albums'], 1):
        ident = album['id']
        title_id = ident + '-title'
        description = ''.join(f'<p>{e(paragraph)}</p>' for paragraph in album['description'])
        header = f'<p class="album-meta">Ponderosa · {e(album["dateline"])}</p><h2 id="{title_id}">{e(album["title"])}</h2><div class="album-description">{description}</div>'
        if album.get('review'):
            review = album['review']
            header += f'<blockquote class="album-review" cite="{e(review["source_url"], quote=True)}"><p>“{e(review["text"]) }”</p><footer><cite>{e(review["publication"])}</cite>, {review["year"]}</footer></blockquote>'
        if album['kind'] == 'youtube':
            poster = album.get('poster')
            poster_class = ' has-album-poster' if poster else ''
            poster_html = ''
            if poster:
                poster_path = '../' + e(poster['image'], quote=True)
                poster_html = f'<a class="album-poster" id="{ident}-poster" href="{poster_path}" aria-label="View the original {e(album["title"], quote=True)} CD launch poster full size"><img src="{poster_path}" alt="{e(poster["alt"], quote=True)}" width="{poster["width"]}" height="{poster["height"]}" loading="lazy" decoding="async"><span>CD launch poster <span aria-hidden="true">↗</span></span></a>'
            tracks = ''.join(
                f'<li><a href="{e(album["url"], quote=True)}&amp;t={track["start_seconds"]}s"><span>{e(track["title"])}</span><time>{e(track["time"])}</time></a></li>'
                for track in album['tracks']
            )
            sections.append(f'''<section class="music-album music-album-featured{poster_class}" id="{ident}" aria-labelledby="{title_id}">
    <a class="album-cover" href="{e(album['url'], quote=True)}" aria-label="Listen to Ponderosa — {e(album['title'], quote=True)} on YouTube"><img src="../{e(album['image'], quote=True)}" alt="Artwork for {e(album['title'], quote=True)}" width="{album['image_width']}" height="{album['image_height']}" decoding="async"></a>
    <div class="album-copy">{header}<a class="album-listen" href="{e(album['url'], quote=True)}">Listen to the full album on YouTube <span aria-hidden="true">↗</span></a><ol class="youtube-tracks" aria-label="{e(album['title'], quote=True)} tracks">{tracks}</ol></div>
    {poster_html}
  </section>''')
        else:
            recording_header = f'<div class="recording-heading"><div class="album-copy">{header}</div><button class="play-album" type="button" hidden>Play album</button></div>'
            if album.get('image'):
                recording_header = f'<div class="recording-intro"><figure class="venue-photo"><img src="../{e(album["image"], quote=True)}" alt="{e(album["image_alt"], quote=True)}" width="{album["image_width"]}" height="{album["image_height"]}" loading="lazy" decoding="async"></figure>{recording_header}</div>'
            tracks = ''.join(
                f'''<li class="audio-track"><span class="track-number" aria-hidden="true">{number:02d}</span><span class="track-title" id="{ident}-track-{number}">{e(track['title'])}</span><span class="track-duration">{e(track['time'])}</span><audio controls preload="none" controlslist="nodownload" aria-labelledby="{title_id} {ident}-track-{number}"><source src="../{e(track['file'], quote=True)}" type="audio/mpeg">Your browser does not support audio playback.</audio></li>'''
                for number, track in enumerate(album['tracks'], 1)
            )
            sections.append(f'''<section class="music-album music-recording" id="{ident}" aria-labelledby="{title_id}" data-recording>
    {recording_header}
    <ol class="audio-tracks" aria-label="{e(album['title'], quote=True)} tracks">{tracks}</ol><p class="playback-status" role="status"></p>
  </section>''')
        collection.append({'@type': 'ListItem', 'position': position, 'url': ORIGIN + '/music/#' + ident, 'name': 'Ponderosa — ' + album['title']})
    bio = ''.join(f'<p>{e(paragraph)}</p>' for paragraph in MUSIC['bio']['paragraphs'])
    history = MUSIC['bio']['archive']
    body = '<div class="wrap music-page"><section class="page-intro"><h1>Music</h1><p>I play guitar and piano.</p></section><section class="band-bio" aria-labelledby="band-title"><h2 id="band-title">Ponderosa</h2>' + bio + f'<p class="band-archive">From the archives: <a href="{e(history["url"], quote=True)}">{e(history["label"])}</a>.</p></section>' + ''.join(sections) + '</div>'
    return shell('music', 'Music | Stuart Hadfield', 'Stuart Hadfield plays guitar and piano and was the lead guitarist in Ponderosa. Listen to Attack of the Rosa!, Live at the Fairview, and the CDIS Sessions EP.', body, collection)


def home():
    selection = ''.join(selected_paper(ident) for ident in ['2611.00678', '2610.09584', '1709.03489', '2312.02279', '1804.09130', '1706.02998', '2303.05509', '2404.01412', '2607.09368', '2108.13305'])
    body = f'''
<div class="wrap">
  <section class="intro" aria-labelledby="home-title">
    <div class="intro-copy">
      <div class="intro-name">
        <h1 id="home-title">Stuart Hadfield</h1>
        <p class="intro-role">Quantum computer scientist</p>
        <p class="intro-affiliation"><a href="https://riacs.usra.edu/quantum/">USRA RIACS</a> · <a href="https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/nasa-quail/">NASA QuAIL</a></p>
      </div>
      <div class="intro-bio">
        <p>I study quantum algorithms for optimization and simulation, with a focus on their performance and computational complexity.</p>
        <p>I work with USRA’s Research Institute for Advanced Computer Science and the Quantum Artificial Intelligence Laboratory (QuAIL) at NASA Ames Research Center. I received my Ph.D. in computer science from Columbia University.</p>
        <div class="intro-links"><a href="{SCHOLAR}">Google Scholar</a><a href="{ORCID}">ORCID</a><a href="https://arxiv.org/a/hadfield_s_1">arXiv</a><a href="https://inspirehep.net/authors/1913623">INSPIRE</a><a href="https://www.linkedin.com/in/stuart-hadfield-4b250715">LinkedIn</a></div>
      </div>
    </div>
    <figure class="portrait"><img src="{PHOTO}" width="1789" height="2048" alt="Stuart Hadfield" fetchpriority="high"></figure>
  </section>
  {recent_updates()}
  <section class="research" id="research" aria-labelledby="research-title">
    <h2 id="research-title">Research Interests</h2>
    <div class="research-areas">
      <div><h3><a href="publications/?topic=Optimization">Quantum optimization</a></h3><p>QAOA, the quantum alternating operator ansatz, hybrid algorithms, and constrained combinatorial problems.</p></div>
      <div><h3><a href="publications/?topic=Complexity">Algorithms &amp; Complexity</a></h3><p>Algorithm design and analysis, approximation guarantees, state preparation, and the prospects for quantum advantage.</p></div>
      <div><h3><a href="publications/?topic=Simulation">Quantum simulation</a></h3><p>Algorithms and circuit primitives for scientific computing and simulating physical systems, from quantum chemistry to high energy physics.</p></div>
    </div>
  </section>
  <section class="selected-work" aria-labelledby="selected-title"><h2 id="selected-title">Selected publications</h2><ul class="selected-list">{selection}</ul><a class="browse-papers" href="publications/">All publications and preprints</a></section>
  <section class="background" id="about" aria-labelledby="background-title">
    <h2 id="background-title">Background</h2>
    <p>I received my Ph.D. in computer science from <a href="https://www.cs.columbia.edu/~stuartah/" title="Former Columbia homepage">Columbia University</a> in 2018, working in theoretical computer science and quantum computing. My advisers were <a href="https://www.cs.columbia.edu/~traub/">Joseph F. Traub</a>, <a href="https://www.cs.columbia.edu/~aho/">Alfred V. Aho</a>, and <a href="https://www.cs.columbia.edu/~ap/">Anargyros Papageorgiou</a>. My dissertation, <a href="https://arxiv.org/abs/1805.03265">Quantum Algorithms for Scientific Computing and Approximate Optimization</a>, is freely available on arXiv. I joined <a href="https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/nasa-quail/">NASA QuAIL</a> and USRA’s <a href="https://riacs.usra.edu/quantum/">Research Institute for Advanced Computer Science (RIACS)</a> in spring 2018.</p>
    <p>Before my Ph.D., I received a master’s degree in computer science from Columbia, an honours degree in theoretical physics from the University of Melbourne, and a bachelor’s degree in engineering physics from the University of British Columbia. My honours thesis studied fault-tolerant quantum computation. I also worked in software and hardware engineering, specializing in embedded systems and performance optimization.</p>
    <p>My broader interests include the mathematical foundations of quantum physics and computation, and the ways science and technology can improve people’s lives. I am a founding member of <a href="https://q4climate.org/">Q4Climate</a>, an initiative exploring quantum computing and climate change.</p>
  </section>
  <section class="contact" id="contact" aria-labelledby="contact-title"><h2 id="contact-title">Contact</h2><p><a class="contact-email" href="mailto:stuart.hadfield@columbia.edu">stuart.hadfield@columbia.edu</a></p><p>New York, NY</p><p class="internship-note">We are often looking for research interns in quantum computing and related areas. See the <a href="https://riacs.usra.edu/quantum/academy/">Feynman Quantum Academy</a> for application details.</p></section>
</div>
'''
    return shell('', 'Stuart Hadfield | Quantum Algorithms, Optimization & Complexity', 'Stuart Hadfield is a quantum computer scientist at USRA/RIACS and NASA QuAIL. Research in quantum algorithms, optimization, complexity, and simulation.', body)


def publication(paper):
    topics = paper.get('topics') or ['Other']
    status = publication_status(paper)
    kind = publication_type(paper)
    venue = publication_venue(paper)
    searchable = ' '.join([paper['title'], *paper.get('alternate_titles', []), *paper['authors'], venue, str(paper['year']), *topics, paper.get('summary', ''), paper.get('arxiv', '')])
    journal = paper.get('journal_url') or paper.get('publication_url') or ('https://doi.org/' + paper['doi'] if paper.get('doi') else '')
    journal_label = 'Conference' if kind == 'conference' else 'PDF' if kind == 'thesis' and journal.endswith('.pdf') else 'Publication'
    journal_link = f'<a href="{e(journal, quote=True)}">{journal_label}</a>' if journal else ''
    preprint_links = f'<a href="{paper_url(paper)}">arXiv</a><a href="https://arxiv.org/pdf/{paper["arxiv"]}">PDF</a>' if paper.get('arxiv') else ''
    summary = f'<details><summary>Summary</summary><div>{e(paper["summary"])}</div></details>' if paper.get('summary') else ''
    return f'''<article class="publication" id="paper-{paper['id'].replace('/', '-')}" data-year="{paper['year']}" data-status="{status}" data-type="{kind}" data-topics="{e('|'.join(topics), quote=True)}" data-search="{e(searchable, quote=True)}">
  <div class="pub-year">{paper['year']}</div>
  <div><h2><a href="{paper_url(paper)}">{e(paper['title'])}</a></h2>
    <div class="pub-authors">{authors(paper)}</div><p class="pub-venue">{e(venue)}</p>
    <div class="pub-links">{preprint_links}{journal_link}{summary}
      <details class="citation"><summary>BibTeX</summary><div><pre><code>{e(bibtex(paper))}</code></pre><button class="copy-citation" type="button" aria-label="Copy citation for {e(paper['title'], quote=True)}">Copy citation</button></div></details>
    </div>
  </div>
</article>'''


def publications():
    years = sorted({p['year'] for p in PAPERS}, reverse=True)
    topics = sorted({t for p in PAPERS for t in p.get('topics', [])})
    options = ''.join(f'<option value="{e(t)}">{e(t)}</option>' for t in topics)
    year_options = ''.join(f'<option value="{y}">{y}</option>' for y in years)
    body = f'''<div class="wrap">
  <section class="page-intro"><h1>Publications</h1><p>Papers and preprints on quantum algorithms, optimization, simulation, and computational complexity.</p><div class="intro-links"><a href="{SCHOLAR}">Google Scholar</a><a href="https://arxiv.org/a/hadfield_s_1">arXiv author page</a><a href="../publications.bib" download>Download BibTeX</a></div></section>
  <section aria-label="Publication list">
    <div class="publication-tools" hidden>
      <div class="filter-fields">
        <div class="field"><label for="publication-search">Search publications</label><input id="publication-search" type="search" placeholder="Title, author, keyword…" autocomplete="off"></div>
        <div class="field"><label for="publication-status">Publication status</label><select id="publication-status" aria-describedby="publication-status-note"><option value="">All statuses</option><option value="published">Published</option><option value="unpublished">Not yet published</option><option value="thesis">Thesis</option></select></div>
        <div class="field"><label for="publication-type">Publication type</label><select id="publication-type"><option value="">All types</option><option value="journal">Journals</option><option value="conference">Conferences</option><option value="preprint">Preprints</option><option value="thesis">Thesis</option></select></div>
        <div class="field"><label for="publication-topic">Topic</label><select id="publication-topic"><option value="">All topics</option>{options}</select></div>
        <div class="field"><label for="publication-year">Year</label><select id="publication-year"><option value="">All years</option>{year_options}</select></div>
      </div>
      <div class="filter-status"><span id="publication-count" role="status" aria-live="polite">{len(PAPERS)} works</span><button class="reset-filters" type="button" hidden>Clear filters</button></div>
      <p class="status-note" id="publication-status-note">Published includes accepted papers, marked “to appear.” Theses are listed separately.</p>
    </div>
    <div class="pub-list">{''.join(publication(p) for p in PAPERS)}</div>
    <div class="empty-state" id="empty-state" hidden><h2>No matching publications</h2><p>Try a different title, author, or keyword.</p></div>
    <p class="pub-note">For my broader publication record, see <a href="{SCHOLAR}">Google Scholar</a>.</p>
  </section>
  <div class="publications-contact"><a href="mailto:stuart.hadfield@columbia.edu">Contact me</a></div>
</div>'''
    return shell('publications', 'Publications | Stuart Hadfield', 'Papers and preprints by Stuart Hadfield on quantum optimization, QAOA, computational complexity, quantum encodings, and simulation. Open-access links and citations.', body)


def main():
    (ROOT / 'index.html').write_text(home())
    (ROOT / 'publications').mkdir(exist_ok=True)
    (ROOT / 'publications/index.html').write_text(publications())
    (ROOT / 'news').mkdir(exist_ok=True)
    (ROOT / 'news/index.html').write_text(news_archive())
    (ROOT / 'music').mkdir(exist_ok=True)
    (ROOT / 'music/index.html').write_text(music())
    (ROOT / 'publications.bib').write_text('\n'.join(bibtex(p) for p in PAPERS))
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n')
    (ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{ORIGIN}/</loc></url><url><loc>{ORIGIN}/publications/</loc></url><url><loc>{ORIGIN}/news/</loc></url><url><loc>{ORIGIN}/music/</loc></url></urlset>\n')
    not_found = '<section class="error-page wrap"><h1>Page not found</h1><p>The page you’re looking for isn’t here.</p><a href="/">Return home</a></section>'
    error = shell('', 'Page not found | Stuart Hadfield', 'Return to Stuart Hadfield’s research website.', not_found).replace('<head>', '<head>\n  <meta name="robots" content="noindex">').replace('href="./', 'href="/').replace('src="./', 'src="/')
    (ROOT / '404.html').write_text(error)
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    for item in dist.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()
    for name in ['index.html', '404.html', 'publications.bib', 'robots.txt', 'sitemap.xml', '.nojekyll', 'googlec17f3c4efc3142ce.html']:
        shutil.copy2(ROOT / name, dist / name)
    for name in ['assets', 'publications', 'news', 'music']:
        shutil.copytree(ROOT / name, dist / name, dirs_exist_ok=True)
    print(f'Built four pages and bibliography for {len(PAPERS)} works.')


if __name__ == '__main__':
    main()
