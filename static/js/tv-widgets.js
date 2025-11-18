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

  function getTradingViewTheme() {
    // Get theme from theme engine if available
    if (window.themeEngine && typeof window.themeEngine.getTradingViewTheme === 'function') {
      return window.themeEngine.getTradingViewTheme();
    }
    // Fallback to data attribute or default
    return document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
  }

  function replacePlaceholders(root, symbol) {
    if (!root) return;

    // Get current theme
    const tvTheme = getTradingViewTheme();

    // Replace text nodes
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (node.nodeValue) {
        if (node.nodeValue.includes('__SYMBOL__')) {
          node.nodeValue = node.nodeValue.replace(/__SYMBOL__/g, symbol);
        }
        // Replace theme placeholders in JSON configs
        if (node.nodeValue.includes('"theme":') || node.nodeValue.includes('"colorTheme":')) {
          node.nodeValue = node.nodeValue.replace(/"theme":\s*"(dark|light)"/g, `"theme": "${tvTheme}"`);
          node.nodeValue = node.nodeValue.replace(/"colorTheme":\s*"(dark|light)"/g, `"colorTheme": "${tvTheme}"`);
        }
      }
    }

    // Replace attributes
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

    // Listen for theme changes to refresh widgets
    window.addEventListener('themechange', () => {
      if (initialized) {
        renderTemplates(currentSymbol);
      }
    });
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
