# Personal website — remaining work

## Design decision

- [ ] Choose a direction before implementing the full aesthetic pass: **Classic academic** (Georgia and blue links), **Quiet modern** (restrained sans serif), or **Compact editorial** (a narrow profile sidebar and serif headings).
- [ ] Apply the chosen typography, spacing, and layout consistently to the homepage and publications page.
- [ ] Replace decorative branding, oversized display text, numbered sections, and promotional copy with a more personal academic presentation.
- [ ] Review the exact public biography, affiliations, contact address, portrait, and featured-paper choices with Stuart.

## Publications

- [ ] Add a publication-status filter alongside search, topic, and year. Distinguish **Published**, **Not yet published**, and **Thesis**. Accepted work remains not yet published until a published version is documented.
- [ ] Combine status filtering with the existing filters and shareable URLs; verify reset and empty-result behavior.
- [ ] Audit incomplete publication metadata before launch. The arXiv author feed can lag journal publication; public ORCID/Crossref records already identify several records needing correction, including QDPLL, dense Ising circuits, non-Abelian Fourier transforms, measurement-based QAOA, and meta-learning.
- [ ] Preserve editorial corrections and acceptance information during automatic refreshes, and verify duplicate handling.
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
