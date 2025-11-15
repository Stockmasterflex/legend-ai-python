(function () {
  const DEFAULT_SYMBOL = 'NASDAQ:AAPL';
  let currentSymbol = DEFAULT_SYMBOL;
  let initialized = false;
  let initialParamPresent = false;

  function normalizeSymbol(raw) {
    if (!raw) return null;
    let symbol = String(raw).trim().toUpperCase();
    if (!symbol) return null;
    if (!symbol.includes(':')) {
      symbol = `NASDAQ:${symbol}`;
    }
    return symbol;
  }

  function getDefaultSymbol() {
    if (document.body?.dataset?.defaultTvSymbol) {
      const normalized = normalizeSymbol(document.body.dataset.defaultTvSymbol);
      if (normalized) return normalized;
    }
    return DEFAULT_SYMBOL;
  }

  function getSymbolFromQuery() {
    try {
      const params = new URLSearchParams(window.location.search);
      const candidate = params.get('tvwidgetsymbol');
      if (candidate) {
        initialParamPresent = true;
      }
      return normalizeSymbol(candidate) || getDefaultSymbol();
    } catch (error) {
      return getDefaultSymbol();
    }
  }

  function updateQueryParam(symbol) {
    if (!window.history || typeof window.history.replaceState !== 'function') return;
    const url = new URL(window.location.href);
    url.searchParams.set('tvwidgetsymbol', symbol);
    window.history.replaceState({}, '', url.toString());
  }

  function replacePlaceholders(root, symbol) {
    if (!root) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (node.nodeValue && node.nodeValue.includes('__SYMBOL__')) {
        node.nodeValue = node.nodeValue.replace(/__SYMBOL__/g, symbol);
      }
    }
    root.querySelectorAll('*').forEach((el) => {
      Array.from(el.attributes).forEach((attr) => {
        if (attr.value.includes('__SYMBOL__')) {
          attr.value = attr.value.replace(/__SYMBOL__/g, symbol);
          el.setAttribute(attr.name, attr.value);
        }
      });
    });
  }

  function renderTemplates(symbol) {
    const containers = document.querySelectorAll('[data-tv-widget-target]');
    containers.forEach((container) => {
      const templateId = container.getAttribute('data-tv-widget-target');
      if (!templateId) return;
      const template = document.getElementById(templateId);
      if (!template) {
        container.innerHTML = '<p class="tv-error">Widget template missing.</p>';
        return;
      }
      const fragment = template.content.cloneNode(true);
      replacePlaceholders(fragment, symbol);
      container.innerHTML = '';
      container.appendChild(fragment);
    });
    document.querySelectorAll('[data-tv-symbol-label]').forEach((label) => {
      label.textContent = symbol;
    });
  }

  function init() {
    currentSymbol = getSymbolFromQuery();
    renderTemplates(currentSymbol);
    initialized = true;
    if (!initialParamPresent) {
      updateQueryParam(currentSymbol);
    }
    document.dispatchEvent(new CustomEvent('legend-tv:ready', { detail: { symbol: currentSymbol } }));
  }

  function setSymbol(rawSymbol, options = {}) {
    const normalized = normalizeSymbol(rawSymbol);
    if (!normalized) return currentSymbol;
    if (normalized === currentSymbol && initialized) {
      document.querySelectorAll('[data-tv-symbol-label]').forEach((label) => {
        label.textContent = normalized;
      });
      return currentSymbol;
    }
    currentSymbol = normalized;
    if (options.updateUrl !== false) {
      updateQueryParam(normalized);
    }
    renderTemplates(normalized);
    if (initialized) {
      document.dispatchEvent(new CustomEvent('legend-tv:symbol-changed', { detail: { symbol: normalized } }));
    }
    return currentSymbol;
  }

  window.LegendTV = {
    getSymbol: () => currentSymbol,
    normalizeSymbol,
    setSymbol,
    refresh: () => renderTemplates(currentSymbol),
  };

  document.addEventListener('DOMContentLoaded', init);
})();
