import urllib2
import base64
import sys

from BingSearchEngine import BingSearchEngine
from DocumentEnum import TITLE, URL, DESC
from QueryExpansion import QueryExpansion



class WrongRangePrecisionError(Exception):
    pass

class MainFunction(object):
    def __init__(self):
        self.bse = BingSearchEngine()
        self.qe = QueryExpansion()

    def helper(self):
        print "python main.py <query> <target precision>"
        print "ex. python main.py 'musk' 0.9"
        sys.exit(1)
    
    def arg_parser(self, commands):
        target_precision = 0.9
        query = ""
        try:
            if len(commands) < 2 or len(commands) > 3:
                self.helper()
            if len(commands) >= 2:
                query = commands[1]
                if len(commands) == 3:
                    target_precision = float(commands[2])
            if  target_precision < 0 or target_precision > 1:
                raise WrongRangePrecisionError
        except ValueError:
            print "please input the number type value between 0 - 1 for precision"
            sys.exit(1)
        except WrongRangePrecisionError:
            print "please input the precision value between 0 - 1"
            sys.exit(1)
        else:
            return query, target_precision

    def is_relevant(self, yes_or_no_relevant_str):
        if yes_or_no_relevant_str.lower() == 'y':
            return True
        if yes_or_no_relevant_str.lower() == 'n':
            return False
        else:
            print "Cannot recognise the answer, count as not relevant."
            return False

    def current_summary(self, curr_precision, target_precision):
        print "\n\n\n======== Current Summary ========"
        print "Target Precision Value:", target_precision
        print "Current Precision Value:", curr_precision

    def query_loop(self):
        curr_precision = 0
        query, target_precision = self.arg_parser(sys.argv)
        relevant_results = []
        non_relecant_results = []
        relevance = 0
        try:
            while True:
                search_results = self.bse.search(query)
                for idx, result in enumerate(search_results):
                    print "--------------------------------"
                    print "Result " + str(idx + 1) + ": "
                    print "Title:", result[TITLE]
                    print "Url:", result[URL]
                    print "Description:", result[DESC]
                    yes_or_no_relevant_str =                                   \
                        raw_input("===> Is this result relevant? (Y/N) ")
                    if self.is_relevant(yes_or_no_relevant_str):
                        relevant_results.append(result)
                        relevance += 1
                    else:
                        non_relecant_results.append(result)
                curr_precision = float(relevance) / 10
                self.current_summary(curr_precision, target_precision)
                if curr_precision >= target_precision:
                    print "Reach the target precision value, yeah!"
                    return 
                if curr_precision == 0:
                    print "So sad, no matching result, stop."
                    return
                if curr_precision == 1:
                    print "100% relevant!! Yeah!"
                    return
                else:
                    print "Current precision is still lower than "             \
                        "target precision value, continue"
                    query = self.qe.get_new_query(
                        query, relevant_results, non_relecant_results, search_results
                    )
                    print search_results
                    print "new query:", query
                    continue
        except KeyboardInterrupt:
            print "\n====================================="
            print "Leaving Query Expansion Program...."
            print "====================================="
            sys.exit(1)

if __name__ == "__main__":
    main = MainFunction()
    main.query_loop()