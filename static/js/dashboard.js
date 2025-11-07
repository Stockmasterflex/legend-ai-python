/*
 * Legend AI Dashboard Controller
 * Vanilla JS + Alpine hooks powering the cyberpunk UI
 */
(function () {
  window.Dashboard = window.Dashboard || { focusTab: () => {} };
  const state = {
    activeTab: 'scanner',
    currentTicker: 'NVDA',
    currentInterval: '1day',
    tvReady: false,
    tvWidgets: {},
    cacheStats: null,
    universeRows: [],
  };

  const els = {};

  document.addEventListener('DOMContentLoaded', () => {
    cacheDom();
    bindEvents();
    window.Dashboard = { focusTab: (tab) => (state.activeTab = tab) };
    initTradingViewWidgets();
    fetchMarketInternals();
    loadWatchlist();
    setInterval(fetchMarketInternals, 300000);
    // Fetch build version and stamp header
    fetch('/api/version').then(r => r.json()).then(v => {
      const el = document.getElementById('build-version');
      if (el && v && v.commit) el.textContent = `(build ${String(v.commit).slice(0,7)})`;
    }).catch(() => {});
  });

  function cacheDom() {
    els.patternForm = document.getElementById('pattern-form');
    els.patternTicker = document.getElementById('pattern-ticker');
    els.patternInterval = document.getElementById('pattern-interval');
    els.patternResults = document.getElementById('pattern-results');
    els.patternLoading = document.getElementById('pattern-loading');
    els.patternAddWatchlist = document.getElementById('pattern-add-watchlist');
    els.patternSnapshot = document.getElementById('pattern-snapshot');

    els.quickSymbol = document.getElementById('quick-symbol-input');
    els.quickTimeframe = document.getElementById('quick-timeframe');
    els.quickScanBtn = document.getElementById('quick-scan-button');
    els.quickSnapshot = document.getElementById('quick-snapshot');

    els.universeForm = document.getElementById('universe-form');
    els.universeTable = document.getElementById('universe-table');
    els.universeLoading = document.getElementById('universe-loading');

    els.watchlistForm = document.getElementById('watchlist-form');
    els.watchlistList = document.getElementById('watchlist-list');
    els.watchlistEmpty = document.getElementById('watchlist-empty');
    els.watchlistFilter = document.getElementById('watchlist-filter');

    els.marketResults = document.getElementById('market-results');
    els.marketLoading = document.getElementById('market-loading');

    els.chartTicker = document.getElementById('chart-ticker');
    els.chartRefresh = document.getElementById('chart-refresh');
    els.chartMulti = document.getElementById('chart-multi');
    els.chartsResults = document.getElementById('charts-results');

    els.toastStack = document.getElementById('toast-stack');
  }

  function bindEvents() {
    els.patternForm?.addEventListener('submit', handlePatternScan);
    els.quickScanBtn?.addEventListener('click', (e) => {
      e.preventDefault();
      if (els.quickSymbol) {
        els.patternTicker.value = els.quickSymbol.value.trim().toUpperCase();
        els.patternInterval.value = els.quickTimeframe.value;
        handlePatternScan(e);
      }
    });
    els.patternAddWatchlist?.addEventListener('click', addPatternToWatchlist);
    els.patternSnapshot?.addEventListener('click', () => generateSnapshot(els.patternTicker.value, els.patternInterval.value));
    els.quickSnapshot?.addEventListener('click', () => generateSnapshot(els.quickSymbol.value, els.quickTimeframe.value));

    els.universeForm?.addEventListener('submit', handleUniverseScan);
    document.getElementById('universe-export')?.addEventListener('click', exportUniverseCsv);

    els.watchlistForm?.addEventListener('submit', handleWatchlistSubmit);
    els.watchlistFilter?.addEventListener('change', loadWatchlist);

    els.chartRefresh?.addEventListener('click', refreshAdvancedChart);
    els.chartMulti?.addEventListener('click', handleMultiTimeframe);
    document.querySelectorAll('[data-timeframe]')
      .forEach((btn) => btn.addEventListener('click', () => setAdvancedTimeframe(btn.dataset.timeframe)));
  }

  async function handlePatternScan(event) {
    event?.preventDefault();
    const ticker = els.patternTicker.value.trim().toUpperCase();
    const interval = els.patternInterval.value;
    if (!ticker) {
      return toast('Enter a ticker to scan.', 'error');
    }
    state.currentTicker = ticker;
    state.currentInterval = interval;
    toggleLoading(els.patternLoading, true);
    try {
      const tf = interval === '1week' ? 'weekly' : 'daily';
      const res = await fetch(`/api/analyze?ticker=${encodeURIComponent(ticker)}&tf=${tf}`);
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(data?.detail || data?.reason || `Analyze failed (${res.status})`);
      }
      renderAnalyzeIntel(data);
      mountAnalyzeChart(ticker, interval);
      toast(`Analyzed ${ticker}`, 'success');
    } catch (err) {
      console.error(err);
      els.patternResults.innerHTML = `<p style="color:#ef4444;">${err.message}</p>`;
      toast(err.message, 'error');
    } finally {
      toggleLoading(els.patternLoading, false);
    }
  }

  function renderAnalyzeIntel(data) {
    if (!data) return;
    const m = data.patterns?.minervini || { pass: false, failed_rules: [] };
    const w = data.patterns?.weinstein || { stage: 0, reason: '' };
    const p = data.plan || {};
    const scorePct = m.pass ? 80 : 40; // placeholder gauge
    els.patternResults.innerHTML = `
      <article class="result-card">
        <div class="result-header">
          <div>
            <div class="ticker-symbol">${data.ticker}</div>
            <div class="pattern-type">Minervini: ${m.pass ? 'PASS' : 'FAIL'}</div>
          </div>
        </div>
        <div class="score-gauge">
          <div class="gauge-bar"><div class="gauge-fill" style="--score:${scorePct}%"></div></div>
          <div class="score-text">${scorePct}/100</div>
        </div>
        <div class="form-grid">
          <div><div class="kpi-label">Weinstein</div><div>Stage ${w.stage} — ${w.reason || ''}</div></div>
          <div><div class="kpi-label">Entry</div><div>$${Number(p.entry || 0).toFixed(2)}</div></div>
          <div><div class="kpi-label">Stop</div><div>$${Number(p.stop || 0).toFixed(2)}</div></div>
          <div><div class="kpi-label">Target</div><div>$${Number(p.target || 0).toFixed(2)}</div></div>
        </div>
      </article>`;
  }

  function mountAnalyzeChart(ticker, interval) {
    const container = document.getElementById('pattern-chart');
    if (!container) return;
    container.innerHTML = '';
    const resolutionMap = { '1day': 'D', '1week': 'W', '60min': '60', '15min': '15' };
    const reso = resolutionMap[interval] || 'D';
    state.tvWidgets.pattern = new TradingView.widget({
      container_id: 'pattern-chart',
      symbol: `NASDAQ:${ticker}`,
      interval: reso,
      theme: 'dark',
      autosize: true,
      style: '1',
      locale: 'en',
      studies: ['EMA21@tv-basicstudies', 'SMA50@tv-basicstudies', 'RSI@tv-basicstudies', 'Volume@tv-basicstudies'],
      toolbar_bg: '#0b0f14',
      hide_top_toolbar: false,
    });
  }

  async function handleUniverseScan(event) {
    event?.preventDefault();
    const universe = document.getElementById('universe-source').value;
    const limit = Number(document.getElementById('universe-limit').value || 25);
    const minScore = Number(document.getElementById('universe-score').value || 7);
    const minRs = Number(document.getElementById('universe-rs').value || 60);
    toggleLoading(els.universeLoading, true);
    els.universeTable.innerHTML = '';
    try {
      const res = await fetch('/api/universe/scan/quick', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ universe, limit, min_score: minScore, min_rs: minRs }),
      });
      const payload = await res.json();
      if (!payload.success) throw new Error(payload.error || 'Universe scan failed');
      renderUniverseTable(payload.data || []);
    } catch (err) {
      console.error(err);
      toast(err.message, 'error');
      els.universeTable.innerHTML = `<tr><td colspan="6">${err.message}</td></tr>`;
    } finally {
      toggleLoading(els.universeLoading, false);
    }
  }

  function renderUniverseTable(rows) {
    state.universeRows = rows;
    if (!rows.length) {
      els.universeTable.innerHTML = '<tr><td colspan="6">No setups found.</td></tr>';
      return;
    }
    els.universeTable.innerHTML = rows.map((row) => {
      const score = Math.round((row.score || 0) * 10);
      return `
        <tr>
          <td>${row.ticker}</td>
          <td>${row.pattern || '—'}</td>
          <td>${score}</td>
          <td>${row.rs_rating ?? '—'}</td>
          <td>${row.atr_percent ? row.atr_percent.toFixed(2) + '%' : '—'}</td>
          <td>
            <button class="btn btn-ghost" data-watch="${row.ticker}">Watch</button>
            <button class="btn btn-ghost" data-chart="${row.ticker}">Chart</button>
          </td>
        </tr>`;
    }).join('');
    els.universeTable.querySelectorAll('[data-watch]').forEach((btn) => {
      btn.addEventListener('click', () => quickAddWatchlist(btn.dataset.watch));
    });
    els.universeTable.querySelectorAll('[data-chart]').forEach((btn) => {
      btn.addEventListener('click', () => updatePatternChart(btn.dataset.chart, '1day'));
    });
  }

  async function handleWatchlistSubmit(event) {
    event.preventDefault();
    const ticker = document.getElementById('watchlist-symbol').value.trim().toUpperCase();
    const reason = document.getElementById('watchlist-reason').value.trim();
    const tags = document.getElementById('watchlist-tags').value.trim();
    if (!ticker) return toast('Enter a ticker for the watchlist.', 'error');
    try {
      const res = await fetch('/api/watchlist/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker, reason, tags }),
      });
      const payload = await res.json();
      if (!payload.success) throw new Error(payload.detail || 'Unable to add watchlist item');
      event.target.reset();
      toast(`${ticker} added to watchlist`, 'success');
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
      renderWatchlist(payload.items || []);
    } catch (err) {
      console.error(err);
      toast(err.message, 'error');
    }
  }

  function renderWatchlist(items) {
    const filter = els.watchlistFilter.value;
    const filtered = items.filter((item) => filter === 'all' || item.status === filter);
    if (!filtered.length) {
      els.watchlistEmpty.style.display = 'flex';
      els.watchlistList.innerHTML = '';
      return;
    }
    els.watchlistEmpty.style.display = 'none';
    els.watchlistList.innerHTML = filtered.map((item) => `
      <article class="result-card">
        <div class="result-header">
          <div>
            <div class="ticker-symbol">${item.ticker}</div>
            <div class="pattern-type">${item.status}</div>
          </div>
          <button class="btn btn-ghost" data-remove="${item.ticker}">Remove</button>
        </div>
        <p>${item.reason || 'No notes yet.'}</p>
        <small>${new Date(item.added_date || item.added_at || Date.now()).toLocaleString()}</small>
      </article>`).join('');
    els.watchlistList.querySelectorAll('[data-remove]').forEach((btn) => btn.addEventListener('click', () => removeWatchlist(btn.dataset.remove)));
  }

  async function removeWatchlist(ticker) {
    if (!ticker) return;
    await fetch(`/api/watchlist/remove/${ticker}`, { method: 'DELETE' });
    toast(`${ticker} removed`, 'success');
    loadWatchlist();
  }

  async function addPatternToWatchlist() {
    const ticker = els.patternTicker.value.trim().toUpperCase();
    if (!ticker) return toast('Scan a ticker first.', 'error');
    try {
      await fetch('/api/watchlist/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker, reason: 'Pattern scanner' }),
      });
      toast(`${ticker} added to watchlist`, 'success');
      loadWatchlist();
    } catch (err) {
      toast(err.message, 'error');
    }
  }

  function quickAddWatchlist(ticker) {
    fetch('/api/watchlist/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ticker, reason: 'Universe scan' }),
    }).then(() => {
      toast(`${ticker} queued`, 'success');
      loadWatchlist();
    }).catch((err) => toast(err.message, 'error'));
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
    if (!data) return;
    els.marketResults.innerHTML = `
      <article class="result-card">
        <div class="result-header">
          <div>
            <div class="kpi-label">Regime</div>
            <div class="ticker-symbol" style="font-size:1.5rem;">${data.regime}</div>
            <p>${data.regime_details?.signal || ''} (${data.regime_details?.confidence || ''})</p>
          </div>
          <div>
            <div class="kpi-label">SPY</div>
            <div>$${Number(data.spy_price || 0).toFixed(2)}</div>
            <p>SMA50 ${Number(data.sma_50 || 0).toFixed(2)} · SMA200 ${Number(data.sma_200 || 0).toFixed(2)}</p>
          </div>
        </div>
        <div class="form-grid">
          <div>
            <div class="kpi-label">% Above 50 EMA</div>
            <div>${Number(data.market_breadth?.pct_above_50ema || 0).toFixed(1)}%</div>
          </div>
          <div>
            <div class="kpi-label">New Highs</div>
            <div>${data.market_breadth?.new_highs || '—'}</div>
          </div>
          <div>
            <div class="kpi-label">New Lows</div>
            <div>${data.market_breadth?.new_lows || '—'}</div>
          </div>
          <div>
            <div class="kpi-label">VIX</div>
            <div>${Number(data.vix || 0).toFixed(2)}</div>
          </div>
        </div>
      </article>`;
    // KPI chips removed from main UI; keep only the detailed card content.
  }


  function exportUniverseCsv() {
    if (!state.universeRows.length) {
      toast('Run a universe scan before exporting.', 'error');
      return;
    }
    const headers = ['Ticker', 'Pattern', 'Score', 'RS', 'ATR%', 'Entry', 'Target'];
    const lines = state.universeRows.map((row) => [
      row.ticker,
      row.pattern || '',
      Math.round((row.score || 0) * 10),
      row.rs_rating ?? '',
      row.atr_percent ?? '',
      row.entry ?? '',
      row.target ?? ''
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

  function toast(message, type = 'info', timeout = 3500) {
    if (!els.toastStack) return;
    const toastEl = document.createElement('div');
    toastEl.className = `toast ${type}`;
    toastEl.textContent = message;
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

  function refreshAdvancedChart() {
    const ticker = els.chartTicker.value.trim().toUpperCase();
    if (!ticker || !state.tvWidgets.advanced) return;
    state.tvWidgets.advanced.onChartReady(() => {
      state.tvWidgets.advanced.chart().setSymbol(ticker, () => toast(`Chart synced to ${ticker}`, 'success'));
    });
  }

  function setAdvancedTimeframe(resolution) {
    if (!state.tvWidgets.advanced) return;
    state.tvWidgets.advanced.onChartReady(() => {
      state.tvWidgets.advanced.chart().setResolution(resolution, () => toast(`Timeframe → ${resolution}`, 'success'));
    });
  }

  function updatePatternChart(ticker, interval) {
    if (!state.tvWidgets.pattern) return;
    const resolutionMap = { '1day': 'D', '1week': 'W', '60min': '60', '15min': '15' };
    const resolution = resolutionMap[interval] || 'D';
    state.tvWidgets.pattern.onChartReady(() => {
      state.tvWidgets.pattern.chart().setSymbol(ticker, () => {
        state.tvWidgets.pattern.chart().setResolution(resolution);
      });
    });
  }

  function initTradingViewWidgets() {
    if (state.tvReady) return;
    if (!window.TradingView) {
      setTimeout(initTradingViewWidgets, 400);
      return;
    }
    state.tvReady = true;
    state.tvWidgets.tape = new TradingView.widget({
      container_id: 'tv-ticker-tape',
      width: '100%',
      colorTheme: 'dark',
      isTransparent: true,
      autosize: true,
      displayMode: 'regular',
      locale: 'en',
      symbols: [
        { proName: 'FOREXCOM:SPXUSD', title: 'S&P 500' },
        { proName: 'NASDAQ:NDX', title: 'Nasdaq 100' },
        { proName: 'CME_MINI:ES1!', title: 'ES' },
        { proName: 'COMEX:GC1!', title: 'Gold' },
        { proName: 'BITSTAMP:BTCUSD', title: 'BTC' }
      ],
    });
    // Do not mount pattern chart until analyze completes
    if (document.getElementById('tv-advanced-chart')) {
      state.tvWidgets.advanced = new TradingView.widget({
        container_id: 'tv-advanced-chart',
        symbol: 'NASDAQ:NVDA',
        interval: 'D',
        theme: 'dark',
        autosize: true,
        style: '1',
        withdateranges: true,
        hide_side_toolbar: false,
        allow_symbol_change: true,
        locale: 'en',
        studies: ['EMA21@tv-basicstudies', 'EMA50@tv-basicstudies', 'EMA200@tv-basicstudies', 'Volume@tv-basicstudies'],
        toolbar_bg: '#0b0f14',
      });
    }
    state.tvWidgets.heatmap = new TradingView.widget({
      container_id: 'tv-heatmap',
      width: '100%',
      height: 500,
      colorTheme: 'dark',
      isTransparent: false,
      autosize: true,
      locale: 'en',
      dataSource: 'SPX',
      widgetType: 'stock-heatmap',
    });

    if (TradingView.MarketOverviewWidget) {
      state.tvWidgets.marketOverview = new TradingView.MarketOverviewWidget({
        container_id: 'tv-market-overview',
        width: '100%',
        height: 500,
        tabs: [
          {
            title: 'US Indices',
            symbols: [
              { s: 'FOREXCOM:SPXUSD' },
              { s: 'NASDAQ:NDX' },
              { s: 'AMEX:DIA' },
              { s: 'CME_MINI:RTY1!' }
            ],
          },
        ],
        theme: 'dark',
        locale: 'en',
      });
    }

    state.tvWidgets.calendar = new TradingView.widget({
      container_id: 'tv-calendar',
      width: '100%',
      height: 500,
      colorTheme: 'dark',
      isTransparent: false,
      locale: 'en',
      importanceFilter: '-1,0,1',
      currencyFilter: 'USD',
      widgetType: 'economic-calendar',
    });
  }
})();
