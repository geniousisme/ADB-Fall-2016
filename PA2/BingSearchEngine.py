import base64
import json
import pprint
import urllib2

class BingSearchEngine(object):
    def __init__(self, bing_key, query):
        query = query.replace(' ', "%20")
        self.bing_key = bing_key
        self.bing_base_url = "https://api.datamarket.azure.com/Data.ashx/Bing/SearchWeb/v1/Composite?Query="
        self.bing_search_url = self.bing_base_url + "%27site%3a" + query + "%20premiership%27&$top=10&$format=json"
        self.categ_urls_dict = {}

    def get_search_match_num_and_urls(self, categ_name, query):
        query = query.replace(' ', "%20")
        account_key_enccode = base64.b64encode(self.bing_key + ':' + self.bing_key)
        headers = {'Authorization': 'Basic ' + account_key_enccode}
        request = urllib2.Request(self.bing_search_url, headers=headers)
        response = urllib2.urlopen(request)
        content = json.load(response)
        match_num = int(content["d"]["results"][0]["WebTotal"])
        urls = []

        for i in xrange(4):
            urls.append(content["d"]["results"][0]["Web"][i]["Url"])


        return match_num, 

if __name__ == "__main__":
    bing_key = "qvgP+C20TXdZWmcBz34xkB2Ud0hG34a8IFmr4OpsaPQ"
    query = "yahoo.com"
    bse = BingSearchEngine(bing_key, query)
    results = bse.get_search_results()
    for result in results:
        pprint.pprint(result)