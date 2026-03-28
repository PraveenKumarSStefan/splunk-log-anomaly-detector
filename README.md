# 🖉 Splunk Log Anomaly Detector

> ML-powered log anomaly detection using Splunk - detects new error signatures, volume spikes, and log gaps.

## Features
- New error signature detection (never seen in 30 days)
- 2-sigma volume spike detection
- Log gap detection (missing heartbeats)
- Alert deduplication

## Quick Start
```bash
git clone https://github.com/PraveenKumarSStefan/splunk-log-anomaly-detector
cd splunk-log-anomaly-detector
pip install -r requirements.txt
python src/anomaly_detector.py
```

## Author
Praveenkumar S | [GitHub](https://github.com/PraveenKumarSStefan)
