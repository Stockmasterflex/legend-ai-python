/**
 * Theme Toggle Component
 * Interactive UI for theme switching
 */

class ThemeToggle {
    constructor(containerId = 'theme-toggle-container') {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.warn(`Theme toggle container "${containerId}" not found`);
            return;
        }

        this.themeEngine = window.themeEngine;
        if (!this.themeEngine) {
            console.error('Theme engine not found. Make sure theme-engine.js is loaded first.');
            return;
        }

        this.isOpen = false;
        this.init();
    }

    /**
     * Initialize the theme toggle component
     */
    init() {
        this.render();
        this.attachEventListeners();
        this.updateActiveTheme();

        // Listen for theme changes
        window.addEventListener('themechange', () => {
            this.updateActiveTheme();
        });
    }

    /**
     * Render the theme toggle UI
     */
    render() {
        const currentTheme = this.themeEngine.getCurrentTheme();
        const themeData = this.themeEngine.getTheme(currentTheme) || { name: 'Dark' };

        this.container.innerHTML = `
            <div class="theme-toggle-wrapper">
                <button
                    class="theme-toggle-btn"
                    id="theme-toggle-btn"
                    aria-label="Toggle theme menu"
                    aria-expanded="false"
                    aria-haspopup="true"
                >
                    <span class="theme-icon" id="theme-current-icon">
                        ${this.getThemeIcon(currentTheme)}
                    </span>
                    <span class="theme-label">${themeData.name}</span>
                    <span class="theme-toggle-arrow">
                        <svg viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M2 4L6 8L10 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </span>
                </button>

                <div class="theme-dropdown" id="theme-dropdown" role="menu">
                    <div class="theme-dropdown-header">
                        <h3 class="theme-dropdown-title">Choose Theme</h3>
                        <p class="theme-dropdown-subtitle">Select your preferred color scheme</p>
                    </div>

                    <ul class="theme-options">
                        ${this.renderThemeOptions()}
                    </ul>

                    <div class="theme-system-option">
                        <button
                            class="theme-option-btn"
                            data-theme="system"
                            role="menuitem"
                        >
                            <span class="theme-option-icon">
                                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" stroke-width="2"/>
                                    <path d="M9 3V21" stroke="currentColor" stroke-width="2"/>
                                </svg>
                            </span>
                            <div class="theme-option-content">
                                <div class="theme-option-name">System</div>
                                <div class="theme-option-description">Follow system preference</div>
                            </div>
                            <span class="theme-option-check">
                                <svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M3 8L7 12L13 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Mobile backdrop -->
            <div class="theme-dropdown-backdrop" id="theme-dropdown-backdrop"></div>
        `;
    }

    /**
     * Render theme options
     */
    renderThemeOptions() {
        const themes = this.themeEngine.getAllThemes();
        const builtInThemes = ['dark', 'light', 'high-contrast'];

        let optionsHTML = '';

        // Render built-in themes first
        builtInThemes.forEach(themeId => {
            if (themes[themeId]) {
                optionsHTML += this.renderThemeOption(themeId, themes[themeId]);
            }
        });

        // Render custom themes
        Object.entries(themes).forEach(([themeId, theme]) => {
            if (!builtInThemes.includes(themeId)) {
                optionsHTML += this.renderThemeOption(themeId, theme, true);
            }
        });

        return optionsHTML;
    }

    /**
     * Render a single theme option
     */
    renderThemeOption(themeId, theme, isCustom = false) {
        const colors = theme.colors || {};
        const customBadge = isCustom ? '<span class="custom-theme-badge">Custom</span>' : '';

        return `
            <li class="theme-option">
                <button
                    class="theme-option-btn"
                    data-theme="${themeId}"
                    role="menuitem"
                >
                    <div class="theme-color-preview">
                        <span style="background: ${colors['bg-primary'] || '#000'}"></span>
                        <span style="background: ${colors['primary'] || '#0f0'}"></span>
                        <span style="background: ${colors['secondary'] || '#f0f'}"></span>
                        <span style="background: ${colors['text-primary'] || '#fff'}"></span>
                    </div>
                    <div class="theme-option-content">
                        <div class="theme-option-name">
                            ${theme.name || themeId}${customBadge}
                        </div>
                        <div class="theme-option-description">
                            ${theme.description || ''}
                        </div>
                    </div>
                    <span class="theme-option-check">
                        <svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M3 8L7 12L13 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </span>
                </button>
            </li>
        `;
    }

    /**
     * Get icon for theme
     */
    getThemeIcon(themeId) {
        const icons = {
            dark: `
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" fill="currentColor"/>
                </svg>
            `,
            light: `
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="5" fill="currentColor"/>
                    <path d="M12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72l1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
            `,
            'high-contrast': `
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10" fill="currentColor"/>
                </svg>
            `,
        };

        return icons[themeId] || icons.dark;
    }

    /**
     * Attach event listeners
     */
    attachEventListeners() {
        const toggleBtn = document.getElementById('theme-toggle-btn');
        const dropdown = document.getElementById('theme-dropdown');
        const backdrop = document.getElementById('theme-dropdown-backdrop');

        if (!toggleBtn || !dropdown) return;

        // Toggle dropdown
        toggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleDropdown();
        });

        // Theme option clicks
        dropdown.addEventListener('click', (e) => {
            const themeBtn = e.target.closest('[data-theme]');
            if (themeBtn) {
                const themeId = themeBtn.dataset.theme;
                this.selectTheme(themeId);
            }
        });

        // Close on backdrop click
        if (backdrop) {
            backdrop.addEventListener('click', () => {
                this.closeDropdown();
            });
        }

        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!this.container.contains(e.target)) {
                this.closeDropdown();
            }
        });

        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.closeDropdown();
                toggleBtn.focus();
            }
        });

        // Keyboard navigation
        dropdown.addEventListener('keydown', (e) => {
            this.handleKeyboardNavigation(e);
        });
    }

    /**
     * Handle keyboard navigation
     */
    handleKeyboardNavigation(e) {
        const options = Array.from(this.container.querySelectorAll('.theme-option-btn'));
        const currentIndex = options.findIndex(opt => opt === document.activeElement);

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                const nextIndex = (currentIndex + 1) % options.length;
                options[nextIndex].focus();
                break;

            case 'ArrowUp':
                e.preventDefault();
                const prevIndex = currentIndex <= 0 ? options.length - 1 : currentIndex - 1;
                options[prevIndex].focus();
                break;

            case 'Home':
                e.preventDefault();
                options[0].focus();
                break;

            case 'End':
                e.preventDefault();
                options[options.length - 1].focus();
                break;

            case 'Enter':
            case ' ':
                e.preventDefault();
                if (document.activeElement.classList.contains('theme-option-btn')) {
                    document.activeElement.click();
                }
                break;
        }
    }

    /**
     * Toggle dropdown open/close
     */
    toggleDropdown() {
        if (this.isOpen) {
            this.closeDropdown();
        } else {
            this.openDropdown();
        }
    }

    /**
     * Open dropdown
     */
    openDropdown() {
        const toggleBtn = document.getElementById('theme-toggle-btn');
        const dropdown = document.getElementById('theme-dropdown');
        const backdrop = document.getElementById('theme-dropdown-backdrop');

        if (!dropdown) return;

        this.isOpen = true;
        dropdown.classList.add('active');
        if (backdrop) backdrop.classList.add('active');
        if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'true');

        // Focus first option
        setTimeout(() => {
            const firstOption = dropdown.querySelector('.theme-option-btn');
            if (firstOption) firstOption.focus();
        }, 100);
    }

    /**
     * Close dropdown
     */
    closeDropdown() {
        const toggleBtn = document.getElementById('theme-toggle-btn');
        const dropdown = document.getElementById('theme-dropdown');
        const backdrop = document.getElementById('theme-dropdown-backdrop');

        if (!dropdown) return;

        this.isOpen = false;
        dropdown.classList.remove('active');
        if (backdrop) backdrop.classList.remove('active');
        if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'false');
    }

    /**
     * Select a theme
     */
    selectTheme(themeId) {
        // Add loading state
        const toggleBtn = document.getElementById('theme-toggle-btn');
        if (toggleBtn) toggleBtn.classList.add('theme-loading');

        // Small delay for visual feedback
        setTimeout(() => {
            if (themeId === 'system') {
                this.themeEngine.setPreference('system');
            } else {
                this.themeEngine.setTheme(themeId);
            }

            // Update UI
            this.updateToggleButton();
            this.updateActiveTheme();

            // Remove loading state
            if (toggleBtn) toggleBtn.classList.remove('theme-loading');

            // Close dropdown
            this.closeDropdown();

            // Announce to screen readers
            this.announceThemeChange(themeId);
        }, 150);
    }

    /**
     * Update toggle button with current theme
     */
    updateToggleButton() {
        const currentTheme = this.themeEngine.getCurrentTheme();
        const themeData = this.themeEngine.getTheme(currentTheme) || { name: 'Dark' };

        const iconEl = document.getElementById('theme-current-icon');
        const labelEl = this.container.querySelector('.theme-label');

        if (iconEl) {
            iconEl.innerHTML = this.getThemeIcon(currentTheme);
        }

        if (labelEl) {
            labelEl.textContent = themeData.name;
        }
    }

    /**
     * Update active state on theme options
     */
    updateActiveTheme() {
        const currentTheme = this.themeEngine.getCurrentTheme();
        const options = this.container.querySelectorAll('.theme-option-btn');

        options.forEach(option => {
            const themeId = option.dataset.theme;
            if (themeId === currentTheme) {
                option.classList.add('active');
                option.setAttribute('aria-current', 'true');
            } else {
                option.classList.remove('active');
                option.removeAttribute('aria-current');
            }
        });
    }

    /**
     * Announce theme change to screen readers
     */
    announceThemeChange(themeId) {
        const announcement = document.createElement('div');
        announcement.setAttribute('role', 'status');
        announcement.setAttribute('aria-live', 'polite');
        announcement.className = 'sr-only';

        const themeData = this.themeEngine.getTheme(themeId) || { name: themeId };
        announcement.textContent = `Theme changed to ${themeData.name}`;

        document.body.appendChild(announcement);

        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 1000);
    }

    /**
     * Refresh the component
     */
    refresh() {
        this.render();
        this.attachEventListeners();
        this.updateActiveTheme();
    }
}

// Auto-initialize if container exists
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('theme-toggle-container')) {
        window.themeToggle = new ThemeToggle();
    }
});

// Export for manual initialization
window.ThemeToggle = ThemeToggle;
