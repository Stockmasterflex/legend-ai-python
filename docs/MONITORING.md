# Monitoring and Observability Guide

This guide explains the monitoring infrastructure for Legend AI and how to use it effectively.

## Overview

Legend AI uses a comprehensive monitoring stack to ensure system reliability and performance:

- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Alertmanager**: Alert routing and management
- **Telegram**: Real-time alert notifications
- **Built-in Monitoring**: Automatic metric collection and health checks

## Getting Started

### Starting the Monitoring Stack

```bash
# Start everything (app + monitoring)
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f app
```

### Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| Application | http://localhost:8000 | - |
| Metrics Endpoint | http://localhost:8000/metrics | - |
| Health Check | http://localhost:8000/health | - |
| Grafana | http://localhost:3000 | admin/admin |
| Prometheus | http://localhost:9090 | - |
| Alertmanager | http://localhost:9093 | - |

## Key Metrics

### Application Performance

**Request Rate**
```promql
rate(http_requests_total[5m])
```

**Error Rate**
```promql
rate(error_rate_total[5m])
```

**Response Time (P95)**
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

**Response Time (P99)**
```promql
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
```

### Database Performance

**Connection Pool Usage**
```promql
db_connections_total{state="active"} / db_connections_pool_size
```

**Query Duration**
```promql
rate(db_query_duration_seconds_sum[5m]) / rate(db_query_duration_seconds_count[5m])
```

### Cache Performance

**Cache Hit Rate**
```promql
rate(cache_hits_total[5m]) / (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m]))
```

### API Quota

**Quota Usage Percentage**
```promql
(api_quota_used / api_quota_limit) * 100
```

## Alert Configuration

### Alert Levels

1. **Critical** (Immediate notification)
   - System unavailable
   - High error rate (>10/min)
   - Database connection pool exhausted

2. **Warning** (Batched notification)
   - Degraded performance
   - High cache miss rate
   - API quota running low

3. **Info** (Daily digest)
   - Application restarts
   - Configuration changes

### Configuring Telegram Alerts

