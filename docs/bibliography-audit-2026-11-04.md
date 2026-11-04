# Bibliography audit — November 4, 2026

The website and downloadable `publications.bib` now contain **52 distinct works**. Every research entry in Stuart Hadfield's November 3 CV is represented. The adjacent JSON file records the source-to-website identifier reconciliation; duplicate index records/preprint versions map to a single work. This is an audit of the inspected inventories as of this date, not a guarantee about inaccessible or unindexed work.

## Sources and coverage

| Source | Entries checked | Distinct website works | Result |
| --- | ---: | ---: | --- |
| Complete CV Research section, pages 2–5 | 52 | 52 | All represented |
| [Identified arXiv author feed](https://arxiv.org/a/hadfield_s_1.atom) | 40 | 40 | All represented |
| [ORCID works](https://pub.orcid.org/v3.0/0000-0002-4607-3921/works) | 35 | 35 | All represented |
| [INSPIRE author literature query](https://inspirehep.net/api/literature?q=a%20Stuart.Hadfield.1&size=100) | 49 of 49 results | 49 | All represented; author identity verified by ORCID and INSPIRE BAI |
| [DBLP author page](https://dblp.org/pid/172/0850.html) | 27 publication records | 21 | All represented; journal/preprint duplicates retained as one website work |
| [NASA QuAIL publications](https://www.nasa.gov/general/quail-publications/) | 41 entries explicitly naming Hadfield | 32 | All represented; older titles and repeated publication/preprint entries reconciled |
| [Former Columbia website](https://www.cs.columbia.edu/~stuartah/) | 9 research entries | 9 | All represented |

The public Google Scholar profile could not be retrieved in this run. No challenge, disallowed pagination or access restriction was bypassed. DBLP's machine-readable XML endpoint returned a challenge; its accessible public HTML records were read instead. INSPIRE's query initially stalled but subsequently returned all 49 results, which were reconciled in full.

## Additions and corrections

The Dupont *Science Advances* paper was added during the selected-publications change immediately before this audit. The full comparison then identified five additional omissions:

| Work | Verified record | Treatment |
| --- | --- | --- |
| Quantum technologies for climate change: Preliminary assessment | [arXiv:2107.05362](https://arxiv.org/abs/2107.05362) | 2021 preprint; full author list and original submission date |
| Toward Quantum Gate-Model Heuristics for Real-World Planning Problems | [IEEE article](https://tqe.ieee.org/2020/10/13/toward-quantum-gate-model-heuristics-for-real-world-planning-problems/), [DOI](https://doi.org/10.1109/TQE.2020.3030609) | Published journal article, 2020, volume 1, pages 1–16 |
| Quantum-Accelerated Global Constraint Filtering | [Publisher-deposited Crossref record](https://api.crossref.org/works/10.1007/978-3-030-58475-7_5), [NASA record](https://ntrs.nasa.gov/citations/20205003667) | CP 2020 proceedings, pages 72–89; distinct from the later Quantum journal paper |
| From Ansätze to Z-Gates: A NASA View of Quantum Computing | [arXiv:1905.02860](https://arxiv.org/abs/1905.02860), [Publisher-deposited Crossref record](https://api.crossref.org/works/10.3233/APC190010), NASA bibliography above | 2019 HPC proceedings book chapter; full 15-author list, volume 34, pages 133–160; conference filter and `incollection` BibTeX |
| Divide and conquer approach to quantum Hamiltonian simulation | [Publisher-deposited Crossref record](https://api.crossref.org/works/10.1088/1367-2630/aab1ef) | New Journal of Physics 20(4), 043003, published April 12, 2018 |

The DOI [10.26421/QIC16.3-4-2](https://doi.org/10.26421/QIC16.3-4-2) was restored to *Quantum algorithms and circuits for scientific computing*, verified against [Rinton Press](https://www.rintonpress.com/journals/qiconline.html) and its [Crossref deposit](https://api.crossref.org/works/10.26421/QIC16.3-4-2).

Index disagreement was handled conservatively. The IEEE publisher's “Toward” and the NJP publisher's “to” replace the CV's “Towards” and “for” in those two titles. NASA's inconsistent 2408.00074 text/2408.00075 link was not imported as another paper. The existing verified 2408.00075 record remains authoritative. ORCID's Zenodo preprint DOIs were not treated as proof of journal publication. Existing accepted/to-appear conventions and separate conference records remain intact.

## Refresh and validation

All five additions have cached records and authoritative metadata overrides, including full author lists, verified venue/type/status and source/check dates. The 40-record arXiv feed was replayed offline after the changes: all 52 works survived, including the DOI-only records. A regression test protects the backfill, distinct CP/Quantum works and NASA chapter citation.

Validation passed: 20 unit tests; three-page build; canonical, structured-data, local-link and publication-count checks; 52 unique identifiers and BibTeX entries; no duplicate DOIs; whitespace check. The ten selected publications and all 21 approved news items are preserved. The News introduction is now “Publications, talks, and other research news.”

Future maintenance should reconcile other inventories with the cache, verify discrepancies against original records, preserve these additions and report source-access limits. A successful arXiv refresh alone is insufficient evidence of completeness.
