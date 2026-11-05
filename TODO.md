# Personal website — remaining work

## Design decision

- [x] Style chosen: **Quiet modern**, with restrained sans serif typography (owner decision, October 30, 2026).
- [x] Palette chosen and applied: **Ink and blue**, in day mode (owner decision, October 30, 2026).
- [x] Apply Quiet modern typography, spacing, and layout consistently to both pages.
- [x] Replace decorative branding, oversized display text, numbered sections, and promotional copy with a simpler academic presentation.
- [x] Use the owner-supplied new portrait, retaining its original bytes and framing it with CSS.
- [x] Expand Background from the older Columbia/GitHub sites: advisers, education, QuAIL history, engineering work, broader interests, and Q4Climate. Rename the research area Algorithms & Complexity.
- [x] Link the existing “Columbia University” text in Background quietly to the former Columbia homepage, matching the current GitHub page.
- [x] Link Joseph F. Traub, Alfred V. Aho, and Anargyros Papageorgiou to their Columbia homepages, and NASA QuAIL and RIACS to their research group pages in the same Background paragraph.
- [x] Introductory links ordered Google Scholar, ORCID, arXiv, LinkedIn, using the LinkedIn URL from the prior GitHub page. Homepage section heading changed to Research Interests. Quantum simulation description updated to the owner’s exact scientific-computing, quantum-chemistry and high-energy-physics wording.
- [x] Update Selected publications: remove QRAO compression from the featured list; add the Boolean/Hamiltonian paper, Wang et al. (2018), NDAR, ND-AWS, and dihedral gates. Keep all works in the full publication list. Spell out Quantum Artificial Intelligence Laboratory (QuAIL) in the introduction and remove collaboration from the homepage wording. The spring 2018 background sentence names both NASA QuAIL and USRA’s Research Institute for Advanced Computer Science (RIACS).
- [x] Stuart accepted version 1 on November 1, 2026, including the public biography, affiliations, contact address, portrait, and featured-paper choices.
- [x] Use the full NASA Ames Research Center name in the introduction and add “New York, NY” in Contact.
- [x] Remove the middle initial from the homepage name and shared footer; preserve names as published in citation records.
- [x] Add a short research-internship note in Contact, linking to the Feynman Quantum Academy for opportunities and application details.
- [x] Add a compact Recent & upcoming section below the introduction and before Research Interests, with at most five dated public paper/event updates and a shared /news/ archive. Initial entries: PRA acceptance, quantum approximation complexity preprint, and two IEEE Quantum Week papers in the proceedings and two talks presented, confirmed by the owner. Preserve the quiet style and existing selected publications.

## Publications

- [x] Add the 2008 University of Melbourne Bachelor of Science Honours thesis, Error Rate Thresholds for Physical Implementations of the Surface Code, using the original PDF and title-page metadata. Retain it during arXiv refreshes and export the honours degree correctly in BibTeX.
- [x] Add a publication-status filter alongside search, topic, and year. Distinguish **Published**, **Not yet published**, and **Thesis**. By owner instruction, accepted papers count as Published and are marked “to appear.”
- [x] Add an independent journal/conference/preprint/thesis filter; show QPL 2022 and other conference names explicitly, include both IEEE Quantum Week papers as to appear, and restore the distinct PMES 2017 conference paper.
- [x] Combine status filtering with the existing filters and shareable URLs; verify reset and empty-result behavior.
- [x] Correct seven verified published records: QDPLL, dense Ising circuits, non-Abelian Fourier transforms, measurement-based QAOA, meta-learning, FOCQS, and iterative MIS. Preserve sources and check dates in the publication overrides.
- [ ] Owner reviews the final publication list, including records without a confirmed journal/conference reference. Status follows the available publication metadata.
- [x] Preserve editorial corrections and acceptance information during refreshes; validate stable IDs, duplicate handling, published status, acceptance, and the separate thesis category.
- [ ] Replace “to appear” details with final proceedings/journal metadata when available.
- [x] Manual arXiv refresh and deployment succeeded after public launch (GitHub Actions run 41357083905, November 1, 2026); the weekly schedule is enabled on main.
- [x] Enabled a separate Sunday-morning ChatGPT Website Maintenance review of the public Scholar profile, with verified metadata changes applied to the repository and deployed after checks. First scheduled date November 8, 2026, around 08:00 New York time. Source-access limits are reported; primary publisher/DOI/arXiv verification protects curated metadata and selected works.

## Domains — owner plan, October 31, 2026

- [x] Plan to use both `stuarthadfield.me` and `stuarthadfield.si`, with `.me` as the main address and `.si` redirecting to it.
- [x] Registered both domains at Porkbun, November 1, 2026; owner completed the $37.59 payment. Both entries appear in Domain Management (order 12369977), expiring November 2, 2027.
- [x] GitHub verified `.me` ownership; DNS checks succeeded and Enforce HTTPS is enabled. The homepage and publications page load at HTTPS. The apex ALIAS and `www` CNAME point to `stuartah.github.io`; retain the ownership TXT. HTTP, `www`, and the old GitHub address return 301 redirects to the `.me` HTTPS address, preserving paths and query strings.
- [ ] Verify forwarding from `.si` and `www.stuarthadfield.si` after public DNS propagation and SSL provisioning. Porkbun saved both 301 rules to `https://stuarthadfield.me` with Include Path enabled (forward IDs 33153284 and 33153297), and created `uixie.porkbun.com` forwarding ALIAS records. The initial registry status was inactive. Porkbun’s subsequent delegation notice confirms the four assigned nameservers; public resolution/redirect tests remain unsuccessful. The .si registry publishes zone updates hourly. Do not repeat registration or keep resetting nameservers.
- [x] Updated canonical URLs, structured data, social metadata, sitemap, robots and Clicky hostname guard to the main `.me` domain. Clicky account allowed domains and Search Console verification remain below.

