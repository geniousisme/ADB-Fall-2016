import base64
import json
import pprint
import urllib2

class BingSearchEngine(object):
    def __init__(self):
        self.bing_base_url = 'https://api.datamarket.azure.com/Bing/Search/Web?Query='

    def get_search_result(self, response):
        content = json.load(response)
        return content["d"]["results"]

    def search(self, bing_key, query, top=10, format='json'):
        query = query.replace(' ', "%20")
        bing_url = self.bing_base_url + '%27' + query + '%27&$top=' + str(top) \
            + '&$format=' + format
        account_key_enccode = base64.b64encode(bing_key + ':' + bing_key)
        headers = {'Authorization': 'Basic ' + account_key_enccode}

        request = urllib2.Request(bing_url, headers=headers)
        response = urllib2.urlopen(request)

        return self.get_search_result(response)

if __name__ == "__main__":
    bse = BingSearchEngine()
    results = bse.search("musk")
    pprint.pprint(results, indent=2)

