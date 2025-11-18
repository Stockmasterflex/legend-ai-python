/**
 * Options Analytics Dashboard
 * Handles data fetching, visualization, and interactions for options analytics
 */

// State management
const state = {
    currentSymbol: 'SPY',
    currentTab: 'chain',
    chainData: null,
    flowData: null,
    volatilityData: null,
    charts: {}
};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadInitialData();
});

function initializeEventListeners() {
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => switchTab(e.target.dataset.tab));
    });

    // Load data button
    document.getElementById('load-data-btn').addEventListener('click', () => {
        const symbol = document.getElementById('symbol-input').value.toUpperCase();
        if (symbol) {
            state.currentSymbol = symbol;
            loadAllData();
        }
    });

    // Symbol input enter key
    document.getElementById('symbol-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            document.getElementById('load-data-btn').click();
        }
    });

    // Strategy buttons
    document.querySelectorAll('.strategy-btn').forEach(btn => {
        btn.addEventListener('click', (e) => selectStrategy(e.target.dataset.strategy));
    });
}

function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        if (btn.dataset.tab === tabName) {
            btn.classList.remove('tab-inactive');
            btn.classList.add('tab-active');
        } else {
            btn.classList.remove('tab-active');
            btn.classList.add('tab-inactive');
        }
    });

    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.add('hidden');
    });
    document.getElementById(`tab-${tabName}`).classList.remove('hidden');

    state.currentTab = tabName;

    // Load tab-specific data if needed
    if (tabName === 'flow' && !state.flowData) {
        loadOptionsFlow();
    } else if (tabName === 'volatility' && !state.volatilityData) {
        loadVolatilityData();
    }
}

async function loadInitialData() {
    await loadAllData();
}

async function loadAllData() {
    showLoading();

    try {
        // Load all data in parallel
        await Promise.all([
            loadOptionsChain(),
            loadMaxPain(),
            loadOIAnalysis(),
            loadGammaExposure(),
            loadUnusualActivity()
        ]);

        // Load tab-specific data based on current tab
        if (state.currentTab === 'flow') {
            await loadOptionsFlow();
        } else if (state.currentTab === 'volatility') {
            await loadVolatilityData();
        }

        hideLoading();
    } catch (error) {
        console.error('Error loading data:', error);
        showError('Failed to load options data. Please try again.');
        hideLoading();
    }
}

// ============================================================================
// OPTIONS CHAIN
// ============================================================================

async function loadOptionsChain() {
    try {
        const response = await fetch(`/api/options/chain/${state.currentSymbol}?include_greeks=true`);
        const data = await response.json();

        state.chainData = data;
        renderOptionsChain(data);
        renderOIHeatmap(data);
    } catch (error) {
        console.error('Error loading options chain:', error);
    }
}

function renderOptionsChain(data) {
    const tbody = document.getElementById('chain-table');
    tbody.innerHTML = '';

    const calls = data.calls || [];
    const puts = data.puts || [];

    // Group by strike
    const strikeMap = new Map();

    calls.forEach(call => {
        if (!strikeMap.has(call.strike)) {
            strikeMap.set(call.strike, { call, put: null });
        } else {
            strikeMap.get(call.strike).call = call;
        }
    });

    puts.forEach(put => {
        if (!strikeMap.has(put.strike)) {
            strikeMap.set(put.strike, { call: null, put });
        } else {
            strikeMap.get(put.strike).put = put;
        }
    });

    // Sort by strike
    const strikes = Array.from(strikeMap.keys()).sort((a, b) => a - b);

    strikes.forEach(strike => {
        const { call, put } = strikeMap.get(strike);

        const row = document.createElement('tr');
        row.className = 'border-b border-gray-800 hover:bg-gray-800/50';

        const callIV = call ? (call.implied_volatility * 100).toFixed(1) + '%' : '--';
        const putIV = put ? (put.implied_volatility * 100).toFixed(1) + '%' : '--';
        const totalOI = (call?.open_interest || 0) + (put?.open_interest || 0);

        row.innerHTML = `
            <td class="py-2 font-mono">${strike.toFixed(2)}</td>
            <td class="text-right py-2">${callIV}</td>
            <td class="text-right py-2">${putIV}</td>
            <td class="text-right py-2">${totalOI.toLocaleString()}</td>
        `;

        tbody.appendChild(row);
    });
}

