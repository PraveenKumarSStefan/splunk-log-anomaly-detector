import requests, time, logging
requests.packages.urllib3.disable_warnings()
log = logging.getLogger(__name__)
class SplunkSearcher:
    def __init__(self, cfg):
        self.host = cfg["host"].rstrip("/")
        self.headers = {"Authorization": "Bearer "+cfg["token"]}
    def search(self, spl, count=500):
        try:
            r = requests.post(self.host+"/services/search/jobs",headers=self.headers,data={"search":"search "+spl,"output_mode":"json"},verify=False,timeout=30)
            sid = r.json()["sid"]
            for _ in range(30):
                s = requests.get(self.host+"/services/search/jobs/"+sid,headers=self.headers,params={"output_mode":"json"},verify=False,timeout=10)
                if s.json()["entry"][0]["content"]["dispatchState"] == "DONE": break
                time.sleep(2)
            res = requests.get(self.host+"/services/search/jobs/"+sid+"/results",headers=self.headers,params={"output_mode":"json","count":count},verify=False,timeout=15)
            return res.json().get("results",[])
        except Exception as e: log.error(f"Failed: {e}"); return []
