import sys

from Category import init_categories

class MainFunction(object):
    def __init__(self):
    	pass

    def __del__(self):
    	pass

    def helper(self):
        print "python main.py <bing_key> <BING_ACCOUNT_KEY> <t_es> <t_ec> <host>"
        print "ex. python main.py XXXXXXXXXXXX 0.6 100 yahoo.com"
        sys.exit(1)

    def run(self):
    	root_categ = init_categories()
    	

