#!/usr/bin/env node
/**
 * Comprehensive E2E Test for All Dashboard Improvements
 * Tests: Charts, Pattern Scanner, Top Setups, Watchlist, Market Internals
 */

const { chromium } = require('playwright');
const fs = require('fs');

// Create screenshots directory
if (!fs.existsSync('screenshots')) {
  fs.mkdirSync('screenshots');
}

async function testAllImprovements() {
  console.log('🚀 Starting Comprehensive Dashboard E2E Tests\n');
  console.log('='.repeat(60));

  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

  // Capture console messages and errors
  const consoleMessages = [];
  page.on('console', msg => {
    const message = `${msg.type()}: ${msg.text()}`;
    consoleMessages.push(message);
    if (msg.type() === 'error') {
      console.log(`❌ Console Error: ${msg.text()}`);
    }
  });
  page.on('pageerror', err => console.log(`❌ Page Error: ${err.message}`));

  try {
    // ===================================================================
    // TEST 1: Navigate and Check Page Load
    // ===================================================================
    console.log('\n📍 TEST 1: Page Load and Initialization');
    console.log('-'.repeat(60));

    await page.goto('https://legend-ai-python-production.up.railway.app/dashboard', {
      waitUntil: 'domcontentloaded'
    });
    await page.waitForTimeout(3000);
    await page.screenshot({ path: 'screenshots/00-dashboard-loaded.png', fullPage: true });
    console.log('✅ Dashboard loaded successfully');

    // ===================================================================
    // TEST 2: Analyze Tab - Chart Rendering & Size
    // ===================================================================
    console.log('\n📍 TEST 2: Analyze Tab - Charts Working & Larger Size');
    console.log('-'.repeat(60));

    // Fill in ticker and analyze
    await page.fill('#pattern-ticker', 'NVDA');
    await page.selectOption('#pattern-interval', '1day');
    console.log('   Filled NVDA ticker...');

    await page.click('#pattern-form button[type="submit"]');
    console.log('   Clicked Analyze button...');

    // Wait for results
    await page.waitForTimeout(8000);

    // Check if chart appeared
    const chartImg = await page.$('#analyze-chart img');
    if (chartImg) {
      const chartSrc = await chartImg.getAttribute('src');
      console.log(`   ✅ Chart rendered! URL: ${chartSrc?.substring(0, 50)}...`);

      // Check chart size
      const box = await chartImg.boundingBox();
      if (box) {
        console.log(`   ✅ Chart dimensions: ${Math.round(box.width)}x${Math.round(box.height)}px`);
        if (box.height >= 450) {
          console.log(`   ✅ Chart height meets requirement (≥450px)`);
        } else {
          console.log(`   ⚠️  Chart height smaller than expected: ${Math.round(box.height)}px`);
        }
      }
    } else {
      console.log('   ❌ No chart image found');
    }

    await page.screenshot({ path: 'screenshots/01-analyze-with-chart.png', fullPage: true });
    console.log('   ✅ Screenshot saved: analyze-with-chart.png');

    // ===================================================================
    // TEST 3: Pattern Scanner - New Patterns Added
    // ===================================================================
    console.log('\n📍 TEST 3: Pattern Scanner - Verify New Patterns');
    console.log('-'.repeat(60));

    await page.click('button[data-tab-target="scanner"]');
    await page.waitForTimeout(1000);

    // Check pattern dropdown
    const patternOptions = await page.$$eval('#scanner-patterns option', options =>
      options.map(opt => opt.textContent)
    );

    console.log(`   Found ${patternOptions.length} pattern options:`);
    const expectedPatterns = [
      'Rising Wedge',
      'Falling Wedge',
      'Ascending Triangle',
      'Symmetrical Triangle',
      'Head & Shoulders',
      'Inverse Head & Shoulders',
      'Pullback to 21 EMA',
      'Pullback to 50 SMA'
    ];

    let foundCount = 0;
    expectedPatterns.forEach(pattern => {
      const found = patternOptions.some(opt => opt.includes(pattern.replace(' & ', ' &amp; ')));
      if (found) {
        console.log(`   ✅ ${pattern}`);
        foundCount++;
      } else {
        console.log(`   ❌ Missing: ${pattern}`);
      }
    });

    if (foundCount === expectedPatterns.length) {
      console.log(`   ✅ All ${expectedPatterns.length} new patterns added!`);
    } else {
      console.log(`   ⚠️  Only ${foundCount}/${expectedPatterns.length} patterns found`);
    }

    await page.screenshot({ path: 'screenshots/02-scanner-patterns.png', fullPage: true });

    // ===================================================================
    // TEST 4: Top Setups Tab
    // ===================================================================
    console.log('\n📍 TEST 4: Top Setups - Verify Layout');
    console.log('-'.repeat(60));

    await page.click('button[data-tab-target="top"]');
    await page.waitForTimeout(2000);

    // Check if refresh button exists
    const refreshBtn = await page.$('#top-setups-refresh');
    if (refreshBtn) {
      console.log('   ✅ Refresh button present');
      await refreshBtn.click();
      console.log('   Clicked refresh...');
      await page.waitForTimeout(5000);
    }

    // Check for setup cards
    const setupCards = await page.$$('.top-setup-card');
    console.log(`   Found ${setupCards.length} setup cards`);

    if (setupCards.length > 0) {
      // Check for Preview chart button
      const previewBtn = await page.$('[data-top-chart]');
      if (previewBtn) {
        console.log('   ✅ Preview chart button exists');
      }
    }

    await page.screenshot({ path: 'screenshots/03-top-setups.png', fullPage: true });

    // ===================================================================
    // TEST 5: Watchlist Tab - CRUD Features
    // ===================================================================
    console.log('\n📍 TEST 5: Watchlist - CRUD Operations');
    console.log('-'.repeat(60));

    await page.click('button[data-tab-target="watchlist"]');
    await page.waitForTimeout(1000);

    // Add a test item
    await page.fill('#watchlist-symbol', 'AAPL');
    await page.fill('#watchlist-reason', 'E2E Test Setup');
    await page.fill('#watchlist-tags', 'Test, Automation');
    await page.click('#watchlist-form button[type="submit"]');
    await page.waitForTimeout(2000);

    // Check if item was added
    const watchlistRows = await page.$$('#watchlist-list tr');
    console.log(`   Found ${watchlistRows.length} watchlist items`);

    if (watchlistRows.length > 0) {
      // Check for Remove button
      const removeBtn = await page.$('[data-remove]');
      if (removeBtn) {
        console.log('   ✅ Remove button exists');
      }
    }

    await page.screenshot({ path: 'screenshots/04-watchlist.png', fullPage: true });

    // ===================================================================
    // TEST 6: Market Internals - TradingView Widgets
    // ===================================================================
    console.log('\n📍 TEST 6: Market Internals - TradingView Widgets');
    console.log('-'.repeat(60));

    await page.click('button[data-tab-target="internals"]');
    await page.waitForTimeout(5000); // Wait for TradingView widgets to load

    // Check for widget containers
    const widgetIds = [
      'tv-ticker-tape',
      'tv-mini-spy',
      'tv-mini-qqq',
      'tv-mini-iwm',
      'tv-market-overview',
      'tv-heatmap',
      'tv-calendar'
    ];

    for (const id of widgetIds) {
      const widget = await page.$(`#${id}`);
      if (widget) {
        const hasIframe = await widget.$('iframe');
        if (hasIframe) {
          console.log(`   ✅ ${id} loaded with iframe`);
        } else {
          console.log(`   ⚠️  ${id} exists but no iframe yet`);
        }
      } else {
        console.log(`   ❌ ${id} not found`);
      }
    }

    await page.screenshot({ path: 'screenshots/05-market-internals.png', fullPage: true });

    // ===================================================================
    // FINAL REPORT
    // ===================================================================
    console.log('\n' + '='.repeat(60));
    console.log('📊 TEST SUMMARY');
    console.log('='.repeat(60));
    console.log('\n✅ All Tests Completed!');
    console.log('\nScreenshots saved:');
    console.log('  • 00-dashboard-loaded.png');
    console.log('  • 01-analyze-with-chart.png');
    console.log('  • 02-scanner-patterns.png');
    console.log('  • 03-top-setups.png');
    console.log('  • 04-watchlist.png');
    console.log('  • 05-market-internals.png');

    console.log('\n📝 Console Messages:');
    const errors = consoleMessages.filter(m => m.startsWith('error:'));
    if (errors.length > 0) {
      console.log(`   ⚠️  ${errors.length} console errors detected`);
      errors.forEach(e => console.log(`      ${e}`));
    } else {
      console.log('   ✅ No console errors');
    }

    console.log('\n🏁 Test suite complete!');

  } catch (error) {
    console.error('\n❌ Test failed with error:', error);
  } finally {
    console.log('\n⏳ Keeping browser open for 10 seconds for review...');
    await page.waitForTimeout(10000);
    await browser.close();
  }
}

// Run the tests
testAllImprovements().catch(console.error);
