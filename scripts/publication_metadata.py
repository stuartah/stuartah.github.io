"""Publication states used by the website's status filter."""


def publication_status(paper):
    explicit = paper.get('publication_status')
    if explicit in ('published', 'unpublished', 'thesis'):
        return explicit
    venue = paper.get('venue', '').strip().casefold()
    if 'thesis' in venue or 'dissertation' in venue:
        return 'thesis'
    if not venue or venue.startswith(('preprint', 'arxiv', 'accepted', 'in press', 'forthcoming', 'submitted')):
        return 'unpublished'
    # Journal/conference references are evidence. Bare DOIs are insufficient:
    # preprints also receive DOIs.
    return 'published'
