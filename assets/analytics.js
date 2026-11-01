/* Reuses the public Clicky site ID on Stuart's Columbia homepage.
 * Preview visits and local checks should not pollute production analytics.
 */
(() => {
  if (window.location.hostname !== 'stuartah.github.io') return;
  const script = document.createElement('script');
  script.src = 'https://static.getclicky.com/js';
  script.async = true;
  script.addEventListener('load', () => {
    try { window.clicky.init(101117148); } catch { /* Analytics must never block the site. */ }
  });
  document.head.appendChild(script);
})();