1. Create a Telegram bot:
   - Talk to [@BotFather](https://t.me/botfather)
   - Use `/newbot` command
   - Save the bot token

2. Get your chat ID:
   - Start a chat with [@userinfobot](https://t.me/userinfobot)
   - Note your chat ID

3. Update `.env`:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
```

4. Restart the application:
```bash
docker-compose restart app
```

### Alert Examples

**High Error Rate Alert**
```
⚠️ High Error Rate Alert

Severity: error
Endpoint: /api/analyze
Rate: 15 errors/min
Threshold: 10/min

Time: 2025-01-18 14:30:00
```

**Database Connection Alert**
```
🗄️ Database Connection Pool Alert

Active Connections: 19
Pool Size: 20
Usage: 95%
Threshold: 80%

Action: Consider increasing pool size
```

## Dashboards

### System Overview Dashboard

The main dashboard shows:

1. **Top Row**: Request rate and error rate
2. **Second Row**: Response times and database connections
3. **Third Row**: Cache hit rate and API quota usage
4. **Bottom Row**: Health status, uptime, and request counts

### Creating Custom Dashboards

1. Access Grafana: http://localhost:3000
2. Click "+" → "Dashboard"
3. Add panel
4. Select Prometheus datasource
5. Enter PromQL query
6. Configure visualization
7. Save dashboard

Example panel query:
```promql
sum(rate(http_requests_total{endpoint="/api/analyze"}[5m]))
```

## Health Checks

### Automated Health Checks

The monitoring service automatically checks:

- Database connectivity (every 60s)
- Redis connectivity (every 60s)
- External API availability (every 60s)

### Manual Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "components": {
    "database": {
      "status": "healthy",
      "connection": true
    },
    "redis": {
      "status": "healthy"
    },
    "external_apis": {
      "twelvedata": "healthy",
      "finnhub": "healthy"
    }
  },
  "uptime_seconds": 3600,
  "version": "1.0.0",
  "build_sha": "abc1234"
}
```

## Monitoring in Production

### Railway Deployment

When deployed to Railway, monitoring automatically:

1. Detects the public domain
2. Configures CORS for the domain
3. Sets up Telegram webhooks
4. Enables health checks

### Scaling Considerations

For high-traffic scenarios:

1. **Increase Prometheus retention**:
```yaml
# prometheus.yml
global:
  retention: 30d
```

2. **Add resource limits**:
```yaml
# docker-compose.yml
services:
  prometheus:
    deploy:
      resources:
        limits:
          memory: 2G
```

3. **Configure remote storage**:
   - Thanos for long-term storage
   - Cortex for multi-tenancy
   - M3DB for scalability

## Troubleshooting

### No Metrics in Grafana

**Problem**: Dashboard shows "No data"

**Solutions**:
1. Check Prometheus is scraping:
   ```bash
   curl http://localhost:9090/api/v1/targets
   ```

2. Verify metrics endpoint:
   ```bash
   curl http://localhost:8000/metrics
   ```

3. Check time range in Grafana (top-right corner)

### Alerts Not Firing

**Problem**: Not receiving Telegram alerts

**Solutions**:
1. Check bot token and chat ID:
   ```bash
   docker-compose exec app env | grep TELEGRAM
   ```

2. Test Telegram manually:
   ```bash
   curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
     -d "chat_id=<CHAT_ID>&text=Test"
   ```

3. Check application logs:
   ```bash
   docker-compose logs app | grep -i alert
   ```

### High Memory Usage

**Problem**: Prometheus consuming too much memory

**Solutions**:
1. Reduce scrape frequency:
```yaml
# prometheus.yml
global:
  scrape_interval: 30s  # Increase from 15s
```

2. Decrease retention:
```yaml
global:
  retention: 7d  # Decrease from 15d
```

3. Remove unused metrics from instrumentation

## Best Practices

### 1. Set Appropriate Thresholds

Don't alert on noise:
```python
# app/telemetry/alerter.py
self.thresholds = {
    "error_rate_5xx": 10,    # Adjust based on your traffic
    "response_time_p95": 5.0, # Adjust based on SLA
}
```

### 2. Use Labels Effectively

Add context to metrics:
```python
HTTP_REQUESTS_TOTAL.labels(
    method="POST",
    endpoint="/api/analyze",
    status_code=200
).inc()
```

### 3. Monitor What Matters

Focus on:
- User-facing metrics (response time, error rate)
- Resource utilization (CPU, memory, connections)
- Business metrics (patterns detected, alerts sent)

### 4. Document Your Alerts

For each alert, document:
- What it means
- Why it's important
- How to investigate
- How to resolve

### 5. Review Regularly

- Weekly: Review alert patterns
- Monthly: Adjust thresholds
- Quarterly: Update dashboards

## Advanced Topics

### Custom Metrics

Add business-specific metrics:

```python
# app/telemetry/metrics.py
PATTERNS_DETECTED = Counter(
    "patterns_detected_total",
    "Total patterns detected",
    ["pattern_type", "confidence"]
)

# In your code
PATTERNS_DETECTED.labels(
    pattern_type="VCP",
    confidence="high"
).inc()
```

### Multi-Environment Monitoring

Use labels to separate environments:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'legend-ai-prod'
    static_configs:
      - targets: ['prod.example.com:8000']
        labels:
          environment: 'production'

  - job_name: 'legend-ai-staging'
    static_configs:
      - targets: ['staging.example.com:8000']
        labels:
          environment: 'staging'
```

### SLO/SLA Monitoring

Define service level objectives:

```yaml
# alert rules
- alert: SLOBreach
  expr: |
    (
      sum(rate(http_requests_total{status_code=~"2.."}[30d]))
      /
      sum(rate(http_requests_total[30d]))
    ) < 0.999
  labels:
    severity: critical
  annotations:
    summary: "SLO breach: 99.9% uptime target not met"
```

## Resources

- [Prometheus Query Examples](https://prometheus.io/docs/prometheus/latest/querying/examples/)
- [Grafana Dashboard Gallery](https://grafana.com/grafana/dashboards/)
- [Alert Rule Best Practices](https://prometheus.io/docs/practices/alerting/)
- [PromQL Tutorial](https://prometheus.io/docs/prometheus/latest/querying/basics/)

## Support

For monitoring-related issues:

1. Check this guide first
2. Review application logs: `docker-compose logs -f`
3. Check Prometheus alerts: http://localhost:9090/alerts
4. Verify Grafana datasource: http://localhost:3000/datasources
