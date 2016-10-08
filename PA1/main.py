import urllib2
import base64
import sys

from BingSearchEngine import BingSearchEngine
from DocumentEnum import TITLE, URL, DESC
from QueryExpansion import QueryExpansion
from Utils import WrongRangePrecisionError, replace_non_ascii_with_space, replace_special_chars

class MainFunction(object):
    def __init__(self):
        self.qe = QueryExpansion()
        self.transcript = open("transcript.txt", "a+")

    def __del__(self):
        self.transcript.close()

    def helper(self):
        print "python main.py <bing_key> <target precision> <query>"
        print "ex. python main.py XXXXXXXXXXXX 0.9 musk"
        sys.exit(1)
    
    def arg_parser(self, commands):
        query = ""
        try:
            if len(commands) < 4 or len(commands) > 5:
                self.helper()
            if len(commands) == 4:
                bing_key = commands[1]
                target_precision = float(commands[2])
                query = commands[3]
                if target_precision < 0 or target_precision > 1:
                    raise WrongRangePrecisionError
        except ValueError:
            print "please input the number type value between 0 - 1 for precision"
            sys.exit(1)
        except WrongRangePrecisionError:
            print "please input the precision value between 0 - 1"
            sys.exit(1)
        else:
            return bing_key, query, target_precision

    def is_relevant(self, yes_or_no_relevant_str):
        yes_or_no_relevant_str = yes_or_no_relevant_str.lower()
        self.transcript.write("Relevant ")
        if yes_or_no_relevant_str == 'y':
            self.transcript.write("YES\n")
            return True
        elif yes_or_no_relevant_str == 'n':
            self.transcript.write("NO\n")
            return False
        else:
            self.transcript.write("NO\n")
            print "Cannot recognise the answer, count as not relevant."
            return False

    def feedback_summary(self, query, curr_precision, target_precision):
        print "\n======================\nFEEDBACK SUMMARY"
        print "Query", query
        print "Precision", curr_precision

    def params_info(self, bing_key, query, target_precision, search_url):
        print "Parameters:"
        print "Client key  =", bing_key
        print "Query       =", query
        print "Precision   =", target_precision
        print "URL:", search_url
        print "Total no of results : 10"
        print "Bing Search Results:"
        print "======================"

    def result_str(self, url, title, desc):
        url_str = "  Url: " + url
        title_str = "  Title: " + title
        desc_str = "  Summary: " + desc
        return '\n'.join(['[', url_str, title_str, desc_str, "]\n\n\n"])

    def query_loop(self):
        bing_key, query, target_precision = self.arg_parser(sys.argv)
        iter_round = 0
        try:
            while True:
                iter_round += 1
                relevant_results = []
                non_relecant_results = []
                curr_precision = relevance = 0
                self.transcript.write("=====================================\n")
                self.transcript.write("ROUND " + str(iter_round) + "\n")
                self.transcript.write("QUERY " + query + "\n\n")
                self.bse = BingSearchEngine(bing_key, query)
                self.params_info(
                    bing_key, query, target_precision, self.bse.bing_search_url
                )
                search_results = self.bse.search()
                for idx, result in enumerate(search_results):
                    self.transcript.write("Result " + str(idx + 1) + "\n")
                    print "Result " + str(idx + 1)
                    print "["
                    print "  Url:", result[URL]
                    print "  Title:", result[TITLE]
                    print "  Summary:", result[DESC]
                    print "]"
                    yes_or_no_relevant_str = raw_input(
                        "===> Is this result relevant? (Y/N) "
                    )
                    if self.is_relevant(yes_or_no_relevant_str):
                        relevant_results.append(result)
                        relevance += 1
                    else:
                        non_relecant_results.append(result)
                    
                    self.transcript.write(
                        self.result_str(
                            result[URL],
                            replace_non_ascii_with_space(result[TITLE]),
                            replace_non_ascii_with_space(result[DESC])
                        )
                    )

                curr_precision = float(relevance) / 10
                self.transcript.write("PRECISION " + str(curr_precision) + "\n")
                self.feedback_summary(query, curr_precision, target_precision)
                if curr_precision >= target_precision:
                    print "Desired precision reached, done"
                    return 
                if curr_precision == 0:
                    print "Below desired precision, but can no longer augment the query"
                    return
                else:
                    print "Still below the desired precision of", target_precision
                    print "Indexing results ...."
                    augmented_words = self.qe.get_augmented_words(
                        query, search_results, relevant_results, non_relecant_results
                    )
                    print "Indexing results ...."
                    print "Augmenting by", augmented_words[0], augmented_words[1]
                    query = query + ' ' + ' '.join(augmented_words)
                    continue
        except KeyboardInterrupt:
            print "\n\n\n"
            print "+------------------------------------+"
            print "| Leaving Query Expansion Program....|"
            print "+------------------------------------+"
            print "Bye ~"
            sys.exit(1)

if __name__ == "__main__":
    main = MainFunction()
    main.query_loop()