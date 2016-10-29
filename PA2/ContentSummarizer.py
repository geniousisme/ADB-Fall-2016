'''
[TODO] Need to Deal With Duplicate url in root url set.
'''
from subprocess import check_output
from Category import CategName

from Util import Web

class ContentSummarizer(object):
    def __init__(self, categ_urlset_dict):
        self.categ_urlset_dict = categ_urlset_dict
        self.urls_len = 0
        self.root_urlset = set()

    def __is_doc_url(self, url):
        return (url[Web.DOC:] == ".pdf" 
                or url[Web.DOC:] == ".ppt"
                or url[Web.DOC:] == ".doc" 
                or url[Web.XDOC:] == ".pptx" 
                or url[Web.XDOC:] == ".docx")
    
    def __page_parser(self, page):
        '''Return set of words
        1. Any part of the text after the "References" line should be ignored.
        2. Also any text within brackets "[....]" should be ignored.
        3. Any character not in the English alphabet should be
            treated as a word separator, and the words are case-insensitive.
        '''
        parsed_page = ""
        references_index = page.find(Web.References)
        is_in_brackets = False
        is_space_already = False
        for i in xrange(references_index):
            char = page[i].lower()
            if not is_in_brackets:
                if char.isalpha():
                    parsed_page += char
                    is_space_already = False
                else:
                    if char == '[':
                        is_in_brackets = True
                    if not is_space_already:
                        parsed_page += ' '
                        is_space_already = True
            else:
                if char == ']':
                    is_in_brackets = False
        return set(parsed_page.split(' '))

    def __fetch_page(self, url):
        '''Return set of words from the url page
        Fetch page through lynx and parse the page
        '''
        if self.__is_doc_url(url):
            print "skip"
            return set()
        try:
            page_output = check_output("lynx --dump " + url, shell=True)
            return self.__page_parser(page_output)

        except Exception as e:
            print e
            print "Error occured, pass"
            pass

    def __summarize_for_categ(self, categ):
        '''Return word document frequency stats(i.e. dictionary) for the categ,
        input: Category class, plz look through Category class code
        output: dictionary, which is java hash_map, ex. {'a':123, 'aaa':345, 'dog':3,...}
        
        Requirement: 
        Should seperate two cases, if categ is "Root" and if categ is not "Root".
        Try to eliminate the time to fetch the page, you can get clues from my code.
        [Hint] use self.root_urlset
        '''
        urlset = self.categ_urlset_dict[categ]
        # Write your code here...

    def summarize(self):
        root_categ = None
        for categ in self.categ_urlset_dict:
            if categ.name == CategName.Root:
                root_categ = categ
                continue
            self.__summarize_for_categ(categ)

        # Eliminate fetched urlset from root urlset
        self.categ_urlset_dict[root_categ] = (
            self.categ_urlset_dict[root_categ] - self.root_urlset
        )
        self.__summarize_for_categ(root_categ)


if __name__ == "__main__":
    cnt_sumarz = ContentSummarizer()
    print cnt_sumarz.fetch_page('http://sports.yahoo.com/nba/players/837/')
    