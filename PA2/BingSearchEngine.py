import base64
import json
import pprint
import urllib2

from Category import CategName

from collections import defaultdict

class BingSearchEngine(object):
    def __init__(self, bing_key):
        self.bing_key = bing_key
        self.bing_base_url = "https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/v1/Composite?Query="
        self.categ_urls_dict = defaultdict(set)
        
    def get_match_num(self, categ, host, query):
        query = query.replace(' ', "%20")
        account_key_enccode = base64.b64encode(self.bing_key + ':' + self.bing_key)
        headers = {'Authorization': 'Basic ' + account_key_enccode}
        bing_search_url = self.bing_base_url + "%27site%3a" + host + "%20" + query +"%27&$top=10&$format=json"
        request = urllib2.Request(bing_search_url, headers=headers)
        response = urllib2.urlopen(request)
        content = json.load(response)
        match_num = float(content["d"]["results"][0]["WebTotal"])
        web_results = content["d"]["results"][0]["Web"]
        
        # Collect urls for Category
        urls = set()
        for i in xrange(len(web_results)):
            if i == 4:
                break
            urls.add(web_results[i]["Url"])
        self.categ_urls_dict[categ.parent_categ].update(urls)
        
        return match_num

if __name__ == "__main__":
    bing_key = "qvgP+C20TXdZWmcBz34xkB2Ud0hG34a8IFmr4OpsaPQ"
    query = "yahoo.com"
    bse = BingSearchEngine(bing_key)
    results = bse.get_match_num(None, query)
    