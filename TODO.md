# Personal website — remaining work

## Design decision

- [x] Style chosen: **Quiet modern**, with restrained sans serif typography (owner decision, October 30, 2026).
- [x] Palette chosen and applied: **Ink and blue**, in day mode (owner decision, October 30, 2026).
- [x] Apply Quiet modern typography, spacing, and layout consistently to both pages.
- [x] Replace decorative branding, oversized display text, numbered sections, and promotional copy with a simpler academic presentation.
- [x] Use the owner-supplied new portrait, retaining its original bytes and framing it with CSS.
- [ ] Review the exact public biography, affiliations, contact address, portrait, and featured-paper choices with Stuart.

## Publications

- [x] Add a publication-status filter alongside search, topic, and year. Distinguish **Published**, **Not yet published**, and **Thesis**. Accepted work remains not yet published until a published version is documented.
- [x] Combine status filtering with the existing filters and shareable URLs; verify reset and empty-result behavior.
- [x] Correct seven verified published records: QDPLL, dense Ising circuits, non-Abelian Fourier transforms, measurement-based QAOA, meta-learning, FOCQS, and iterative MIS. Preserve sources and check dates in the publication overrides.
- [ ] Owner reviews the final publication list, including records without a confirmed journal/conference reference. Status follows the available publication metadata.
- [x] Preserve editorial corrections and acceptance information during refreshes; validate stable IDs, duplicate handling, published status, acceptance, and the separate thesis category.
- [ ] Confirm the weekly/manual publication-refresh workflow after public deployment.

## Public launch

- [ ] Stuart reviews and accepts the exact preview for launch.
- [ ] Select **GitHub Actions** as the repository's Pages publishing source.
- [ ] Merge the reviewed branch and confirm both public pages, HTTPS, navigation, downloads, and phone layout.
- [ ] Confirm that deployment and publication refreshes work under the repository's actual branch-protection settings.

## Clicky

- [ ] Add `stuartah.github.io` to **additional domains** for existing Clicky site ID `101117148`, keeping domain validation enabled.
- [ ] Confirm page views and outbound activity in the authenticated dashboard after launch. Preview visits are deliberately excluded.
- [ ] If a personal domain is adopted later, update both Clicky's allowed domains and the production-hostname guard.

## Google search

- [ ] Verify the URL-prefix property `https://stuartah.github.io/` in Google Search Console using the verification file or meta tag Google supplies.
- [ ] Submit `https://stuartah.github.io/sitemap.xml` and request indexing of the homepage and publications page.
- [ ] Update the link on the Columbia homepage and, where editable, the Scholar, ORCID, and institutional profiles.
- [ ] Check indexing and search appearance after Google has had time to crawl the public version.

## Later decisions

- [ ] Decide whether to use a personal domain; check availability before purchasing or changing DNS.
- [ ] Revisit publication sources beyond arXiv if needed for more complete journal metadata. Do not scrape Google Scholar.

Talks, a resources page, and a CV are outside the first-version scope.

The current public homepage stays in place while designs are being reviewed. This checklist records work; it does not create reminders or background execution.
