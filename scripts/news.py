"""Shared news archive and bounded homepage selection."""
from datetime import date, timedelta
from html import escape

HOMEPAGE_LIMIT = 5
KINDS = ('talk', 'publication', 'preprint')


def entry_date(entry):
    value = entry['date']
    return date.fromisoformat(value + '-01' if len(value) == 7 else value)


def ordered_news(entries):
    seen = set()
    for entry in entries:
        if entry['id'] in seen:
            raise ValueError('Duplicate news ID: ' + entry['id'])
        seen.add(entry['id'])
        entry_date(entry)
        if entry['kind'] not in KINDS or not entry['segments']:
            raise ValueError('News needs a category and text.')
    return sorted(entries, key=lambda item: (entry_date(item), item['id']), reverse=True)


def homepage_news(entries, today=None):
    """Keep current owner-pinned items and a reasonable recent category mix.

    Only approved entries enter the shared list. Reserve one of each available
    category from the last year, then fill by date. Older entries stay archived.
    """
    entries = ordered_news(entries)
    selected = [entry for entry in entries if entry.get('pinned')]
    if len(selected) > HOMEPAGE_LIMIT:
        raise ValueError('More pinned news than homepage slots.')
    cutoff = (today or date.today()) - timedelta(days=365)
    for kind in KINDS:
        if any(entry['kind'] == kind for entry in selected):
            continue
        candidate = next((entry for entry in entries
                          if entry['kind'] == kind and entry_date(entry) >= cutoff), None)
        if candidate and len(selected) < HOMEPAGE_LIMIT:
            selected.append(candidate)
    for entry in entries:
        if len(selected) == HOMEPAGE_LIMIT:
            break
        if entry not in selected:
            selected.append(entry)
    return ordered_news(selected)


def news_items(entries):
    items = []
    for entry in entries:
        text = ''.join(
            f'<a href="{escape(part["url"], quote=True)}">{escape(part["text"])}</a>'
            if part.get('url') else escape(part['text'])
            for part in entry['segments']
        )
        items.append(f'<li id="news-{escape(entry["id"], quote=True)}"><time datetime="{escape(entry["date"], quote=True)}">{escape(entry["date_label"])}</time><p>{text}</p></li>')
    return '<ul class="updates-list">' + ''.join(items) + '</ul>'
