# Personal website — remaining work

## Design decision

- [x] Style chosen: **Quiet modern**, with restrained sans serif typography (owner decision, October 30, 2026).
- [x] Palette chosen and applied: **Ink and blue**, in day mode (owner decision, October 30, 2026).
- [x] Apply Quiet modern typography, spacing, and layout consistently to both pages.
- [x] Replace decorative branding, oversized display text, numbered sections, and promotional copy with a simpler academic presentation.
- [x] Use the owner-supplied new portrait, retaining its original bytes and framing it with CSS.
- [x] Expand Background from the older Columbia/GitHub sites: advisers, education, QuAIL history, engineering work, broader interests, and Q4Climate. Rename the research area Algorithms & Complexity.
- [x] Link the existing “Columbia University” text in Background quietly to the former Columbia homepage, matching the current GitHub page.
- [x] Introductory links ordered Google Scholar, ORCID, arXiv, LinkedIn, using the LinkedIn URL from the prior GitHub page. Homepage section heading changed to Research Interests. Quantum simulation description updated to the owner’s exact scientific-computing, quantum-chemistry and high-energy-physics wording.
- [x] Update Selected publications: remove QRAO compression from the featured list; add the Boolean/Hamiltonian paper, Wang et al. (2018), ND-AWS, and dihedral gates. Keep all works in the full publication list. Spell out Quantum Artificial Intelligence Laboratory (QuAIL) in the introduction and remove collaboration from the homepage wording.
- [ ] Review the exact public biography, affiliations, contact address, portrait, and featured-paper choices with Stuart.

## Publications

- [x] Add a publication-status filter alongside search, topic, and year. Distinguish **Published**, **Not yet published**, and **Thesis**. By owner instruction, accepted papers count as Published and are marked “to appear.”
- [x] Add an independent journal/conference/preprint/thesis filter; show QPL 2022 and other conference names explicitly, include both IEEE Quantum Week papers as to appear, and restore the distinct PMES 2017 conference paper.
- [x] Combine status filtering with the existing filters and shareable URLs; verify reset and empty-result behavior.
- [x] Correct seven verified published records: QDPLL, dense Ising circuits, non-Abelian Fourier transforms, measurement-based QAOA, meta-learning, FOCQS, and iterative MIS. Preserve sources and check dates in the publication overrides.
- [ ] Owner reviews the final publication list, including records without a confirmed journal/conference reference. Status follows the available publication metadata.
- [x] Preserve editorial corrections and acceptance information during refreshes; validate stable IDs, duplicate handling, published status, acceptance, and the separate thesis category.
- [ ] Replace “to appear” details with final proceedings/journal metadata when available.
- [ ] Confirm the weekly/manual publication-refresh workflow after public deployment.

## Domains — owner plan, October 31, 2026

- [x] Plan to use both `stuarthadfield.me` and `stuarthadfield.si`, with `.me` as the main address and `.si` redirecting to it.
- [ ] Register both domains after confirming final availability and checkout prices.
- [ ] Verify and connect `.me` to GitHub Pages, including HTTPS and `www` handling.
- [ ] Configure an HTTPS permanent (301) redirect from `.si` to `.me`, preserving requested paths; verify both the homepage and `/publications/`.
- [ ] Update canonical URLs, structured data, sitemap, Clicky hostname guard/allowed domains, and Search Console for the chosen main domain before launch.

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

- [ ] Revisit publication sources beyond arXiv if needed for more complete journal metadata. Do not scrape Google Scholar.

Talks, a resources page, and a CV are outside the first-version scope.

The current public homepage stays in place while designs are being reviewed. This checklist records work; it does not create reminders or background execution.
