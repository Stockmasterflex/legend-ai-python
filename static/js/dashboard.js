/*
 * Legend AI Dashboard Controller
 * Vanilla JS + Alpine hooks powering the cyberpunk UI
 */
(function () {
  // Initialize Dashboard object immediately to prevent Alpine.js errors
  window.Dashboard = window.Dashboard || { 
    focusTab: function(tab) {
      // Stub function that will be replaced on DOMContentLoaded
      // This prevents errors if Alpine.js tries to call it before initialization
      if (document.readyState === 'loading') {
        console.log('Dashboard not initialized yet, tab:', tab);
      }
    },
    initialized: false
  };
  const state = {
    activeTab: 'analyze',
    currentTicker: 'NVDA',
    currentInterval: '1day',
    cacheStats: null,
    universeRows: [],
    topSetups: [],
    topSetupsLoaded: false,
    topSetupsRefreshing: false,
    chartRequestId: 0,
    analyzeChartRequest: null,
    watchlistEdit: null,
    watchlistItems: [],
  };

  const WATCHLIST_TAG_LIBRARY = [
    'Breakout',
    'Momentum',
    'VCP',
    'Pullback',
    'Earnings',
    'Post-earnings drift',
    'Leader',
    'Laggard',
    'Reclaim of 21 EMA',
    'Reclaim of 50 SMA',
    'First pullback',
    'Late-stage base',
    'Extended',
    'Gap up',
    'Base-on-base',
    'Short squeeze',
    'Power trend',
  ];

  function mapTickerToTvSymbol(ticker, source) {
    const clean = (ticker || '').trim().toUpperCase();
    if (!clean) return null;
    if (source && source.toUpperCase().includes('NYSE')) {
      return `NYSE:${clean}`;
    }
    return `NASDAQ:${clean}`;
  }

  function buildTvLabLink(ticker, source) {
    const symbol = mapTickerToTvSymbol(ticker, source) || 'NASDAQ:AAPL';
    return `/tv?tvwidgetsymbol=${encodeURIComponent(symbol)}`;
  }

  const els = {};

  document.addEventListener('DOMContentLoaded', () => {
    try {
      console.log('Dashboard initializing...');
      cacheDom();
      bindEvents();
      initTabNavigation();
      initTagControls();
      initWatchlistDensity();
      hydrateAnalyzeFromTv();
      window.Dashboard = { 
        focusTab: (tab) => switchTab(tab),
        initialized: true
      };
      console.log('Dashboard initialized successfully');
      fetchMarketInternals();
      loadWatchlist();
      loadTopSetups();
      handleUniverseScan();
      setInterval(fetchMarketInternals, 300000);
    } catch (error) {
      console.error('Dashboard initialization error:', error);
      // Show error to user
      const errorMsg = document.createElement('div');
      errorMsg.style.cssText = 'position:fixed;top:0;left:0;right:0;background:#ef4444;color:white;padding:20px;z-index:10000;font-family:monospace;';
      errorMsg.innerHTML = `<strong>Dashboard Error:</strong> ${error.message}<br><small>Check browser console (F12) for details.</small>`;
      document.body.appendChild(errorMsg);
    }
    // Fetch build version and stamp header
    fetch('/api/version')
      .then(r => r.json())
      .then(v => {
        const el = document.getElementById('build-version');
        if (el && v && v.commit && String(v.commit).trim() !== 'unknown') {
          el.textContent = `(build ${String(v.commit).slice(0,7)})`;
        } else if (el) {
          el.textContent = '';
        }
      })
      .catch(() => {
        const el = document.getElementById('build-version');
        if (el) el.textContent = '';
      });
  });

  function cacheDom() {
    els.patternForm = document.getElementById('pattern-form');
    els.patternTicker = document.getElementById('pattern-ticker');
    els.patternInterval = document.getElementById('pattern-interval');
    els.patternResults = document.getElementById('pattern-results');
    els.patternLoading = document.getElementById('pattern-loading');
    els.patternChart = document.getElementById('analyze-chart');
    els.patternAddWatchlist = document.getElementById('pattern-add-watchlist');
    els.patternSnapshot = document.getElementById('pattern-snapshot');
    els.analyzeChartStatus = document.getElementById('analyze-chart-status');
    els.analyzeChartTitle = document.getElementById('analyze-chart-title');
    els.analyzeStatusLive = document.getElementById('analyze-status-live');

    els.quickSymbol = document.getElementById('quick-symbol-input');
    els.quickTimeframe = document.getElementById('quick-timeframe');
    els.quickScanBtn = document.getElementById('quick-scan-button');
    els.quickScanForm = document.getElementById('quick-scan-form');
    els.quickSnapshot = document.getElementById('quick-snapshot');

    els.universeForm = document.getElementById('universe-form');
    els.universeTable = document.getElementById('universe-table');
    els.universeLoading = document.getElementById('universe-loading');

    els.watchlistForm = document.getElementById('watchlist-form');
    els.watchlistList = document.getElementById('watchlist-list');
    els.watchlistEmpty = document.getElementById('watchlist-empty');
    els.watchlistFilter = document.getElementById('watchlist-filter');
    els.watchlistTagFilter = document.getElementById('watchlist-tag-filter');
    els.watchlistSymbol = document.getElementById('watchlist-symbol');
    els.watchlistReason = document.getElementById('watchlist-reason');
    els.watchlistStatus = document.getElementById('watchlist-status');
    els.watchlistTags = document.getElementById('watchlist-tags');
    els.watchlistSubmit = document.getElementById('watchlist-submit');
    els.watchlistCancel = document.getElementById('watchlist-cancel');
    els.watchlistModeIndicator = document.getElementById('watchlist-mode-indicator');
    els.watchlistDensityButtons = document.querySelectorAll('[data-density]');
    els.watchlistTableWrapper = document.querySelector('.watchlist-table-wrapper');
    if (els.watchlistCancel) {
      els.watchlistCancel.hidden = true;
    }
    els.scannerMeta = document.getElementById('universe-meta');

    els.topGrid = document.getElementById('top-setups-grid');
    els.topEmpty = document.getElementById('top-setups-empty');
    els.topLoading = document.getElementById('top-setups-loading');
    els.topMeta = document.getElementById('top-setups-meta');
    els.topRefresh = document.getElementById('top-setups-refresh');

    els.marketResults = document.getElementById('market-results');
    els.marketLoading = document.getElementById('market-loading');
    els.marketRefresh = document.getElementById('market-refresh');

    els.chartTicker = document.getElementById('chart-ticker');
    els.chartRefresh = document.getElementById('chart-refresh');
    els.chartMulti = document.getElementById('chart-multi');
    els.chartsResults = document.getElementById('charts-results');

    els.toastStack = document.getElementById('toast-stack');
    setAnalyzeChartTitle('Waiting for scan');
    setAnalyzeChartStatus('Idle', 'muted');
  }

  function initTagControls() {
    renderTagButtons(els.watchlistTags);
    renderTagButtons(els.watchlistTagFilter);
    setupTagToggleGroup(els.watchlistTags);
    setupTagToggleGroup(els.watchlistTagFilter, () => renderWatchlist());
  }

  function renderTagButtons(container) {
    if (!container) return;
    const frag = document.createDocumentFragment();
    WATCHLIST_TAG_LIBRARY.forEach((tag) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'tag-toggle';
      btn.dataset.tag = tag;
      btn.textContent = tag;
      frag.appendChild(btn);
    });
    container.innerHTML = '';
    container.appendChild(frag);
  }

  function setupTagToggleGroup(container, onChange) {
    if (!container) return;
    container.querySelectorAll('[data-tag]').forEach((btn) => {
      btn.setAttribute('aria-pressed', btn.classList.contains('active') ? 'true' : 'false');
      btn.addEventListener('click', () => {
        const isActive = btn.classList.toggle('active');
        btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
        if (typeof onChange === 'function') {
          onChange(readTagSelection(container));
        }
      });
    });
  }

  function initWatchlistDensity() {
    if (!els.watchlistDensityButtons || !els.watchlistDensityButtons.length || !els.watchlistTableWrapper) {
      return;
    }
    const setDensity = (density) => {
      els.watchlistTableWrapper.classList.toggle('compact', density === 'compact');
      els.watchlistDensityButtons.forEach((btn) => {
        btn.classList.toggle('active', btn.dataset.density === density);
      });
    };
    els.watchlistDensityButtons.forEach((btn) => {
      btn.addEventListener('click', () => setDensity(btn.dataset.density));
    });
  }

  function hydrateAnalyzeFromTv() {
    if (!window.LegendTV || typeof window.LegendTV.getSymbol !== 'function') return;
    const symbol = window.LegendTV.getSymbol();
    if (!symbol) return;
    const ticker = symbol.split(':').pop();
    if (!ticker) return;
    if (els.patternTicker) els.patternTicker.value = ticker;
    if (els.quickSymbol) els.quickSymbol.value = ticker;
  }

  function syncTradingViewSymbol(ticker, source) {
    if (!ticker || !window.LegendTV || typeof window.LegendTV.setSymbol !== 'function') return;
    const tvSymbol = mapTickerToTvSymbol(ticker, source);
    if (!tvSymbol) return;
    window.LegendTV.setSymbol(tvSymbol);
  }

  function readTagSelection(container) {
    return Array.from(container?.querySelectorAll('.tag-toggle.active') || [])
      .map((btn) => btn.dataset.tag)
      .filter(Boolean);
  }

  function setTagSelection(container, tags = []) {
    if (!container) return;
    const lookup = new Set((tags || []).map((tag) => tag.trim()));
    container.querySelectorAll('[data-tag]').forEach((btn) => {
      const isActive = lookup.has(btn.dataset.tag);
      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });
  }

  function initTabNavigation() {
    const tabs = document.querySelectorAll('.tabs-header .tab-button');
    tabs.forEach((btn) => {
      const tabKey = btn.dataset.tabTarget;
      if (!tabKey) return;
      btn.addEventListener('click', (event) => {
        event.preventDefault();
        switchTab(tabKey);
      });
      btn.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          btn.click();
        }
      });
    });
    document.querySelectorAll('[x-cloak]').forEach((el) => el.removeAttribute('x-cloak'));
    switchTab(state.activeTab || 'analyze');
  }

  // New: fetch /api/analyze with timeout and loading guards
  async function fetchAnalyze(ticker, tf) {
    if (!ticker) {
      toast('Enter a ticker to scan.', 'error');
      return;
    }
    state.currentTicker = ticker;
    state.currentInterval = tf === 'weekly' ? '1week' : '1day';
    toggleLoading(els.patternLoading, true);
    const btn = els.patternForm?.querySelector('button[type="submit"]');
    const origLabel = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = 'Analyzing…'; }
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 15000);
    try {
      const url = `/api/analyze?ticker=${encodeURIComponent(ticker)}&tf=${tf}`;
      console.log('Fetching analyze:', url);
      const res = await fetch(url, { signal: controller.signal });
      console.log('Analyze response status:', res.status);
      const data = await res.json().catch((e) => {
        console.error('JSON parse error:', e);
        return { error: 'Invalid response from server' };
      });
      if (!res.ok) {
        const errorMsg = data?.detail || data?.reason || data?.error || `Analyze failed (${res.status})`;
        throw new Error(errorMsg);
      }
      console.log('Analyze data received:', Object.keys(data));
      renderAnalyzeIntel(data);
      const hasSnapshot = typeof data.chart_url === 'string' && data.chart_url.length > 0;
      loadAnalyzeChart(ticker, tf, data?.plan || {}, hasSnapshot ? data.chart_url : null);
      syncTradingViewSymbol(ticker, data?.universe?.source || data?.universe?.exchange);
      toast(`Analyzed ${ticker}`, 'success');
    } catch (err) {
      console.error('Analyze error:', err);
      const errorMsg = err.message || 'Unknown error occurred';
      if (els.patternResults) {
        els.patternResults.innerHTML = `<p style="color:#ef4444;padding:20px;">Error: ${errorMsg}</p>`;
      }
      toast(errorMsg, 'error');
      renderAnalyzeChartImage(null, { placeholder: 'Chart unavailable' });
    } finally {
      clearTimeout(timer);
      toggleLoading(els.patternLoading, false);
      if (btn) { btn.disabled = false; btn.textContent = origLabel; }
    }
  }

  function switchTab(tab) {
    const tabs = Array.from(document.querySelectorAll('.tabs-header .tab-button'));
    const panes = {
      analyze: document.getElementById('tab-analyze'),
      scanner: document.getElementById('tab-scanner'),
      top: document.getElementById('tab-top'),
      internals: document.getElementById('tab-internals'),
      watchlist: document.getElementById('tab-watchlist'),
    };
    // Unmount analyze view on leave
    if (state.activeTab === 'analyze' && tab !== 'analyze') {
      const container = document.getElementById('analyze-chart');
      if (container) container.innerHTML = '';
    }
    state.activeTab = tab;
    if (tab === 'top' && !state.topSetupsLoaded) {
      loadTopSetups();
    }
    tabs.forEach((btn) => {
      const tabKey = btn.dataset.tabTarget || (btn.textContent || '').toLowerCase();
      const isActive = tabKey === tab;
      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-selected', isActive ? 'true' : 'false');
      btn.setAttribute('role', 'tab');
      btn.setAttribute('tabindex', isActive ? '0' : '-1');
    });
    Object.entries(panes).forEach(([key, el]) => {
      if (!el) return;
      const on = key === tab;
      if (on) {
        el.removeAttribute('hidden');
      } else {
        el.setAttribute('hidden', 'true');
      }
      el.setAttribute('role', 'tabpanel');
      el.setAttribute('aria-hidden', on ? 'false' : 'true');
    });
  }

  function debounce(fn, wait) {
    let t;
    return function (...args) {
      clearTimeout(t);
      t = setTimeout(() => fn.apply(this, args), wait);
    };
  }

  function bindEvents() {
    els.patternForm?.addEventListener('submit', (e) => {
      e.preventDefault();
      const ticker = els.patternTicker.value.trim().toUpperCase();
      const tf = els.patternInterval.value === '1week' ? 'weekly' : 'daily';
      fetchAnalyze(ticker, tf);
    });

    // Quick search form submit (supports Enter key)
    els.quickScanForm?.addEventListener('submit', (e) => {
      e.preventDefault();
      els.quickScanBtn?.click();
    });

    els.quickScanBtn?.addEventListener('click', (e) => {
      e.preventDefault();
      if (els.quickSymbol) {
        els.patternTicker.value = els.quickSymbol.value.trim().toUpperCase();
        els.patternInterval.value = els.quickTimeframe.value;
        const tf = els.patternInterval.value === '1week' ? 'weekly' : 'daily';
        debounce(() => fetchAnalyze(els.patternTicker.value.trim().toUpperCase(), tf), 300)();
      }
    });
    els.patternAddWatchlist?.addEventListener('click', addPatternToWatchlist);
    els.patternSnapshot?.addEventListener('click', () => generateSnapshot(els.patternTicker.value, els.patternInterval.value));
    els.quickSnapshot?.addEventListener('click', () => generateSnapshot(els.quickSymbol.value, els.quickTimeframe.value));

    els.universeForm?.addEventListener('submit', handleUniverseScan);
    document.getElementById('universe-export')?.addEventListener('click', exportUniverseCsv);

    els.watchlistForm?.addEventListener('submit', handleWatchlistSubmit);
    els.watchlistFilter?.addEventListener('change', () => renderWatchlist());
    els.watchlistCancel?.addEventListener('click', () => exitWatchlistEditMode());

    els.topRefresh?.addEventListener('click', () => loadTopSetups(true));
    els.marketRefresh?.addEventListener('click', () => fetchMarketInternals());
    els.patternChart?.addEventListener('click', handleChartShellClick);

    els.chartMulti?.addEventListener('click', handleMultiTimeframe);
  }

  function renderAnalyzeIntel(data) {
    if (!data) return;
    const m = data.patterns?.minervini || { passed: false, failed_rules: [] };
    const w = data.patterns?.weinstein || { stage: 0, reason: '' };
    const vcp = data.patterns?.vcp || { detected: false, score: 0 };
    const p = data.plan || {};
    const intel = data.intel || {};
    const rs = data.relative_strength || {};
    const meta = data.universe || {};
    const minPass = !!(m.passed ?? m.pass);
    const rsRank = Number(rs.rank ?? 0);
    const scorePct = rsRank ? rsRank : (minPass ? 75 : 35);
    const ma = data.indicators?.ma_distances || {};
    const dist21 = typeof ma.vs_ema21_pct === 'number' ? `${ma.vs_ema21_pct >= 0 ? '+' : ''}${ma.vs_ema21_pct.toFixed(2)}%` : '—';
    const dist50 = typeof ma.vs_sma50_pct === 'number' ? `${ma.vs_sma50_pct >= 0 ? '+' : ''}${ma.vs_sma50_pct.toFixed(2)}%` : '—';
    const rmult = Number(p.risk_r || intel.r_multiple || 0);
    const atrPct = typeof p.atr_percent === 'number' ? `${p.atr_percent.toFixed(2)}%` : '—';

    const failureList = (intel.rule_failures?.length ? intel.rule_failures : m.failed_rules || [])
      .slice(0, 5)
      .map((rule) => `<li>${rule}</li>`)
      .join('');

    const snapshotLink = typeof data.chart_url === 'string' && data.chart_url.length > 0
      ? `<a class="btn btn-secondary btn-compact" href="${data.chart_url}" target="_blank" rel="noopener">Snapshot</a>`
      : '<span style="color:var(--color-text-secondary)">Snapshot unavailable</span>';
    const tvHref = buildTvLabLink(data.ticker, meta.source || meta.exchange);
    const tvLink = `<a class="btn btn-tv btn-compact" href="${tvHref}" target="_blank" rel="noopener">TV</a>`;

    els.patternResults.innerHTML = `
      <article class="result-card">
        <div class="result-header">
          <div>
            <div class="ticker-symbol">${data.ticker}</div>
            <div class="pattern-type">${data.timeframe?.toUpperCase() || ''} · ${meta.universe || 'Off-universe'}</div>
            <small>${meta.sector || 'Sector N/A'}</small>
          </div>
          <div class="result-actions">
            ${snapshotLink}
            ${tvLink}
          </div>
        </div>
        <div class="score-gauge">
          <div class="gauge-bar"><div class="gauge-fill" style="--score:${scorePct}%"></div></div>
          <div class="score-text">${scorePct}/100</div>
        </div>
        <div class="form-grid">
          <div><div class="kpi-label">Minervini</div><div>${minPass ? 'PASS ✅' : 'FAIL ⚠️'}</div></div>
          <div><div class="kpi-label">Weinstein</div><div>Stage ${w.stage} — ${w.reason || ''}</div></div>
          <div><div class="kpi-label">VCP</div><div>${vcp.detected ? 'Yes' : 'No'} · score ${Number(vcp.score || 0).toFixed(1)}</div></div>
          <div><div class="kpi-label">RS Rank</div><div>${rs.rank ?? '—'} (${typeof rs.delta_vs_spy === 'number' ? `${rs.delta_vs_spy.toFixed(2)} pts vs SPY` : 'vs SPY N/A'})</div></div>
          <div><div class="kpi-label">Dist to 21EMA</div><div>${dist21}</div></div>
          <div><div class="kpi-label">Dist to 50SMA</div><div>${dist50}</div></div>
          <div><div class="kpi-label">R Multiple</div><div>${rmult.toFixed(2)}R</div></div>
          <div><div class="kpi-label">ATR%</div><div>${atrPct}</div></div>
          <div><div class="kpi-label">Entry</div><div>$${Number(p.entry || 0).toFixed(2)}</div></div>
          <div><div class="kpi-label">Stop</div><div>$${Number(p.stop || 0).toFixed(2)}</div></div>
          <div><div class="kpi-label">Target</div><div>$${Number(p.target || 0).toFixed(2)}</div></div>
        </div>
        ${failureList ? `<div class="rule-failures"><div class="kpi-label">Failed Rules</div><ul>${failureList}</ul></div>` : ''}
      </article>`;
  }

  // Render analyze chart image (ChartIMG URL). No client-side secrets.
  function renderAnalyzeChartImage(url, options = {}) {
    if (!els.patternChart) return;
    setChartShellLoading(false);
    els.patternChart.innerHTML = '';
    if (typeof url === 'string' && url.length > 0) {
      const link = document.createElement('a');
      link.href = url;
      link.target = '_blank';
      link.rel = 'noopener';
      const img = document.createElement('img');
      img.src = url;
      img.alt = 'Analyze snapshot';
      img.loading = 'lazy';
      link.appendChild(img);
      els.patternChart.appendChild(link);
    } else {
      const msg = document.createElement('p');
      msg.className = 'chart-empty';
      msg.textContent = options.placeholder || 'Chart snapshot unavailable';
      els.patternChart.appendChild(msg);
    }
  }

  function renderAnalyzeChartError(message) {
    if (!els.patternChart) return;
    setChartShellLoading(false);
    els.patternChart.innerHTML = `
      <div class="chart-error">
        <p>${message || 'Chart unavailable'}</p>
        <button class="btn btn-secondary btn-compact" type="button" data-chart-retry="1">Retry chart</button>
      </div>`;
  }

  function setAnalyzeChartTitle(text) {
    if (els.analyzeChartTitle) {
      els.analyzeChartTitle.textContent = text || 'Chart View';
    }
  }

  function setAnalyzeChartStatus(message, tone = 'muted') {
    if (!els.analyzeChartStatus) return;
    const classes = ['chart-status'];
    if (tone) classes.push(tone);
    els.analyzeChartStatus.className = classes.join(' ');
    els.analyzeChartStatus.textContent = message;
  }

  function setChartShellLoading(isLoading) {
    if (!els.patternChart) return;
    els.patternChart.classList.toggle('loading', Boolean(isLoading));
  }

  function handleChartShellClick(event) {
    const retry = event.target.closest('[data-chart-retry]');
    if (retry) {
      event.preventDefault();
      retryAnalyzeChart();
    }
  }

  function retryAnalyzeChart() {
    if (!state.analyzeChartRequest) return;
    const { ticker, tf, plan } = state.analyzeChartRequest;
    loadAnalyzeChart(ticker, tf, plan);
  }

  function mapTimeframeToInterval(tf) {
    const value = (tf || '').toString().toLowerCase();
    if (value.includes('week')) return '1W';
    if (value.includes('60')) return '60';
    return '1D';
  }

  async function fetchChartImage(ticker, tf, plan = {}) {
    const interval = mapTimeframeToInterval(tf);
    const res = await fetch('/api/charts/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ticker,
        interval,
        entry: plan.entry,
        stop: plan.stop,
        target: plan.target,
      }),
    });
    const payload = await res.json().catch(() => ({}));
    if (!res.ok || !payload.success || !payload.chart_url) {
      throw new Error(payload.error || `Chart unavailable (${res.status})`);
    }
    return payload.chart_url;
  }

  function renderPreviewImage(slot, url, altLabel = 'Chart preview') {
    if (!slot) return;
    const img = document.createElement('img');
    img.src = url;
    img.alt = altLabel;
    img.loading = 'lazy';
    img.className = 'preview-thumb';
    img.addEventListener('error', () => {
      slot.innerHTML = '<p class="chart-empty compact">Chart unavailable</p>';
    }, { once: true });
    slot.innerHTML = '';
    slot.appendChild(img);
  }

  function loadAnalyzeChart(ticker, tf, plan = {}, fallbackUrl = null) {
    const timeframeLabel = tf === 'weekly' ? '1W' : '1D';
    setAnalyzeChartTitle(`${ticker} • ${timeframeLabel}`);
    state.analyzeChartRequest = { ticker, tf, plan };
    const requestId = ++state.chartRequestId;
    if (fallbackUrl) {
      renderAnalyzeChartImage(fallbackUrl);
      setAnalyzeChartStatus('Snapshot updated', 'success');
      return;
    }
    setAnalyzeChartStatus('Generating chart…', 'loading');
    setChartShellLoading(true);
    fetchChartImage(ticker, tf, plan)
      .then((url) => {
        if (requestId !== state.chartRequestId) return;
        renderAnalyzeChartImage(url);
        setAnalyzeChartStatus('Chart synced', 'success');
      })
      .catch((error) => {
        if (requestId !== state.chartRequestId) return;
        console.error('Analyze chart error:', error);
        renderAnalyzeChartError(error.message || 'Chart unavailable');
        setAnalyzeChartStatus(error.message || 'Chart unavailable', 'error');
      })
      .finally(() => {
        if (requestId === state.chartRequestId) {
          setChartShellLoading(false);
        }
      });
  }

  async function handleUniverseScan(event) {
    event?.preventDefault();
    const universe = document.getElementById('universe-source').value;
    const limit = Number(document.getElementById('universe-limit').value || 50);
    const minScore = Number(document.getElementById('universe-score').value || 6.5);
    const minRs = Number(document.getElementById('universe-rs').value || 55);
    const timeframe = document.getElementById('scanner-timeframe')?.value || '1day';
    const sector = document.getElementById('scanner-sector')?.value || 'all';
    const atrCapRaw = document.getElementById('scanner-atr')?.value;
    const patternSelect = document.getElementById('scanner-patterns');
    const patternTypes = Array.from(patternSelect?.selectedOptions || [])
      .map((opt) => opt.value)
      .filter((val) => val && val !== 'all');
    toggleLoading(els.universeLoading, true);
    if (els.universeTable) {
      els.universeTable.setAttribute('aria-busy', 'true');
      els.universeTable.innerHTML = '<tr><td colspan="11" class="scanner-message">Scanning universe…</td></tr>';
    }
    try {
      const res = await fetch('/api/universe/scan/quick', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          universe,
          limit,
          min_score: minScore,
          min_rs: minRs,
          timeframe,
          sector: sector === 'all' ? null : sector,
          pattern_types: patternTypes.length ? patternTypes : null,
          max_atr_percent: atrCapRaw ? Number(atrCapRaw) : null,
        }),
      });
      const payload = await res.json();
      if (!payload.success) throw new Error(payload.error || 'Universe scan failed');
      renderScannerMeta(payload.stats || {});
      renderUniverseTable(payload.data || []);
    } catch (err) {
      console.error(err);
      toast(err.message, 'error');
      if (els.universeTable) {
        els.universeTable.innerHTML = `<tr><td colspan="11">${err.message}</td></tr>`;
      }
    } finally {
      toggleLoading(els.universeLoading, false);
      if (els.universeTable) {
        els.universeTable.removeAttribute('aria-busy');
      }
    }
  }

  function renderUniverseTable(rows) {
    state.universeRows = rows;
    if (!rows.length) {
      els.universeTable.innerHTML = '<tr><td colspan="11">No setups found.</td></tr>';
      return;
    }
    els.universeTable.innerHTML = rows.map((row) => {
      const score = Number(row.score || 0).toFixed(1);
      const entry = formatCurrency(row.entry);
      const stop = formatCurrency(row.stop);
      const target = formatCurrency(row.target);
      const atrPercent = typeof row.atr_percent === 'number' ? `${row.atr_percent.toFixed(2)}%` : '—';
      const risk = computeRiskReward(row.entry, row.stop, row.target);
      const previewMarkup = row.chart_url
        ? `<img src="${row.chart_url}" alt="${row.ticker} chart" class="preview-thumb" loading="lazy" />`
        : '<p class="chart-empty compact">Use Preview chart to render.</p>';
      return `
        <tr>
          <td>
            <div class="ticker-symbol">${row.ticker}</div>
            <small>${row.source || 'Universe'}</small>
          </td>
          <td>${row.pattern || '—'}</td>
          <td>${score}</td>
          <td>${row.rs_rating ?? '—'}</td>
          <td>${atrPercent}</td>
          <td>${row.sector || '—'}</td>
          <td>${entry}</td>
          <td>${stop}</td>
          <td>${target}</td>
          <td>${risk}</td>
          <td>
            <div class="preview-block">
              <div class="scanner-chart-slot" data-slot="${row.ticker}">
                ${previewMarkup}
              </div>
              <button class="btn btn-ghost btn-compact" type="button" data-scan-chart="${row.ticker}">Preview chart</button>
            </div>
          </td>
          <td>
            <div class="button-row">
              <button class="btn btn-primary btn-compact" type="button" data-scan-analyze="${row.ticker}">Analyze</button>
              <button class="btn btn-secondary btn-compact" type="button" data-scan-watch="${row.ticker}">Watch</button>
              <a class="btn btn-tv btn-compact" href="${buildTvLabLink(row.ticker, row.source)}" target="_blank" rel="noopener">TV</a>
            </div>
          </td>
        </tr>`;
    }).join('');
    attachScannerRowActions();
  }

  function attachScannerRowActions() {
    els.universeTable?.querySelectorAll('[data-scan-watch]').forEach((btn) => {
      btn.addEventListener('click', () => quickAddWatchlist(btn.dataset.scanWatch, 'Universe scan', ['Scanner']));
    });
    els.universeTable?.querySelectorAll('[data-scan-analyze]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const ticker = btn.dataset.scanAnalyze;
        if (!ticker) return;
        switchTab('analyze');
        if (els.patternTicker) {
          els.patternTicker.value = ticker;
        }
        fetchAnalyze(ticker, 'daily');
      });
    });
    els.universeTable?.querySelectorAll('[data-scan-chart]').forEach((btn) => {
      btn.addEventListener('click', () => handleScannerChartPreview(btn.dataset.scanChart));
    });
  }

  function handleScannerChartPreview(ticker) {
    if (!ticker) return;
    const slot = els.universeTable?.querySelector(`[data-slot="${ticker}"]`);
    if (!slot) return;
    slot.innerHTML = '<p class="chart-empty compact">Generating…</p>';
    const row = state.universeRows.find((item) => item.ticker === ticker);
    if (!row) return;
    const tf = row.timeframe === '1week' ? '1week' : '1day';
    fetchChartImage(ticker, tf, { entry: row.entry, stop: row.stop, target: row.target })
      .then((url) => {
        renderPreviewImage(slot, url, `${ticker} chart preview`);
      })
      .catch((error) => {
        slot.innerHTML = `<p class="chart-empty compact">${error.message || 'Chart unavailable'}</p>`;
      });
  }

  function renderScannerMeta(stats = {}) {
    if (!els.scannerMeta) return;
    const universe = stats.universe || stats.requested_universe || '—';
    const timeframe = (stats.timeframe || '').toString().toUpperCase() || '1DAY';
    const scanned = stats.scanned ?? '—';
    const cache = stats.cache_hits ?? '—';
    const score = stats.min_score ?? '—';
    const rs = stats.min_rs ?? '—';
    const sector = stats.sector_filter ? stats.sector_filter.replace(/\b\w/g, (ch) => ch.toUpperCase()) : 'All';
    const metaMap = {
      universe,
      sector,
      timeframe,
      scanned,
      cache,
      score,
      rs,
    };
    Object.entries(metaMap).forEach(([key, value]) => {
      const target = els.scannerMeta.querySelector(`[data-meta="${key}"]`);
      if (target) target.textContent = value;
    });
  }

  function formatCurrency(value) {
    if (value === undefined || value === null || Number.isNaN(Number(value))) {
      return '—';
    }
    return `$${Number(value).toFixed(2)}`;
  }

  function computeRiskReward(entry, stop, target) {
    const e = Number(entry);
    const s = Number(stop);
    const t = Number(target);
    if (!Number.isFinite(e) || !Number.isFinite(s) || !Number.isFinite(t)) {
      return '—';
    }
    const risk = e - s;
    const reward = t - e;
    if (risk <= 0) return '—';
    return (reward / risk).toFixed(2);
  }

  function normalizeTags(tags) {
    if (!tags) return [];
    if (Array.isArray(tags)) {
      return tags.map((tag) => String(tag).trim()).filter(Boolean);
    }
    return String(tags)
      .split(',')
      .map((tag) => tag.trim())
      .filter(Boolean);
  }

  function setSelectValues(selectEl, values = []) {
    if (!selectEl) return;
    const set = new Set(values);
    Array.from(selectEl.options).forEach((option) => {
      option.selected = set.has(option.value);
    });
  }

  function enterWatchlistEdit(ticker) {
    if (!ticker || !state.watchlistItems.length) return;
    const item = state.watchlistItems.find((row) => row.ticker === ticker);
    if (!item) return;
    state.watchlistEdit = ticker;
    if (els.watchlistSymbol) {
      els.watchlistSymbol.value = ticker;
      els.watchlistSymbol.disabled = true;
    }
    if (els.watchlistReason) {
      els.watchlistReason.value = item.reason || '';
    }
    if (els.watchlistStatus) {
      els.watchlistStatus.value = item.status || 'Watching';
    }
    setTagSelection(els.watchlistTags, normalizeTags(item.tags));
    if (els.watchlistSubmit) {
      els.watchlistSubmit.textContent = 'Update watchlist';
    }
    if (els.watchlistModeIndicator) {
      els.watchlistModeIndicator.textContent = `Editing ${ticker}`;
      els.watchlistModeIndicator.classList.add('editing');
    }
    if (els.watchlistCancel) {
      els.watchlistCancel.hidden = false;
    }
    els.watchlistForm?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  function exitWatchlistEditMode() {
    state.watchlistEdit = null;
    if (els.watchlistSymbol) {
      els.watchlistSymbol.disabled = false;
      els.watchlistSymbol.value = '';
    }
    if (els.watchlistReason) {
      els.watchlistReason.value = '';
    }
    if (els.watchlistStatus) {
      els.watchlistStatus.value = 'Watching';
    }
    setTagSelection(els.watchlistTags, []);
    if (els.watchlistSubmit) {
      els.watchlistSubmit.textContent = 'Add to watchlist';
    }
    if (els.watchlistCancel) {
      els.watchlistCancel.hidden = true;
    }
    if (els.watchlistModeIndicator) {
      els.watchlistModeIndicator.textContent = 'Adding new ticker';
      els.watchlistModeIndicator.classList.remove('editing');
    }
  }

  async function handleWatchlistSubmit(event) {
    event.preventDefault();
    const ticker = (els.watchlistSymbol?.value || '').trim().toUpperCase();
    const reason = (els.watchlistReason?.value || '').trim();
    const tags = readTagSelection(els.watchlistTags);
    const status = els.watchlistStatus?.value || 'Watching';
    if (!ticker) return toast('Enter a ticker for the watchlist.', 'error');
    try {
      const isEdit = state.watchlistEdit && state.watchlistEdit === ticker;
      const endpoint = isEdit ? `/api/watchlist/${ticker}` : '/api/watchlist/add';
      const payload = isEdit
        ? { reason, status, tags }
        : { ticker, reason, status, tags };
      const res = await fetch(endpoint, {
        method: isEdit ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const response = await res.json();
      if (!res.ok || !response.success) {
        throw new Error(response.detail || response.error || 'Unable to save watchlist item');
      }
      exitWatchlistEditMode();
      toast(isEdit ? `${ticker} updated` : `${ticker} added to watchlist`, 'success');
      loadWatchlist();
    } catch (err) {
      console.error(err);
      toast(err.message, 'error');
    }
  }

  async function loadWatchlist() {
    try {
      const res = await fetch('/api/watchlist');
      const payload = await res.json();
      if (!payload.success) throw new Error(payload.detail || 'Failed to load watchlist');
      state.watchlistItems = payload.items || [];
      renderWatchlist();
    } catch (err) {
      console.error(err);
      toast(err.message, 'error');
    }
  }

  function renderWatchlist(items = state.watchlistItems || []) {
    const filter = els.watchlistFilter?.value || 'all';
    const tagFilters = readTagSelection(els.watchlistTagFilter);
    const filtered = items.filter((item) => {
      const status = item.status || 'Watching';
      const matchesStatus = filter === 'all' || status === filter;
      const tags = normalizeTags(item.tags);
      const matchesTags = !tagFilters.length || tagFilters.every((tag) => tags.includes(tag));
      return matchesStatus && matchesTags;
    });
    if (!filtered.length) {
      if (els.watchlistEmpty) {
        const hasFilters = filter !== 'all' || tagFilters.length > 0;
        els.watchlistEmpty.textContent = hasFilters
          ? 'No watchlist items match the current filters.'
          : 'No watchlist items yet.';
        els.watchlistEmpty.style.display = 'block';
      }
      if (els.watchlistList) els.watchlistList.innerHTML = '';
      return;
    }
    if (els.watchlistEmpty) {
      els.watchlistEmpty.style.display = 'none';
      els.watchlistEmpty.textContent = 'No watchlist items yet.';
    }
    els.watchlistList.innerHTML = filtered.map((item) => {
      const added = formatWatchlistDate(item.added_date || item.added_at);
      const status = item.status || 'Watching';
      const tags = normalizeTags(item.tags);
      const rsLabel = typeof item.rs_rating === 'number'
        ? item.rs_rating.toFixed(0)
        : (item.rs || '—');
      const atrLabel = typeof item.atr_percent === 'number'
        ? `${item.atr_percent.toFixed(2)}%`
        : '—';
      const statusKey = status.toLowerCase().replace(/\s+/g, '-') || 'watching';
      const previewMarkup = item.chart_url
        ? `<img src="${item.chart_url}" alt="${item.ticker} preview" class="preview-thumb" loading="lazy" />`
        : '<p class="chart-empty compact">Use Preview to load chart.</p>';
      const tagsMarkup = buildTagMarkup(tags);
      return `
        <tr>
          <td>
            <div class="ticker-symbol">${item.ticker}</div>
            <small>${item.pattern || item.status || ''}</small>
          </td>
          <td><span class="status-pill status-${statusKey}" data-status="${statusKey}">${status}</span></td>
          <td>${rsLabel || '—'}</td>
          <td>${atrLabel}</td>
          <td>${item.reason || 'No notes yet.'}</td>
          <td><div class="tag-stack">${tagsMarkup}</div></td>
          <td>${added}</td>
          <td>
            <div class="button-row">
              <button class="btn btn-primary btn-compact" data-analyze="${item.ticker}">Analyze</button>
              <button class="btn btn-secondary btn-compact" data-edit="${item.ticker}">Edit</button>
              <button class="btn btn-ghost btn-compact" data-preview="${item.ticker}">Preview chart</button>
              <a class="btn btn-tv btn-compact" data-tv-link="${item.ticker}" href="${buildTvLabLink(item.ticker, item.source)}" target="_blank" rel="noopener">TV</a>
              <button class="btn btn-danger btn-compact" data-remove="${item.ticker}">Remove</button>
            </div>
            <div class="preview-block" data-watch-preview="${item.ticker}">${previewMarkup}</div>
          </td>
        </tr>`;
    }).join('');
    attachWatchlistActions();
  }

  function attachWatchlistActions() {
    els.watchlistList?.querySelectorAll('[data-remove]').forEach((btn) => {
      btn.addEventListener('click', () => removeWatchlist(btn.dataset.remove));
    });
    els.watchlistList?.querySelectorAll('[data-analyze]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const ticker = btn.dataset.analyze;
        if (!ticker) return;
        switchTab('analyze');
        if (els.patternTicker) {
          els.patternTicker.value = ticker;
        }
        const tf = els.patternInterval.value === '1week' ? 'weekly' : 'daily';
        fetchAnalyze(ticker, tf);
      });
    });
    els.watchlistList?.querySelectorAll('[data-edit]').forEach((btn) => {
      btn.addEventListener('click', () => enterWatchlistEdit(btn.dataset.edit));
    });
    els.watchlistList?.querySelectorAll('[data-preview]').forEach((btn) => {
      btn.addEventListener('click', () => handleWatchlistPreview(btn.dataset.preview));
    });
  }

  function buildTagMarkup(tags = []) {
    if (!tags.length) {
      return '<span class="tag-pill tag-pill-muted">No tags</span>';
    }
    const visible = tags.slice(0, 3);
    const remaining = tags.slice(3);
    const visibleMarkup = visible.map((tag) => `<span class="tag-pill">${tag}</span>`).join('');
    if (!remaining.length) return visibleMarkup;
    const moreLabel = remaining.join(', ');
    return `${visibleMarkup}<span class="tag-pill tag-pill-more" title="${moreLabel}">+${remaining.length} more</span>`;
  }

  function formatWatchlistDate(value) {
    if (!value) return '—';
    const ts = new Date(value);
    if (Number.isNaN(ts.getTime())) return '—';
    return ts.toLocaleString();
  }

  async function removeWatchlist(ticker) {
    if (!ticker) return;
    try {
      const res = await fetch(`/api/watchlist/remove/${ticker}`, { method: 'DELETE' });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail || 'Unable to remove watchlist item');
      }
      toast(`${ticker} removed`, 'success');
      loadWatchlist();
    } catch (err) {
      console.error(err);
      toast(err.message, 'error');
    }
  }

  async function addPatternToWatchlist() {
    const ticker = els.patternTicker.value.trim().toUpperCase();
    if (!ticker) return toast('Scan a ticker first.', 'error');
    quickAddWatchlist(ticker, 'Pattern scanner', ['Analyze']);
  }

  function quickAddWatchlist(ticker, reason = 'Universe scan', tags = [], status = 'Watching') {
    fetch('/api/watchlist/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ticker, reason, tags, status }),
    })
      .then((res) => res.json())
      .then((payload) => {
        if (!payload.success) throw new Error(payload.detail || 'Unable to add watchlist item');
        toast(`${ticker} added to watchlist`, 'success');
        loadWatchlist();
      })
      .catch((err) => {
        console.error(err);
        toast(err.message, 'error');
      });
  }

  async function loadTopSetups(force = false) {
    if (!els.topGrid || state.topSetupsRefreshing) return;
    state.topSetupsRefreshing = true;
    if (force) state.topSetupsLoaded = false;
    toggleLoading(els.topLoading, true);
    els.topEmpty?.classList.remove('active');
    try {
      const res = await fetch('/api/top-setups?limit=10');
      const payload = await res.json();
      if (!res.ok || payload.success === false) {
        throw new Error(payload.detail || 'Top setups unavailable');
      }
      state.topSetupsLoaded = true;
      state.topSetups = payload.results || [];
      renderTopSetups(state.topSetups, payload);
      if (els.topMeta) {
        if (payload.count) {
          const ts = payload.generated_at ? new Date(payload.generated_at) : new Date();
          const tsLabel = Number.isNaN(ts.getTime()) ? '' : ts.toLocaleTimeString();
          const freshness = payload.cached ? 'cached' : 'live';
          els.topMeta.textContent = `Updated ${tsLabel || 'recently'} (${freshness})`;
        } else {
          els.topMeta.textContent = `No setups ≥ ${payload.min_score}`;
        }
      }
    } catch (err) {
      console.error(err);
      if (els.topGrid) {
        els.topGrid.innerHTML = `<p style="color:#ef4444;">${err.message}</p>`;
      }
      if (els.topMeta) {
        els.topMeta.textContent = err.message;
      }
    } finally {
      state.topSetupsRefreshing = false;
      toggleLoading(els.topLoading, false);
      if (!state.topSetups.length) {
        els.topEmpty?.classList.add('active');
      } else {
        els.topEmpty?.classList.remove('active');
      }
    }
  }

  function renderTopSetups(results = []) {
    if (!els.topGrid) return;
    if (!results.length) {
      els.topGrid.innerHTML = '';
      return;
    }
    const cards = results.map((item) => {
      const score = Number(item.score || 0).toFixed(1);
      const entry = Number(item.entry || 0).toFixed(2);
      const stop = Number(item.stop || 0).toFixed(2);
      const target = Number(item.target || 0).toFixed(2);
      const riskReward = Number(item.risk_reward || 0).toFixed(2);
      const chartContent = item.chart_url
        ? `<img src="${item.chart_url}" alt="${item.ticker} chart" class="preview-thumb" loading="lazy" />`
        : '<p class="chart-empty compact">Use Preview chart to sync a fresh snapshot.</p>';
      return `
        <article class="result-card top-setup-card">
          <div class="result-header">
            <div>
              <div class="ticker-symbol">${item.ticker}</div>
              <div class="pattern-type">${item.pattern || 'Setup'}</div>
            </div>
            <div class="top-score-badge">${score}/10</div>
          </div>
          <div class="top-plan-grid">
            <div><div class="kpi-label">Entry</div><div class="top-plan-value">$${entry}</div></div>
            <div><div class="kpi-label">Stop</div><div class="top-plan-value">$${stop}</div></div>
            <div><div class="kpi-label">Target</div><div class="top-plan-value">$${target}</div></div>
          </div>
          <div class="top-card-actions">
            <div>
              <div class="kpi-label">Risk/Reward</div>
              <div>${riskReward}R • ${item.source || 'Universe'}</div>
            </div>
          <div class="top-card-buttons">
            <button class="btn btn-primary" data-open-analyze="${item.ticker}">Analyze</button>
            <button class="btn btn-primary" data-watch="${item.ticker}">Watchlist</button>
            <button class="btn btn-secondary" data-top-chart="${item.ticker}">Preview chart</button>
          </div>
          </div>
          <div class="top-card-preview">
            <div class="scanner-chart-slot" data-top-slot="${item.ticker}">
              ${chartContent}
            </div>
          </div>
        </article>`;
    }).join('');
    els.topGrid.innerHTML = cards;
    attachTopSetupActions();
  }

  function attachTopSetupActions() {
    els.topGrid?.querySelectorAll('[data-open-analyze]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const ticker = btn.dataset.openAnalyze;
        if (!ticker) return;
        switchTab('analyze');
        if (els.patternTicker) {
          els.patternTicker.value = ticker;
          els.patternInterval.value = '1day';
        }
        fetchAnalyze(ticker, 'daily');
      });
    });
    els.topGrid?.querySelectorAll('[data-watch]').forEach((btn) => {
      btn.addEventListener('click', () => quickAddWatchlist(btn.dataset.watch, 'Top setup', ['Top Setup']));
    });
    els.topGrid?.querySelectorAll('[data-top-chart]').forEach((btn) => {
      btn.addEventListener('click', () => handleTopSetupChartPreview(btn.dataset.topChart));
    });
  }

  function handleTopSetupChartPreview(ticker) {
    if (!ticker) return;
    const slot = els.topGrid?.querySelector(`[data-top-slot="${ticker}"]`);
    if (!slot) return;
    slot.innerHTML = '<p class="chart-empty compact">Generating…</p>';
    const row = state.topSetups.find((item) => item.ticker === ticker);
    if (!row) return;
    fetchChartImage(ticker, '1day', { entry: row.entry, stop: row.stop, target: row.target })
      .then((url) => {
        renderPreviewImage(slot, url, `${ticker} chart preview`);
      })
      .catch((error) => {
        slot.innerHTML = `<p class="chart-empty compact">${error.message || 'Chart unavailable'}</p>`;
      });
  }

  function handleWatchlistPreview(ticker) {
    if (!ticker) return;
    const slot = els.watchlistList?.querySelector(`[data-watch-preview="${ticker}"]`);
    if (!slot) return;
    slot.innerHTML = '<p class="chart-empty compact">Loading…</p>';
    fetchChartImage(ticker, els.patternInterval?.value || '1day')
      .then((url) => {
        renderPreviewImage(slot, url, `${ticker} preview`);
      })
      .catch((error) => {
        slot.innerHTML = `<p class="chart-empty compact">${error.message || 'Chart unavailable'}</p>`;
      });
  }

  async function fetchMarketInternals() {
    toggleLoading(els.marketLoading, true);
    try {
      const res = await fetch('/api/market/internals');
      const payload = await res.json();
      if (!payload.success) throw new Error(payload.detail || 'Market internals unavailable');
      renderMarketInternals(payload.data);
    } catch (err) {
      console.error(err);
      toast(err.message, 'error');
    } finally {
      toggleLoading(els.marketLoading, false);
    }
  }

  function renderMarketInternals(data) {
    if (!data || !els.marketResults) return;
    const breadth = data.market_breadth || {};
    const regimeDetails = data.regime_details || {};
    const volatility = data.volatility || {};
    const apiUsage = data.api_usage || {};
    const usageRows = Object.entries(apiUsage).map(([name, stats]) => {
      const pct = stats?.percent !== undefined ? `${Number(stats.percent).toFixed(0)}%` : '—';
      return `<span>${name.toUpperCase()} • ${pct} used</span>`;
    }).join('');
    els.marketResults.innerHTML = `
      <div class="summary-card">
        <p class="eyebrow">Market regime</p>
        <h3>${data.regime || 'Unknown'}</h3>
        <p>${regimeDetails.signal || ''} (${regimeDetails.confidence || ''})</p>
      </div>
      <div class="summary-card">
        <p class="eyebrow">SPY</p>
        <h3>$${Number(data.spy_price || 0).toFixed(2)}</h3>
        <p>SMA50 ${Number(data.sma_50 || 0).toFixed(2)} · SMA200 ${Number(data.sma_200 || 0).toFixed(2)}</p>
      </div>
      <div class="summary-card">
        <p class="eyebrow">Breadth</p>
        <p>% > 50EMA: ${Number(breadth.pct_above_50ema || 0).toFixed(1)}%</p>
        <p>% > 200EMA: ${Number(breadth.pct_above_200ema || 0).toFixed(1)}%</p>
        <p>Highs/Lows: ${breadth.new_highs_52w || 0} / ${breadth.new_lows_52w || 0}</p>
      </div>
      <div class="summary-card">
        <p class="eyebrow">Volatility</p>
        <h3>${volatility.vix_level ? Number(volatility.vix_level).toFixed(2) : 'n/a'}</h3>
        <p>${volatility.volatility_status || 'Unknown'}</p>
      </div>
      <div class="summary-card">
        <p class="eyebrow">API usage</p>
        <div class="api-usage">
          ${usageRows || '<span>No usage data</span>'}
        </div>
      </div>`;
  }


  function exportUniverseCsv() {
    if (!state.universeRows.length) {
      toast('Run a universe scan before exporting.', 'error');
      return;
    }
    const headers = ['Ticker', 'Pattern', 'Score', 'RS', 'ATR%', 'Sector', 'Timeframe', 'Entry', 'Stop', 'Target', 'RiskReward'];
    const lines = state.universeRows.map((row) => [
      row.ticker,
      row.pattern || '',
      Number(row.score || 0).toFixed(1),
      row.rs_rating ?? '',
      row.atr_percent ?? '',
      row.sector || '',
      row.timeframe || '',
      row.entry ?? '',
      row.stop ?? '',
      row.target ?? '',
      computeRiskReward(row.entry, row.stop, row.target)
    ]);
    const csv = [headers.join(','), ...lines.map((line) => line.join(','))].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `legend-ai-universe-${Date.now()}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function toggleLoading(el, show) {
    if (!el) return;
    el.classList.toggle('active', Boolean(show));
  }

  async function safeFetch(url, options = {}, { silent = false } = {}) {
    try {
      const response = await fetch(url, options);
      const contentType = response.headers.get('content-type') || '';
      const expectsJson = contentType.includes('application/json');
      const data = expectsJson ? await response.json().catch(() => ({})) : {};
      if (!response.ok) {
        const message = data?.detail || data?.error || `Request failed (${response.status})`;
        throw new Error(message);
      }
      return data;
    } catch (error) {
      console.error('Fetch error:', error);
      if (!silent && error.name !== 'AbortError') {
        toast(error.message || 'Network error occurred', 'error');
      }
      throw error;
    }
  }

  function disableButtonTemporarily(button, busyText = 'Working…') {
    if (!button) return () => {};
    const previous = button.textContent;
    button.disabled = true;
    button.textContent = busyText;
    return () => {
      button.disabled = false;
      button.textContent = previous;
    };
  }

  function toast(message, type = 'info', timeout = 3500) {
    if (!els.toastStack) return;
    const toastEl = document.createElement('div');
    toastEl.className = `toast ${type}`;

    const messageSpan = document.createElement('span');
    messageSpan.textContent = message;
    toastEl.appendChild(messageSpan);

    const closeBtn = document.createElement('button');
    closeBtn.className = 'toast-close';
    closeBtn.setAttribute('aria-label', 'Dismiss notification');
    closeBtn.textContent = '×';
    closeBtn.addEventListener('click', () => toastEl.remove());
    toastEl.appendChild(closeBtn);

    els.toastStack.appendChild(toastEl);
    setTimeout(() => toastEl.remove(), timeout);
  }

  function updateKpiScan() {
    if (!els.kpi.lastScan) return;
    els.kpi.lastScan.textContent = new Date().toLocaleTimeString();
    els.kpi.scanStatus.textContent = 'Live';
    els.kpi.scanStatus.className = 'kpi-status status-healthy';
  }

  async function generateSnapshot(ticker, interval) {
    const symbol = (ticker || '').trim().toUpperCase();
    if (!symbol) return toast('Provide a ticker for snapshots.', 'error');
    const normalizedMap = { '1day': '1D', '1week': '1W', '60min': '60', '15min': '15', '60m': '60', '15m': '15' };
    const apiInterval = normalizedMap[(interval || '').toLowerCase()] || (interval?.toUpperCase() || '1D');
    try {
      const res = await fetch('/api/charts/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker: symbol, interval: apiInterval }),
      });
      const payload = await res.json();
      if (!payload.success) throw new Error(payload.error || 'Snapshot failed');
      window.open(payload.chart_url, '_blank');
    } catch (err) {
      toast(err.message, 'error');
    }
  }

  async function handleMultiTimeframe() {
    const ticker = els.chartTicker.value.trim().toUpperCase();
    if (!ticker) return toast('Enter a ticker for multi-timeframe charts.', 'error');
    els.chartsResults.innerHTML = '<p>Generating multi-timeframe charts…</p>';
    try {
      const res = await fetch('/api/charts/multi', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker, timeframes: ['1day', '1week', '60min'] }),
      });
      const payload = await res.json();
      if (!payload.success) throw new Error(payload.error || 'Multi-timeframe failed');
      const cards = Object.entries(payload.charts || {}).map(([tf, url]) => `
        <article class="result-card">
          <div class="result-header">
            <div class="pattern-type">${tf.toUpperCase()}</div>
          </div>
          <a class="btn btn-secondary" href="${url}" target="_blank" rel="noopener">Open snapshot</a>
        </article>`).join('');
      els.chartsResults.innerHTML = cards || '<p>No charts generated.</p>';
    } catch (err) {
      els.chartsResults.innerHTML = `<p>${err.message}</p>`;
      toast(err.message, 'error');
    }
  }

})();
