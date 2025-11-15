# Playwright MCP Server Setup Guide

**Status**: ✅ Installed and Configured
**Date**: 2025-11-13

---

## What Is Playwright MCP?

The **Playwright MCP server** enables Claude to:
- **Navigate websites** - Open URLs, click links, fill forms
- **Interact with elements** - Click buttons, enter text, select options
- **Take screenshots** - Capture visual state of pages
- **Execute JavaScript** - Run custom scripts in browser context
- **Test UIs** - Verify buttons work, tabs switch, forms submit

**Key Advantage**: Uses browser's **accessibility tree** (structured data) instead of pixel-based screenshots, so it's faster and more reliable.

---

## ✅ Installation Complete

### For Claude Code / Claude Desktop

Added to: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "-y",
        "@playwright/mcp@latest",
        "--browser", "chrome",
        "--viewport-size", "1920x1080"
      ]
    }
  }
}
```

### For Cursor

Add the same configuration to Cursor's settings:

1. **Open Cursor Settings**:
   - Mac: `Cmd+Shift+P` → "Preferences: Open User Settings (JSON)"
   - Or: Cursor → Settings → Extensions → MCP

2. **Add to `cursor.json` or MCP config**:
   ```json
   {
     "mcp.servers": {
       "playwright": {
         "command": "npx",
         "args": ["-y", "@playwright/mcp@latest", "--browser", "chrome", "--viewport-size", "1920x1080"]
       }
     }
   }
   ```

3. **Restart Cursor**

---

## 🧪 How to Use with Claude Code

### Test Your Dashboard

Ask Claude Code to test your dashboard:

```
Hey Claude, use the Playwright MCP to test my dashboard at https://legend-ai-python-production.up.railway.app/dashboard

1. Navigate to the URL
2. Wait for page to load
3. Check console for "Dashboard initialized successfully"
4. Click each tab button (Analyze, Scanner, Top Setups, Internals, Watchlist)
5. Verify content appears for each tab
6. Take a screenshot of the working dashboard
7. Test the Quick Scan: enter "AAPL" and click Scan
8. Report any errors or issues
```

Claude will:
1. Launch Chrome browser
2. Navigate to your dashboard
3. Click all the buttons
4. Verify everything works
5. Give you a detailed report
6. Provide screenshots

---

## 🎯 Available MCP Tools

Once Playwright MCP is loaded, Claude can use these tools:

| Tool | Description |
|------|-------------|
| `playwright_navigate` | Navigate to a URL |
| `playwright_screenshot` | Take a screenshot of current page |
| `playwright_click` | Click an element by selector |
| `playwright_fill` | Fill a form field |
| `playwright_select_option` | Select dropdown option |
| `playwright_console` | Get browser console messages |
| `playwright_execute` | Execute custom JavaScript |
| `playwright_hover` | Hover over an element |
| `playwright_press` | Press keyboard keys |
| `playwright_snapshot` | Get accessibility tree snapshot |
| `playwright_wait` | Wait for an element or condition |

---

## 🔧 Configuration Options

### Headless vs Headed

**Headed** (current - see browser):
```json
"args": ["-y", "@playwright/mcp@latest", "--browser", "chrome"]
```

**Headless** (background, faster):
```json
"args": ["-y", "@playwright/mcp@latest", "--browser", "chrome", "--headless"]
```

### Different Browsers

**Chrome** (default):
```json
"args": ["--browser", "chrome"]
```

**Firefox**:
```json
"args": ["--browser", "firefox"]
```

**WebKit** (Safari engine):
```json
"args": ["--browser", "webkit"]
```

**Edge**:
```json
"args": ["--browser", "msedge"]
```

### Mobile Testing

**iPhone 15**:
```json
"args": ["--device", "iPhone 15"]
```

**Pixel 7**:
```json
"args": ["--device", "Pixel 7"]
```

### Custom Viewport

```json
"args": ["--viewport-size", "1920x1080"]
```

### Save Session/Videos

**Save traces** (for debugging):
```json
"args": ["--save-trace"]
```

**Save videos**:
```json
"args": ["--save-video", "1920x1080"]
```

---

## 📋 Example Test Scenarios

### 1. Basic Dashboard Test

```
Test the Legend AI dashboard:
1. Navigate to https://legend-ai-python-production.up.railway.app/dashboard
2. Wait for "Dashboard initialized successfully" in console
3. Take a screenshot
4. Report any console errors
```

### 2. Tab Functionality Test

```
Test all dashboard tabs:
1. Open the dashboard
2. Click "Analyze" tab - verify content appears
3. Click "Pattern Scanner" tab - verify content appears
4. Click "Top Setups" tab - verify content appears
5. Click "Market Internals" tab - verify content appears
6. Click "Watchlist" tab - verify content appears
7. Take screenshots of each tab
```

### 3. Form Interaction Test

```
Test the Quick Scan feature:
1. Open dashboard
2. Find the "Quick symbol" input field
3. Type "AAPL"
4. Click the "Scan" button
5. Wait for results to load
6. Take screenshot of results
7. Verify no errors in console
```

### 4. API Integration Test

```
Test the Analyze form:
1. Go to Analyze tab
2. Enter "NVDA" in ticker field
3. Select "Daily" interval
4. Click "Analyze pattern"
5. Wait for API response
6. Verify Minervini/Weinstein/VCP results appear
7. Screenshot the results
```

---

## 🐛 Troubleshooting

### "Playwright not found"

Install Playwright browsers:
```bash
npx playwright install chrome
```

### "Command not found: npx"

Install Node.js 18+:
```bash
brew install node
```

### "MCP server not responding"

1. **Restart Claude Desktop/Cursor**
2. **Check logs**:
   - Mac: `~/Library/Logs/Claude/mcp.log`
3. **Test manually**:
   ```bash
   npx @playwright/mcp@latest --help
   ```

### "Browser won't launch"

Try headless mode:
```json
"args": ["--headless"]
```

---

## 🎨 VS Code Integration (Bonus)

If you want Playwright in VS Code with Cursor:

1. Install VS Code extension: "Playwright Test for VSCode"
2. Configure in `.vscode/settings.json`:
   ```json
   {
     "playwright.reuseBrowser": true,
     "playwright.env": {
       "HEADED": "1"
     }
   }
   ```

---

## 🚀 Next Steps

Now that Playwright MCP is installed:

1. **Restart Claude Desktop** (if you're using it standalone)
2. **Test basic navigation**:
   ```
   Use Playwright to navigate to google.com and take a screenshot
   ```

3. **Test your dashboard**:
   ```
   Use Playwright to test my Legend AI dashboard and verify all tabs work
   ```

4. **Share with Cursor**: Copy the same config to Cursor's MCP settings

5. **Share with Codex**: Codex can also use MCP servers if configured in your Cursor settings

---

## 🔗 Resources

- **Official Docs**: https://github.com/microsoft/playwright-mcp
- **Playwright Docs**: https://playwright.dev
- **MCP Specification**: https://modelcontextprotocol.io
- **Example Servers**: https://github.com/modelcontextprotocol/servers

---

**Now Claude can actually browse and test your dashboard!** 🎭
