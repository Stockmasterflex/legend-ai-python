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
    tvReady: false,
    tvWidgets: {},
    cacheStats: null,
    universeRows: [],
    topSetups: [],
    topSetupsLoaded: false,
    topSetupsRefreshing: false,
  };

  const els = {};

  document.addEventListener('DOMContentLoaded', () => {
    try {
      console.log('Dashboard initializing...');
      cacheDom();
      bindEvents();
      initTabNavigation();
      window.Dashboard = { 
        focusTab: (tab) => switchTab(tab),
        initialized: true
      };
      console.log('Dashboard initialized successfully');
      initTradingViewWidgets();
      fetchMarketInternals();
      loadWatchlist();
      loadTopSetups();
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

    els.topGrid = document.getElementById('top-setups-grid');
    els.topEmpty = document.getElementById('top-setups-empty');
    els.topLoading = document.getElementById('top-setups-loading');
    els.topMeta = document.getElementById('top-setups-meta');
    els.topRefresh = document.getElementById('top-setups-refresh');

    els.marketResults = document.getElementById('market-results');
    els.marketLoading = document.getElementById('market-loading');

    els.chartTicker = document.getElementById('chart-ticker');
    els.chartRefresh = document.getElementById('chart-refresh');
    els.chartMulti = document.getElementById('chart-multi');
    els.chartsResults = document.getElementById('charts-results');

    els.toastStack = document.getElementById('toast-stack');
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
      renderAnalyzeChartImage(data?.chart_url);
      toast(`Analyzed ${ticker}`, 'success');
    } catch (err) {
      console.error('Analyze error:', err);
      const errorMsg = err.message || 'Unknown error occurred';
      if (els.patternResults) {
        els.patternResults.innerHTML = `<p style="color:#ef4444;padding:20px;">Error: ${errorMsg}</p>`;
      }
      toast(errorMsg, 'error');
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

    els.topRefresh?.addEventListener('click', () => loadTopSetups(true));

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
      ? `<a class="btn btn-secondary" href="${data.chart_url}" target="_blank" rel="noopener">Open full snapshot</a>`
      : '<span style="color:var(--color-text-secondary)">Snapshot unavailable</span>';

    els.patternResults.innerHTML = `
      <article class="result-card">
        <div class="result-header">
          <div>
            <div class="ticker-symbol">${data.ticker}</div>
            <div class="pattern-type">${data.timeframe?.toUpperCase() || ''} · ${meta.universe || 'Off-universe'}</div>
            <small>${meta.sector || 'Sector N/A'}</small>
          </div>
          <div>
            ${snapshotLink}
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
          <div class="button-row">
            <button class="btn btn-ghost" data-analyze="${item.ticker}">Analyze Again</button>
            <button class="btn btn-ghost" data-remove="${item.ticker}">Remove</button>
          </div>
        </div>
        <p>${item.reason || 'No notes yet.'}</p>
        ${item.tags ? `<small>Tags: ${item.tags}</small>` : ''}
        <small>${new Date(item.added_date || item.added_at || Date.now()).toLocaleString()}</small>
      </article>`).join('');
    els.watchlistList.querySelectorAll('[data-remove]').forEach((btn) => btn.addEventListener('click', () => removeWatchlist(btn.dataset.remove)));
    els.watchlistList.querySelectorAll('[data-analyze]').forEach((btn) => btn.addEventListener('click', () => {
      const ticker = btn.dataset.analyze;
      if (!ticker) return;
      els.patternTicker.value = ticker;
      const tf = els.patternInterval.value === '1week' ? 'weekly' : 'daily';
      fetchAnalyze(ticker, tf);
    }));
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
    const cards = results.map((item, idx) => {
      const score = Number(item.score || 0).toFixed(1);
      const entry = Number(item.entry || 0).toFixed(2);
      const stop = Number(item.stop || 0).toFixed(2);
      const target = Number(item.target || 0).toFixed(2);
      const riskReward = Number(item.risk_reward || 0).toFixed(2);
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
            <div><div class="kpi-label">Entry</div><div>$${entry}</div></div>
            <div><div class="kpi-label">Stop</div><div>$${stop}</div></div>
            <div><div class="kpi-label">Target</div><div>$${target}</div></div>
          </div>
          <div class="top-card-actions">
            <div>
              <div class="kpi-label">Risk/Reward</div>
              <div>${riskReward}R • ${item.source || 'Universe'}</div>
            </div>
            <div class="top-card-buttons">
              <button class="btn btn-primary" data-open-analyze="${item.ticker}">Open in Analyze</button>
              <button class="btn btn-ghost" data-watch="${item.ticker}">Watchlist</button>
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
      btn.addEventListener('click', () => quickAddWatchlist(btn.dataset.watch));
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
    // Do not mount any TradingView chart by default on Analyze
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
