'''
TODO::Imporve the performance, now it take too long to calculate
TODO::some interface is not clear enough to do some modification
TODO::delete some not used func
'''

import re
import math
import string

from VectorCompute import VectorCompute
from DocumentEnum import TITLE, URL, DESC
from Utils import stop_words, special_chars
from Utils import replace_non_ascii_with_space, replace_special_chars
from Utils import clean_up_title, split_input_doc_to_words, count_frequency

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

    def initialize_query_expansion(self):
        self.all_word_stats = {}
        self.all_words_vector = set()
        self.idf_vector = []

    def build_input_doc(self, res_json):
        modified_title = clean_up_title(res_json[TITLE])
        input_res_list = [
                modified_title,
                res_json[URL],
                res_json[DESC]
        ]   
        input_doc = ' '.join(input_res_list)
        input_doc = replace_special_chars(input_doc)
        return input_doc

    def initialize_query_vector(self, query):
        query_vector = []
        query_words = split_input_doc_to_words(query)
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
            words = split_input_doc_to_words(input_doc)
            for word in words:
                #TODO::Some non word issue, ex.\u0252 for musk case
                self.all_words_vector.add(word)
        self.all_words_vector = list(self.all_words_vector)
        self.idf_vector = self.compute_idf_vector(all_res_jsons)

    def compute_tf_vector(self, input_doc):
        word_stats = count_frequency(input_doc)
        total_freq = sum(word_stats.values())
        tf_vector = []
        for word in self.all_words_vector:
            if word_stats.get(word):
                tf_vector.append(word_stats.get(word) / total_freq)
            else:
                tf_vector.append(0)        
        return tf_vector
    
    def is_word_in_doc(self, word, doc):
        return word in split_input_doc_to_words(doc)
    
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

    def get_tfidf_vectors(self, res_jsons):
        tfidf_vectors = []
        for res_json in res_jsons:
            input_doc = self.build_input_doc(res_json)
            tf_vector = self.compute_tf_vector(input_doc)
            tfidf_vector = self.vect_com.dot_product(tf_vector, self.idf_vector)
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
        query_words = split_input_doc_to_words(query)
        augmented_words = []
        i = 0
        while len(augmented_words) < 2 and i < len(self.all_words_vector):
            word = self.all_words_vector[i]
            i += 1
            if word in query_words:
                continue
            else:
                augmented_words.append(word)
        return augmented_words

