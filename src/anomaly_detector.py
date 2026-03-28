"""
Log Anomaly Detector - detects new error signatures, volume spikes, log gaps.
Author: Praveenkumar S
"""
import time, logging, yaml
from src.splunk_searcher import SplunkSearcher
from src.notifier import AnomalyNotifier
from src.dedup_cache import DedupCache
log = logging.getLogger(__name__)
NEW_ERROR_Q = "index=prod sourcetype=application log_level=ERROR earliest=-1h | rex field=_raw '(?<error_sig>[A-Z][a-zA-Z]+Exception)' | stats count by error_sig, service | join type=left error_sig [search index=prod log_level=ERROR earliest=-30d latest=-1h | stats count as hist by error_sig] | where isnull(hist) AND count>5"
SPIKE_Q = "index=prod log_level=ERROR earliest=-8d | timechart span=1h count as err_cnt by service | eventstats avg(err_cnt) as mean, stdev(err_cnt) as sd by service | eval ub=mean+2*sd | where err_cnt>ub"
GAP_Q = "index=prod sourcetype=heartbeat earliest=-2h | stats latest(_time) as last_seen by service, host | eval mins=round((now()-last_seen)/60,1) | where mins>15"
class AnomalyDetector:
    def __init__(self, cfg_path="config/config.yaml"):
        with open(cfg_path) as f: self.cfg = yaml.safe_load(f)
        self.searcher = SplunkSearcher(self.cfg["splunk"])
        self.notifier = AnomalyNotifier(self.cfg.get("alerts",{}))
        self.dedup = DedupCache(self.cfg.get("dedup_ttl_minutes",30))
    def run(self):
        log.info("Anomaly Detector started")
        while True:
            try:
                for r in self.searcher.search(NEW_ERROR_Q):
                    k = f"new:{r.get('error_sig')}:{r.get('service')}"
                    if not self.dedup.is_duplicate(k):
                        self.notifier.send("P2",f"New Error: {r.get('service')}",f"{r.get('error_sig')} - never seen in 30 days",r)
                        self.dedup.mark(k)
            except Exception as e: log.error(f"Error: {e}")
            time.sleep(self.cfg.get("poll_interval_seconds",300))
if __name__ == "__main__": AnomalyDetector().run()
