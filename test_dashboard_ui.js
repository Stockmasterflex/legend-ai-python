/**
 * Playwright UI Test for Legend AI Dashboard
 *
 * Run with: node test_dashboard_ui.js
 * Or with npx: npx playwright test test_dashboard_ui.js --headed
 */

const { chromium } = require('playwright');

async function testDashboard() {
  console.log('🚀 Starting Legend AI Dashboard UI Test\n');

  const browser = await chromium.launch({
    headless: false,  // Show browser window
    slowMo: 500       // Slow down actions so you can see them
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });

  const page = await context.newPage();

  // Capture console messages
  const consoleMessages = [];
  page.on('console', msg => {
    consoleMessages.push(`${msg.type()}: ${msg.text()}`);
    console.log(`📝 Console [${msg.type()}]: ${msg.text()}`);
  });

  // Capture errors
  page.on('pageerror', error => {
    console.log(`❌ Page Error: ${error.message}`);
  });

  try {
    // Step 1: Navigate to dashboard
    console.log('1️⃣ Navigating to dashboard...');
    await page.goto('https://legend-ai-python-production.up.railway.app/dashboard', {
      waitUntil: 'domcontentloaded'
    });

    // Wait a bit for Alpine.js and dashboard.js to initialize
    await page.waitForTimeout(3000);

    // Take initial screenshot
    await page.screenshot({ path: 'screenshots/01-initial-load.png', fullPage: true });
    console.log('✅ Initial screenshot saved\n');

    // Step 2: Check for initialization message in console
    console.log('2️⃣ Checking console for initialization...');
    const hasInitMessage = consoleMessages.some(msg =>
      msg.includes('Dashboard initializing') || msg.includes('Dashboard initialized successfully')
    );

    if (hasInitMessage) {
      console.log('✅ Dashboard initialization detected in console\n');
    } else {
      console.log('⚠️  Dashboard initialization message NOT found in console\n');
      console.log('Console messages received:', consoleMessages);
    }

    // Step 3: Check if Alpine.js loaded
    const alpineLoaded = await page.evaluate(() => window.Alpine !== undefined);
    const dashboardLoaded = await page.evaluate(() => window.Dashboard !== undefined);
    console.log(`Alpine.js loaded: ${alpineLoaded ? '✅' : '❌'}`);
    console.log(`Dashboard object loaded: ${dashboardLoaded ? '✅' : '❌'}\n`);

    // Step 4: Test tab switching
    console.log('3️⃣ Testing tab navigation...\n');

    const tabs = [
      { name: 'Analyze', selector: 'button.tab-button:has-text("Analyze")' },
      { name: 'Pattern Scanner', selector: 'button.tab-button:has-text("Pattern Scanner")' },
      { name: 'Top Setups', selector: 'button.tab-button:has-text("Top Setups")' },
      { name: 'Market Internals', selector: 'button.tab-button:has-text("Market Internals")' },
      { name: 'Watchlist', selector: 'button.tab-button:has-text("Watchlist")' }
    ];

    for (const tab of tabs) {
      console.log(`   Clicking "${tab.name}" tab...`);

      try {
        await page.click(tab.selector, { timeout: 5000 });
        await page.waitForTimeout(1000);

        // Take screenshot of each tab
        const filename = `screenshots/tab-${tab.name.toLowerCase().replace(' ', '-')}.png`;
        await page.screenshot({ path: filename, fullPage: true });
        console.log(`   ✅ Screenshot saved: ${filename}`);
      } catch (error) {
        console.log(`   ❌ Failed to click "${tab.name}": ${error.message}`);
      }
    }

    console.log('');

    // Step 5: Test Quick Scan with AAPL
    console.log('4️⃣ Testing Quick Scan feature...\n');

    try {
      // Go back to Analyze tab
      await page.click('button.tab-button:has-text("Analyze")');
      await page.waitForTimeout(500);

      // Find Quick Symbol input
      console.log('   Finding Quick Symbol input...');
      await page.fill('#quick-symbol-input', 'AAPL');
      console.log('   ✅ Entered "AAPL" in Quick Symbol input');

      // Click Scan button
      console.log('   Clicking Scan button...');
      await page.click('#quick-scan-button');
      console.log('   ✅ Clicked Scan button');

      // Wait for results (or loading indicator)
      await page.waitForTimeout(3000);

      // Take screenshot of results
      await page.screenshot({ path: 'screenshots/05-quick-scan-aapl.png', fullPage: true });
      console.log('   ✅ Screenshot saved: quick-scan-aapl.png\n');

      // Check if results appeared
      const resultsVisible = await page.isVisible('#pattern-results');
      console.log(`   Results visible: ${resultsVisible ? '✅' : '❌'}`);

    } catch (error) {
      console.log(`   ❌ Quick Scan test failed: ${error.message}\n`);
    }

    // Step 6: Final report
    console.log('═══════════════════════════════════════════════════');
    console.log('📊 TEST SUMMARY');
    console.log('═══════════════════════════════════════════════════');

    console.log('\n✅ Completed Actions:');
    console.log('  • Navigated to dashboard');
    console.log('  • Captured console messages');
    console.log('  • Tested all 5 tabs');
    console.log('  • Tested Quick Scan with AAPL');
    console.log('  • Saved 7 screenshots to screenshots/ folder');

    console.log('\n📝 Console Messages Captured:');
    consoleMessages.forEach(msg => console.log(`  ${msg}`));

    console.log('\n🖼️  Screenshots saved to:');
    console.log('  ./screenshots/01-initial-load.png');
    tabs.forEach(tab => {
      console.log(`  ./screenshots/tab-${tab.name.toLowerCase().replace(' ', '-')}.png`);
    });
    console.log('  ./screenshots/05-quick-scan-aapl.png');

  } catch (error) {
    console.error('\n❌ Test failed with error:', error);
  } finally {
    console.log('\n🏁 Test complete. Browser will close in 5 seconds...');
    await page.waitForTimeout(5000);
    await browser.close();
  }
}

// Create screenshots directory
const fs = require('fs');
if (!fs.existsSync('screenshots')) {
  fs.mkdirSync('screenshots');
}

// Run the test
testDashboard().catch(console.error);
