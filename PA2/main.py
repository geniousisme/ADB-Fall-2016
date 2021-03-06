import sys

from BingSearchEngine import BingSearchEngine
from ContentSummarizer import ContentSummarizer
from QProber import QProber
from Util import WrongRangeError

class MainFunction(object):
    def __init__(self):
        self.qprober = QProber()
        self.cnt_summr = None

    def helper(self):
        print "python main.py <bing_key> <BING_ACCOUNT_KEY> <t_es> <t_ec> <host>"
        print "ex. python main.py XXXXXXXXXXXX 0.6 100 yahoo.com"
        sys.exit(1)

    def arg_parser(self, commands):
        try:
            if len(commands) < 5 or len(commands) > 6:
                self.helper()
            else:
                bing_key = commands[1]
                target_especificity = float(commands[2])
                target_ecoverage = int(commands[3])
                host = commands[4]
                if target_especificity < 0 or target_especificity > 1:
                    raise WrongRangeError
        except ValueError as ve:
            print ve.message
        except WrongRangeError as wre:
            print wre.message
        except:
            sys.exit(1)
        else:
            return bing_key, target_especificity, target_ecoverage, host

    def run(self):
        try:
            bing_key, t_es, t_ec, host = self.arg_parser(sys.argv)
            self.qprober.probe(bing_key, t_es, t_ec, host)
            self.cnt_summr = ContentSummarizer(
                self.qprober.bse.categ_urls_dict, host
            )
            self.cnt_summr.summarize()

        except KeyboardInterrupt:
            print "\n\n\n"
            print "+------------------------------------+"
            print "|      Leaving Proj2 Program....     |"
            print "+------------------------------------+"
            print "Bye ~"
            sys.exit(1)

        
if __name__ == "__main__":
    main = MainFunction()
    main.run()
