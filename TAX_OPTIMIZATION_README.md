# Tax Optimization System

A comprehensive automated tax optimization system for Legend AI trading platform, featuring wash sale detection, tax loss harvesting, gain/loss reporting, scenario planning, and exports for tax software.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Data Models](#data-models)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Tax Rules Reference](#tax-rules-reference)

---

## Overview

The Tax Optimization System provides automated tools to help users minimize tax liabilities and maximize after-tax returns through:

1. **Wash Sale Detection** - IRS 30-day rule compliance
2. **Tax Loss Harvesting** - Identifying opportunities to offset gains
3. **Gain/Loss Reporting** - Comprehensive tax reporting
4. **Scenario Planning** - What-if analysis for tax planning
5. **Export Capabilities** - TurboTax CSV, Form 8949, CPA reports

## Features

### 1. Wash Sale Detection

**IRS 30-Day Rule Tracking**
- Automatically detects purchases within 30 days before or after a loss sale
- Calculates disallowed losses and cost basis adjustments
- Provides warnings before executing potentially problematic trades

**Alternative Security Suggestions**
- Recommends similar but not "substantially identical" securities
- Maintains exposure while avoiding wash sale violations
- Includes correlation and similarity scores

**API Endpoint:** `POST /api/tax/wash-sale/check`

```python
# Example: Check if a sale triggers wash sale rule
POST /api/tax/wash-sale/check
{
  "symbol": "AAPL",
  "sale_date": "2024-06-01T00:00:00",
  "loss_amount": -500.0,
  "user_id": "default"
}

# Response
{
  "success": true,
  "wash_sale": {
    "is_violation": true,
    "days_until_safe": 15,
    "disallowed_loss": "$500.00",
    "alternative_securities": [
      {
        "symbol": "MSFT",
        "similarity_score": 0.85,
        "reasons": ["Same sector", "Similar market cap"]
      }
    ]
  }
}
```

### 2. Tax Loss Harvesting

**Opportunity Identification**
- Scans portfolio for positions with unrealized losses
- Calculates potential tax savings based on user's tax bracket
- Prioritizes by estimated tax benefit

**Smart Replacement**
- Suggests replacement securities to maintain market exposure
- Ensures wash sale compliance
- Tracks 31-day safe harbor period

**API Endpoint:** `GET /api/tax/harvest/opportunities`

```python
# Example: Get tax loss harvesting opportunities
GET /api/tax/harvest/opportunities?user_id=default&min_loss=100&tax_bracket=0.24

# Response
{
  "success": true,
  "count": 3,
  "total_potential_savings": 1200.00,
  "opportunities": [
    {
      "symbol": "TSLA",
      "unrealized_loss": "$2,000.00",
      "estimated_tax_savings": "$480.00",
      "replacement_suggestions": [
        {"symbol": "GM", "similarity_score": 0.75}
      ],
      "days_until_wash_safe": 31
    }
  ]
}
```

### 3. Gain/Loss Reports

**Comprehensive Tax Reporting**
- Short-term vs long-term capital gains segregation
- Realized vs unrealized position tracking
- Wash sale adjustment accounting
- Tax year summaries

**Tax Impact Estimates**
- Bracket-aware tax calculations
- Effective rate computation
- 2024 federal tax brackets (single filer)

**API Endpoints:**
- `GET /api/tax/report/gains-losses` - Full gain/loss report
- `POST /api/tax/report/tax-estimate` - Tax impact estimate

```python
# Example: Get gain/loss report for 2024
GET /api/tax/report/gains-losses?user_id=default&tax_year=2024

# Response
{
  "success": true,
  "tax_year": 2024,
  "summary": {
    "short_term_gains": "$5,000.00",
    "short_term_losses": "$1,000.00",
    "net_short_term": "$4,000.00",
    "long_term_gains": "$10,000.00",
    "long_term_losses": "$500.00",
    "net_long_term": "$9,500.00",
    "total_net_gain_loss": "$13,500.00"
  },
  "realized_count": 15,
  "unrealized_count": 8
}
```

### 4. Scenario Planning

**What-If Analysis**
- Compare different sale timing scenarios
- Analyze impact of holding for long-term treatment
- Evaluate bracket management strategies
- Donation strategy planning

**Optimal Timing**
- Short-term vs long-term treatment comparison
- Tax bracket jump avoidance
- Year-end planning recommendations

**API Endpoint:** `POST /api/tax/scenario/sale-timing`

```python
# Example: Analyze sale timing scenarios
POST /api/tax/scenario/sale-timing
{
  "symbol": "AAPL",
  "quantity": 100,
  "current_gain": 5000.0
}

# Response
{
  "success": true,
  "scenarios": [
    {
      "name": "Sell Now (Short-Term)",
      "current_tax": "$1,200.00",
      "tax_savings": "$0.00"
    },
    {
      "name": "Wait for Long-Term",
      "projected_tax": "$750.00",
      "tax_savings": "$450.00"
    }
  ],
  "best_scenario": "Wait for Long-Term"
}
```

### 5. Export for Tax Software

**TurboTax CSV Export**
- Direct import into TurboTax
- Properly formatted for investment income section
- Includes all required fields

**IRS Form 8949 Preparation**
- Structured data for Form 8949
- Separate short-term and long-term transactions
- Wash sale adjustment codes

**CPA Report**
- Comprehensive year-end report
- All transactions with tax lot details
- Unrealized position summary

**API Endpoints:**
- `GET /api/tax/export/turbotax` - TurboTax CSV
- `GET /api/tax/export/form-8949` - Form 8949 data
- `GET /api/tax/export/cpa-report` - Full CPA report

```python
# Example: Export to TurboTax CSV
GET /api/tax/export/turbotax?user_id=default&tax_year=2024

# Response includes CSV data ready for import
{
  "success": true,
  "format": "turbotax_csv",
  "csv_data": "Security Name,Symbol,Shares,...",
  "instructions": [
    "1. Save CSV data to file",
    "2. In TurboTax, go to Investment Income",
    "3. Select Import from CSV"
  ]
}
```

## API Endpoints

### Dashboard

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tax/health` | GET | Health check |
| `/api/tax/dashboard` | GET | Comprehensive tax dashboard |

### Wash Sale Detection

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tax/wash-sale/check` | POST | Check if sale triggers wash sale |
| `/api/tax/wash-sale/alternatives/{symbol}` | GET | Get alternative securities |

### Tax Loss Harvesting

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tax/harvest/opportunities` | GET | Get harvesting opportunities |
| `/api/tax/harvest/execute` | POST | Execute a tax loss harvest |

### Reporting

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tax/report/gains-losses` | GET | Get gain/loss report |
| `/api/tax/report/tax-estimate` | POST | Estimate tax impact |

### Scenario Planning

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tax/scenario/sale-timing` | POST | Analyze sale timing scenarios |

### Exports

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tax/export/turbotax` | GET | Export TurboTax CSV |
| `/api/tax/export/form-8949` | GET | Export Form 8949 data |
| `/api/tax/export/cpa-report` | GET | Export comprehensive CPA report |

## Usage Examples

### Example 1: Year-End Tax Planning

```python
import requests

# 1. Get tax dashboard
response = requests.get("http://localhost:8000/api/tax/dashboard?tax_year=2024")
dashboard = response.json()

print(f"Net gain/loss: {dashboard['summary']['total_net_gain_loss']}")
print(f"Estimated tax: {dashboard['summary']['estimated_tax']}")

# 2. Check for tax loss harvesting opportunities
response = requests.get(
    "http://localhost:8000/api/tax/harvest/opportunities?tax_bracket=0.24"
)
opportunities = response.json()

print(f"Found {opportunities['count']} opportunities")
print(f"Potential savings: ${opportunities['total_potential_savings']}")

# 3. Execute harvest on best opportunity
if opportunities['count'] > 0:
    best_opp = opportunities['opportunities'][0]

    # Execute harvest
    response = requests.post(
        "http://localhost:8000/api/tax/harvest/execute",
        json={
            "tax_lot_id": best_opp['tax_lot_id'],
            "replacement_symbol": best_opp['replacement_suggestions'][0]['symbol']
        }
    )
    result = response.json()
    print(f"Harvested: {result['harvest']['loss_realized']}")
```

### Example 2: Wash Sale Check Before Trading

```python
import requests
from datetime import datetime

# Before selling at a loss, check wash sale rule
response = requests.post(
    "http://localhost:8000/api/tax/wash-sale/check",
    json={
        "symbol": "AAPL",
        "sale_date": datetime.now().isoformat(),
        "loss_amount": -1000.0
    }
)

wash_sale = response.json()['wash_sale']

if wash_sale['is_violation']:
    print("⚠️ WARNING: Wash sale violation detected!")
    print(f"Wait {wash_sale['days_until_safe']} days to avoid violation")
    print("\nConsider these alternatives:")
    for alt in wash_sale['alternative_securities']:
        print(f"  - {alt['symbol']} (similarity: {alt['similarity_score']})")
else:
    print("✅ Clear to sell - no wash sale violation")
```

### Example 3: Export for Tax Filing

```python
import requests

# Export to TurboTax
response = requests.get(
    "http://localhost:8000/api/tax/export/turbotax?tax_year=2024"
)
export = response.json()

# Save CSV to file
with open("capital_gains_2024.csv", "w") as f:
    f.write(export['csv_data'])

print("✅ Exported to capital_gains_2024.csv")
print("Ready for TurboTax import!")

# Also get Form 8949 data for manual filing
response = requests.get(
    "http://localhost:8000/api/tax/export/form-8949?tax_year=2024"
)
form_8949 = response.json()

print(f"\nForm 8949 entries: {len(form_8949['entries'])}")
```

## Data Models

### TaxLot
Tracks individual purchase lots for tax basis calculation.

```python
{
  "symbol": "AAPL",
  "quantity": 100,
  "cost_basis": 15000.0,
  "price_per_share": 150.0,
  "purchase_date": "2024-01-01T00:00:00",
  "holding_period": "short_term",
  "wash_sale_disallowed": 0.0,
  "adjusted_cost_basis": 15000.0
}
```

### CapitalGain
Records realized capital gains/losses.

```python
{
  "symbol": "AAPL",
  "quantity": 100,
  "sale_price": 180.0,
  "sale_date": "2024-06-01T00:00:00",
  "proceeds": 18000.0,
  "cost_basis": 15000.0,
  "gain_loss": 3000.0,
  "holding_period": "short_term",
  "tax_year": 2024
}
```

### WashSale
Tracks wash sale violations.

```python
{
  "symbol": "AAPL",
  "loss_sale_date": "2024-06-01T00:00:00",
  "loss_amount": -500.0,
  "status": "violation",
  "days_between": 14,
  "disallowed_loss": 500.0,
  "suggested_alternatives": ["MSFT", "GOOGL"]
}
```

## Database Schema

The system uses 4 PostgreSQL tables:

1. **tax_lots** - Individual purchase lot tracking
2. **capital_gains** - Realized gain/loss records
3. **wash_sales** - Wash sale violation tracking
4. **tax_harvest_logs** - Tax loss harvesting history

To create the tables:

```bash
# Run Alembic migration
alembic upgrade head
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tax optimization tests
pytest tests/test_tax_optimization.py -v

# Run specific test
pytest tests/test_tax_optimization.py::test_wash_sale_violation -v

# Run with coverage
pytest tests/test_tax_optimization.py --cov=app.services.tax_optimizer --cov-report=html
```

## Tax Rules Reference

### IRS Wash Sale Rule (30-Day Rule)

**What is it?**
- Cannot deduct a loss if you buy substantially identical security within 30 days before or after the loss sale
- Total wash sale window: 61 days (30 days before + sale day + 30 days after)

**What happens if violated?**
- Loss is disallowed for current tax year
- Disallowed loss is added to cost basis of new purchase
- Holding period of new purchase includes old holding period

**How to avoid:**
- Wait 31 days after loss sale before repurchasing
- Buy a similar but not "substantially identical" security
- Use suggested alternatives from the system

### Holding Period

**Short-Term (≤ 1 year)**
- Taxed as ordinary income
- Can be taxed at rates up to 37% (2024)

**Long-Term (> 1 year)**
- Preferential tax rates
- 0%, 15%, or 20% depending on income
- Generally much more favorable

**Strategy:**
- Hold winners > 1 year for long-term treatment
- Harvest short-term losses to offset short-term gains
- Consider timing of sales around 1-year mark

### Tax Loss Harvesting

**Optimal Timing:**
- Review portfolio quarterly
- Accelerate in Q4 for year-end planning
- Consider market conditions and future outlook

**Best Practices:**
- Harvest losses to offset gains
- Up to $3,000 loss can offset ordinary income (per year)
- Excess losses carry forward indefinitely
- Maintain market exposure with replacements

**Considerations:**
- Transaction costs
- Bid-ask spreads
- Market timing risk
- Long-term investment thesis

## Important Disclaimers

⚠️ **This system is for informational purposes only and does not constitute tax advice.**

- Always consult a qualified tax professional or CPA
- Tax laws vary by jurisdiction and change frequently
- Individual circumstances affect tax treatment
- System uses 2024 federal tax rates (single filer)
- State and local taxes not included
- Alternative Minimum Tax (AMT) not considered

## Support

For questions or issues:
- Open an issue on GitHub
- Check `/docs` for API documentation
- Review test cases for usage examples

## License

Copyright © 2024 Legend AI
