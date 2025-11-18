# Legend AI Dashboard Architecture Analysis

## Project Overview
- **Type**: Server-rendered Flask/FastAPI web application with vanilla JavaScript
- **Framework**: FastAPI (Python backend) + Vanilla JS (frontend)
- **Styling**: Custom CSS with cyberpunk design system
- **No React/Vue/Svelte** - Pure server-side rendering with progressive enhancement

---

## 1. ENTRY POINTS & ROUTING

### Backend Entry Point
**File**: `/home/user/legend-ai-python/app/main.py`
- FastAPI application initialization
- Middleware setup:
  - MetricsMiddleware (line 70) - performance tracking
  - StructuredLoggingMiddleware (line 74) - logging
  - RateLimitMiddleware (line 78) - 60 requests/minute per IP
  - CORSMiddleware (line 87) - configurable origins
- Static files mounted: `/static` -> `/home/user/legend-ai-python/static`
- Multiple API routers included (dashboard, patterns, charts, etc.)

### Dashboard Route
**File**: `/home/user/legend-ai-python/app/api/dashboard.py`
- **GET /dashboard** - Renders main dashboard HTML
- **GET /dashboard/test** - Test endpoint
- Serves: `/home/user/legend-ai-python/templates/dashboard.html`
- Handles template injection and build SHA resolution

---

## 2. DASHBOARD STRUCTURE (5 Main Tabs)

### HTML Template
**File**: `/home/user/legend-ai-python/templates/dashboard.html` (619 lines)

Tab Navigation (lines 48-55):
```
├── Analyze (tab-analyze) - Single ticker pattern analysis
├── Pattern Scanner (tab-scanner) - Bulk universe scanning
├── Top Setups (tab-top) - Best daily ideas (S&P 500 + NASDAQ)
├── Market Internals (tab-internals) - Market regime & breadth
└── Watchlist (tab-watchlist) - Managed watched stocks
```

**Key HTML Sections**:
1. **Hero Section** (lines 15-46)
   - Title & subtitle
   - Quick symbol search
   - Timeframe selector

2. **Analyze Tab** (lines 57-193)
   - Pattern form (ticker, timeframe)
   - Results grid
   - Chart panel (analyze-chart-panel)
   - TradingView widget demo (tradingview-demo-layout)

3. **Scanner Tab** (lines 195-349)
   - Universe selector (NASDAQ 100, S&P 500, focus)
   - Controls: timeframe, limit, score, RS, ATR filters
   - Pattern focus multi-select
   - Sector filter
   - Meta panel (scan stats)
   - Results table (scanner-table)

4. **Top Setups Tab** (lines 351-402)
   - Status bar (last scan, next scan, count)
   - Refresh controls
   - Results grid/table

5. **Watchlist Tab** (lines 404-536)
   - Add/edit form
   - Status dropdown (Watching, Setup, Triggered, Closed)
   - Tags system (Breakout, Momentum, VCP, etc.)
   - Watchlist table with controls

6. **Market Internals Tab** (lines 537+)
   - Market regime display
   - Breadth indicators

---

## 3. LAYOUT STRUCTURE & GRID SYSTEM

### Main Container Layout
**File**: `/home/user/legend-ai-python/static/css/dashboard.css` (2,336 lines)

#### Analyze Tab Layout (Lines 132-133)
```css
.analyze-panels {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(min(320px, 100%), 1.2fr);
    /* Results panel | Chart panel */
}
```

#### Scanner Table Layout (Lines 260-261)
```css
.scanner-meta-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    /* 2-column for metadata badges */
}
```

#### Results Grid (Lines 378-405)
- KPI Grid: `grid-template-columns: repeat(auto-fit, minmax(250px, 1fr))`
- Results Grid: `grid-template-columns: repeat(auto-fit, minmax(min(460px, 100%), 1fr))`
- Flexible: auto-fit with min/max constraints

---

## 4. CSS & STYLING APPROACH

### Design System Files

#### 1. Cyberpunk Design System
**File**: `/home/user/legend-ai-python/static/css/cyberpunk-design-system.css` (891 lines)