function renderOIHeatmap(data) {
    const container = document.getElementById('oi-heatmap');

    const calls = data.calls || [];
    const puts = data.puts || [];

    // Prepare data for heatmap
    const strikes = [...new Set([...calls.map(c => c.strike), ...puts.map(p => p.strike)])].sort((a, b) => a - b);

    const callOI = strikes.map(strike => {
        const call = calls.find(c => c.strike === strike);
        return call ? call.open_interest : 0;
    });

    const putOI = strikes.map(strike => {
        const put = puts.find(p => p.strike === strike);
        return put ? put.open_interest : 0;
    });

    const options = {
        series: [
            {
                name: 'Calls',
                data: callOI
            },
            {
                name: 'Puts',
                data: putOI
            }
        ],
        chart: {
            type: 'bar',
            height: 300,
            stacked: false,
            background: 'transparent',
            toolbar: {
                show: false
            }
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '70%',
            }
        },
        dataLabels: {
            enabled: false
        },
        xaxis: {
            categories: strikes.map(s => s.toFixed(2)),
            labels: {
                style: {
                    colors: '#9ca3af'
                }
            }
        },
        yaxis: {
            labels: {
                style: {
                    colors: '#9ca3af'
                },
                formatter: (val) => val.toLocaleString()
            }
        },
        colors: ['#10b981', '#ef4444'],
        legend: {
            labels: {
                colors: '#e5e7eb'
            }
        },
        grid: {
            borderColor: '#374151'
        },
        theme: {
            mode: 'dark'
        }
    };

    if (state.charts.oiHeatmap) {
        state.charts.oiHeatmap.destroy();
    }

    state.charts.oiHeatmap = new ApexCharts(container, options);
    state.charts.oiHeatmap.render();
}

async function loadMaxPain() {
    try {
        const response = await fetch(`/api/options/chain/${state.currentSymbol}/max-pain`);
        const data = await response.json();

        document.getElementById('kpi-max-pain').textContent = data.max_pain_strike ? `$${data.max_pain_strike.toFixed(2)}` : '--';
    } catch (error) {
        console.error('Error loading max pain:', error);
    }
}

async function loadOIAnalysis() {
    try {
        const response = await fetch(`/api/options/chain/${state.currentSymbol}/oi-analysis`);
        const data = await response.json();

        document.getElementById('kpi-pc-ratio').textContent = data.put_call_ratio?.toFixed(2) || '--';
        document.getElementById('kpi-total-oi').textContent = data.total_oi ? data.total_oi.toLocaleString() : '--';
    } catch (error) {
        console.error('Error loading OI analysis:', error);
    }
}

async function loadGammaExposure() {
    try {
        const response = await fetch(`/api/options/chain/${state.currentSymbol}/gamma-exposure`);
        const data = await response.json();

        const gexValue = data.total_gex || 0;
        const gexFormatted = gexValue >= 1e9 ? `$${(gexValue / 1e9).toFixed(2)}B` :
                            gexValue >= 1e6 ? `$${(gexValue / 1e6).toFixed(2)}M` :
                            `$${gexValue.toFixed(0)}`;

        document.getElementById('kpi-gex').textContent = gexFormatted;
    } catch (error) {
        console.error('Error loading gamma exposure:', error);
    }
}

async function loadUnusualActivity() {
    try {
        const response = await fetch(`/api/options/chain/${state.currentSymbol}/unusual-activity`);
        const data = await response.json();

        renderUnusualActivity(data.unusual_contracts || []);
    } catch (error) {
        console.error('Error loading unusual activity:', error);
    }
}

