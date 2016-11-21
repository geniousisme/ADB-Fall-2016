from collections import defaultdict

from Candidate import Candidate, ItemSet
from Util import get_transactions

class AssocRulesExtractor(object):
    def __init__(self, filename, min_supp, min_conf):
        self.filename = filename
        self.min_supp = min_supp
        self.min_conf = min_conf
        self.total_trans = 0

    def get_L1_itemset(self):
        l1_itemset = Candidate()
        transactions = get_transactions(self.filename)
        self.total_trans = len(transactions)
        
        for trans in transactions:
            for item in trans:
                l1_itemset[set([item])] = (
                    l1_itemset.get(set([item])) + 1.0 / self.total_trans
                )
        candidateK = []
        for itemset in l1_itemset:
            if l1_itemset.get(itemset) >= self.min_supp:
                candidateK.append(itemset)

    def apriori_gen(self):
        pass
    
    def apriori(self):
        self.get_L1_itemset()

    def run(self):
        self.apriori()