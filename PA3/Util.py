from __future__ import print_function
from csv import reader
from re import sub

from itertools import combinations, permutations

def get_transactions(filename):
    with open(filename, 'r') as csvfile:
        csv_reader = reader(csvfile, delimiter=',')
        result = []
        for row in csv_reader:
            row_result = []
            for item in row:
                item = replace_non_ascii_with_space(item)
                item = item.strip('\n').strip('\r')
                row_result.append(item)
            result.append(set(row_result))
    return result

def replace_non_ascii_with_space(input_doc):
    return sub(r'[^\x00-\x7F]+', ' ', input_doc)

def get_subsets(k_itemset):
    return set(combinations(k_itemset, len(k_itemset) - 1))

def get_perms(itemsets):
    return list(permutations(itemsets))

def gen_output(min_supp, min_conf, supp_candidate, conf_candidate, output):
    print(
        "==Frequent itemsets (min_sup=" + str(int(min_supp * 100)) + "%)",
        file=output
    )
    for itemset in sorted(
        supp_candidate, key=supp_candidate.get, reverse=True
    ):
        itemset_str = ', '.join(list(itemset.itm_set))
        print(
            '[' + itemset_str + ']'
            + ', ' 
            + str(round(supp_candidate[itemset], 2) * 100) + '%',
            file=output
        )
    print("", file=output)
    print(
        "==High-confidence association rules (min_conf="
        + str(int(min_conf * 100)) + "%)",
        file=output
    )
    for lhs_itemset_rhs in sorted(
        conf_candidate, key=conf_candidate.get, reverse=True
    ):
        lhs_str = '[' + ', '.join(list(lhs_itemset_rhs[0])) + ']'
        rhs_str = '[' + str(lhs_itemset_rhs[1]) + '] '
        itemset_str = lhs_str + " => " + rhs_str
        print(
            itemset_str
            + "(Conf: "
            + str(round(conf_candidate[lhs_itemset_rhs][0], 2) * 100)
            + "%, "
            + "Supp: "
            + str(round(conf_candidate[lhs_itemset_rhs][1], 2) * 100)
            + "%)",
            file=output
        )
