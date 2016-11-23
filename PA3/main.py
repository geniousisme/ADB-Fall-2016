import sys

from AssocRulesExtractor import AssocRulesExtractor
from Error import WrongRangeError

class MainFunc(object):
    def __init__(self):
        self.are = None

    def helper(self):
        print "python main.py <INTEGRATED_DATASET_FILENAME> <min_supp> <min_conf>"
        print "ex. python main.py INTEGRATED-DATASET.csv 0.3 0.5"
        sys.exit(1)

    def arg_parser(self, commands):
        try:
            if len(commands) < 4 or len(commands) > 4:
                self.helper()
            else:
                file_name = commands[1]
                min_supp = float(commands[2])
                min_conf = float(commands[3])
                if (min_supp < 0 or min_supp > 1 
                        or min_conf < 0 or min_conf > 1):
                    raise WrongRangeError

        except ValueError as ve:
            print ve.message
            sys.exit(1)

        except WrongRangeError as wre:
            print wre.message
            sys.exit(1)

        else:
            return file_name, min_supp, min_conf

    def run(self):
        file_name, min_supp, min_conf = self.arg_parser(sys.argv)
        self.are = AssocRulesExtractor(file_name, min_supp, min_conf)
        self.are.apriori()


if __name__ == "__main__":
    main = MainFunc()
    main.run()