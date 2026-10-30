"""Curated publication status, venue types, and display conventions."""
import re


def is_to_appear(paper):
    return paper.get('publication_stage') == 'accepted' or bool(re.match(
        r'^(accepted\b|in press\b|forthcoming\b|to appear\b)',
        paper.get('venue', '').strip(), re.I))


def publication_status(paper):
    # Accepted papers belong with published work by the owner's convention.
    if is_to_appear(paper):
        return 'published'
    explicit = paper.get('publication_status')
    if explicit in ('published', 'unpublished', 'thesis'):
        return explicit
    venue = paper.get('venue', '').strip().casefold()
    if 'thesis' in venue or 'dissertation' in venue:
        return 'thesis'
    if not venue or venue.startswith(('preprint', 'arxiv', 'submitted')):
        return 'unpublished'
    # Journal/conference references are evidence. Bare DOIs are insufficient:
    # preprints also receive DOIs.
    return 'published'


def publication_type(paper):
    explicit = paper.get('publication_type')
    if explicit in ('journal', 'conference', 'preprint', 'thesis'):
        return explicit
    status = publication_status(paper)
    if status == 'thesis':
        return 'thesis'
    if re.search(r'\b(eptcs|proceedings|conference|workshop|workshops|qpl|qce)\b', paper.get('venue', ''), re.I):
        return 'conference'
    return 'journal' if status == 'published' else 'preprint'


def publication_venue(paper):
    venue = paper.get('venue', '').strip()
    if is_to_appear(paper):
        venue = re.sub(r'^(accepted\b|in press\b|forthcoming\b|to appear\b)[\s,:–—-]*', '', venue, flags=re.I)
        if not re.search(r'\bto appear\b', venue, re.I):
            venue = f'{venue} (to appear)' if venue else 'To appear'
    return venue