function renderUnusualActivity(contracts) {
    const container = document.getElementById('unusual-activity');
    container.innerHTML = '';

    if (!contracts.length) {
        container.innerHTML = '<p class="text-gray-500 text-center py-8">No unusual activity detected</p>';
        return;
    }

    contracts.slice(0, 10).forEach(contract => {
        const div = document.createElement('div');
        div.className = 'bg-gray-800/50 rounded-lg p-3 flex justify-between items-center';

        const typeClass = contract.type === 'call' ? 'bullish' : 'bearish';

        div.innerHTML = `
            <div>
                <div class="font-medium ${typeClass}">${contract.strike} ${contract.type.toUpperCase()}</div>
                <div class="text-sm text-gray-400">${contract.expiry}</div>
            </div>
            <div class="text-right">
                <div class="font-medium">Vol: ${contract.volume.toLocaleString()}</div>
                <div class="text-sm text-gray-400">OI: ${contract.open_interest.toLocaleString()}</div>
            </div>
            <div class="text-right">
                <div class="font-medium">${(contract.volume_oi_ratio).toFixed(1)}x</div>
                <div class="text-sm text-gray-400">Premium: $${(contract.implied_premium / 1000).toFixed(0)}K</div>
            </div>
        `;

        container.appendChild(div);
    });
}

// ============================================================================
// OPTIONS FLOW
// ============================================================================

async function loadOptionsFlow() {
    try {
        const response = await fetch(`/api/options/flow/${state.currentSymbol}?limit=50`);
        const data = await response.json();

        state.flowData = data;
        renderFlowFeed(data.trades || []);
        renderFlowCharts(data.trades || []);
    } catch (error) {
        console.error('Error loading options flow:', error);
    }
}

function renderFlowFeed(trades) {
    const container = document.getElementById('flow-feed');
    container.innerHTML = '';

    if (!trades.length) {
        container.innerHTML = '<p class="text-gray-500 text-center py-8">No flow data available</p>';
        return;
    }

    trades.slice(0, 30).forEach(trade => {
        const div = document.createElement('div');
        const flowClass = trade.sentiment === 'bullish' ? 'flow-bullish' : 'flow-bearish';

        div.className = `flow-item ${flowClass} rounded p-2 text-sm`;

        const time = new Date(trade.timestamp).toLocaleTimeString();

        div.innerHTML = `
            <div class="flex justify-between items-center">
                <div>
                    <span class="font-mono font-medium">${trade.strike} ${trade.type.toUpperCase()}</span>
                    <span class="text-gray-400 ml-2">${trade.expiry}</span>
                </div>
                <div class="text-right">
                    <div class="font-medium">${trade.size}x @ $${trade.price.toFixed(2)}</div>
                    <div class="text-xs text-gray-400">${trade.trade_type} • ${time}</div>
                </div>
            </div>
        `;

        container.appendChild(div);
    });
}

function renderFlowCharts(trades) {
    // Flow by type chart
    const typeCounts = trades.reduce((acc, trade) => {
        acc[trade.trade_type] = (acc[trade.trade_type] || 0) + 1;
        return acc;
    }, {});

    const typeChart = document.getElementById('flow-type-chart');
    if (typeChart) {
        if (state.charts.flowType) {
            state.charts.flowType.destroy();
        }

        state.charts.flowType = new Chart(typeChart, {
            type: 'doughnut',
            data: {
                labels: Object.keys(typeCounts),
                datasets: [{
                    data: Object.values(typeCounts),
                    backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#e5e7eb'
                        }
                    }
                }
            }
        });
    }

    // Sentiment chart
    const sentimentCounts = trades.reduce((acc, trade) => {
        acc[trade.sentiment] = (acc[trade.sentiment] || 0) + 1;
        return acc;
    }, {});

    const sentimentChart = document.getElementById('sentiment-chart');
    if (sentimentChart) {
        if (state.charts.sentiment) {
            state.charts.sentiment.destroy();
        }

        state.charts.sentiment = new Chart(sentimentChart, {
            type: 'bar',
            data: {
                labels: Object.keys(sentimentCounts),
                datasets: [{
                    label: 'Trade Count',
                    data: Object.values(sentimentCounts),
                    backgroundColor: Object.keys(sentimentCounts).map(s =>
                        s === 'bullish' ? '#10b981' : '#ef4444'
                    )
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        ticks: {
                            color: '#9ca3af'
                        },
                        grid: {
                            color: '#374151'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#9ca3af'
                        },
                        grid: {
                            color: '#374151'
                        }
                    }
                }
            }
        });
    }
}

