from collections import defaultdict

from Candidate import Candidate, ItemSet
from Util import get_transactions, get_subsets

class AssocRulesExtractor(object):
    def __init__(self, filename, min_supp, min_conf):
        self.filename = filename
        self.min_supp = min_supp
        self.min_conf = min_conf
        self.total_trans = 0
        self.transactions = []

    def get_L1_itemset(self):
        l1_itemset = Candidate()
        self.transactions = get_transactions(self.filename)
        self.total_trans = len(self.transactions)
        
        for trans in self.transactions:
            for item in trans:
                if not item:
                    continue
                l1_itemset[item] = (
                    l1_itemset.get(item) + 1.0 / self.total_trans
                )
        l1_itemset_result = []
        for itemset in l1_itemset:
            if l1_itemset.get(itemset) >= self.min_supp:
                l1_itemset_result.append(itemset)
        return set(l1_itemset_result)

    def apriori_gen(self, L_k_1_itemset):
        '''
        Take Section 2.1.1 - Apriori Candidate Generation 
        as reference to implement, there are two steps: join & prune
        '''

        '''
        join step, 2.1.1, p3
        '''
        L_k_1_itemset_list = list(L_k_1_itemset)
        candidates_k = []
        for i in xrange(len(L_k_1_itemset_list)):
            for j in xrange(i + 1, len(L_k_1_itemset_list)):
                if L_k_1_itemset_list[i][:-1] == L_k_1_itemset_list[j][:-1]:
                    tmp_candidate = list(L_k_1_itemset_list[i][:])
                    tmp_candidate.append(L_k_1_itemset_list[j][-1])
                    candidates_k.append(set(tmp_candidate))
        '''
        prune step, 2.1.1, p4
        '''
        for candidate in candidates_k:
            k_1_subsets = get_subsets(candidate)
            for subset in k_1_subsets:
                if subset not in L_k_1_itemset:
                    candidates_k.remove(candidate)

        return candidates_k

    def apriori(self):
        L_k_1_itemset = self.get_L1_itemset()
        while L_k_1_itemset:
            candidates_k = self.apriori_gen(L_k_1_itemset)
                
            
    def run(self):
        self.apriori()