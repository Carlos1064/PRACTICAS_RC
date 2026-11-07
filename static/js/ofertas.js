(function () {
  const form = document.querySelector('[data-offer-search]');
  const results = document.querySelector('#offer-results');
  if (!form || !results) return;

  let requestController;
  let searchTimer;
  const buildUrl = function (page) {
    const url = new URL(form.action, window.location.origin);
    new FormData(form).forEach(function (value, key) {
      if (String(value).trim()) url.searchParams.set(key, value);
    });
    if (page) url.searchParams.set('page', page);
    return url;
  };
  const loadResults = async function (url, pushHistory) {
    if (requestController) requestController.abort();
    requestController = new AbortController();
    results.setAttribute('aria-busy', 'true');
    results.classList.add('is-loading');
    try {
      const response = await fetch(url, {
        headers: {'X-Requested-With': 'XMLHttpRequest', 'Accept': 'text/html'},
        signal: requestController.signal
      });
      if (!response.ok) throw new Error('No fue posible cargar las ofertas.');
      results.innerHTML = await response.text();
      if (pushHistory) window.history.pushState({}, '', url);
    } catch (error) {
      if (error.name !== 'AbortError') {
        results.innerHTML = '<div class="empty-state"><h2>No pudimos actualizar los resultados</h2><p>Revisa tu conexión e inténtalo de nuevo.</p></div>';
      }
    } finally {
      results.setAttribute('aria-busy', 'false');
      results.classList.remove('is-loading');
    }
  };

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    loadResults(buildUrl(), true);
  });
  form.querySelectorAll('select').forEach(function (select) {
    select.addEventListener('change', function () { loadResults(buildUrl(), true); });
  });
  const query = form.querySelector('[name="q"]');
  if (query) query.addEventListener('input', function () {
    window.clearTimeout(searchTimer);
    searchTimer = window.setTimeout(function () { loadResults(buildUrl(), true); }, 280);
  });
  results.addEventListener('click', function (event) {
    const link = event.target.closest('a.page-link');
    if (!link || link.classList.contains('is-disabled')) return;
    const url = new URL(link.href, window.location.origin);
    if (url.origin !== window.location.origin) return;
    event.preventDefault();
    loadResults(url, true);
  });
  window.addEventListener('popstate', function () {
    const params = new URLSearchParams(window.location.search);
    for (const [name, value] of params.entries()) {
      const field = form.elements.namedItem(name);
      if (field) field.value = value;
    }
    ['q', 'tipo', 'categoria', 'modalidad', 'ciudad'].forEach(function (name) {
      if (!params.has(name) && form.elements.namedItem(name)) form.elements.namedItem(name).value = '';
    });
    loadResults(new URL(window.location.href), false);
  });
})();
