from DocumentEnum import TITLE, URL, DESC

class QueryExpansion(object):
	def __init__(self):
		self.tf = []
		self.idf = []

	def generate_new_query(self, old_query, relevant_res, non_relevant_res):
		return old_query

