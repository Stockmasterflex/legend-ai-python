const { chromium } = require('playwright');

async function testChartIssue() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

  // Capture console and errors
  page.on('console', msg => {
    const type = msg.type();
    const text = msg.text();
    console.log('CONSOLE [' + type + ']:', text);
  });
  page.on('pageerror', err => console.log('ERROR:', err.message));

  await page.goto('https://legend-ai-python-production.up.railway.app/dashboard');
  await page.waitForTimeout(3000);

  console.log('\n✅ Page loaded, clicking to Analyze tab...\n');

  // Ensure we're on Analyze tab
  const analyzeBtn = page.locator('button[data-tab-target="analyze"]');
  await analyzeBtn.click();

  // Fill in NVDA and analyze
  await page.fill('#pattern-ticker', 'NVDA');
  await page.selectOption('#pattern-interval', '1day');

  console.log('🔍 Submitting analyze for NVDA...\n');
  const submitBtn = page.locator('#pattern-form button[type="submit"]');
  await submitBtn.click();

  console.log('⏳ Waiting for API response...\n');
  await page.waitForTimeout(10000); // Wait for API

  // Check chart panel
  const chartPanel = await page.$('#analyze-chart');
  const chartHTML = await chartPanel?.innerHTML();
  console.log('\n📊 Chart Panel HTML:', chartHTML?.substring(0, 500) || 'EMPTY OR NULL');

  const chartStatus = await page.textContent('#analyze-chart-status');
  console.log('\n📍 Chart Status:', chartStatus);

  const chartTitle = await page.textContent('#analyze-chart-title');
  console.log('📍 Chart Title:', chartTitle);

  // Check if image exists
  const imgTag = await page.$('#analyze-chart img');
  if (imgTag) {
    const src = await imgTag.getAttribute('src');
    console.log('\n✅ Image found! SRC:', src);
  } else {
    console.log('\n❌ No <img> tag found in chart panel');
  }

  // Take screenshot
  await page.screenshot({ path: 'screenshots/chart-issue.png', fullPage: true });
  console.log('\n📸 Screenshot saved: screenshots/chart-issue.png');

  await page.waitForTimeout(3000);
  await browser.close();
}

testChartIssue().catch(console.error);