## Public launch

Owner instruction, November 1, 2026: carry out as much of the launch as possible, with owner interaction for required sign-in, checkout, or verification. Version 1 is accepted. Prepare and push the final copy, mark the PR ready after successful checks, configure hosting and owned domains, then merge and verify the public deployment. Keep `.me` as the main domain and `.si` as the redirect. Both domains are now registered; remaining provider checks and external-profile updates are recorded below. No additional paid service is assumed.

- [x] Stuart accepted the reviewed preview as version 1 on November 1, 2026; the public GitHub Pages deployment is complete.
- [x] Selected **GitHub Actions** as the Pages publishing source in the owner's authenticated GitHub session, November 1, 2026.
- [x] Merged PR #1 at 78a31a466ee7f8da4284f93e79ee7928fad605c2. Public homepage and publications page, HTTPS, conference/status filters, reset, and the 41-record BibTeX download verified. Deployment run 41356686373 succeeded. Prior 390px phone QA passed; a final live phone spot check remains.
- [x] Public deployment and manual publication refresh both passed under the repository's current settings.

## Clicky

- [x] Added `stuarthadfield.me`, `www.stuarthadfield.me`, and `stuartah.github.io` to **additional domains** for existing Clicky site ID `101117148`; Clicky confirmed Successfully updated. Domain validation remains enabled and outbound tracking remains enabled. Existing Columbia data/site ID preserved.
- [ ] Confirm an outbound event in Clicky using an independent/private browser. Clicky documents automatic exclusion of owners’ visits. Preview visits remain excluded.
- [x] The authenticated Clicky Domains report now includes `stuarthadfield.me` hits alongside Columbia traffic, confirming receipt from the new website. Aggregate counts are retained privately; outbound-event receipt remains unverified.
- [x] Include aggregate Clicky checks in the private weekly Website Maintenance task and a concise traffic section in the existing owner Project Status & Backup report. Preserve its current monthly cadence and existing recipient. Keep analytics data private.
- [x] Updated the production-hostname guard for `.me`, its `www` variant, and the original GitHub address.

## Google search

- [x] Verified the URL-prefix property `https://stuartah.github.io/` and requested homepage indexing. Its sitemap was submitted but last showed Couldn’t fetch; publications indexing is unconfirmed.
- [x] Google confirmed Domain-property ownership for `stuarthadfield.me` via DNS TXT. Keep the Google and GitHub ownership TXT records.
- [x] Google acknowledged submission of `https://stuarthadfield.me/sitemap.xml` and accepted indexing requests for both the `.me` homepage and publications page. After HTTPS became active, Google processed the sitemap successfully and discovered both URLs; direct HTTPS retrieval also returns 200 application/xml.
- [x] Google sitemap status is Success, with two discovered pages. The sitemap was resubmitted once after HTTPS became active; no duplicate page-indexing requests were made.
- [x] Submitted Search Console Change of Address from `stuartah.github.io` to `stuarthadfield.me`. Google passed redirect/ownership validation and confirmed the move is in progress on November 1, 2026 ET. Both Search Console properties and their verification methods are retained.
- [ ] Monitor Google’s canonical selection: the first homepage crawl succeeded and indexing is allowed, but Google currently reports Duplicate, Google chose different canonical than user. The declared canonical is correctly `.me`; Google did not show its selected alternative. The accepted move notification, existing redirects and canonical/sitemap signals should be allowed to process before further changes. Do not repeatedly request indexing.
- [ ] Update the link on the Columbia homepage and, where editable, the Scholar, ORCID, and institutional profiles.
- [ ] Check indexing and search appearance after Google has had time to crawl the public version.

## Later decisions

- [x] Supplement the arXiv feed with the scheduled public Scholar-profile review and verified publisher/DOI metadata. Respect source-access rules and do not bulk-scrape Scholar.

A separate Talks page, a resources page, and a CV remain outside scope. Selected paper milestones and confirmed recent/upcoming talks can appear in the compact homepage updates section.

Version 1 is live at https://stuarthadfield.me/ as of November 1, 2026, with the original GitHub URL redirecting to it. The .si redirect activation, independent analytics event confirmation, Google indexing/search appearance, and external profile links remain in progress. This checklist records work; it does not create reminders or background execution.

- [x] Backfill the November 2025 NDAR publication, December 2025 Brazil plenary and measurement-driven preprint; add the November 2026 IQO Tree and pushforwards papers. Preserve the IEEE item and a reasonable talk/publication/preprint mix on the homepage.

- [x] Cross-check the current CV for the same news period: add the Oslo invited talk, Quantum DPLL/PRA, scalar-field scattering/PRX Quantum, constraints/ACM publications and IEEE warm-start paper award; add the two missing journal records to the bibliography.

## Music

- [x] Add Music to the shared primary navigation and introduce guitar and piano.
- [x] Add a short Ponderosa biography identifying Stuart as lead guitarist, with a surviving 2004 SHiNDiG listing.
- [x] Expand Attack of the Rosa! from the YouTube description; list all ten tracks with direct timestamp links.
- [x] Add all seven Fairview and three CDIS recordings with browser playback and no download links. Native download controls are suppressed where supported; public playback cannot prevent copying.
- [x] Search for historical band/Myspace material and images. No original Myspace URL or further correctly identified band photos were recovered; retain the verified album cover.
- [ ] Travel map deferred by owner.