**Design Tokens** (lines 11-112):
- **Colors**: Dark background (#0b0f14), neon accents (purple #9b5cff, aqua #20f0ff)
- **Typography**: Inter font, JetBrains Mono for code
- **Spacing**: 8px base unit (--spacing-sm = 0.5rem)
- **Border Radius**: 6px to 9999px
- **Shadows**: sm/md/lg/xl variants
- **Glow Effects**: Purple, aqua, success, error
- **Transitions**: fast (150ms), base (250ms), slow (350ms)
- **Z-Index Scale**: 1000-1070 (dropdown, modal, tooltip)

**Components Styled**:
- Buttons (.btn, .btn-primary, .btn-secondary, .btn-ghost)
- Forms (.form-group, .radio-group, .select)
- Tables (.table, scrollable on mobile)
- Modals (.modal, 95% width on mobile)
- Toasts (.toast-container, bottom-right)
- Spinners and loading states

#### 2. Dashboard-Specific Styles
**File**: `/home/user/legend-ai-python/static/css/dashboard.css` (2,336 lines)

**Sections**:
- Hero section (gradient background, clamp() for responsive text)
- KPI cards (hover effects, status badges)
- Tabs navigation (active state, ARIA support)
- Form layouts (multi-column on desktop, single on mobile)
- Table wrappers (overflow-x scrollable)
- TradingView widget grid
- Chart shell/panel styling
- Loading overlays and spinners
- Watchlist density toggle

---

## 5. RESPONSIVE DESIGN & MOBILE SUPPORT

### Current Breakpoints & Media Queries

**File**: `/home/user/legend-ai-python/static/css/dashboard.css`

#### Breakpoint 1440px (Lines 824-832)
```css
@media (max-width: 1440px) {
    .analyze-panels { grid-template-columns: 1.1fr 1.1fr; }
    .internals-grid { grid-template-columns: repeat(2, 1fr); }
}
```
- For 1200-1440px screens: Slightly more balanced 2-column layout

#### Breakpoint 900px (Lines 834-850)
```css
@media (max-width: 900px) {
    .analyze-panels { grid-template-columns: 1fr; } /* Stack vertically */
    .analyze-chart-panel { order: 2; }
    .scanner-controls { grid-template-columns: 1fr; }
    .scanner-meta-grid { grid-template-columns: repeat(2, 1fr); }
}
```
- For tablets & smaller: Single column layouts, chart moves below results

#### Breakpoint 768px (Lines 1213-1281)
```css
@media (max-width: 768px) {
    .hero h1 { font-size: 2em; }
    .kpi-grid { grid-template-columns: 1fr; }
    .results-grid { grid-template-columns: 1fr; }
    .top-plan-grid { grid-template-columns: 1fr; }
    .top-card-buttons .btn { flex: 1; }
    .result-header { flex-direction: column; }
}
```
- For phones & small tablets: Single column, reduced font sizes, full-width buttons

#### Breakpoint 480px (Lines 1283-1295)
```css
@media (max-width: 480px) {
    .container { padding: var(--spacing-sm); /* 8px */ }
    .hero { padding: var(--spacing-lg); }
    .hero h1 { font-size: 1.75em; }
}
```
- For small phones: Minimal padding, compact hero

#### Viewport Meta Tag (Line 5 in HTML)
```html
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

#### Font Scaling (Cyberpunk CSS, Lines 842-847)
```css
@media (max-width: 768px) {
    :root {
        --font-size-4xl: 1.875rem;
        --font-size-3xl: 1.5rem;
        --font-size-2xl: 1.25rem;
    }
}
```

#### Responsive Units Used
- `clamp()` for fluid sizing (hero h1 uses `clamp(1.75rem, 5vw, 3rem)`)
- `auto-fit` with `minmax()` for flexible grids
- `min()` for responsive max-widths on mobile
- Flex `flex-direction: column` on mobile

---

## 6. JAVASCRIPT ARCHITECTURE

### Main Controller
**File**: `/home/user/legend-ai-python/static/js/dashboard.js` (2,073 lines)

**Module Structure** (IIFE - Immediately Invoked Function Expression):
```javascript
(function () {
  // Global Dashboard namespace
  window.Dashboard = {
    focusTab: function(tab) { ... },
    initialized: boolean
  };
  
  // State management
  const state = {
    activeTab, currentTicker, currentInterval, 
    chartRequestId, watchlistItems, topSetups, ...
  };
  
  // Components/Helpers
  const LoadingStates = { show, hide, toast }
  const WATCHLIST_TAG_LIBRARY = [...]
  
  // DOM Cache
  const els = { patternForm, patternTicker, ... }
  
  // Init on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', () => {
    cacheDom()
    bindEvents()
    initTabNavigation()
    initTagControls()
    loadWatchlist()
    loadTopSetups()
  })
})()
```

**Key Functions**:
- `cacheDom()` - Cache DOM element references
- `bindEvents()` - Attach event listeners
- `initTabNavigation()` - Tab switching logic
- `switchTab(tab)` - Show/hide tab panes
- `fetchAnalyze(ticker, tf)` - Fetch pattern analysis
- `handleUniverseScan()` - Bulk universe scan
- `loadWatchlist()` - Load saved watchlist
- `loadTopSetups()` - Load daily best ideas
- `toast(message, type, timeout)` - Notifications
- `safeFetch(url, options)` - Error-handling fetch wrapper

**Event Handlers**:
- Form submissions (pattern-form, universe-form)
- Tab button clicks
- Watchlist add/edit/delete
- Export CSV
- Top setups refresh
- Quick scan form

### TradingView Integration
**File**: `/home/user/legend-ai-python/static/js/tv-widgets.js` (122 lines)
- Loads TradingView Lightweight Charts embed
- Syncs symbol between dashboard and TradingView widgets
- Window.LegendTV namespace for symbol communication

---

## 7. COMPONENT INVENTORY

### Form Components
- **Pattern Analyze Form** (tab-analyze)
  - Ticker input with datalist (NASDAQ:NVDA, NASDAQ:AAPL, etc.)
  - Timeframe radio (Daily, Weekly)
  - Submit "Analyze pattern" button
  - "Add to watchlist" & "Generate snapshot" buttons

- **Universe Scanner Form** (tab-scanner)
  - Universe dropdown (NASDAQ 100, S&P 500, focus list)
  - Timeframe select
  - Limit input (10-150)
  - Score & RS filters
  - ATR% filter
  - Multi-select pattern focus (17 patterns)
  - Sector filter dropdown
  - "Run scan" & "Export CSV" buttons

- **Watchlist Form** (tab-watchlist)
  - Symbol input
  - Status dropdown (Watching, Setup, Triggered, Closed)
  - Notes/reason text input
  - Multi-select tags (Breakout, Momentum, VCP, etc.)

### Data Display Components
- **Results Grid** - Responsive card grid for pattern results
- **Scanner Table** - Scrollable table with 12 columns (ticker, pattern, score, RS, ATR%, sector, entry, stop, target, R:R, chart, actions)
- **Top Setups Table** - Simpler table for daily best ideas
- **Watchlist Table** - List of saved securities with status & tags
- **KPI Cards** - Dashboard metrics (hover effects, status badges)
- **Market Internals Grid** - Market breadth & regime widgets

### UI Components
- **Header/Hero** - Title, quick search, timeframe selector
- **Tabs Navigation** - 5 tab buttons with ARIA attributes
- **Loading Overlay** - Spinner + message (position: fixed over content)
- **Toast Notifications** - Bottom-right stacked notifications
- **Chart Shell** - Container for Chart-IMG or embedded charts
- **TradingView Widget** - Advanced chart + Symbol info + Technical analysis + Company profile + Fundamentals + News

### Mobile-Specific Features
- **Watchlist Density Toggle** - Compact/normal view toggle
- **Quick Search** - Header form for fast symbol lookup
- **Responsive Forms** - Stack on mobile, horizontal on desktop
- **Table Scrolling** - Horizontal scroll on small screens
- **Touch-friendly Buttons** - Full-width on mobile

---

## 8. API ENDPOINTS USED

From dashboard.js event handlers:
- **GET /api/patterns/analyze** - Pattern detection
- **GET /api/universe/scan** - Bulk universe scan
- **GET /api/watchlist** - Fetch watchlist
- **POST /api/watchlist** - Add to watchlist
- **PUT /api/watchlist/{id}** - Update watchlist item
- **DELETE /api/watchlist/{id}** - Remove from watchlist
- **GET /api/top-setups** - Fetch daily top setups
- **POST /api/universe/scan/top** - Manual top setups scan
- **POST /api/charts/generate** - Generate snapshot chart
- **GET /api/market/internals** - Market breadth data
- **GET /api/version** - Build version info
- **GET /api/cache/stats** - Cache statistics

---

## 9. FILE STRUCTURE SUMMARY

```
/home/user/legend-ai-python/
├── app/
│   ├── main.py                      # FastAPI app + routing
│   ├── api/
│   │   ├── dashboard.py             # /dashboard endpoint
│   │   ├── patterns.py              # Pattern detection API
│   │   ├── charts.py                # Chart generation
│   │   ├── watchlist.py             # Watchlist CRUD
│   │   └── ... (20+ API modules)
│   └── routers/
│       ├── ai_chat.py
│       └── advanced_analysis.py
├── templates/
│   ├── dashboard.html               # Main template (619 lines)
│   └── partials/
│       └── tv_widget_templates.html # TradingView embeds
├── static/
│   ├── js/
│   │   ├── dashboard.js             # Main controller (2,073 lines)
│   │   └── tv-widgets.js            # TradingView integration (122 lines)
│   └── css/
│       ├── cyberpunk-design-system.css  # Design tokens (891 lines)
│       └── dashboard.css                # Dashboard layout (2,336 lines)
└── ... (config, services, utils, etc.)
```

---

## 10. KEY TECHNOLOGIES & PATTERNS

### Frontend
- **Vanilla JavaScript** (no frameworks)
- **IIFE** (module pattern for encapsulation)
- **DOM caching** (for performance)
- **Event delegation** (for dynamic content)
- **Async/await** for API calls
- **Fetch API** with error handling

### CSS
- **CSS Custom Properties** (design tokens)
- **CSS Grid** (primary layout)
- **Flexbox** (secondary layout, components)
- **Clamp function** (fluid typography)
- **Media Queries** (responsive design)
- **Backdrop filters** (frosted glass effect)
- **CSS variables** for transitions, shadows, glows

### Backend
- **FastAPI** (async Python framework)
- **Jinja2** templating (template injection)
- **Static file mounting**
- **Middleware stack** (metrics, logging, CORS, rate-limit)
- **Environment-based configuration**

### Design
- **Dark mode only** (cyberpunk aesthetic)
- **Neon color palette** (purple, aqua, lime, magenta)
- **Glow effects** (box-shadow, text)
- **Hover animations** (translateY, color shifts)
- **Reduced motion support** (@media prefers-reduced-motion)

---

## 11. BUILD & CACHING

### Cache Busting
- Static assets use version parameter: `/static/css/dashboard.css?v=__VERSION__`
- Version resolved from: BUILD_SHA, GIT_COMMIT, RAILWAY_GIT_COMMIT_SHA, or `git rev-parse --short HEAD`
- Build SHA displayed in hero section: "BUILD {{ build_sha }}"

### Performance Optimizations
- Static file mounting for instant delivery
- Redis caching (optional, configured in settings)
- Client-side state management (no server session needed)
- Chart request ID tracking (prevent duplicate renders)
- Toast queue for UI feedback

---

## SUMMARY: Dashboard is Production-Ready for Mobile Optimization

**Current State**:
✅ Responsive design (breakpoints at 1440, 900, 768, 480px)
✅ Mobile-first CSS patterns (auto-fit, minmax, clamp)
✅ Viewport meta tag configured
✅ Touch-friendly button sizing on mobile
✅ Table scrolling on small screens
✅ Form reflow (horizontal → vertical)
✅ Accessible ARIA labels & semantic HTML

**Optimization Opportunities**:
- Add progressive image loading (lazy loading)
- Optimize TradingView widget for mobile (currently full grid)
- Consider native mobile app with React Native
- Add touch gestures for chart interactions
- Implement offline mode with Service Workers
- Add mobile-specific tab design (bottom nav vs top tabs)

