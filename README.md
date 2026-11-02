# Stuart Hadfield — research website

A small static site for GitHub Pages: a homepage and a publication list. No package installation or application server is required. The owner-selected design is Quiet modern with the Ink and blue palette, using a fixed light appearance. The new owner-supplied portrait is retained byte for byte in `assets/stuart-hadfield.jpg` and framed with CSS; no image retouching is applied.

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

The list can be filtered by search, publication status, publication type, topic, and year; filters combine and persist in the URL. Published includes accepted journal and conference papers, displayed with “to appear.” Journal articles, conference papers, preprints, and the dissertation have independent type labels. QPL is classified as a conference even though Crossref calls its proceedings-series record a journal article. A bare DOI does not establish publication.

`data/publications.json` is the cached bibliography. `data/overrides.json` holds intentional corrections, acceptance status, selected summaries, and topic labels; it takes precedence over feed metadata. When an accepted paper appears, update its venue/DOI and remove `publication_stage: accepted` from its override. New browsing labels are inferred conservatively from titles and arXiv subject categories. Titles, authors, journal references, and dates come from public records. Display years use the journal reference when supplied, otherwise the preprint year; individual overrides can refine this.

The list is not guaranteed to include work absent from the arXiv author record. Google Scholar and ORCID remain linked. Seven verified publication updates are recorded in the overrides with publisher/Crossref source URLs and check dates. Alternate preprint titles remain searchable when a published title differs. Conference metadata is curated with source URLs: both QCE 2026 technical papers, QPL 2022 (proceedings published in 2023), IPDPSW 2024, and PMES 2017. The distinct PMES paper has no separate arXiv ID and is maintained as a DOI-linked record; refreshes retain it. BibTeX uses article, inproceedings, phdthesis, or misc entries and includes venue and to-appear details.

After launch, GitHub Actions refreshes publications weekly and on manual request, saves changed records, rebuilds the site, and publishes the same build. Failed imports stop publication and leave the live version intact. Repository protections may require adapting direct publication-update commits to pull requests.

A separate ChatGPT Website Maintenance task reviews the public Google Scholar author profile on Sunday mornings around 08:00 America/New_York, starting November 8, 2026. Scholar is a discovery source: new papers and title, venue, DOI, year, or publication-status changes must be verified against primary sources before updating the cached bibliography and editorial overrides, running checks, and deploying. Accepted papers remain Published with “to appear” until final publication is verified. The review preserves the owner-selected homepage works and copy. This is an assistant task, not a Scholar importer in GitHub Actions. Public-profile access is checked within Google's current robots rules; blocked or incomplete access is reported and primary-source checks continue. The task does not bulk-scrape Scholar or bypass challenges.

The same private weekly review checks aggregate Clicky traffic, keeping Columbia and personal-domain hits distinct. Its traffic summary feeds the existing owner Project Status & Backup email, which currently runs monthly. Analytics records stay outside this public repository.

## Launch

1. Review and merge the redesign branch.
2. In **Settings → Pages → Build and deployment**, choose **GitHub Actions** as the publishing source, then run the site workflow. The included workflow validates pull requests without deploying them.
3. The production domain is `https://stuarthadfield.me/`. GitHub Pages also redirects the original `stuartah.github.io` address and `www.stuarthadfield.me` to it.

Both personal domains were registered at Porkbun on November 1, 2026. The `.me` apex uses an ALIAS to `stuartah.github.io`; `www` uses a CNAME to the same target. Keep the GitHub ownership TXT record. Porkbun has saved 301 forwarding rules for the `.si` apex and `www` to `.me` with path preservation; public DNS propagation and forwarding verification remain pending. DNS propagation, HTTPS and redirect checks are tracked in `TODO.md`.

## Clicky

The tracker reuses **site ID 101117148** from the Columbia homepage, using HTTPS and asynchronous loading. The hostname guard permits `stuarthadfield.me`, its `www` variant, and `stuartah.github.io`; local and review previews do not create analytics traffic.

In Clicky's existing site preferences, add `stuarthadfield.me`, `www.stuarthadfield.me`, and `stuartah.github.io` to **additional domains**, keeping domain validation enabled. This combines the new website and the Columbia homepage under the existing site ID; Clicky's Domains report can distinguish them. Successful event receipt must be checked in the authenticated Clicky dashboard after launch; it cannot be verified from public source code.

## Google search

The site includes static crawlable text and links, unique titles and descriptions, canonical HTTPS URLs, `robots.txt`, `sitemap.xml`, and Schema.org profile metadata. Structured data helps describe the page; it does not promise a special search result.

After the site is public:

1. Add the Domain property `stuarthadfield.me` to Google Search Console and verify using Google’s DNS TXT record. Retain the already verified URL-prefix property `https://stuartah.github.io/` and its verification file.
2. Submit `https://stuarthadfield.me/sitemap.xml` and use URL Inspection to request indexing of the homepage and publications page.
3. Link to this address from the Columbia page, Google Scholar profile, ORCID, and institutional profile where editable.

Google decides whether and when to index pages. Requests and sitemaps help discovery but do not guarantee indexing or ranking. The builder’s `ORIGIN` constant is `https://stuarthadfield.me`; generated canonical URLs, structured data, social metadata, robots and sitemap use that address.
