'''
TODO::Imporve the performance, now it take too long to calculate
TODO::some interface is not clear enough to do some modification
TODO::delete some not used func
'''

import re
import math
import string

from urlparse import urlparse

from VectorCompute import VectorCompute
from DocumentEnum import TITLE, URL, DESC
from Utils import stop_words, special_chars

class QueryExpansion(object):
    def __init__(self):
        self.vect_com = VectorCompute()
        self.all_word_stats = {}
        self.all_words_vector = set()
        self.idf_vector = []

        # param for Rocchio
        self.alpha = 1.0
        self.beta = 0.75
        self.gama = 0.15

    def replace_words_with_target_str(self, input_doc, 
            replaced_words, target_str=" "):
        replaced_words_regex = re.compile(
            '|'.join(map(re.escape, replaced_words))
        )
        updated_text = replaced_words_regex.sub(target_str, input_doc)
        return updated_text

    def replace_non_ascii_with_space(self, input_doc):
        return re.sub(r'[^\x00-\x7F]+', ' ', input_doc)

    def replace_special_chars(self, input_doc):
        input_ascii_doc = self.replace_non_ascii_with_space(input_doc)
        return self.replace_words_with_target_str(input_ascii_doc, special_chars)

    def get_info_from_url(self, url):
        urlparse_obj = urlparse(url)
        return (urlparse_obj.path + urlparse_obj.params
                + urlparse_obj.query + urlparse_obj.fragment)

    def count_frequency(self, item_str):
        item_stats = {}
        items = self.split_input_doc_to_words(item_str)
        for item in items:
            if item_stats.get(item):
                item_stats[item] += 1.0
            else:
                item_stats[item] = 1.0
        return item_stats

    def remove_stop_words(self, words):
        i = 0
        while i < len(words):
            if words[i].lower() in stop_words or words[i] == '':
                words.pop(i)
            else:
                if not isinstance(words[i], str):
                    words[i] = words[i].encode('utf-8')
                words[i] = words[i].lower()
                i += 1
        return words

    def split_input_doc_to_words(self, input_doc):
        words = input_doc.split(' ')
        words = self.remove_stop_words(words)
        return words

    def initialize_query_expansion(self):
        self.all_word_stats = {}
        self.all_words_vector = set()
        self.idf_vector = []

    def build_input_doc(self, res_json):
        input_res_list = [
                res_json[TITLE], 
                res_json[URL],
                res_json[DESC]
        ]        
        input_doc = ' '.join(input_res_list)
        input_doc = self.replace_special_chars(input_doc)
        return input_doc

    def initialize_query_vector(self, query):
        query_vector = []
        query_words = self.split_input_doc_to_words(query)
        for word in self.all_words_vector:
            if word in query_words:
                query_vector.append(1.0)
            else:
                query_vector.append(0.0)
        return query_vector

    def build_all_words(self, all_res_jsons):
        self.initialize_query_expansion()
        for res_json in all_res_jsons:
            input_doc = self.build_input_doc(res_json)
            words = self.split_input_doc_to_words(input_doc)
            for word in words:
                #TODO::Some non word issue, ex.\u0252 for musk case
                self.all_words_vector.add(word)
        self.all_words_vector = list(self.all_words_vector)
        self.idf_vector = self.compute_idf_vector(all_res_jsons)

    def compute_tf_vector(self, input_doc):
        word_stats = self.count_frequency(input_doc)
        total_freq = sum(word_stats.values())
        tf_vector = []
        for word in self.all_words_vector:
            if word_stats.get(word):
                tf_vector.append(word_stats.get(word) / total_freq)
            else:
                tf_vector.append(0)        
        return tf_vector
    
    def is_word_in_doc(self, word, doc):
        return word in self.split_input_doc_to_words(doc)
    
    def compute_idf_vector(self, all_res_jsons):
        D = float(len(all_res_jsons))
        idf_vector = [0.0] * len(self.all_words_vector)
        for res_json in all_res_jsons:
            input_doc = self.build_input_doc(res_json)
            for idx, word in enumerate(self.all_words_vector):
                if self.is_word_in_doc(word, input_doc):
                    idf_vector[idx] += 1.0
        for i in xrange(len(idf_vector)):
            idf_vector[i] = math.log(D / idf_vector[i], 2)
        return idf_vector

    def get_factor_vector(self, res_jsons):
        factor_vector = [1] * len(self.all_words_vector)
        for res_json in res_jsons:
            input_title_doc = self.replace_special_chars(res_json[TITLE])
            title_words = self.split_input_doc_to_words(input_title_doc)
            for idx, word in enumerate(self.all_words_vector):
                if word in title_words:
                    factor_vector[idx] = 1.2
        return factor_vector

    def get_tfidf_vectors(self, res_jsons):
        tfidf_vectors = []
        # factor_vector = self.get_factor_vector(res_jsons)
        for res_json in res_jsons:
            input_doc = self.build_input_doc(res_json)
            tf_vector = self.compute_tf_vector(input_doc)
            tfidf_vector = self.vect_com.dot_product(tf_vector, self.idf_vector)
            # tfidf_vector = self.vect_com.dot_product(tfidf_vector, factor_vector)
            tfidf_vectors.append(tfidf_vector)
        return tfidf_vectors
    
    def compute_weight_vector(self, query, all_res_jsons, 
            relevant_res_jsons, non_relevant_res_jsons):
        self.build_all_words(all_res_jsons)
        query_vector = self.initialize_query_vector(query)
        tfidf_vectors = []
        R = len(relevant_res_jsons) if relevant_res_jsons else 1
        NR = len(non_relevant_res_jsons) if non_relevant_res_jsons else 1

        relevant_tfidf_vectors = self.get_tfidf_vectors(
            relevant_res_jsons
        )
        non_relevant_tfidf_vectors = self.get_tfidf_vectors(
            non_relevant_res_jsons
        )
        # Rocchio's Algo
        relevant_tfidf_vectors_sum = self.vect_com.vector_sum(
            relevant_tfidf_vectors
        )
        non_relevant_tfidf_vectors_sum = self.vect_com.vector_sum(
            non_relevant_tfidf_vectors
        )
        query_vector = self.vect_com.vector_multiply(
            query_vector,
            self.alpha
        )
        relevant_tfidf_vectors_sum = self.vect_com.vector_multiply(
            relevant_tfidf_vectors_sum,
            self.beta / R
        )
        non_relevant_tfidf_vectors_sum = self.vect_com.vector_multiply(
            non_relevant_tfidf_vectors_sum,
             -self.gama / NR
        )
        vectors = []
        if query_vector:
            vectors.append(query_vector)
        if relevant_tfidf_vectors_sum:
            vectors.append(relevant_tfidf_vectors_sum)
        if non_relevant_tfidf_vectors_sum:
            vectors.append(non_relevant_tfidf_vectors_sum)
        rocchio_query_vector = self.vect_com.vector_sum(vectors)

        return rocchio_query_vector

    def get_augmented_words(self, query, all_res_jsons, 
            relevant_res_jsons, non_relevant_res_jsons):
        word_weight_dict = {}
        weight_vector = self.compute_weight_vector(
            query, all_res_jsons, relevant_res_jsons, non_relevant_res_jsons
        )
        for idx, word in enumerate(self.all_words_vector):
            word_weight_dict[word] = weight_vector[idx]

        self.all_words_vector = sorted(
            self.all_words_vector, key=word_weight_dict.get, reverse=True
        )
        
        # pick two words from the sorted word vector
        query_words = self.split_input_doc_to_words(query)
        augmented_words = []
        i = 0
        while len(augmented_words) < 2 and i < len(self.all_words_vector):
            word = self.all_words_vector[i]
            i += 1
            if word in query_words or not isinstance(word, str):
                continue
            else:
                augmented_words.append(word)
        return augmented_words
