from Util import get_candidates

class AssocRulesExtractor(object):
    def __init__(self, filename, min_support, min_confidence):
        self.filename = filename
        self.min_supp = min_support
        self.min_conf = min_confidence

    def apriori(self):
        candidates = get_candidates(self.filename)
        


    def run(self):
        pass