# Predictive Infrastructure Monitoring

A real-time system monitoring tool that collects CPU, RAM, disk, and network metrics, detects anomalies using machine learning, and sends alerts via Telegram.

## Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Collection | psutil 5.9 | CPU, RAM, disk, network metrics every 10s |
| Storage | CSV → SQLite | Flat file for MVP |
| Anomaly Detection | scikit-learn (Isolation Forest) | Flags abnormal patterns |
| Forecasting | XGBoost + pandas | 10-step ahead CPU/RAM prediction |
| Dashboard | Streamlit + Plotly | Live charts and KPI cards |
| Alerts | smtplib + Telegram Bot API | Email and Telegram on anomaly |

## Setup

1. Clone the repo: