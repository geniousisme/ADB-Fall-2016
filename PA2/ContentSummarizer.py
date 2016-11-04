from subprocess import check_output

from Util import Web

class ContentSummarizer(object):
    def __init__(self, categ_urlset_dict, host):
        self.categ_urlset_dict = categ_urlset_dict
        self.host = host
        self.root_urlset = set()
        self.root_content_summary = {}

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
            treated as a word separator, and the words are not case-sensitive.
        '''
        parsed_page = ""
        references_index = page.find(Web.References)
        end = references_index if references_index > -1 else len(page)
        is_in_brackets = False
        is_space_already = False
        for i in xrange(end):
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
        return set(parsed_page.split())

    def __fetch_page(self, url):
        '''Return set of words from the url page
        Fetch page through lynx and parse the page
        '''
        print "Getting page:", url

        if self.__is_doc_url(url):
            print "skip\n\n"
            return set()
        try:
            page_output = check_output("lynx --dump " + url, shell=True)
            print "\n\n"
            return self.__page_parser(page_output)

        except Exception as e:
            print e
            print "Error occured, pass\n\n"
            return set()

    def __summarize_for_categ(self, categ):
        urlset = self.categ_urlset_dict[categ]
        urlset_len = len(urlset)
        if not categ.is_root_categ():
            content_summary = {}
        else:
            content_summary = self.root_content_summary

        # Count word document frequency
        url_count = 1
        for url in urlset:
            print url_count, '/', urlset_len
            page_wordset = self.__fetch_page(url)
            for word in page_wordset:
                content_summary[word] = content_summary.get(word, 0.0) + 1.0
                if not categ.is_root_categ() and url not in self.root_urlset:
                    self.root_content_summary[word] = (
                        self.root_content_summary.get(word, 0.0) + 1.0
                    )
            url_count += 1

        # Record the word doc freq into the file
        f = open(categ.name + '-' + self.host + '.txt', 'w')
        for word, freq in sorted(content_summary.items()):
            f.write(word + '#' + str(freq) + '\n')
        f.close()

    def summarize(self):
        root_categ = None
        for categ in self.categ_urlset_dict:
            if categ.is_root_categ():
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
    