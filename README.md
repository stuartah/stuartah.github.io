# Stuart Hadfield — research website

A small static site for GitHub Pages: a homepage, a publication list, and a news archive. No package installation or application server is required. The owner-selected design is Quiet modern with the Ink and blue palette, using a fixed light appearance. The new owner-supplied portrait is retained byte for byte in `assets/stuart-hadfield.jpg` and framed with CSS; no image retouching is applied.

## Editing

The shared page layout and homepage copy live in `scripts/build.py`; styles and behavior live in `assets/`.

The Recent & upcoming section and `/news/` archive share `data/news.json`. All owner-approved announcements remain in the archive, newest first and grouped by year. The homepage shows at most five: retain explicit `pinned` entries (the IEEE item is pinned for now), reserve a recent talk, publication milestone and new preprint when each category is available within the last year, then fill with the newest items. Category preference does not force stale announcements into the selection. Review old pins with Stuart. Use `kind: talk|publication|preprint|award`, public primary-source links, check dates, and past-tense wording after events. Dates may use YYYY-MM for month-only announcements; publication records retain exact arXiv submission dates. Removing a pin or a homepage slot never deletes archive history. Future new announcements still require Stuart's selection; the existing weekly task proposes candidates and maintains the approved list.

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

The November 4, 2026 bibliography audit reconciled the complete 52-entry CV research list with the identified arXiv feed, ORCID, INSPIRE, DBLP, NASA's QuAIL publications and the former Columbia website. The audit and source-access limits are recorded in `docs/bibliography-audit-2026-11-04.md`. The author feed is incomplete: verified work outside it is retained in the cache and overrides. Future reviews must compare these other inventories rather than treating a successful feed refresh as proof of completeness. Google Scholar remains a discovery source when accessible.

Alternate preprint titles remain searchable when a published title differs. Conference metadata is curated with source URLs: both QCE 2026 technical papers, QPL 2022 (proceedings published in 2023), IPDPSW 2024, PMES 2017, and CP 2020. Separate conference and journal works remain distinct. DOI-linked records without an arXiv ID survive refreshes. The NASA HPC proceedings chapter is grouped with conferences and exports as `incollection`; other BibTeX entries use `article`, `inproceedings`, `phdthesis`, or `misc` as appropriate.

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

## Music

`/music/` contains a short Ponderosa biography and three recordings, and is linked from the shared primary navigation and footer. `data/music.json` maintains the biography, album descriptions, track order, durations and sources. The original YouTube artwork thumbnail is retained in `assets/ponderosa-attack-of-the-rosa.jpg`. All ten Rosa tracks link directly to their start times in the full-album video.

Fairview uses 192 kbps MP3 listening copies made from the original 320 kbps files; CDIS retains its original 128 kbps MP3 files. Each track has native playback controls, and Play album starts an ordered sequence. Starting another player pauses the previous one. Preload is disabled, and there are no download links. Native download controls are suppressed where supported, but public playback cannot prevent copying. Original source filenames and original/public checksums are in `docs/ponderosa-audio-provenance.json`; historical research and source limits are in `docs/ponderosa-archive-research.md`. The generator builds all four pages, so scheduled publication refreshes retain the Music page and navigation.
