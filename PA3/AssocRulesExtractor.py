from collections import OrderedDict

from Candidate import Candidate, ItemSet
from Util import get_transactions, get_subsets, get_perms, gen_output
from Util import loading_animation

class AssocRulesExtractor(object):
    '''
    Implementation of Apriori Algo, in paper
    "Fast Algorithms for Mining Association Rules"
    Rakesh Agrawal, Ramakrishnan Srikant
    IBM Almaden Research Center
    '''
    def __init__(self, filename, min_supp, min_conf):
        print "Loading",
        self.filename = filename
        self.min_supp = min_supp
        self.min_conf = min_conf
        self.total_trans = 0
        self.transactions = []
        self.supp_candidate = Candidate()
        self.conf_candidate = OrderedDict()
        self.output = open('output.txt', 'w')

    def __del__(self):
        self.output.close()
        del self.output
        print

    def get_candidate_with_min_supp(self, src_candidate):
        for itemset in src_candidate:
            if src_candidate.get(itemset) < self.min_supp:
                del src_candidate[itemset]
        self.supp_candidate.extend(src_candidate)
        return src_candidate

    def gen_associate_rules_with_min_conf(self, src_candidate):
        if not src_candidate:
            return
        for itemset in src_candidate:
            assoc_rules = get_perms(itemset)
            for rule in assoc_rules:
                lhs = rule[:-1]
                rhs = rule[-1]
                conf = (
                    self.supp_candidate[ItemSet(rule)]
                    / self.supp_candidate[ItemSet(lhs)]
                )
                if conf >= self.min_conf:
                    self.conf_candidate[tuple([ItemSet(lhs), rhs])] = (
                        conf, self.supp_candidate[ItemSet(rule)]
                    )
        
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
        L1_itemset = self.get_candidate_with_min_supp(L1_itemset)
        return L1_itemset

    def apriori_gen(self, Lk_1_itemset):
        '''
        Take Section 2.1.1 - Apriori Candidate Generation 
        as reference to implement, there are two steps: join & prune
        '''

        '''
        join step, sec 2.1.1, p3
        '''
        Lk_1_itemset_list = list(Lk_1_itemset)
        candidate_k = Candidate()
        for i in xrange(len(Lk_1_itemset_list)):
            for j in xrange(i + 1, len(Lk_1_itemset_list)):
                if Lk_1_itemset_list[i][:-1] == Lk_1_itemset_list[j][:-1]:
                    tmp_candidate_list = (
                        list(Lk_1_itemset_list[i][:])
                        + [Lk_1_itemset_list[j][-1]]
                    )
                    candidate_k.append(tmp_candidate_list)
        '''
        prune step, sec 2.1.1, p4
        '''
        for itemset in candidate_k:
            k_1_subsets = get_subsets(itemset)
            for subset in k_1_subsets:
                if subset not in Lk_1_itemset:
                    del candidate_k[itemset]
                    break
        return candidate_k

    def subset(self, candidate, transactions):
        '''
        Didn't follow the approach in sec 2.1.2,
        only use the concept in sec 2.1 Fig.1 line 5 to implement.
        '''
        Ct_candidate = Candidate()
        for trans in transactions:
            for itemset in candidate:
                if itemset.is_subset_of(trans):
                    Ct_candidate[itemset] = (
                        Ct_candidate.get(itemset) + 1.0 / self.total_trans
                    )
        return Ct_candidate

    def apriori(self):
        '''
        Apriori Algo - p3 - Fig.1
        '''
        Lk_itemset = self.get_L1_itemset()
        while Lk_itemset:
            candidate_k = self.apriori_gen(Lk_itemset)
            Ct_candidate = self.subset(candidate_k, self.transactions)
            Lk_itemset = self.get_candidate_with_min_supp(Ct_candidate)
            self.gen_associate_rules_with_min_conf(Lk_itemset)
            loading_animation()
            
        gen_output(
            self.min_supp, 
            self.min_conf, 
            self.supp_candidate, 
            self.conf_candidate, 
            self.output
        )
            