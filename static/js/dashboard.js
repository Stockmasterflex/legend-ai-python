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

  const TRADINGVIEW_CTORS = {
    'ticker-tape': 'tickerTape',
    'stock-heatmap': 'StockHeatmapWidget',
    'market-overview': 'MarketOverviewWidget',
    'economic-calendar': 'EconomicCalendarWidget',
  };

  const els = {};

  document.addEventListener('DOMContentLoaded', () => {
    cacheDom();
    bindEvents();
    window.Dashboard = { focusTab: (tab) => switchTab(tab) };
    initTradingViewWidgets();
    fetchMarketInternals();
    loadWatchlist();
    setInterval(fetchMarketInternals, 300000);
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
      const res = await fetch(url, { signal: controller.signal });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data?.detail || data?.reason || `Analyze failed (${res.status})`);
      renderAnalyzeIntel(data);
      renderAnalyzeChartImage(data?.chart_url);
      toast(`Analyzed ${ticker}`, 'success');
    } catch (err) {
      console.error(err);
      els.patternResults.innerHTML = `<p style=\"color:#ef4444;\">${err.message}</p>`;
      toast(err.message, 'error');
      renderAnalyzeChartImage(null);
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
    tabs.forEach((btn) => {
      const label = (btn.textContent || '').toLowerCase();
      const isActive = label.includes(tab);
      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-selected', isActive ? 'true' : 'false');
      btn.setAttribute('role', 'tab');
      btn.setAttribute('tabindex', isActive ? '0' : '-1');
      btn.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          btn.click();
        }
      });
    });
    Object.entries(panes).forEach(([key, el]) => {
      if (!el) return;
      const on = key === tab;
      el.style.display = on ? '' : 'none';
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
      renderAnalyzeChartImage(data);
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
    const m = data.patterns?.minervini || { passed: false, failed_rules: [] };
    const w = data.patterns?.weinstein || { stage: 0, reason: '' };
    const vcp = data.patterns?.vcp || { detected: false, score: 0 };
    const p = data.plan || {};
    const minPass = !!(m.passed ?? m.pass);
    const scoreMeta = computeAnalyzeScore({
      minPass,
      failedRules: m.failed_rules || [],
      stage: Number(w.stage || 0),
      vcpScore: Number(vcp.score || 0),
      vcpDetected: Boolean(vcp.detected),
      dist21: Math.abs(d21),
      riskMultiple: Number(rmult || 0),
    });
    const grade = describeScoreGrade(scoreMeta.total);

    const lastRow = (data.ohlcv && data.ohlcv.length) ? data.ohlcv[data.ohlcv.length - 1] : {};
    const lastC = Number(lastRow?.c || 0);
    const ema21Last = Number((data.indicators?.ema21 || []).slice(-1)[0] || 0);
    const sma50Last = Number((data.indicators?.sma50 || []).slice(-1)[0] || 0);
    const d21 = ema21Last ? ((lastC - ema21Last) / ema21Last) * 100 : 0;
    const d50 = sma50Last ? ((lastC - sma50Last) / sma50Last) * 100 : 0;
    const rmult = Number(p.risk_r || 0);

    const failed = (m.failed_rules || []).slice(0, 5).join(', ');

    const snapshotLink = typeof data.chart_url === 'string' && data.chart_url.length > 0
      ? `<a class="btn btn-secondary" href="${data.chart_url}" target="_blank" rel="noopener">Open full snapshot</a>`
      : '<span style="color:var(--color-text-secondary)">Snapshot unavailable</span>';

    els.patternResults.innerHTML = `
      <article class="result-card">
        <div class="result-header">
          <div>
            <div class="ticker-symbol">${data.ticker}</div>
            <div class="pattern-type">Minervini: ${minPass ? 'PASS' : 'FAIL'}</div>
          </div>
          <div>
            ${snapshotLink}
          </div>
        </div>
        <div class="score-gauge">
          <div class="gauge-bar"><div class="gauge-fill" style="--score:${scoreMeta.total}%"></div></div>
          <div class="score-meta">
            <div class="score-text">${scoreMeta.total}/100</div>
            <span class="badge ${grade.badge}">${grade.label}</span>
            <p class="score-caption">${grade.description}</p>
          </div>
        </div>
        <ul class="score-breakdown">
          ${scoreMeta.breakdown.map((item) => `<li><span>${item.label}</span><strong>${item.points} pts</strong></li>`).join('')}
        </ul>
        <div class="form-grid">
          <div><div class="kpi-label">Weinstein</div><div>Stage ${w.stage} — ${w.reason || ''}</div></div>
          <div><div class="kpi-label">VCP</div><div>${vcp.detected ? 'Yes' : 'No'} · score ${Number(vcp.score || 0).toFixed(1)}</div></div>
          <div><div class="kpi-label">Dist to 21EMA</div><div>${d21 >= 0 ? '+' : ''}${d21.toFixed(2)}%</div></div>
          <div><div class="kpi-label">Dist to 50SMA</div><div>${d50 >= 0 ? '+' : ''}${d50.toFixed(2)}%</div></div>
          <div><div class="kpi-label">R Multiple</div><div>${rmult.toFixed(2)}R</div></div>
          <div><div class="kpi-label">Entry</div><div>$${Number(p.entry || 0).toFixed(2)}</div></div>
          <div><div class="kpi-label">Stop</div><div>$${Number(p.stop || 0).toFixed(2)}</div></div>
          <div><div class="kpi-label">Target</div><div>$${Number(p.target || 0).toFixed(2)}</div></div>
        </div>
        ${failed ? `<p style="margin-top:8px;color:var(--color-text-secondary)">Failed: ${failed}</p>` : ''}
      </article>`;
  }

// Render analyze chart image (server-provided chart_url). No client-side secrets.
function renderAnalyzeChartImage(url) {
    const container = document.getElementById('analyze-chart');
    if (!container) return;
    container.innerHTML = '';
    if (typeof url === 'string' && url.length > 0) {
      const link = document.createElement('a');
      link.href = url;
      link.target = '_blank';
      link.rel = 'noopener';
      link.style.display = 'block';
      link.style.background = '#0b0f14';
      link.style.borderRadius = '8px';
      const img = document.createElement('img');
      img.src = url;
      img.alt = 'Analyze snapshot';
      img.style.display = 'block';
      img.style.width = '100%';
      img.style.height = 'auto';
      img.loading = 'lazy';
      link.appendChild(img);
      container.appendChild(link);
    } else {
      const p = document.createElement('p');
      p.textContent = 'Chart snapshot unavailable';
      p.style.color = 'var(--color-text-secondary)';
      container.appendChild(p);
    }
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
      renderMarketInternals(payload.data, { cached: payload.cached, ttl: payload.cache_ttl_seconds });
    } catch (err) {
      console.error(err);
      toast(err.message, 'error');
    } finally {
      toggleLoading(els.marketLoading, false);
    }
  }

  function renderMarketInternals(data, meta = {}) {
    if (!data) return;
    const breadth = data.market_breadth || {};
    const vol = data.volatility || {};
    const apiUsage = data.api_usage || {};
    const timestamp = data.timestamp ? new Date(data.timestamp).toLocaleString() : '';
    const advDecline = `${breadth.advances ?? '—'} adv / ${breadth.declines ?? '—'} dec`;
    const advRatio = Number.isFinite(breadth.advance_decline_ratio)
      ? `${Number(breadth.advance_decline_ratio).toFixed(1)}% adv rate`
      : 'Advance/decline sample';
    const cacheLabel = meta.cached ? 'HIT' : 'LIVE';
    const ttlLabel = meta.ttl ? `${Math.round(meta.ttl / 60)}m ttl` : '—';
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
        <p class="kpi-detail">Last updated ${timestamp || 'recently'} · sample ${breadth.sample_size ?? '—'} tickers</p>
      </article>
      <article class="result-card">
        <div class="result-header">
          <div>
            <div class="kpi-label">Breadth snapshot</div>
            <div class="ticker-symbol" style="font-size:1.25rem;">${advDecline}</div>
            <p>${advRatio}</p>
          </div>
          <div>
            <div class="kpi-label">% Above MAs</div>
            <div>${Number(breadth.pct_above_50ema ?? 0).toFixed(1)}% / ${Number(breadth.pct_above_200ema ?? 0).toFixed(1)}%</div>
            <p>50 EMA / 200 EMA</p>
          </div>
        </div>
        <div class="form-grid">
          <div>
            <div class="kpi-label">52W Highs</div>
            <div>${breadth.new_highs_52w ?? '—'}</div>
          </div>
          <div>
            <div class="kpi-label">52W Lows</div>
            <div>${breadth.new_lows_52w ?? '—'}</div>
          </div>
          <div>
            <div class="kpi-label">Advances</div>
            <div>${breadth.advances ?? '—'}</div>
          </div>
          <div>
            <div class="kpi-label">Declines</div>
            <div>${breadth.declines ?? '—'}</div>
          </div>
        </div>
      </article>
      <article class="result-card">
        <div class="result-header">
          <div>
            <div class="kpi-label">Volatility</div>
            <div class="ticker-symbol" style="font-size:1.25rem;">${vol.vix_level ? Number(vol.vix_level).toFixed(2) : '—'}</div>
            <p>${vol.volatility_status || 'Unknown'}</p>
          </div>
          <div>
            <div class="kpi-label">API usage</div>
            <div>${apiUsage.status || '—'}</div>
            <p>${apiUsage.requests_remaining ? `${apiUsage.requests_remaining} calls left` : ''}</p>
          </div>
        </div>
        <div class="form-grid">
          <div>
            <div class="kpi-label">Cache</div>
            <div>${cacheLabel} (${ttlLabel})</div>
          </div>
          <div>
            <div class="kpi-label">Notes</div>
            <div>${vol.success === false ? 'VIX fallback' : 'Healthy'}</div>
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
    waitForTradingView(() => {
      if (state.tvReady) return;
      state.tvReady = true;
      state.tvWidgets.tape = mountTradingViewWidget('ticker-tape', {
        container_id: 'tv-ticker-tape',
        symbols: [
          { proName: 'FOREXCOM:SPXUSD', title: 'S&P 500' },
          { proName: 'NASDAQ:NDX', title: 'Nasdaq 100' },
          { proName: 'CME_MINI:ES1!', title: 'ES' },
          { proName: 'COMEX:GC1!', title: 'Gold' },
          { proName: 'BITSTAMP:BTCUSD', title: 'BTC' }
        ],
        showSymbolLogo: true,
        displayMode: 'regular',
        isTransparent: true,
      });
      // Do not mount any TradingView chart by default on Analyze
      state.tvWidgets.heatmap = mountTradingViewWidget('stock-heatmap', {
        container_id: 'tv-heatmap',
        height: 520,
        dataSource: 'SPX',
      });

      state.tvWidgets.marketOverview = mountTradingViewWidget('market-overview', {
        container_id: 'tv-market-overview',
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
          {
            title: 'Futures',
            symbols: [
              { s: 'CME_MINI:ES1!' },
              { s: 'CME_MINI:NQ1!' },
              { s: 'NYMEX:CL1!' },
              { s: 'COMEX:GC1!' }
            ],
          },
        ],
      });

      state.tvWidgets.calendar = mountTradingViewWidget('economic-calendar', {
        container_id: 'tv-calendar',
        height: 520,
        importanceFilter: '-1,0,1',
        currencyFilter: 'USD',
      });
    });
  }

  function waitForTradingView(callback, attempt = 0) {
    if (window.TradingView && typeof window.TradingView === 'object') {
      callback();
      return;
    }
    if (attempt > 25) {
      console.warn('TradingView never became available; skipping widget mount.');
      return;
    }
    setTimeout(() => waitForTradingView(callback, attempt + 1), 250);
  }

  function mountTradingViewWidget(type, options) {
    if (!options?.container_id) {
      console.warn('Missing container for TradingView widget', type);
      return null;
    }
    const defaults = {
      autosize: true,
      width: '100%',
      colorTheme: 'dark',
      isTransparent: false,
      locale: 'en',
      ...options,
    };
    const ctorName = TRADINGVIEW_CTORS[type];
    if (!ctorName) {
      console.warn('Unknown TradingView widget type', type);
      return null;
    }
    const ctor = ctorName === 'widget' ? window.TradingView.widget : window.TradingView[ctorName];
    if (typeof ctor !== 'function') {
      console.warn('TradingView constructor unavailable for', type);
      showTradingViewFallback(options.container_id);
      return null;
    }
    try {
      return new ctor(defaults);
    } catch (err) {
      console.error('TradingView mount failed', type, err);
      showTradingViewFallback(options.container_id);
      return null;
    }
  }

  function showTradingViewFallback(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;
    el.innerHTML = '<p class="tv-fallback">TradingView widget unavailable</p>';
  }

  function computeAnalyzeScore({ minPass, failedRules, stage, vcpScore, vcpDetected, dist21, riskMultiple }) {
    const trendScore = minPass ? 40 : Math.max(0, 40 - (failedRules.length * 5));
    const stageScore = stage === 2 ? 25 : stage === 1 ? 18 : stage === 3 ? 10 : stage === 4 ? 4 : 8;
    const vcpPoints = vcpDetected ? Math.min(20, (Math.max(vcpScore, 0) / 10) * 20) : Math.min(10, (Math.max(vcpScore, 0) / 10) * 10);
    const baseDist = Math.abs(dist21 || 0);
    const distScore = baseDist <= 2 ? 10 : baseDist <= 5 ? 6 : baseDist <= 8 ? 3 : 0;
    const riskScore = riskMultiple >= 2 ? 5 : riskMultiple >= 1.5 ? 3 : riskMultiple > 1 ? 1 : 0;
    const breakdown = [
      { label: 'Trend template', points: Math.round(trendScore) },
      { label: 'Weinstein stage', points: Math.round(stageScore) },
      { label: 'VCP signal', points: Math.round(vcpPoints) },
      { label: 'Distance to 21EMA', points: distScore },
      { label: 'Risk / Reward', points: riskScore },
    ];
    const total = Math.max(0, Math.min(100, breakdown.reduce((sum, item) => sum + item.points, 0)));
    return { total, breakdown };
  }

  function describeScoreGrade(score) {
    if (score >= 90) return { label: 'A+', badge: 'success', description: 'Institutional-grade setup' };
    if (score >= 80) return { label: 'A', badge: 'success', description: 'Strong trend alignment' };
    if (score >= 70) return { label: 'B', badge: 'warning', description: 'Constructive but monitor volume' };
    if (score >= 60) return { label: 'C', badge: 'warning', description: 'Needs better trend evidence' };
    return { label: 'D', badge: 'error', description: 'High risk – fails most rules' };
  }
})();
