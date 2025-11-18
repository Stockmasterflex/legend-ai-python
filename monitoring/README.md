# Legend AI Monitoring Setup

Comprehensive monitoring infrastructure for Legend AI with Prometheus, Grafana, and automated Telegram alerts.

## Features

- **Real-time Metrics**: HTTP request rates, response times, error rates
- **Database Monitoring**: Connection pool usage, query performance
- **API Quota Tracking**: Monitor external API usage (TwelveData, Finnhub, etc.)
- **Health Checks**: Automated health monitoring for all services
- **Automated Alerts**: Telegram notifications for critical issues
- **Visual Dashboards**: Grafana dashboards for system overview

## Architecture

```
┌─────────────────┐
│   Legend AI     │
│   FastAPI App   │──► Exposes /metrics endpoint
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Prometheus    │──► Scrapes metrics every 15s
│                 │──► Evaluates alert rules
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Alertmanager   │──► Routes alerts to Telegram
└─────────────────┘

         │
         ▼
┌─────────────────┐
│    Grafana      │──► Visualizes metrics
│   Dashboards    │
└─────────────────┘
```

## Quick Start

### 1. Start Monitoring Stack

```bash
# Start all services including monitoring
docker-compose up -d

# Verify services are running
docker-compose ps
```

### 2. Access Monitoring Interfaces

- **Grafana**: http://localhost:3000
  - Username: `admin`
  - Password: `admin`

- **Prometheus**: http://localhost:9090

- **Alertmanager**: http://localhost:9093

- **Application Metrics**: http://localhost:8000/metrics

### 3. Configure Telegram Alerts

Set the following environment variables in `.env`:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

## Metrics Overview

### HTTP Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `http_requests_total` | Counter | Total HTTP requests by method, endpoint, status |
| `http_request_duration_seconds` | Histogram | Request latency distribution |
| `http_request_size_bytes` | Summary | Request size |
| `http_response_size_bytes` | Summary | Response size |

### Error Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `error_rate_total` | Counter | Application errors by type and severity |
| `analyze_errors_total` | Counter | Errors in /api/analyze endpoint |
| `scan_errors_total` | Counter | Errors in /api/scan endpoint |

### Database Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `db_connections_total` | Gauge | Active/idle database connections |
| `db_connections_pool_size` | Gauge | Connection pool size |
| `db_connections_pool_overflow` | Gauge | Overflow connections |
| `db_query_duration_seconds` | Histogram | Query execution time |

### API Quota Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `api_quota_used` | Gauge | Current quota usage |
| `api_quota_limit` | Gauge | Quota limit |
| `api_quota_remaining` | Gauge | Remaining quota |

### Health Check Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `health_check_status` | Gauge | Health status (1=healthy, 0=unhealthy) |
| `health_check_duration_seconds` | Histogram | Health check duration |

### System Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `uptime_seconds` | Gauge | Application uptime |
| `app_info` | Info | Application version and build info |

## Alert Rules

### Critical Alerts

Sent immediately to Telegram:

- **HighErrorRate**: >10 server errors (5xx) in 5 minutes
- **VerySlowAPIResponseTime**: P95 latency >10 seconds
- **DatabaseConnectionPoolCritical**: >95% pool usage
- **DatabaseHealthCheckFailed**: Database unreachable for 2 minutes
- **RedisHealthCheckFailed**: Redis unreachable for 2 minutes

### Warning Alerts

Batched notifications:

- **High4xxRate**: >50 client errors (4xx) in 5 minutes
- **SlowAPIResponseTime**: P95 latency >5 seconds
- **DatabaseConnectionPoolHigh**: >80% pool usage
- **APIQuotaWarning**: >80% quota used
- **HighCacheMissRate**: >50% cache misses

### Info Alerts

Less frequent notifications:

- **ApplicationRestarted**: App uptime <5 minutes

## Telegram Alert Format

Alerts are sent to Telegram with the following format:

```
⚠️ *High Error Rate Alert*

*Severity:* error
*Endpoint:* /api/analyze
*Rate:* 15 errors/min
*Threshold:* 10/min

*Time:* 2025-01-18 14:30:00
```

## Grafana Dashboards

### Legend AI - System Overview

Pre-configured dashboard includes:

1. **Request Rate**: Requests per second by endpoint
2. **Error Rate**: Errors per second by severity
3. **Response Time (P95)**: 95th percentile latency
4. **Database Connection Pool**: Pool usage over time
5. **Cache Hit Rate**: Cache effectiveness
6. **API Quota Usage**: External API quota consumption
7. **Health Check Status**: Real-time health of all components
8. **Uptime**: Application uptime
9. **Total Requests**: Request count (last 5 minutes)
10. **Error Count**: Error count (last 5 minutes)

