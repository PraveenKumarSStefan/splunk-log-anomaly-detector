import requests, logging
from datetime import datetime
log = logging.getLogger(__name__)
class AnomalyNotifier:
    def __init__(self, cfg): self.webhook = cfg.get("slack_webhook")
    def send(self, severity, title, message, extra=None):
        if not self.webhook: return
        try: requests.post(self.webhook,json={"text":f"[{severity}] {title}: {message}"},timeout=10)
        except Exception as e: log.error(f"Alert failed: {e}")
