/*
 * Legend AI Dashboard - Mobile Controller
 * Touch interactions, gestures, and mobile-specific features
 */
(function () {
    'use strict';

    // Mobile state
    const mobileState = {
        isMobile: window.innerWidth <= 768,
        currentTab: 0,
        touchStartX: 0,
        touchStartY: 0,
        touchEndX: 0,
        touchEndY: 0,
        isPulling: false,
        pullDistance: 0,
        fabMenuOpen: false,
        drawerOpen: false,
        menuOpen: false,
        scrollY: 0,
    };

    // Tab configuration
    const tabs = ['analyze', 'scanner', 'top', 'internals', 'watchlist'];
    const tabIcons = {
        analyze: '📊',
        scanner: '🔍',
        top: '⭐',
        internals: '📈',
        watchlist: '👁️',
    };

    // ============================================================================
    // Haptic Feedback
    // ============================================================================
    function hapticFeedback(style = 'light') {
        if (!navigator.vibrate) return;

        const patterns = {
            light: [10],
            medium: [20],
            heavy: [30],
            success: [10, 50, 10],
            error: [50, 100, 50],
        };

        navigator.vibrate(patterns[style] || patterns.light);
    }

    // ============================================================================
    // Bottom Navigation Bar
    // ============================================================================
    function createBottomNav() {
        const nav = document.createElement('nav');
        nav.className = 'mobile-bottom-nav';
        nav.setAttribute('role', 'navigation');
        nav.setAttribute('aria-label', 'Main navigation');

        tabs.forEach((tab, index) => {
            const button = document.createElement('button');
            button.className = `mobile-nav-item ${index === 0 ? 'active' : ''}`;
            button.setAttribute('data-tab', tab);
            button.setAttribute('role', 'tab');
            button.setAttribute('aria-selected', index === 0 ? 'true' : 'false');

            const icon = document.createElement('span');
            icon.className = 'mobile-nav-icon';
            icon.textContent = tabIcons[tab] || '•';

            const label = document.createElement('span');
            label.textContent = tab.charAt(0).toUpperCase() + tab.slice(1);

            button.appendChild(icon);
            button.appendChild(label);

            button.addEventListener('click', () => {
                hapticFeedback('light');
                switchToTab(index);
            });

            nav.appendChild(button);
        });

        document.body.appendChild(nav);
    }

    // ============================================================================
    // Floating Action Button (FAB)
    // ============================================================================
    function createFAB() {
        const fab = document.createElement('button');
        fab.className = 'mobile-fab';
        fab.innerHTML = '+';
        fab.setAttribute('aria-label', 'Quick actions');

        fab.addEventListener('click', () => {
            hapticFeedback('medium');
            toggleFABMenu();
        });

        // FAB Menu
        const menu = document.createElement('div');
        menu.className = 'mobile-fab-menu';
        menu.innerHTML = `
            <button class="mobile-fab-menu-item" data-action="quick-scan">
                <span class="mobile-fab-menu-item-icon">🔍</span>
                <span>Quick Scan</span>
            </button>
            <button class="mobile-fab-menu-item" data-action="add-watchlist">
                <span class="mobile-fab-menu-item-icon">➕</span>
                <span>Add to Watchlist</span>
            </button>
            <button class="mobile-fab-menu-item" data-action="refresh">
                <span class="mobile-fab-menu-item-icon">🔄</span>
                <span>Refresh Data</span>
            </button>
        `;

        menu.querySelectorAll('.mobile-fab-menu-item').forEach(item => {
            item.addEventListener('click', (e) => {
                hapticFeedback('light');
                const action = e.currentTarget.getAttribute('data-action');
                handleFABAction(action);
                toggleFABMenu();
            });
        });

        document.body.appendChild(fab);
        document.body.appendChild(menu);
    }

    function toggleFABMenu() {
        const menu = document.querySelector('.mobile-fab-menu');
        const fab = document.querySelector('.mobile-fab');

        mobileState.fabMenuOpen = !mobileState.fabMenuOpen;

        if (mobileState.fabMenuOpen) {
            menu.classList.add('active');
            fab.style.transform = 'rotate(45deg)';
        } else {
            menu.classList.remove('active');
            fab.style.transform = 'rotate(0deg)';
        }
    }

    function handleFABAction(action) {
        switch (action) {
            case 'quick-scan':
                const quickInput = document.getElementById('quick-symbol-input');
                if (quickInput) {
                    openDrawer('Quick Scan', createQuickScanForm());
                }
                break;
            case 'add-watchlist':
                switchToTab(4); // Watchlist tab
                break;
            case 'refresh':
                refreshCurrentTab();
                break;
        }
    }

    function createQuickScanForm() {
        const form = document.createElement('form');
        form.innerHTML = `
            <div class="form-field">
                <label for="mobile-quick-symbol">Symbol</label>
                <input
                    type="text"
                    id="mobile-quick-symbol"
                    placeholder="AAPL"
                    pattern="[A-Z][A-Z0-9.^-]{0,9}"
                    style="text-transform: uppercase;"
                    required
                />
            </div>
            <div class="form-field">
                <label for="mobile-quick-timeframe">Timeframe</label>
                <select id="mobile-quick-timeframe">
                    <option value="1day">Daily</option>
                    <option value="1week">Weekly</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 16px;">
                Scan Pattern
            </button>
        `;

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const symbol = document.getElementById('mobile-quick-symbol').value;
            const timeframe = document.getElementById('mobile-quick-timeframe').value;

            // Trigger the desktop scan
            const desktopInput = document.getElementById('pattern-ticker');
            if (desktopInput) {
                desktopInput.value = symbol;
                const desktopForm = document.getElementById('pattern-form');
                if (desktopForm) {
                    desktopForm.dispatchEvent(new Event('submit'));
                }
            }

            closeDrawer();
            switchToTab(0); // Switch to Analyze tab
            hapticFeedback('success');
        });

        return form;
    }

    // ============================================================================
    // Drawer / Action Sheet
    // ============================================================================
    function createDrawer() {
        const overlay = document.createElement('div');
        overlay.className = 'mobile-drawer-overlay';

        const drawer = document.createElement('div');
        drawer.className = 'mobile-drawer';
        drawer.innerHTML = `
            <div class="mobile-drawer-handle"></div>
            <div class="mobile-drawer-header">
                <h3 class="mobile-drawer-title"></h3>
                <button class="mobile-drawer-close" aria-label="Close">×</button>
            </div>
            <div class="mobile-drawer-content"></div>
        `;

        overlay.addEventListener('click', closeDrawer);
        drawer.querySelector('.mobile-drawer-close').addEventListener('click', closeDrawer);

        // Swipe to close
        let startY = 0;
        const handle = drawer.querySelector('.mobile-drawer-handle');

        handle.addEventListener('touchstart', (e) => {
            startY = e.touches[0].clientY;
        });

        handle.addEventListener('touchmove', (e) => {
            const currentY = e.touches[0].clientY;
            const diff = currentY - startY;

            if (diff > 0) {
                drawer.style.transform = `translateY(${diff}px)`;
            }
        });

        handle.addEventListener('touchend', (e) => {
            const endY = e.changedTouches[0].clientY;
            const diff = endY - startY;

            if (diff > 100) {
                closeDrawer();
            } else {
                drawer.style.transform = 'translateY(0)';
            }
        });

        document.body.appendChild(overlay);
        document.body.appendChild(drawer);
    }

    function openDrawer(title, content) {
        const overlay = document.querySelector('.mobile-drawer-overlay');
        const drawer = document.querySelector('.mobile-drawer');
        const drawerTitle = drawer.querySelector('.mobile-drawer-title');
        const drawerContent = drawer.querySelector('.mobile-drawer-content');

        drawerTitle.textContent = title;
        drawerContent.innerHTML = '';

        if (typeof content === 'string') {
            drawerContent.innerHTML = content;
        } else {
            drawerContent.appendChild(content);
        }

        overlay.classList.add('active');
        drawer.classList.add('active');
        document.body.classList.add('drawer-open');
        mobileState.drawerOpen = true;

        hapticFeedback('light');
    }

    function closeDrawer() {
        const overlay = document.querySelector('.mobile-drawer-overlay');
        const drawer = document.querySelector('.mobile-drawer');

        overlay.classList.remove('active');
        drawer.classList.remove('active');
        document.body.classList.remove('drawer-open');
        mobileState.drawerOpen = false;

        hapticFeedback('light');
    }

    // ============================================================================
    // Hamburger Menu
    // ============================================================================
    function createHamburgerMenu() {
        const hamburger = document.createElement('button');
        hamburger.className = 'mobile-hamburger';
        hamburger.setAttribute('aria-label', 'Menu');
        hamburger.innerHTML = '<span></span><span></span><span></span>';

        const panel = document.createElement('div');
        panel.className = 'mobile-menu-panel';
        panel.innerHTML = `
            <button class="mobile-menu-item" data-action="export-csv">
                <span class="mobile-menu-item-icon">📥</span>
                <span>Export CSV</span>
            </button>
            <button class="mobile-menu-item" data-action="refresh-all">
                <span class="mobile-menu-item-icon">🔄</span>
                <span>Refresh All Data</span>
            </button>
            <button class="mobile-menu-item" data-action="settings">
                <span class="mobile-menu-item-icon">⚙️</span>
                <span>Settings</span>
            </button>
            <button class="mobile-menu-item" data-action="help">
                <span class="mobile-menu-item-icon">❓</span>
                <span>Help & Support</span>
            </button>
        `;

        hamburger.addEventListener('click', () => {
            hapticFeedback('light');
            toggleMenu();
        });

        panel.querySelectorAll('.mobile-menu-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const action = e.currentTarget.getAttribute('data-action');
                handleMenuAction(action);
                toggleMenu();
            });
        });

        const overlay = document.querySelector('.mobile-drawer-overlay');
        overlay.addEventListener('click', () => {
            if (mobileState.menuOpen) {
                toggleMenu();
            }
        });

        document.body.appendChild(hamburger);
        document.body.appendChild(panel);
    }

    function toggleMenu() {
        const hamburger = document.querySelector('.mobile-hamburger');
        const panel = document.querySelector('.mobile-menu-panel');
        const overlay = document.querySelector('.mobile-drawer-overlay');

        mobileState.menuOpen = !mobileState.menuOpen;

        if (mobileState.menuOpen) {
            hamburger.classList.add('active');
            panel.classList.add('active');
            overlay.classList.add('active');
        } else {
            hamburger.classList.remove('active');
            panel.classList.remove('active');
            overlay.classList.remove('active');
        }
    }

    function handleMenuAction(action) {
        hapticFeedback('light');

        switch (action) {
            case 'export-csv':
                const exportBtn = document.querySelector('#universe-export, #top-setups-export');
                if (exportBtn) exportBtn.click();
                break;
            case 'refresh-all':
                refreshCurrentTab();
                showToast('Refreshing data...', 'info');
                break;
            case 'settings':
                showToast('Settings coming soon!', 'info');
                break;
            case 'help':
                showToast('Help documentation coming soon!', 'info');
                break;
        }
    }

    // ============================================================================
    // Swipeable Tabs
    // ============================================================================
    function initSwipeableTabs() {
        const tabsContent = document.querySelector('.tabs-content');
        if (!tabsContent) return;

        let startX = 0;
        let currentX = 0;
        let isDragging = false;

        tabsContent.addEventListener('touchstart', (e) => {
            if (!mobileState.isMobile) return;
            startX = e.touches[0].clientX;
            isDragging = true;
        }, { passive: true });

        tabsContent.addEventListener('touchmove', (e) => {
            if (!isDragging || !mobileState.isMobile) return;
            currentX = e.touches[0].clientX;

            const diff = currentX - startX;
            const threshold = 50;

            // Show swipe indicators
            if (Math.abs(diff) > threshold) {
                if (diff > 0 && mobileState.currentTab > 0) {
                    showSwipeIndicator('left');
                } else if (diff < 0 && mobileState.currentTab < tabs.length - 1) {
                    showSwipeIndicator('right');
                }
            }
        }, { passive: true });

        tabsContent.addEventListener('touchend', (e) => {
            if (!isDragging || !mobileState.isMobile) return;

            const endX = e.changedTouches[0].clientX;
            const diff = endX - startX;
            const threshold = 100;

            if (Math.abs(diff) > threshold) {
                if (diff > 0 && mobileState.currentTab > 0) {
                    // Swipe right - previous tab
                    switchToTab(mobileState.currentTab - 1);
                    hapticFeedback('light');
                } else if (diff < 0 && mobileState.currentTab < tabs.length - 1) {
                    // Swipe left - next tab
                    switchToTab(mobileState.currentTab + 1);
                    hapticFeedback('light');
                }
            }

            hideSwipeIndicators();
            isDragging = false;
        }, { passive: true });
    }

    function showSwipeIndicator(direction) {
        let indicator = document.querySelector(`.mobile-swipe-indicator.${direction}`);

        if (!indicator) {
            indicator = document.createElement('div');
            indicator.className = `mobile-swipe-indicator ${direction}`;
            indicator.textContent = direction === 'left' ? '‹' : '›';
            document.body.appendChild(indicator);
        }

        indicator.classList.add('active');
    }

    function hideSwipeIndicators() {
        document.querySelectorAll('.mobile-swipe-indicator').forEach(indicator => {
            indicator.classList.remove('active');
        });
    }

    function switchToTab(index) {
        if (index < 0 || index >= tabs.length) return;

        mobileState.currentTab = index;
        const tabName = tabs[index];

        // Update bottom nav
        document.querySelectorAll('.mobile-nav-item').forEach((item, i) => {
            if (i === index) {
                item.classList.add('active');
                item.setAttribute('aria-selected', 'true');
            } else {
                item.classList.remove('active');
                item.setAttribute('aria-selected', 'false');
            }
        });

        // Switch tab using the desktop function if available
        if (window.Dashboard && window.Dashboard.focusTab) {
            window.Dashboard.focusTab(tabName);
        } else {
            // Fallback: manually switch tabs
            const tabButtons = document.querySelectorAll('.tab-button');
            tabButtons.forEach(btn => {
                if (btn.getAttribute('data-tab-target') === tabName) {
                    btn.click();
                }
            });
        }
    }

    // ============================================================================
    // Pull to Refresh
    // ============================================================================
    function initPullToRefresh() {
        const indicator = document.createElement('div');
        indicator.className = 'pull-to-refresh-indicator';
        indicator.innerHTML = '<span class="spinner"></span><span>Pull to refresh</span>';
        document.body.appendChild(indicator);

        let startY = 0;
        let isPulling = false;

        document.addEventListener('touchstart', (e) => {
            if (!mobileState.isMobile) return;
            if (window.scrollY === 0) {
                startY = e.touches[0].clientY;
                isPulling = true;
            }
        }, { passive: true });

        document.addEventListener('touchmove', (e) => {
            if (!isPulling || !mobileState.isMobile) return;

            const currentY = e.touches[0].clientY;
            const diff = currentY - startY;

            if (diff > 0 && window.scrollY === 0) {
                mobileState.pullDistance = diff;

                if (diff > 80) {
                    indicator.classList.add('active');
                    indicator.innerHTML = '<span class="spinner"></span><span>Release to refresh</span>';
                }
            }
        }, { passive: true });

        document.addEventListener('touchend', (e) => {
            if (!isPulling || !mobileState.isMobile) return;

            if (mobileState.pullDistance > 80) {
                hapticFeedback('success');
                indicator.innerHTML = '<span class="spinner"></span><span>Refreshing...</span>';

                setTimeout(() => {
                    refreshCurrentTab();
                    indicator.classList.remove('active');
                    indicator.innerHTML = '<span class="spinner"></span><span>Pull to refresh</span>';
                }, 1000);
            } else {
                indicator.classList.remove('active');
            }

            isPulling = false;
            mobileState.pullDistance = 0;
        }, { passive: true });
    }

    function refreshCurrentTab() {
        const currentTabName = tabs[mobileState.currentTab];

        // Trigger refresh based on current tab
        switch (currentTabName) {
            case 'analyze':
                const analyzeForm = document.getElementById('pattern-form');
                if (analyzeForm) {
                    const submitEvent = new Event('submit', { cancelable: true });
                    analyzeForm.dispatchEvent(submitEvent);
                }
                break;
            case 'scanner':
                const scannerForm = document.getElementById('universe-form');
                if (scannerForm) {
                    const submitEvent = new Event('submit', { cancelable: true });
                    scannerForm.dispatchEvent(submitEvent);
                }
                break;
            case 'top':
                const refreshBtn = document.getElementById('top-setups-refresh');
                if (refreshBtn) refreshBtn.click();
                break;
            case 'internals':
                const marketRefresh = document.getElementById('market-refresh');
                if (marketRefresh) marketRefresh.click();
                break;
            case 'watchlist':
                // Reload watchlist
                if (window.Dashboard && window.Dashboard.loadWatchlist) {
                    window.Dashboard.loadWatchlist();
                }
                break;
        }

        hapticFeedback('success');
    }

    // ============================================================================
    // Lazy Loading Images
    // ============================================================================
    function initLazyLoading() {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px',
        });

        // Observe all images with data-src attribute
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });

        // Re-observe when new images are added
        const mutationObserver = new MutationObserver(() => {
            document.querySelectorAll('img[data-src]').forEach(img => {
                if (!img.dataset.observed) {
                    imageObserver.observe(img);
                    img.dataset.observed = 'true';
                }
            });
        });

        mutationObserver.observe(document.body, {
            childList: true,
            subtree: true,
        });
    }

    // ============================================================================
    // Debounced Search
    // ============================================================================
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    function initDebouncedSearch() {
        const searchInputs = document.querySelectorAll('#watchlist-search, input[type="search"]');

        searchInputs.forEach(input => {
            const debouncedSearch = debounce((e) => {
                const value = e.target.value.toLowerCase();
                // Trigger search logic
                if (input.id === 'watchlist-search') {
                    filterWatchlist(value);
                }
            }, 300);

            input.addEventListener('input', debouncedSearch);
        });
    }

    function filterWatchlist(query) {
        const rows = document.querySelectorAll('#watchlist-list tr');

        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            if (text.includes(query)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    // ============================================================================
    // Virtual Scrolling (Simplified)
    // ============================================================================
    function initVirtualScrolling() {
        const tables = document.querySelectorAll('.scanner-table, .top-setups-table');

        tables.forEach(table => {
            const tbody = table.querySelector('tbody');
            if (!tbody) return;

            // For mobile, we'll show all rows but optimize rendering
            // This is a simplified version - a full implementation would use windowing
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    }
                });
            }, {
                rootMargin: '100px',
            });

            tbody.querySelectorAll('tr').forEach(row => {
                observer.observe(row);
            });
        });
    }

    // ============================================================================
    // Collapsible Sections
    // ============================================================================
    function initCollapsibleSections() {
        if (!mobileState.isMobile) return;

        // Wrap sections in collapsible containers
        const sections = document.querySelectorAll('.scanner-controls, .top-setups-header');

        sections.forEach(section => {
            if (section.classList.contains('collapsible-section')) return;

            const wrapper = document.createElement('div');
            wrapper.className = 'collapsible-section';

            const header = document.createElement('button');
            header.className = 'collapsible-header';
            header.innerHTML = `
                <span>Filters & Options</span>
                <span class="collapsible-icon">▼</span>
            `;

            const content = document.createElement('div');
            content.className = 'collapsible-content';

            section.parentNode.insertBefore(wrapper, section);
            wrapper.appendChild(header);
            wrapper.appendChild(content);
            content.appendChild(section);

            header.addEventListener('click', () => {
                wrapper.classList.toggle('collapsed');
                hapticFeedback('light');
            });

            // Start collapsed
            wrapper.classList.add('collapsed');
        });
    }

    // ============================================================================
    // Toast Notifications
    // ============================================================================
    function showToast(message, type = 'info') {
        const toastStack = document.getElementById('toast-stack') || createToastStack();

        const toast = document.createElement('div');
        toast.className = `toast ${type} show`;
        toast.innerHTML = `
            <span>${message}</span>
            <button class="toast-close" aria-label="Close">×</button>
        `;

        toast.querySelector('.toast-close').addEventListener('click', () => {
            removeToast(toast);
        });

        toastStack.appendChild(toast);

        // Auto-remove after 3 seconds
        setTimeout(() => {
            removeToast(toast);
        }, 3000);

        hapticFeedback('light');
    }

    function createToastStack() {
        const stack = document.createElement('div');
        stack.id = 'toast-stack';
        stack.className = 'toast-stack';
        document.body.appendChild(stack);
        return stack;
    }

    function removeToast(toast) {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }

    // ============================================================================
    // Deep Linking
    // ============================================================================
    function initDeepLinking() {
        const hash = window.location.hash.slice(1);

        if (hash) {
            const tabIndex = tabs.indexOf(hash);
            if (tabIndex >= 0) {
                switchToTab(tabIndex);
            }
        }

        // Update hash when tab changes
        window.addEventListener('hashchange', () => {
            const newHash = window.location.hash.slice(1);
            const tabIndex = tabs.indexOf(newHash);
            if (tabIndex >= 0) {
                switchToTab(tabIndex);
            }
        });
    }

    // ============================================================================
    // Resize Handler
    // ============================================================================
    function handleResize() {
        const wasMobile = mobileState.isMobile;
        mobileState.isMobile = window.innerWidth <= 768;

        if (wasMobile !== mobileState.isMobile) {
            // Reinitialize if switching between mobile and desktop
            if (mobileState.isMobile) {
                initCollapsibleSections();
            }
        }
    }

    // ============================================================================
    // Initialization
    // ============================================================================
    function init() {
        console.log('Mobile controller initializing...');

        // Check if mobile
        mobileState.isMobile = window.innerWidth <= 768;

        if (!mobileState.isMobile) {
            console.log('Not mobile, skipping mobile features');
            return;
        }

        // Create mobile UI components
        createBottomNav();
        createFAB();
        createDrawer();
        createHamburgerMenu();

        // Initialize features
        initSwipeableTabs();
        initPullToRefresh();
        initLazyLoading();
        initDebouncedSearch();
        initVirtualScrolling();
        initCollapsibleSections();
        initDeepLinking();

        // Event listeners
        window.addEventListener('resize', debounce(handleResize, 250));

        console.log('Mobile controller initialized');
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose mobile utilities globally
    window.MobileUtils = {
        hapticFeedback,
        showToast,
        openDrawer,
        closeDrawer,
        switchToTab,
    };
})();
