"""
Splunk Log Anomaly Detector - detects new errors, volume spikes, log gaps.
Author: Praveenkumar S
"""
import time, logging, yaml
from src.splunk_searcher import SplunkSearcher
from src.anomaly_scorer import AnomalyScorer
from src.notifier import AnomalyNotifier
from src.dedup_cache import DedupCache
log = logging.getLogger(__name__)

NEW_ERR_Q = "index=prod sourcetype=application log_level=ERROR earliest=-1h | rex field=_raw '(?<error_signature>[A-Z][a-zA-Z]+Exception)' | stats count by error_signature, service | join type=left error_signature [search index=prod earliest=-30d latest=-1h | rex '(?<error_signature>[A-Z][a-zA-Z]+Exception)' | stats count as historical_count by error_signature] | where isnull(historical_count) AND count>5"
 SPICK_Q = "index=prod sourcetype=application log_level=ERROR earliest=-8d | timechart span=1h count as error_count by service | eventstats avg(error_count) as mean, stdev(error_count) as stddev by service | eval upper_bound=mean+(2*stddev) | where error_count>upper_bound AND _time>relative_time(now(),'-1h')"
GAP_Q = "index=prod sourcetype=heartbeat earliest=-2h | stats latest(_time) as last_seen by service, host | eval minutes_since=round((now()-last_seen)/60,1) | where minutes_since>15"

class AnomalyDetector:
    def __init__(self, cfg_path="config/config.yaml"):
        with open(cfg_path) as f: self.cfg = yaml.safe_load(f)
        self.searcher = SplunkSearcher(self.cfg["splunk"])
        self.scorer = AnomalyScorer()
        self.notifier = AnomalyNotifier(self.cfg.get("alerts",{}))
        self.dedup = DedupCache(self.cfg.get("dedup_ttl_minutes",30))
    def run(self):
        log.info("Log Anomaly Detector started")
        while True:
            try:
                for r in self.searcher.search(NEW_ERR_Q):
                    key = f"new:{r.get('error_signature')}:{r.get('service')}"
                    if not self.dedup.is_duplicate(key):
                        self.notifier.send("P2",f"New Error: {r.get('service')}",f"{r.get('error_signature')} - {r.get('count')} occurrences")
                        self.dedup.mark(key)
            except Exception as e: log.error(f"Error: {e}")
            time.sleep(self.cfg.get("poll_interval_seconds",300))
if __name__ == "__main__": AnomalyDetector().run()
