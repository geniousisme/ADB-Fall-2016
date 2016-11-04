from requests import head
from subprocess import check_output

from Util import Web

class ContentSummarizer(object):
    def __init__(self, categ_urlset_dict, host):
        self.categ_urlset_dict = categ_urlset_dict
        self.host = host
        self.root_urlset = set()
        self.root_content_summary = {}

    def __is_non_html_url(self, url):
        r = head(url)
        return "text/html" not in r.headers["content-type"]
    
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

        # Follow Professor Java parser script to implement
        parsed_page = ""
        recording = True
        wrotespace = False
        for i in xrange(end):
            char = page[i]
            if recording:
                if char == '[':
                    recording = False
                    if not wrotespace:
                        parsed_page += ' '
                        wrotespace = True
                    continue
                else:
                    if char.isalpha() and ord(char) < 128:
                        parsed_page += char.lower()
                        wrotespace = False
                    else:
                        if not wrotespace:
                            parsed_page += ' '
                            wrotespace = True
            else:
                if char == ']':
                    recording = True
                    continue
        return set(parsed_page.split())

    def __fetch_page(self, url):
        '''Return set of words from the url page
        Fetch page through lynx and parse the page
        '''
        print "Getting page:", url

        if self.__is_non_html_url(url):
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
        print "Creating Content Summary for:" + categ.name
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
        print "Extracting topic content summaries..."
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
    
