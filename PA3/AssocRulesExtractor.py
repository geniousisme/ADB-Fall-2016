from collection import defaultdict

from Candidate import Candidate, ItemSet
from Util import get_transactions


class AssocRulesExtractor(object):
    def __init__(self, filename, min_support, min_confidence):
        self.filename = filename
        self.min_supp = min_support
        self.min_conf = min_confidence
        self.total_trans_num = 0
        self.support = defaultdict(list)
        self.confidence = {}

    def gen_L1_itemset(self):
        transactions = get_transactions(self.filename)
        self.total_trans = len(transactions)
        for trans in transactions:
            for candidate in trans:
                

    def apriori_gen(self):
        pass
    
    def apriori(self):
        self.gen_L1_itemset()

    def run(self):
        pass