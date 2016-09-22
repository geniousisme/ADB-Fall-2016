import base64
import json
import pprint
import urllib2

class BingSearchEngine(object):
	def __init__(self):
		self.account_key = 'qvgP+C20TXdZWmcBz34xkB2Ud0hG34a8IFmr4OpsaPQ'
		self.bing_base_url = 												   \
			'https://api.datamarket.azure.com/Bing/Search/Web?Query='

	def get_search_result(self, response):
		content = json.load(response)
		return content["d"]["results"]

	def search(self, query, top, format='json'):
		bing_url = self.bing_base_url + '%27' + query + '%27&$top=' + str(top) \
			+ '&$format=' + format
		account_key_enccode = 												   \
			base64.b64encode(self.account_key + ':' + self.account_key)
		headers = {'Authorization': 'Basic ' + account_key_enccode}

		request = urllib2.Request(bing_url, headers=headers)
		response = urllib2.urlopen(request)

		return self.get_search_result(response)

if __name__ == "__main__":
	bse = BingSearchEngine()
	pprint.pprint(bse.search("musk", 10), indent=2)