// ============================================================================
// VOLATILITY SURFACE
// ============================================================================

async function loadVolatilityData() {
    try {
        const [skewResponse, termResponse] = await Promise.all([
            fetch(`/api/options/volatility/${state.currentSymbol}/skew`),
            fetch(`/api/options/volatility/${state.currentSymbol}/term-structure`)
        ]);

        const skewData = await skewResponse.json();
        const termData = await termResponse.json();

        state.volatilityData = { skew: skewData, term: termData };

        renderVolatilitySkew(skewData);
        renderTermStructure(termData);
    } catch (error) {
        console.error('Error loading volatility data:', error);
    }
}

function renderVolatilitySkew(data) {
    const container = document.getElementById('vol-skew-chart');

    const options = {
        series: [
            {
                name: 'Call IV',
                data: data.strikes.map((strike, i) => ({ x: strike, y: data.call_ivs[i] * 100 }))
            },
            {
                name: 'Put IV',
                data: data.strikes.map((strike, i) => ({ x: strike, y: data.put_ivs[i] * 100 }))
            }
        ],
        chart: {
            type: 'line',
            height: 300,
            background: 'transparent',
            toolbar: {
                show: false
            }
        },
        stroke: {
            curve: 'smooth',
            width: 3
        },
        xaxis: {
            type: 'numeric',
            title: {
                text: 'Strike',
                style: {
                    color: '#9ca3af'
                }
            },
            labels: {
                style: {
                    colors: '#9ca3af'
                }
            }
        },
        yaxis: {
            title: {
                text: 'Implied Volatility (%)',
                style: {
                    color: '#9ca3af'
                }
            },
            labels: {
                style: {
                    colors: '#9ca3af'
                }
            }
        },
        colors: ['#10b981', '#ef4444'],
        legend: {
            labels: {
                colors: '#e5e7eb'
            }
        },
        grid: {
            borderColor: '#374151'
        },
        theme: {
            mode: 'dark'
        }
    };

    if (state.charts.volSkew) {
        state.charts.volSkew.destroy();
    }

    state.charts.volSkew = new ApexCharts(container, options);
    state.charts.volSkew.render();
}

function renderTermStructure(data) {
    const container = document.getElementById('term-structure-chart');

    const options = {
        series: [{
            name: 'IV',
            data: data.days_to_expiry.map((days, i) => ({ x: days, y: data.ivs[i] * 100 }))
        }],
        chart: {
            type: 'line',
            height: 250,
            background: 'transparent',
            toolbar: {
                show: false
            }
        },
        stroke: {
            curve: 'smooth',
            width: 3
        },
        xaxis: {
            title: {
                text: 'Days to Expiry',
                style: {
                    color: '#9ca3af'
                }
            },
            labels: {
                style: {
                    colors: '#9ca3af'
                }
            }
        },
        yaxis: {
            title: {
                text: 'IV (%)',
                style: {
                    color: '#9ca3af'
                }
            },
            labels: {
                style: {
                    colors: '#9ca3af'
                }
            }
        },
        colors: ['#6366f1'],
        grid: {
            borderColor: '#374151'
        },
        theme: {
            mode: 'dark'
        }
    };

    if (state.charts.termStructure) {
        state.charts.termStructure.destroy();
    }

    state.charts.termStructure = new ApexCharts(container, options);
    state.charts.termStructure.render();
}

