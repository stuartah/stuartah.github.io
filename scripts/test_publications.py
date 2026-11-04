import unittest
from sync_publications import merge_records, parse_feed
from publication_metadata import publication_status, publication_type, publication_venue


def feed(author='Stuart Hadfield', ident='2609.07090v2', title='A paper'):
    return f'''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
      <id>https://arxiv.org/abs/{ident}</id><title>{title}</title>
      <published>2026-09-07T00:00:00Z</published><author><name>{author}</name></author>
    </entry></feed>'''.encode()


class PublicationImportTests(unittest.TestCase):
    def test_accepted_counts_as_published_and_shows_to_appear(self):
        paper = {'venue': 'Accepted, Physical Review A', 'doi': '10.1103/example'}
        self.assertEqual(publication_status(paper), 'published')
        self.assertEqual(publication_venue(paper), 'Physical Review A (to appear)')

    def test_preprint_doi_is_not_evidence_of_publication(self):
        self.assertEqual(publication_status({'venue': 'Preprint', 'doi': '10.48550/arXiv.1234.56789'}), 'unpublished')

    def test_proceedings_series_and_explicit_types(self):
        self.assertEqual(publication_type({'venue': 'EPTCS 394, 2023, pp. 262-301'}), 'conference')
        self.assertEqual(publication_type({'venue': 'Physical Review A'}), 'journal')
        self.assertEqual(publication_type({'venue': 'Preprint'}), 'preprint')

    def test_current_conference_and_acceptance_records_survive_refresh(self):
        import json
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        existing = json.loads((root / 'data/publications.json').read_text())
        overrides = json.loads((root / 'data/overrides.json').read_text())
        imported = [{'id': ident, 'year': 2026, 'venue': 'Preprint', 'doi': ''} for ident in ('2606.28234', '2604.26047', '2512.21046')]
        result = {p['id']: p for p in merge_records(existing, imported, overrides)}
        for ident in ('2606.28234', '2604.26047', '2512.21046'):
            self.assertEqual(publication_status(result[ident]), 'published')
            self.assertIn('to appear', publication_venue(result[ident]))
        for ident in ('2606.28234', '2604.26047', '2204.01307', '2403.11514', 'pmes-2017-hard-soft-constraints'):
            self.assertEqual(publication_type(result[ident]), 'conference')
        self.assertIn('QPL 2022', result['2204.01307']['venue'])

    def test_thesis_is_separate_from_the_published_paper_filter(self):
        self.assertEqual(publication_status({'venue': 'Ph.D. dissertation, Columbia University'}), 'thesis')

    def test_cv_backfill_keeps_verified_journal_metadata_after_arxiv_refresh(self):
        import json
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        existing = json.loads((root / 'data/publications.json').read_text())
        overrides = json.loads((root / 'data/overrides.json').read_text())
        ids = ('2407.01975', '2407.13819')
        imported = [{'id': ident, 'year': 2024, 'date': '2024-07-01',
                     'venue': 'Preprint', 'doi': '', 'authors': ['Stuart Hadfield']}
                    for ident in ids]
        records = {p['id']: p for p in merge_records(existing, imported, overrides)}
        for ident in ids:
            self.assertEqual(publication_type(records[ident]), 'journal')
            self.assertEqual(publication_status(records[ident]), 'published')
            self.assertNotIn('to appear', publication_venue(records[ident]))
            self.assertEqual(records[ident]['year'], 2026)
            self.assertTrue(records[ident]['doi'])
            self.assertGreater(len(records[ident]['authors']), 1)

    def test_melbourne_honours_thesis_survives_refresh_and_exports_correct_degree(self):
        from build import bibtex, PAPERS
        existing = {p['id']: p for p in PAPERS}
        ident = 'melbourne-2008-surface-code-thesis'
        records = {p['id']: p for p in merge_records(PAPERS, parse_feed(feed()), {})}
        thesis = records[ident]
        self.assertEqual(thesis, existing[ident])
        self.assertEqual(publication_status(thesis), 'thesis')
        self.assertEqual(publication_type(thesis), 'thesis')
        self.assertEqual(thesis['school'], 'University of Melbourne')
        citation = bibtex(thesis)
        self.assertIn('Honours thesis', citation)
        self.assertIn('University of Melbourne', citation)
        self.assertNotIn('@phdthesis', citation)
        self.assertNotIn('Columbia University', citation)
        self.assertIn('@phdthesis', bibtex(records['1805.03265']))
        self.assertIn('Columbia University', bibtex(records['1805.03265']))

    def test_journal_and_conference_references_count_as_publication(self):
        self.assertEqual(publication_status({'venue': 'Physical Review A 114, 022404'}), 'published')
        self.assertEqual(publication_status({'venue': '2024 IEEE IPDPS Workshops'}), 'published')

    def test_versions_have_one_stable_identifier(self):
        self.assertEqual(parse_feed(feed())[0]['id'], '2609.07090')

    def test_other_hadfields_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'identity mismatch'):
            parse_feed(feed(author='Charles Hadfield'))

    def test_empty_or_unexpected_responses_are_rejected(self):
        with self.assertRaises(ValueError):
            parse_feed(b'<feed xmlns="http://www.w3.org/2005/Atom"/>')
        with self.assertRaises(ValueError):
            parse_feed(feed(ident='not-a-paper'))

    def test_missing_upstream_records_and_editorial_details_survive(self):
        old = [{'id': 'old', 'year': 2020, 'title': 'Keep me'}, {'id': '2609.07090', 'year': 2026, 'summary': 'Local explanation'}]
        imported = parse_feed(feed())
        overrides = {'2609.07090': {'year': 2026, 'title': 'Edited title', 'venue': 'Accepted'}}
        result = {p['id']: p for p in merge_records(old, imported, overrides)}
        self.assertIn('old', result)
        self.assertEqual(result['2609.07090']['title'], 'Edited title')
        self.assertEqual(result['2609.07090']['summary'], 'Local explanation')
        self.assertEqual(result['2609.07090']['venue'], 'Accepted')

    def test_doi_duplicates_prefer_the_curated_record(self):
        records = [{'id': 'one', 'year': 2020, 'doi': '10.1234/example'}, {'id': 'two', 'year': 2021, 'doi': 'https://doi.org/10.1234/EXAMPLE'}]
        result = merge_records(records, [], {'one': {'year': 2020, 'title': 'Preferred'}})
        self.assertEqual([p['id'] for p in result], ['one'])

    def test_new_journal_metadata_is_not_frozen_by_a_summary(self):
        old = [{'id': 'one', 'year': 2020, 'venue': 'Preprint', 'doi': ''}]
        updated = [{'id': 'one', 'year': 2021, 'venue': 'Quantum', 'doi': '10.1234/new'}]
        result = merge_records(old, updated, {'one': {'summary': 'Local explanation'}})[0]
        self.assertEqual((result['year'], result['venue'], result['doi']), (2021, 'Quantum', '10.1234/new'))
        self.assertEqual(result['summary'], 'Local explanation')


if __name__ == '__main__':
    unittest.main()
