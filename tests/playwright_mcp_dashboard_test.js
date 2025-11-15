const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function run() {
  const dashboardUrl = process.env.DASHBOARD_URL || 'https://legend-ai-python-production.up.railway.app/dashboard';
  const quickSymbol = process.env.DASHBOARD_SYMBOL || 'NVDA';
  const screenshotDir = path.join('screenshots', 'playwright-mcp');
  fs.mkdirSync(screenshotDir, { recursive: true });

  const consoleMessages = [];
  const pageErrors = [];
  const requestFailures = [];
  const stepLog = [];
  let stepCounter = 0;

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const page = await context.newPage();

  page.on('console', (msg) => {
    const entry = { type: msg.type(), text: msg.text() };
    consoleMessages.push(entry);
    console.log(`[console:${entry.type}] ${entry.text}`);
  });

  page.on('pageerror', (error) => {
    pageErrors.push(error.message);
    console.log(`[pageerror] ${error.message}`);
  });

  page.on('requestfailed', (request) => {
    const failure = request.failure();
    requestFailures.push({ url: request.url(), method: request.method(), error: failure?.errorText });
    console.log(`[requestfailed] ${request.method()} ${request.url()} :: ${failure?.errorText}`);
  });

  const recordStep = async (label, description) => {
    stepCounter += 1;
    const fileName = `step-${String(stepCounter).padStart(2, '0')}-${label}.png`;
    const filePath = path.join(screenshotDir, fileName);
    await page.screenshot({ path: filePath, fullPage: true });
    stepLog.push({ order: stepCounter, label, description, screenshot: filePath });
    console.log(`📸 Step ${stepCounter}: ${description} -> ${filePath}`);
    return filePath;
  };

  const runAnalyzeScenario = async (symbol, intervalValue, label) => {
    try {
      console.log(`Analyzing ${symbol} on ${intervalValue}…`);
      await page.fill('#pattern-ticker', symbol);
      await page.selectOption('#pattern-interval', intervalValue);
      await Promise.all([
        page.waitForResponse((response) => response.url().includes('/api/analyze') && response.request().method() === 'GET', { timeout: 60000 }).catch(() => null),
        page.click('#pattern-form button[type="submit"]'),
      ]);
      await page.waitForSelector('#pattern-results .result-card', { timeout: 30000 });
      await page.waitForSelector('#analyze-chart img', { timeout: 30000 });
      await recordStep(`analyze-${label}`, `Analyze ${symbol} (${intervalValue}) rendered chart + intel`);
    } catch (error) {
      console.log(`Analyze flow failed for ${symbol}: ${error.message}`);
    }
  };

  const summary = {
    url: dashboardUrl,
    consoleInitMessage: false,
    libs: { alpine: false, dashboard: false, initialized: false },
    tabs: [],
    quickScan: { symbol: quickSymbol, status: 'not-run' },
    screenshots: stepLog,
  };

  try {
    console.log('Navigating to dashboard…');
    await page.goto(dashboardUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(2000);
    await recordStep('dashboard-loaded', 'Dashboard loaded with hero + tabs visible');

    console.log('Waiting for initialization console message…');
    await page.waitForTimeout(2000);
    summary.consoleInitMessage = consoleMessages.some((entry) => entry.text.includes('Dashboard initialized successfully'));
    await recordStep('console-check', 'Post-load state while monitoring console logs');

    const libs = await page.evaluate(() => ({
      hasAlpine: typeof window.Alpine !== 'undefined',
      hasDashboard: typeof window.Dashboard !== 'undefined',
      dashboardInitialized: !!(window.Dashboard && window.Dashboard.initialized),
    }));
    summary.libs = {
      alpine: libs.hasAlpine,
      dashboard: libs.hasDashboard,
      initialized: libs.dashboardInitialized,
    };
    console.log('Library presence:', summary.libs);
    await recordStep('library-check', 'State after verifying Alpine/Dashboard availability');

    const tabs = [
      { name: 'Analyze', selector: 'button.tab-button:has-text("Analyze")', key: 'analyze' },
      { name: 'Pattern Scanner', selector: 'button.tab-button:has-text("Pattern Scanner")', key: 'scanner' },
      { name: 'Top Setups', selector: 'button.tab-button:has-text("Top Setups")', key: 'top' },
      { name: 'Market Internals', selector: 'button.tab-button:has-text("Market Internals")', key: 'internals' },
      { name: 'Watchlist', selector: 'button.tab-button:has-text("Watchlist")', key: 'watchlist' },
    ];

    for (const tab of tabs) {
      console.log(`Switching to ${tab.name} tab…`);
      let tabResult = { name: tab.name, success: false, error: null };
      try {
        await page.click(tab.selector, { timeout: 5000 });
        await page.waitForTimeout(1500);
        await recordStep(`tab-${tab.key}`, `${tab.name} tab after click`);
        if (tab.key === 'internals') {
          await Promise.all([
            page.waitForSelector('#tv-heatmap iframe', { timeout: 15000 }).catch(() => null),
            page.waitForSelector('#tv-market-overview iframe', { timeout: 15000 }).catch(() => null),
          ]);
        }
        tabResult.success = true;
      } catch (error) {
        tabResult.error = error.message;
        console.log(`Failed to click ${tab.name}: ${error.message}`);
      }
      summary.tabs.push(tabResult);
    }

    console.log('Returning to Analyze tab…');
    try {
      await page.click('button.tab-button:has-text("Analyze")', { timeout: 5000 });
      await page.waitForTimeout(1000);
      await recordStep('return-analyze', 'Analyze tab re-focused');
    } catch (error) {
      console.log(`Failed to return to Analyze tab: ${error.message}`);
    }

    console.log('Running additional analyze flows (NVDA/IBM/AAPL)…');
    await runAnalyzeScenario('NVDA', '1day', 'nvda-daily');
    await runAnalyzeScenario('IBM', '1day', 'ibm-daily');
    await runAnalyzeScenario('AAPL', '1week', 'aapl-weekly');

    console.log(`Filling Quick Symbol input with ${quickSymbol}…`);
    try {
      await page.click('#quick-symbol-input', { timeout: 5000 });
      await page.fill('#quick-symbol-input', '');
      await page.fill('#quick-symbol-input', quickSymbol);
      await recordStep('quick-symbol-entry', `Quick Symbol set to ${quickSymbol}`);
    } catch (error) {
      console.log(`Unable to fill Quick Symbol input: ${error.message}`);
      summary.quickScan.status = 'input-error';
      summary.quickScan.error = error.message;
    }

    console.log('Clicking Scan button…');
    let responseData = null;
    let responseStatus = null;
    let apiError = null;
    if (summary.quickScan.status !== 'input-error') {
      try {
        const [apiResponse] = await Promise.all([
          page.waitForResponse(
            (response) => {
              const url = response.url();
              return url.includes('/api/analyze') && url.includes(`ticker=${encodeURIComponent(quickSymbol)}`);
            },
            { timeout: 20000 }
          ).catch((error) => {
            apiError = error.message;
            return null;
          }),
          (async () => {
            await page.click('#quick-scan-button', { timeout: 5000 });
            await recordStep('quick-scan-click', 'Scan button pressed');
          })(),
        ]);

        if (apiResponse) {
          responseStatus = apiResponse.status();
          try {
            responseData = await apiResponse.json();
          } catch (jsonError) {
            apiError = `Response JSON parse failed: ${jsonError.message}`;
          }
        }

        const resultLocator = page.locator('#pattern-results .result-card');
        await resultLocator.waitFor({ timeout: 20000 }).catch(() => {});
        await recordStep('quick-scan-results', 'Analyze tab after API response');
      } catch (error) {
        apiError = error.message;
      }

      summary.quickScan.status = apiError ? 'api-error' : 'completed';
      summary.quickScan.responseStatus = responseStatus;
      summary.quickScan.error = apiError;
      if (responseData) {
        summary.quickScan.responseKeys = Object.keys(responseData || {});
        summary.quickScan.resultTicker = responseData?.ticker;
      }
    }

    console.log('Running Pattern Scanner end-to-end…');
    try {
      await page.click('button.tab-button:has-text("Pattern Scanner")', { timeout: 5000 });
      await page.selectOption('#universe-source', 'nasdaq100');
      await page.selectOption('#scanner-timeframe', '1day');
      await page.fill('#universe-limit', '45');
      await page.selectOption('#scanner-patterns', ['VCP', 'Flat Base']);
      await page.click('#universe-form button[type="submit"]');
      // `#universe-table` is already the `<tbody>` node, so we wait directly for rows
      await page.waitForSelector('#universe-table tr', { timeout: 60000 });
      const scannerRows = await page.locator('#universe-table tr').count();
      if (scannerRows === 0) {
        await page.waitForSelector('#universe-table td:has-text("No setups found")', { timeout: 5000 }).catch(() => {});
      }
      await recordStep('scanner-results', 'Pattern scanner results grid');
      const previewBtn = await page.$('[data-scan-chart]');
      if (previewBtn) {
        await previewBtn.click();
        await page.waitForTimeout(2000);
        await recordStep('scanner-preview', 'Scanner preview chart rendered');
      }

      // Rising wedge specific scan
      await page.evaluate(() => {
        const select = document.getElementById('scanner-patterns');
        if (select) {
          Array.from(select.options).forEach((opt) => {
            opt.selected = false;
          });
        }
      });
      await page.selectOption('#scanner-patterns', ['Rising Wedge']);
      await page.click('#universe-form button[type="submit"]');
      await page.waitForSelector('#universe-table tr, #universe-table td', { timeout: 60000 });
      await recordStep('scanner-wedge', 'Scanner filtered to Rising Wedge');

      // Mixed pattern scan
      await page.evaluate(() => {
        const select = document.getElementById('scanner-patterns');
        if (select) {
          Array.from(select.options).forEach((opt) => {
            opt.selected = false;
          });
        }
      });
      await page.selectOption('#scanner-patterns', ['VCP', '21 EMA Pullback', 'Ascending Triangle']);
      await page.click('#universe-form button[type="submit"]');
      await page.waitForSelector('#universe-table tr, #universe-table td', { timeout: 60000 });
      await recordStep('scanner-mix', 'Scanner using VCP + 21 EMA Pullback + Ascending Triangle');
    } catch (error) {
      console.log(`Pattern scanner check failed: ${error.message}`);
    }

    console.log('Validating Top Setups preview chart…');
    try {
      await page.click('button.tab-button:has-text("Top Setups")', { timeout: 5000 });
      await page.waitForTimeout(2000);
      await page.click('#top-setups-refresh', { timeout: 5000 }).catch(() => {});
      await page.waitForTimeout(3000);
      const analyzeButton = await page.$('[data-open-analyze]');
      if (analyzeButton) {
        const ticker = await analyzeButton.getAttribute('data-open-analyze');
        await analyzeButton.click();
        await page.waitForSelector('#pattern-results .result-card', { timeout: 20000 });
        await recordStep('top-analyze', `Analyze triggered from Top Setups (${ticker})`);
        await page.click('button.tab-button:has-text("Top Setups")', { timeout: 5000 });
        await page.waitForTimeout(1500);
      }
      const watchBtn = await page.$('[data-watch]');
      if (watchBtn) {
        await watchBtn.click();
        await page.waitForTimeout(1000);
      }
      const topPreviewBtn = await page.$('[data-top-chart]');
      if (topPreviewBtn) {
        await topPreviewBtn.click();
        await page.waitForTimeout(2000);
        await recordStep('top-preview', 'Top setups preview chart');
      }
      const entryValueText = await page.locator('.top-plan-value').first().textContent();
      if (entryValueText && entryValueText.includes('\n')) {
        throw new Error('Top setups tile value wraps to multiple lines');
      }
    } catch (error) {
      console.log(`Top setups preview failed: ${error.message}`);
    }

    console.log('Exercising Watchlist CRUD…');
    try {
      await page.click('button.tab-button:has-text("Watchlist")', { timeout: 5000 });
      await page.waitForSelector('#watchlist-form', { timeout: 5000, state: 'visible' });
      await page.fill('#watchlist-symbol', 'AAPL');
      await page.selectOption('#watchlist-status', 'Watching');
      await page.fill('#watchlist-reason', 'Playwright auto test');
      const tagToggleExists = await page.$('#watchlist-tags [data-tag="Breakout"]');
      if (tagToggleExists) {
        await page.click('#watchlist-tags [data-tag="Breakout"]');
        await page.click('#watchlist-tags [data-tag="Reclaim of 21 EMA"]');
      } else {
        await page.selectOption('#watchlist-tags', ['Breakout', 'Momentum']).catch(() => {});
      }
      await page.click('#watchlist-form button[type="submit"]');
      await page.waitForSelector('#watchlist-list tr', { timeout: 10000 });
      await recordStep('watchlist-after-add', 'Watchlist after adding AAPL');
      const editBtn = await page.$('[data-edit="AAPL"]');
      if (editBtn) {
        await editBtn.click();
        await page.fill('#watchlist-reason', 'Playwright edit ready');
        await page.selectOption('#watchlist-status', 'Triggered').catch(() => {});
        if (tagToggleExists) {
          await page.click('#watchlist-tags [data-tag="Breakout"]');
          await page.click('#watchlist-tags [data-tag="Reclaim of 21 EMA"]');
          await page.click('#watchlist-tags [data-tag="Leader"]');
          await page.click('#watchlist-tags [data-tag="Late-stage base"]');
        } else {
          await page.selectOption('#watchlist-tags', ['Leader', 'Late-stage base']).catch(() => {});
        }
        await page.click('#watchlist-form button[type="submit"]');
        await page.waitForSelector('#watchlist-list tr', { timeout: 10000 });
        await recordStep('watchlist-after-edit', 'Watchlist after editing AAPL');
        const reasonCell = await page.textContent('#watchlist-list tr td:nth-child(3)');
        if (!reasonCell || !reasonCell.includes('Playwright edit ready')) {
          throw new Error('Watchlist edit did not persist updated notes');
        }
      }
      const tagFilterToggle = await page.$('#watchlist-tag-filter [data-tag="Leader"]');
      if (tagFilterToggle) {
        await tagFilterToggle.click();
        await page.waitForTimeout(1500);
        await recordStep('watchlist-filtered', 'Watchlist filtered by Leader tag');
        await tagFilterToggle.click();
      } else {
        await page.selectOption('#watchlist-tag-filter', ['Leader']).catch(() => {});
        await page.waitForTimeout(1500);
        await recordStep('watchlist-filtered', 'Watchlist filtered by Leader tag');
        await page.selectOption('#watchlist-tag-filter', []).catch(() => {});
      }
      if (await page.$('[data-tv-link="AAPL"]')) {
        const [tvPage] = await Promise.all([
          context.waitForEvent('page'),
          page.click('[data-tv-link="AAPL"]')
        ]);
        await tvPage.waitForLoadState('domcontentloaded');
        await tvPage.waitForSelector('[data-testid="tv-lab-advanced-chart"]', { timeout: 30000 }).catch(() => {});
        await tvPage.close();
      }
      const removeBtn = await page.$('[data-remove="AAPL"]');
      if (removeBtn) {
        await removeBtn.click();
        await page.waitForTimeout(1500);
        await recordStep('watchlist-after-remove', 'Watchlist after removing AAPL');
      }
    } catch (error) {
      console.log(`Watchlist test failed: ${error.message}`);
    }

    console.log('Playwright MCP style test complete.');
    console.log('Summary:', JSON.stringify(summary, null, 2));
  } catch (error) {
    console.error('Test failed:', error);
    summary.error = error.message;
  } finally {
    await browser.close();
  }

  return { summary, consoleMessages, pageErrors, requestFailures, steps: stepLog };
}

run()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error('Unhandled test error:', error);
    process.exit(1);
  });
