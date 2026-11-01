/* Navigation and progressive enhancement. All research content is static HTML. */
document.documentElement.classList.add('js');

const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#primary-nav');
if (toggle && nav) {
  const setOpen = open => {
    nav.dataset.open = String(open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? 'Close' : 'Menu';
  };
  toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
  nav.addEventListener('click', event => { if (event.target.closest('a')) setOpen(false); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      setOpen(false);
      toggle.focus();
    }
  });
}

const tools = document.querySelector('.publication-tools');
if (tools) {
  const search = document.querySelector('#publication-search');
  const topic = document.querySelector('#publication-topic');
  const year = document.querySelector('#publication-year');
  const status = document.querySelector('#publication-status');
  const type = document.querySelector('#publication-type');
  const papers = [...document.querySelectorAll('.publication')];
  const count = document.querySelector('#publication-count');
  const empty = document.querySelector('#empty-state');
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const searchable = new Map(papers.map(paper => [paper, normalize(paper.dataset.search)]));
  const update = (writeUrl = true) => {
    const query = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    let shown = 0;
    papers.forEach(paper => {
      const match = query.every(term => searchable.get(paper).includes(term)) &&
        (!topic.value || paper.dataset.topics.split('|').includes(topic.value)) &&
        (!year.value || paper.dataset.year === year.value) &&
        (!status.value || paper.dataset.status === status.value) &&
        (!type.value || paper.dataset.type === type.value);
      paper.hidden = !match;
      shown += Number(match);
    });
    count.textContent = `${shown} of ${papers.length} works`;
    empty.hidden = shown > 0;
    document.querySelectorAll('.reset-filters').forEach(button => {
      button.hidden = !search.value && !topic.value && !year.value && !status.value && !type.value;
    });
    if (writeUrl) {
      const url = new URL(window.location.href);
      for (const [key, value] of [['q', search.value.trim()], ['topic', topic.value], ['year', year.value], ['status', status.value], ['type', type.value]]) {
        if (value) url.searchParams.set(key, value); else url.searchParams.delete(key);
      }
      window.history.replaceState(null, '', url);
    }
  };
  const restore = () => {
    const params = new URLSearchParams(window.location.search);
    search.value = params.get('q') || '';
    topic.value = params.get('topic') || '';
    year.value = params.get('year') || '';
    status.value = params.get('status') || '';
    type.value = params.get('type') || '';
    update(false);
  };
  tools.hidden = false;
  search.addEventListener('input', () => update());
  topic.addEventListener('change', () => update());
  year.addEventListener('change', () => update());
  status.addEventListener('change', () => update());
  type.addEventListener('change', () => update());
  document.querySelectorAll('.reset-filters').forEach(button => button.addEventListener('click', () => {
    search.value = ''; topic.value = ''; year.value = ''; status.value = ''; type.value = ''; update(); search.focus();
  }));
  window.addEventListener('popstate', restore);
  restore();
}

document.querySelectorAll('.copy-citation').forEach(button => button.addEventListener('click', async () => {
  const text = button.parentElement.querySelector('code').textContent;
  try {
    await navigator.clipboard.writeText(text);
    button.textContent = 'Copied';
  } catch {
    button.textContent = 'Select the citation above to copy';
  }
}));
