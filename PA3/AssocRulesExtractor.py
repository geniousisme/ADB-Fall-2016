from collections import defaultdict

from Candidate import Candidate, ItemSet
from Util import get_transactions, get_subsets

class AssocRulesExtractor(object):
    '''
    Implementation of Apriori Algo, in paper
    "Fast Algorithms for Mining Association Rules"
    Rakesh Agrawal, Ramakrishnan Srikant
    IBM Almaden Research Center
    '''
    def __init__(self, filename, min_supp, min_conf):
        self.filename = filename
        self.min_supp = min_supp
        self.min_conf = min_conf
        self.total_trans = 0
        self.transactions = []
        self.L1_len = 0

    def get_L1_itemset(self):
        L1_itemset = Candidate()
        self.transactions = get_transactions(self.filename)
        self.total_trans = len(self.transactions)
        
        for trans in self.transactions:
            for item in trans:
                if not item:
                    continue
                L1_itemset[item] = (
                    L1_itemset.get(item) + 1.0 / self.total_trans
                )
        L1_itemset_result = []
        for itemset in L1_itemset:
            if L1_itemset.get(itemset) >= self.min_supp:
                L1_itemset_result.append(itemset)
        self.L1_len = len(L1_itemset_result)
        return set(L1_itemset_result)

    def apriori_gen(self, Lk_1_itemset):
        '''
        Take Section 2.1.1 - Apriori Candidate Generation 
        as reference to implement, there are two steps: join & prune
        '''

        '''
        join step, sec 2.1.1, p3
        '''
        Lk_1_itemset_list = list(Lk_1_itemset)
        candidates_k = Candidate()
        for i in xrange(len(Lk_1_itemset_list)):
            for j in xrange(i + 1, len(Lk_1_itemset_list)):
                if Lk_1_itemset_list[i][:-1] == Lk_1_itemset_list[j][:-1]:
                    tmp_candidate_list = (
                        list(Lk_1_itemset_list[i][:])
                        + [Lk_1_itemset_list[j][-1]]
                    )
                    candidates_k.append(tmp_candidate_list)
        '''
        prune step, sec 2.1.1, p4
        '''
        for candidate in candidates_k:
            k_1_subsets = get_subsets(candidate)
            for subset in k_1_subsets:
                if subset not in Lk_1_itemset:
                    candidates_k.remove(candidate)

        return candidates_k
    
    # read paper subset section to confirm the functionality
    def subset(self, candidates, transactions):
        Ct_itemset = Candidate()
        for trans in transactions:
            for candidate in candidates:
                if set(candidate).issubset(trans):
                    Ct_itemset[candidate] = (
                        Ct_itemset.get(candidate) + 1.0 / self.total_trans
                    )
        return Ct_itemset

    def apriori(self):
        '''
        Apriori Algo - p3 - Fig.1
        '''
        Lk_itemset = self.get_L1_itemset()
        idx = 0
        while Lk_itemset and idx < self.L1_len:
            candidates_k = self.apriori_gen(Lk_itemset)
            Ct_itemset = self.subset(candidates_k, self.transactions)
            for ct_candidate in Ct_itemset:
                if Ct_itemset.get(ct_candidate) < self.min_supp:
                    del Ct_itemset[ct_candidate]
            Lk_itemset = Ct_itemset
            idx += 1
            
    def run(self):
        self.apriori()
