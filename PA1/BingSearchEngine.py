import base64
import json
import pprint
import urllib2

class BingSearchEngine(object):
    def __init__(self, bing_key, query):
    	query = query.replace(' ', "%20")
    	self.bing_key = bing_key
        self.bing_base_url = 'https://api.datamarket.azure.com/Bing/Search/Web?Query='
        self.bing_search_url = self.bing_base_url + '%27' + query + '%27&$top=10&$format=json'

    def get_search_result(self, response):
        content = json.load(response)
        return content["d"]["results"]

    def search(self):
        account_key_enccode = base64.b64encode(self.bing_key + ':' + self.bing_key)
        headers = {'Authorization': 'Basic ' + account_key_enccode}
        request = urllib2.Request(self.bing_search_url, headers=headers)
        response = urllib2.urlopen(request)

        return self.get_search_result(response)