// ============================================================================
// STRATEGY BUILDER
// ============================================================================

function selectStrategy(strategy) {
    const paramsContainer = document.getElementById('strategy-params');

    // Highlight selected button
    document.querySelectorAll('.strategy-btn').forEach(btn => {
        if (btn.dataset.strategy === strategy) {
            btn.classList.add('gradient-bg');
            btn.classList.remove('bg-gray-800');
        } else {
            btn.classList.remove('gradient-bg');
            btn.classList.add('bg-gray-800');
        }
    });

    // Show relevant parameters
    let html = '';

    if (strategy === 'vertical') {
        html = `
            <h3 class="font-bold mb-2">Vertical Spread</h3>
            <div class="space-y-2">
                <input type="number" placeholder="Long Strike" class="w-full px-3 py-2 bg-gray-900 rounded" id="param-long-strike" value="145">
                <input type="number" placeholder="Short Strike" class="w-full px-3 py-2 bg-gray-900 rounded" id="param-short-strike" value="150">
                <input type="number" placeholder="Debit" class="w-full px-3 py-2 bg-gray-900 rounded" id="param-debit" value="2.50">
                <select class="w-full px-3 py-2 bg-gray-900 rounded" id="param-type">
                    <option value="call">Call Spread</option>
                    <option value="put">Put Spread</option>
                </select>
                <button class="w-full px-4 py-2 gradient-bg rounded" onclick="analyzeVerticalSpread()">Analyze</button>
            </div>
        `;
    } else if (strategy === 'iron-condor') {
        html = `
            <h3 class="font-bold mb-2">Iron Condor</h3>
            <div class="space-y-2">
                <input type="number" placeholder="Put Long Strike" class="w-full px-3 py-2 bg-gray-900 rounded" id="param-put-long" value="140">
                <input type="number" placeholder="Put Short Strike" class="w-full px-3 py-2 bg-gray-900 rounded" id="param-put-short" value="145">
                <input type="number" placeholder="Call Short Strike" class="w-full px-3 py-2 bg-gray-900 rounded" id="param-call-short" value="155">
                <input type="number" placeholder="Call Long Strike" class="w-full px-3 py-2 bg-gray-900 rounded" id="param-call-long" value="160">
                <input type="number" placeholder="Credit" class="w-full px-3 py-2 bg-gray-900 rounded" id="param-credit" value="1.50">
                <button class="w-full px-4 py-2 gradient-bg rounded" onclick="analyzeIronCondor()">Analyze</button>
            </div>
        `;
    } else if (strategy === 'straddle') {
        html = `
            <h3 class="font-bold mb-2">Straddle</h3>
            <div class="space-y-2">
                <input type="number" placeholder="Strike" class="w-full px-3 py-2 bg-gray-900 rounded" id="param-strike" value="150">
                <input type="number" placeholder="Call Price" class="w-full px-3 py-2 bg-gray-900 rounded" id="param-call-price" value="5.00">
                <input type="number" placeholder="Put Price" class="w-full px-3 py-2 bg-gray-900 rounded" id="param-put-price" value="4.50">
                <select class="w-full px-3 py-2 bg-gray-900 rounded" id="param-position">
                    <option value="true">Long Straddle</option>
                    <option value="false">Short Straddle</option>
                </select>
                <button class="w-full px-4 py-2 gradient-bg rounded" onclick="analyzeStraddle()">Analyze</button>
            </div>
        `;
    }

    paramsContainer.innerHTML = html;
}

