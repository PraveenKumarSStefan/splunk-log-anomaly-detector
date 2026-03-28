import requests, logging
from datetime import datetime
log = logging.getLogger(__name__)
class AnomalyNotifier:
    def __init__(self, cfg):
        self.webhook = cfg.get("slack_webhook")
        self.channel = cfg.get("slack_channel","#log-anomalies")
    def send(self, sev, title, msg, extra=None):
        if not self.webhook: return
        try: requests.post(self.webhook, json={"text":f"[{sev}] {title}: {msg}"}, timeout=10)
        except Exception as e: log.error(f"Failed: {e}")
