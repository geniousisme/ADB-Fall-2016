import re
import math

from urlparse import urlparse

from VectorCompute import VectorCompute
from DocumentEnum import TITLE, URL, DESC
from Utils import stop_words, special_chars

class QueryExpansion(object):
    def __init__(self):
        self.vect_com = VectorCompute()
        self.all_word_stats = {}
        self.all_words_vector = []
        self.idf_vector = []
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

    def replace_stop_words(self, input_doc):
        return self.replace_words_with_target_str(input_doc, stop_words)

    def replace_special_chars(self, input_doc):
        return self.replace_words_with_target_str(input_doc, special_chars)

    def get_info_from_url(self, url):
        urlparse_obj = urlparse(url)
        return (urlparse_obj.path + urlparse_obj.params
                + urlparse_obj.query + urlparse_obj.fragment)

    def count_frequency(self, item_str):
        item_stats = {}
        items = self.split_input_doc_to_words(item_str)
        for item in items:
            item = item.lower()
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
                words[i] = words[i].lower()
                i += 1
        return words

    def split_input_doc_to_words(self, input_doc):
        words = input_doc.split(' ')
        words = self.remove_stop_words(words)
        return words

    def initialize_query_expansion(self):
        self.all_word_stats = {}
        self.all_words_vector = []
        self.idf_vector = []

    def build_input_doc(self, res_json):
        input_res_list = [
                res_json[TITLE], 
                # self.get_info_from_url(rexs_json[URL]),
                res_json[DESC]
        ]        
        input_doc = ' '.join(input_res_list)
        # input_doc = self.replace_stop_words(input_doc)
        input_doc = self.replace_special_chars(input_doc)
        return input_doc

    def initialize_query_vector(self, query):
        query_vector = []
        for word in self.all_words_vector:
            if word == query:
                query_vector.append(1.0)
            else:
                query_vector.append(0.0)
        return query_vector

    def build_all_words(self, all_res_jsons):
        self.initialize_query_expansion()
        for res_json in all_res_jsons:
            input_doc = self.build_input_doc(res_json)
            words = self.split_input_doc_to_words(input_doc)
            # print "words in build all words", words
            for word in words:
                word = word.lower()
                #TODO::Some non word issue, ex.\u0252 for musk case
                if self.all_word_stats.get(word):
                    self.all_word_stats[word] += 1.0
                else:
                    self.all_word_stats[word] = 1.0
        self.all_words_vector = self.all_word_stats.keys()
        self.idf_vector = self.compute_idf_vector(all_res_jsons)

    def compute_tf_vector(self, input_doc):
        word_stats = self.count_frequency(input_doc)
        total_freq = sum(word_stats.values())
        # print "total_freq", total_freq
        tf_vector = []
        for word in self.all_words_vector:
            if word_stats.get(word):
                tf_vector.append(word_stats.get(word) / total_freq)
            else:
                tf_vector.append(0)
        # for word in self.all_words_vector:
        #     if word_stats.get(word):
        #         print "word:", word, "freq:", word_stats.get(word), "tf:", (word_stats.get(word) / total_freq)
        
        return tf_vector
    
    def is_word_in_doc(self, word, doc):
        return word in doc.lower()
    
    def compute_idf_vector(self, all_res_jsons):
        D = float(len(all_res_jsons))
        idf_vector = [0] * len(self.all_words_vector)
        # print "all word vector", self.all_words_vector
        for res_json in all_res_jsons:
            input_doc = self.build_input_doc(res_json)
            for idx, word in enumerate(self.all_words_vector):
                #TODO::Some value will be larger than 10, dont know why.
                if self.is_word_in_doc(word, input_doc):
                    idf_vector[idx] += 1
        print "D total document number:", D
        for i in xrange(len(idf_vector)):
            print "word:", self.all_words_vector[i] + ", d # include", self.all_words_vector[i], ":", idf_vector[i]
        for i in xrange(len(idf_vector)):
            idf_vector[i] = math.log(D / idf_vector[i], 2)
        # for i in xrange(len(idf_vector)):
        #     print "word:", self.all_words_vector[i], "idf:", idf_vector[i]
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
        R = len(relevant_res_jsons)
        NR = len(non_relevant_res_jsons)
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
        vectors = [query_vector, relevant_tfidf_vectors_sum, non_relevant_tfidf_vectors_sum]
        rocchio_query_vector = self.vect_com.vector_sum(vectors)
        return rocchio_query_vector

    def get_new_query(self, query, all_res_jsons, 
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
        augmented_words = []
        query_words = self.split_input_doc_to_words(query)
        print query_words
        i = 0
        while len(augmented_words) < 2 and i < len(self.all_words_vector):
            word = self.all_words_vector[i]
            i += 1
            if word in query_words:
                continue
            else:
                augmented_words.append(word)

        print "result word vector\n", self.all_words_vector
        print "augment word 1:", augmented_words[0]
        print "augment word 2:", augmented_words[1]

        return query + " " + augmented_words[0] + " " + augmented_words[1]


if __name__ == "__main__":
    qe = QueryExpansion()
    # test_json = [{u'Description': u'Musk is a class of aromatic substances commonly used as base notes in perfumery. They include glandular secretions from animals such as the musk deer, numerous plants ...', u'Title': u'Musk - Wikipedia, the free encyclopedia', u'Url': u'https://en.wikipedia.org/wiki/Musk', u'__metadata': {u'type': u'WebResult', u'uri': u"https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query='musk'&$skip=0&$top=1"}, u'DisplayUrl': u'https://en.wikipedia.org/wiki/Musk', u'ID':{u'Description': u'Musk definition, a substance secreted in a glandular sac under the skin of the abdomen of the male musk deer, having a strong odor, and used in perfumery. See more.', u'Title': u'Musk | Define Musk at Dictionary.com', u'Url': u'http://www.dictionary.com/browse/musk', u'__metadata': {u'type': u'WebResult', u'uri': u"https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query='musk'&$skip=1&$top=1"}, u'DisplayUrl': u'www.dictionary.com/browse/musk', u'ID': u'739945b9-dfaf-4d00-8d2b-73db4fd1029a'}, {u'Description': u'GUADALAJARA, Mexico \u2014 Elon Musk\u2019s plans to get to Mars start with a really big rocket. For years, Mr. Musk, the billionaire founder of the SpaceX ...', u'Title': u'Elon Musk\u2019s Plan: Get Humans to Mars, and Beyond - The New ...', u'Url': u'http://www.nytimes.com/2016/09/28/science/elon-musk-spacex-mars-exploration.html', u'__metadata': {u'type': u'WebResult', u'uri': u"https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query='musk'&$skip=2&$top=1"}, u'DisplayUrl': u'www.nytimes.com/2016/09/28/science/elon-musk-spacex-mars...', u'ID': u'e6e6fa19-4ac0-4406-9db9-8f7a148a4b53'}, {u'Description': u'When billionaire tech entrepreneur Elon Musk lays out his vision for colonizing Mars, what should viewers and listeners expect? "I think it\'s going to ...', u'Title': u'This Afternoon, Elon Musk Unveils His Plan For Colonizing ...', u'Url': u'http://www.npr.org/sections/thetwo-way/2016/09/27/495622695/this-afternoon-elon-musk-unveils-his-plan-for-colonizing-mars', u'__metadata': {u'type': u'WebResult', u'uri': u"https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query='musk'&$skip=3&$top=1"}, u'DisplayUrl': u'www.npr.org/.../2016/...elon-musk-unveils-his-plan-for-colonizing-mars', u'ID': u'a36e5863-345a-48e6-a042-f6590ff9e29d'}, {u'Description': u'If Elon Musk has his way, a ticket to Mars will one day cost the same as the median U.S. house price \u2014 about $200,000. Not cheap, but arguably affordable.', u'Title': u'Elon Musk Makes His Case for Colonizing Mars - NBC News', u'Url': u'http://www.nbcnews.com/tech/tech-news/elon-musk-makes-his-case-colonizing-mars-n655641', u'__metadata': {u'type': u'WebResult', u'uri': u"https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query='musk'&$skip=4&$top=1"}, u'DisplayUrl': u'www.nbcnews.com/tech/tech-news/elon-musk-makes-his-case-colonizing...', u'ID': u'2ef139c1-89ad-46fd-b1f0-5d8fdc003dae'}, {u'Description': u'SpaceX plans to build a \u201cself-sustaining city\u201d on Mars, company founder Elon Musk announced today. Here\u2019s what we know about how they plan to do it.', u'Title': u'[NEWS] This Is How Elon Musk Plans to Build a City on Mars', u'Url': u'http://gizmodo.com/this-is-how-elon-musk-plans-to-build-a-city-on-mars-up-1787146547', u'__metadata': {u'type': u'WebResult', u'uri': u"https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query='musk'&$skip=5&$top=1"}, u'DisplayUrl': u'gizmodo.com/this-is-how-elon-musk-plans-to-build-a-city-on-mars-up...', u'ID': u'b0a31d9a-1d62-464f-a5a1-37a075175d3f'}, {u'Description': u':a strong-smelling material that is used in perfumes and is obtained from a gland of an Asian deer (musk deer) or is prepared artificially', u'Title': u'Musk | Definition of Musk by Merriam-Webster', u'Url': u'http://www.merriam-webster.com/dictionary/musk', u'__metadata': {u'type': u'WebResult', u'uri': u"https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query='musk'&$skip=6&$top=1"}, u'DisplayUrl': u'www.merriam-webster.com/dictionary/musk', u'ID': u'f3f87a2c-a7ed-444a-b181-6261578f1b27'}, {u'Description': u"The much-anticipated speech comes just a few weeks after one of SpaceX's rockets blew up, leaving questions about the the future of the company.", u'Title': u'Elon Musk offers glimpse of rocket and spacecraft he plans ...', u'Url': u'https://www.washingtonpost.com/news/the-switch/wp/2016/09/27/elon-musk-to-discuss-his-vision-for-how-he-plans-to-colonize-mars/', u'__metadata': {u'type': u'WebResult', u'uri': u"https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query='musk'&$skip=7&$top=1"}, u'DisplayUrl': u'https://www.washingtonpost.com/news/the-switch/wp/2016/09/27/elon...', u'ID': u'4985c733-33ae-4c75-94ab-75e9e4a35885'}, {u'Description': u'Elon Reeve Musk (/ \u02c8 i\u02d0 l \u0252 n \u02c8 m \u028c s k /; born June 28, 1971) is a South African-born Canadian-American business magnate, investor, engineer and ...', u'Title': u'Elon Musk - Wikipedia, the free encyclopedia', u'Url': u'https://en.wikipedia.org/wiki/Elon_Musk', u'__metadata': {u'type': u'WebResult', u'uri': u"https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query='musk'&$skip=8&$top=1"}, u'DisplayUrl': u'https://en.wikipedia.org/wiki/Elon_Musk', u'ID': u'4e576c38-7869-483b-9855-23e39c5b7cce'}, {u'Description': u'SpaceX needs a big rocket to colonize Mars with people, and Elon Musk just debuted the fiery Raptor engine for his Interplanetary Transport System.', u'Title': u"Elon Musk just revealed SpaceX's Raptor rocket engine for ...", u'Url': u'http://www.businessinsider.com/elon-musk-raptor-mars-rocket-engine-2016-9', u'__metadata': {u'type': u'WebResult', u'uri': u"https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query='musk'&$skip=9&$top=1"}, u'DisplayUrl': u'www.businessinsider.com/elon-musk-raptor-mars-rocket-engine-2016-9', u'ID': u'c84a34ce-4837-4f8b-92ff-c1709739a4d3'}]
    test_json = [
        {u'Description': u'When billionaire tech entrepreneur Elon Musk lays out his vision for colonizing Mars, what should viewers and listeners expect? "I think it\'s going to ...', u'Title': u'This Afternoon, Elon Musk Unveils His Plan For Colonizing ...', u'Url': u'http://www.npr.org/sections/thetwo-way/2016/09/27/495622695/this-afternoon-elon-musk-unveils-his-plan-for-colonizing-mars', u'__metadata': {u'type': u'WebResult', u'uri': u"https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query='musk'&$skip=3&$top=1"}, u'DisplayUrl': u'www.npr.org/.../2016/...elon-musk-unveils-his-plan-for-colonizing-mars', u'ID': u'a36e5863-345a-48e6-a042-f6590ff9e29d'},
        {u'Description': u'If Elon Musk has his way, a ticket to Mars will one day cost the same as the median U.S. house price \u2014 about $200,000. Not cheap, but arguably affordable.', u'Title': u'Elon Musk Makes His Case for Colonizing Mars - NBC News', u'Url': u'http://www.nbcnews.com/tech/tech-news/elon-musk-makes-his-case-colonizing-mars-n655641', u'__metadata': {u'type': u'WebResult', u'uri': u"https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query='musk'&$skip=4&$top=1"}, u'DisplayUrl': u'www.nbcnews.com/tech/tech-news/elon-musk-makes-his-case-colonizing...', u'ID': u'2ef139c1-89ad-46fd-b1f0-5d8fdc003dae'},
        # {u'Description': u'SpaceX plans to build a \u201cself-sustaining city\u201d on Mars, company founder Elon Musk announced today. Here\u2019s what we know about how they plan to do it.', u'Title': u'[NEWS] This Is How Elon Musk Plans to Build a City on Mars', u'Url': u'http://gizmodo.com/this-is-how-elon-musk-plans-to-build-a-city-on-mars-up-1787146547', u'__metadata': {u'type': u'WebResult', u'uri': u"https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query='musk'&$skip=5&$top=1"}, u'DisplayUrl': u'gizmodo.com/this-is-how-elon-musk-plans-to-build-a-city-on-mars-up...', u'ID': u'b0a31d9a-1d62-464f-a5a1-37a075175d3f'},
        # {u'Description': u'SpaceX needs a big rocket to colonize Mars with people, and Elon Musk just debuted the fiery Raptor engine for his Interplanetary Transport System.', u'Title': u"Elon Musk just revealed SpaceX's Raptor rocket engine for ...", u'Url': u'http://www.businessinsider.com/elon-musk-raptor-mars-rocket-engine-2016-9', u'__metadata': {u'type': u'WebResult', u'uri': u"https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query='musk'&$skip=9&$top=1"}, u'DisplayUrl': u'www.businessinsider.com/elon-musk-raptor-mars-rocket-engine-2016-9', u'ID': u'c84a34ce-4837-4f8b-92ff-c1709739a4d3'}
    ]
    print qe.build_all_words(test_json)
    # print qe.build_input_doc(test_json[0])
    # test_input_doc = qe.build_input_doc(test_json[0])
    # print qe.build_input_doc(test_json[1])
    # test_input_doc2 = qe.build_input_doc(test_json[1])
    print "all_words_vector", qe.all_words_vector
    # print "=========== tf doc 1 ================="
    # print qe.compute_tf_vector(test_input_doc)
    # print "=========== tf doc 2 ================="
    # print qe.compute_tf_vector(test_input_doc2)
    # print "=========== idf doc ================="
    # print qe.compute_idf_vector(test_json)
    

    # tfidf_vector = qe.compute_weight_vector(test_json)
    # print tfidf_vector
    # print "tfidf vector width", len(tfidf_vector)
    # print "tfidf vector length", len(tfidf_vector[0])
