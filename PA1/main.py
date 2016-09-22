

import urllib2
import base64
from BingSearchEngine import BingSearchEngine
import sys

class WrongRangePrecisionError(Exception):
    pass


class MainFunction(object):
    def __init__(self):
        self.bse = BingSearchEngine()

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
                    target_precision = int(commands[2])
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

    def query_loop(self):
        query, target_precision = self.arg_parser(sys.argv)
        print "query", query
        print "precision", target_precision

if __name__ == "__main__":
    main = MainFunction()
    main.query_loop()