## Customization

### Adding New Metrics

1. Define metric in `app/telemetry/metrics.py`:

```python
from prometheus_client import Counter

MY_CUSTOM_METRIC = Counter(
    "my_custom_metric_total",
    "Description of my metric",
    ["label1", "label2"]
)
```

2. Instrument your code:

```python
from app.telemetry.metrics import MY_CUSTOM_METRIC

MY_CUSTOM_METRIC.labels(label1="value1", label2="value2").inc()
```

### Adding New Alert Rules

1. Create a new rule file in `monitoring/prometheus/alerts/`:

```yaml
groups:
  - name: my_alerts
    interval: 30s
    rules:
      - alert: MyAlert
        expr: my_metric > 100
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "My alert is firing"
          description: "Metric is {{ $value }}"
```

2. Reload Prometheus configuration:

```bash
curl -X POST http://localhost:9090/-/reload
```

### Customizing Telegram Alerts

Edit alert thresholds in `app/telemetry/alerter.py`:

```python
self.thresholds = {
    "error_rate_5xx": 10,      # Adjust this
    "error_rate_4xx": 50,       # And this
    "response_time_p95": 5.0,   # And this
    # ...
}
```

## Monitoring Best Practices

### 1. Alert Fatigue Prevention

- Set appropriate thresholds to avoid noise
- Use cooldown periods between alerts (default: 5 minutes)
- Group related alerts together
- Suppress warnings when critical alerts are firing

### 2. Dashboard Organization

- Keep the most important metrics at the top
- Use color coding (red=critical, yellow=warning, green=healthy)
- Set reasonable time ranges (default: last 1 hour)
- Enable auto-refresh (default: 30 seconds)

### 3. Performance Impact

Monitoring has minimal impact on application performance:

- Metrics collection: <1ms overhead per request
- Prometheus scraping: Every 15 seconds
- Alerter checks: Every 60 seconds
- Total overhead: <0.1% CPU, <50MB RAM

### 4. Data Retention

Default retention periods:

- Prometheus: 15 days
- Grafana: Unlimited (uses Prometheus as datasource)
- Alertmanager: 120 hours

Adjust in `prometheus.yml` if needed:

```yaml
global:
  retention: 30d  # Keep 30 days of data
```

## Troubleshooting

### Prometheus Not Scraping Metrics

1. Check if `/metrics` endpoint is accessible:
```bash
curl http://localhost:8000/metrics
```

2. Check Prometheus targets:
Visit http://localhost:9090/targets

3. Verify network connectivity:
```bash
docker-compose exec prometheus ping app
```

### Grafana Dashboard Empty

1. Verify Prometheus datasource:
- Grafana → Configuration → Data Sources → Prometheus
- Test connection

2. Check time range and refresh interval

3. Verify metrics are being collected:
```bash
curl http://localhost:9090/api/v1/query?query=up
```

### Telegram Alerts Not Working

1. Verify bot token and chat ID in `.env`

2. Check application logs:
```bash
docker-compose logs app | grep -i telegram
```

3. Test Telegram manually:
```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d "chat_id=<CHAT_ID>&text=Test"
```

### High Memory Usage

If Prometheus uses too much memory:

1. Reduce retention period
2. Decrease scrape frequency
3. Remove unused metrics

## Production Deployment

For production environments:

### 1. Secure Grafana

Change default password:

```yaml
# docker-compose.yml
environment:
  - GF_SECURITY_ADMIN_PASSWORD=strong_password_here
```

### 2. Enable HTTPS

Use reverse proxy (nginx/traefik) with SSL certificates

### 3. External Prometheus

For large-scale deployments, run Prometheus on dedicated infrastructure:

- Use remote storage (e.g., Thanos, Cortex)
- Implement high availability with Prometheus replicas
- Use federation for multi-cluster setups

### 4. Alerting Redundancy

Configure multiple alert channels:

- Telegram for immediate notifications
- Email for detailed reports
- PagerDuty/Opsgenie for critical alerts

## Cost Considerations

- Prometheus: Free, open-source
- Grafana: Free, open-source
- Alertmanager: Free, open-source
- Telegram: Free
- Infrastructure: ~$10-20/month for monitoring stack (1 CPU, 2GB RAM)

## Support

For issues or questions:

1. Check the logs: `docker-compose logs -f`
2. Review Prometheus alerts: http://localhost:9090/alerts
3. Check Grafana dashboards: http://localhost:3000

## References

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [FastAPI Metrics Guide](https://fastapi.tiangolo.com/advanced/custom-request-and-route/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)
