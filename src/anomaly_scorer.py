class AnomalyScorer:
    def score_new_error(self, r):
        s = 50
        c = int(r.get("count",0))
        if c > 100: s += 30
        elif c > 50: s += 20
        elif c > 20: s += 10
        return min(s,100)
    def score_spike(self, factor):
        if factor > 10: return 90
        if factor > 5: return 70
        return 50