async function analyzeVerticalSpread() {
    const data = {
        long_strike: parseFloat(document.getElementById('param-long-strike').value),
        short_strike: parseFloat(document.getElementById('param-short-strike').value),
        debit: parseFloat(document.getElementById('param-debit').value),
        spread_type: document.getElementById('param-type').value,
        spot_price: 150,
        num_contracts: 1
    };

    try {
        const response = await fetch('/api/options/strategies/vertical-spread', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        renderPnLDiagram(result);
        updateStrategyMetrics(result);
    } catch (error) {
        console.error('Error analyzing spread:', error);
    }
}

async function analyzeIronCondor() {
    const data = {
        put_long_strike: parseFloat(document.getElementById('param-put-long').value),
        put_short_strike: parseFloat(document.getElementById('param-put-short').value),
        call_short_strike: parseFloat(document.getElementById('param-call-short').value),
        call_long_strike: parseFloat(document.getElementById('param-call-long').value),
        credit: parseFloat(document.getElementById('param-credit').value),
        spot_price: 150,
        num_contracts: 1
    };

    try {
        const response = await fetch('/api/options/strategies/iron-condor', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        renderPnLDiagram(result);
        updateStrategyMetrics(result);
    } catch (error) {
        console.error('Error analyzing iron condor:', error);
    }
}

async function analyzeStraddle() {
    const data = {
        strike: parseFloat(document.getElementById('param-strike').value),
        call_price: parseFloat(document.getElementById('param-call-price').value),
        put_price: parseFloat(document.getElementById('param-put-price').value),
        spot_price: 150,
        num_contracts: 1,
        is_long: document.getElementById('param-position').value === 'true'
    };

    try {
        const response = await fetch('/api/options/strategies/straddle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        renderPnLDiagram(result);
        updateStrategyMetrics(result);
    } catch (error) {
        console.error('Error analyzing straddle:', error);
    }
}

function renderPnLDiagram(data) {
    const container = document.getElementById('pnl-chart');

    const pnlData = data.pnl_profile || [];

    const options = {
        series: [{
            name: 'P&L',
            data: pnlData.map(p => ({ x: p.price, y: p.pnl }))
        }],
        chart: {
            type: 'line',
            height: 350,
            background: 'transparent',
            toolbar: {
                show: false
            }
        },
        stroke: {
            curve: 'smooth',
            width: 3
        },
        xaxis: {
            title: {
                text: 'Stock Price',
                style: {
                    color: '#9ca3af'
                }
            },
            labels: {
                style: {
                    colors: '#9ca3af'
                }
            }
        },
        yaxis: {
            title: {
                text: 'Profit/Loss ($)',
                style: {
                    color: '#9ca3af'
                }
            },
            labels: {
                style: {
                    colors: '#9ca3af'
                },
                formatter: (val) => `$${val.toFixed(0)}`
            }
        },
        colors: ['#6366f1'],
        grid: {
            borderColor: '#374151'
        },
        theme: {
            mode: 'dark'
        },
        annotations: {
            yaxis: [{
                y: 0,
                borderColor: '#ef4444',
                strokeDashArray: 2
            }]
        }
    };

    if (state.charts.pnl) {
        state.charts.pnl.destroy();
    }

    state.charts.pnl = new ApexCharts(container, options);
    state.charts.pnl.render();
}

function updateStrategyMetrics(data) {
    const maxProfit = data.max_profit;
    const maxLoss = data.max_loss;

    document.getElementById('strategy-max-profit').textContent =
        maxProfit === 'Unlimited' ? maxProfit : `$${maxProfit.toFixed(2)}`;

    document.getElementById('strategy-max-loss').textContent =
        maxLoss === 'Unlimited' ? maxLoss : `$${Math.abs(maxLoss).toFixed(2)}`;

    document.getElementById('strategy-rr').textContent =
        data.risk_reward_ratio ? data.risk_reward_ratio.toFixed(2) : '--';
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function showLoading() {
    // Implement loading indicator
}

function hideLoading() {
    // Hide loading indicator
}

function showError(message) {
    alert(message);
}
