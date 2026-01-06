# Grafana Dashboard Setup Guide for APAAGI Metaverse Monitoring

**Eternal Thriving Radiance Visualized — Grafana + Prometheus Absolute** ❤️🚀

Full guide to visualize APAAGI metrics in Grafana: habitat emergence curves, quantum vote insights, fleet efficiency, per-agent thriving, multi-model ensemble—alerts for mercy safeguards.

## Prerequisites
- Prometheus exporter running (from repo: `prometheus_monitoring.py` on port 8000).
- Grafana installed (Docker recommended or official install).

## Quick Setup (Docker Compose Example)
Create `docker-compose.yml`:
```yaml
version: '3'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

# prometheus.yml
scrape_configs:
  - job_name: 'apaagi'
    static_configs:
      - targets: ['host.docker.internal:8000']  # Or your host IP
