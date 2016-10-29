'''
[TODO] Need to Deal With Duplicate url in root url set.
'''
from subprocess import check_output

from Util import Web

class ContentSummarizer(object):
    def __init__(self):
        pass

    def __is_doc_url(self, url):
        return (url[Web.DOC:] == ".pdf" 
                or url[Web.DOC:] == ".ppt"
                or url[Web.DOC:] == ".doc" 
                or url[Web.XDOC:] == ".pptx" 
                or url[Web.XDOC:] == ".docx")
    
    def __fetch_page(self, url):
        if self.__is_doc_url(url):
            print "skip"
            return set()
        try:
            output = check_output("lynx --dump " + url, shell=True)
            '''
            1. Any part of the text after the "References" line should be ignored. 
            2. Also any text within brackets "[....]" should be ignored. 
            3. Any character not in the English alphabet should be treated as a word separator, 
                and the words are case-insensitive. 
            '''
            parsed_output = ""
            references_index = output.find(Web.References)
            is_in_brackets = False
            is_space_already = False
            for i in xrange(references_index):
                char = output[i].lower()
                if not is_in_brackets:
                    if char.isalpha():
                        parsed_output += char
                        is_space_already = False
                    else:
                        if char == '[':
                            is_in_brackets = True
                        if not is_space_already:
                            parsed_output += ' '
                            is_space_already = True
                else:
                    if char == ']':
                        is_in_brackets = False
            return set(parsed_output.split(' '))

        except Exception as e:
            print e
            print "Error occured, pass"
            pass

    def summarize(self):
        pass

if __name__ == "__main__":
    cnt_sumarz = ContentSummarizer()
    print cnt_sumarz.fetch_page('http://sports.yahoo.com/nba/players/837/')
    