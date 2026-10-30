import unittest
from sync_publications import merge_records, parse_feed
from publication_metadata import publication_status


def feed(author='Stuart Hadfield', ident='2609.07090v2', title='A paper'):
    return f'''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
      <id>https://arxiv.org/abs/{ident}</id><title>{title}</title>
      <published>2026-09-07T00:00:00Z</published><author><name>{author}</name></author>
    </entry></feed>'''.encode()


class PublicationImportTests(unittest.TestCase):
    def test_accepted_and_preprint_dois_do_not_count_as_published(self):
        self.assertEqual(publication_status({'venue': 'Accepted, Physical Review A', 'doi': '10.1103/example'}), 'unpublished')
        self.assertEqual(publication_status({'venue': 'Preprint', 'doi': '10.48550/arXiv.1234.56789'}), 'unpublished')

    def test_thesis_is_separate_from_the_published_paper_filter(self):
        self.assertEqual(publication_status({'venue': 'Ph.D. dissertation, Columbia University'}), 'thesis')

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
