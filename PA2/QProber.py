from collections import defaultdict

from BingSearchEngine import BingSearchEngine
from Category import CategName, init_categories

class QProber(object):
    def __init__(self):
        self.bse = None

    def probe(self, bing_key, target_especificity, target_ecoverage, host):
        print "Classifying..."
        self.bse = BingSearchEngine(bing_key)
        self.host = host
        self.categ_specificity_dict = defaultdict(float)
        self.categ_coverage_dict = defaultdict(float)
        self.result_categ_dict = {}
        t_espec = target_especificity
        t_ecov = target_ecoverage
        self.root_categ = init_categories()
        self.result_categ_dict[self.root_categ] = {}
        self.classify(self.root_categ, t_ecov, t_espec, 1.0)
        self.result_categ_dict
    
    def classify(self, src_categ, t_ecov, t_espec, src_categ_espec):
        '''R
        Implementation of 
        '''
        total_coverage = 0
        for sub_categ in src_categ.sub_categs:
            for query in sub_categ.queries:
                self.categ_coverage_dict[sub_categ] += (
                    self.bse.get_match_num(sub_categ, self.host, query)
                )
            total_coverage += self.categ_coverage_dict[sub_categ]

        for sub_categ in src_categ.sub_categs:
            self.categ_specificity_dict[sub_categ] = (
                (src_categ_espec
                * self.categ_coverage_dict[sub_categ]
                / total_coverage)
            )

            print "Specificity for category:", sub_categ, "is", self.categ_specificity_dict[sub_categ]
            print "Coverage for category:", sub_categ, "is", self.categ_coverage_dict[sub_categ]

            if (self.categ_specificity_dict[sub_categ] >= t_espec and 
                    self.categ_coverage_dict[sub_categ] >= t_ecov):
                if src_categ == self.root_categ:
                    self.result_categ_dict[src_categ][sub_categ] = []
                    self.classify(
                        sub_categ, 
                        t_ecov, 
                        t_espec, 
                        self.categ_specificity_dict[sub_categ]
                    )
                else:
                    self.result_categ_dict[self.root_categ][
                        src_categ
                    ].append(sub_categ)




