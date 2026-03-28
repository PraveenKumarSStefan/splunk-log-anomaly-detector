class AnomalyScorer:
    def score_new_error(self, r):
        c = int(r.get("count",0))
        if c > 100: return 80
        if c > 50: return 70
        return 50
