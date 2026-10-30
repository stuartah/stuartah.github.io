# Stuart Hadfield — research website

A small static site for GitHub Pages: a homepage and a publication list. No package installation or application server is required. The original portrait is retained.

## Editing

The shared page layout and homepage copy live in `scripts/build.py`; styles and behavior live in `assets/`.

```sh
python3 scripts/build.py
python3 scripts/check_site.py
python3 -m unittest discover -s scripts -p 'test_*.py'
```

Generated HTML is committed so it can also be served directly. `dist/` contains an identical public-only deployment bundle.

## Publications

```sh
python3 scripts/sync_publications.py
python3 scripts/build.py
```

The importer reads `https://arxiv.org/a/hadfield_s_1.atom`, an identified author feed. It checks authorship, merges by stable arXiv ID, removes duplicate DOIs, and preserves existing records if a paper is absent upstream. Invalid or failed responses leave the cached list untouched. The visitor never waits for an external publication service.

`data/publications.json` is the cached bibliography. `data/overrides.json` holds intentional corrections, acceptance status, selected summaries, and topic labels; it takes precedence over feed metadata. New browsing labels are inferred conservatively from titles and arXiv subject categories. Titles, authors, journal references, and dates come from public records. Display years use the journal reference when supplied, otherwise the preprint year; individual overrides can refine this.

The list is not guaranteed to include work absent from the arXiv author record. Google Scholar and ORCID remain linked. Google Scholar is not scraped. Other metadata sources can be added later.

After launch, GitHub Actions refreshes publications weekly and on manual request, saves changed records, rebuilds the site, and publishes the same build. Failed imports stop publication and leave the live version intact. Repository protections may require adapting direct publication-update commits to pull requests.

## Launch

1. Review and merge the redesign branch.
2. In **Settings → Pages → Build and deployment**, choose **GitHub Actions** as the publishing source, then run the site workflow. The included workflow validates pull requests without deploying them.
3. Confirm the deployment at `https://stuartah.github.io/`.

## Clicky

The tracker reuses **site ID 101117148** from the Columbia homepage, using HTTPS and asynchronous loading. It runs only on `stuartah.github.io`, so local and review previews do not create analytics traffic.

In Clicky's existing site preferences, add `stuartah.github.io` to **additional domains**, keeping domain validation enabled. This combines both domains under the existing site ID; Clicky's Domains report can distinguish them. If a personal domain is added later, update that setting and the hostname guard in `assets/analytics.js`. Successful event receipt must be checked in the authenticated Clicky dashboard after launch; it cannot be verified from public source code.

## Google search

The site includes static crawlable text and links, unique titles and descriptions, canonical HTTPS URLs, `robots.txt`, `sitemap.xml`, and Schema.org profile metadata. Structured data helps describe the page; it does not promise a special search result.

After the site is public:

1. Add the URL-prefix property `https://stuartah.github.io/` to Google Search Console and verify ownership using an HTML file or meta tag supplied by Google. A `github.io` subdomain is not a domain whose DNS we control.
2. Submit `https://stuartah.github.io/sitemap.xml` and use URL Inspection to request indexing of the homepage and publications page.
3. Link to this address from the Columbia page, Google Scholar profile, ORCID, and institutional profile where editable.

Google decides whether and when to index pages. Requests and sitemaps help discovery but do not guarantee indexing or ranking. If a custom domain is chosen later, update the single `ORIGIN` constant in the builder and set up redirects and verification for that domain.
