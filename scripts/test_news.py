from datetime import date
import unittest

from news import homepage_news, news_items, ordered_news


def item(ident, kind='preprint', when='2026-10-01', **extra):
    return {'id': ident, 'date': when, 'date_label': 'Oct 2026',
            'kind': kind, 'segments': [{'text': ident}], **extra}


class NewsSelectionTests(unittest.TestCase):
    def test_new_announcements_do_not_erase_archive_or_category_mix(self):
        entries = [item(str(i), when=f'2026-10-{i:02}') for i in range(1, 9)]
        entries += [item('talk', 'talk', '2026-09-01'),
                    item('publication', 'publication', '2026-08-01')]
        selected = homepage_news(entries, date(2026, 11, 4))
        self.assertEqual(len(selected), 5)
        self.assertEqual({e['kind'] for e in selected}, {'talk', 'publication', 'preprint'})
        self.assertEqual(len(ordered_news(entries)), 10)
        self.assertIn('news-1', news_items(ordered_news(entries)))
        self.assertNotIn('1', [e['id'] for e in selected])

    def test_explicit_pin_survives_until_editor_releases_it(self):
        entries = [item(str(i), when=f'2026-10-{i:02}') for i in range(1, 8)]
        entries.append(item('ieee', 'talk', '2026-09-16', pinned=True))
        self.assertIn('ieee', [e['id'] for e in homepage_news(entries, date(2028, 1, 1))])
        entries[-1]['pinned'] = False
        self.assertNotIn('ieee', [e['id'] for e in homepage_news(entries, date(2028, 1, 1))])

    def test_category_preference_does_not_force_old_events(self):
        entries = [item(str(i), when=f'2026-10-{i:02}') for i in range(1, 7)]
        entries.append(item('old-talk', 'talk', '2024-01-01'))
        self.assertNotIn('old-talk', [e['id'] for e in homepage_news(entries, date(2026, 11, 4))])

    def test_month_precision_duplicate_ids_and_empty_state(self):
        self.assertEqual(ordered_news([item('oct'), item('nov', when='2026-11')])[0]['id'], 'nov')
        with self.assertRaises(ValueError):
            ordered_news([item('same'), item('same')])
        with self.assertRaises(ValueError):
            homepage_news([item(str(i), pinned=True) for i in range(6)])
        self.assertEqual(homepage_news([]), [])

    def test_source_text_and_url_attributes_are_escaped(self):
        entry = item('safe')
        entry['segments'] = [{'text': '<script> & text', 'url': 'https://example.org/?a="&b=2'}]
        rendered = news_items([entry])
        self.assertNotIn('<script>', rendered)
        self.assertIn('&lt;script&gt; &amp; text', rendered)
        self.assertIn('a=&quot;&amp;b=2', rendered)


if __name__ == '__main__':
    unittest.main()
