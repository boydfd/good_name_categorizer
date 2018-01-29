import codecs
import operator
import logging
import os

from gensim import corpora, models, similarities
from jieba import posseg

import jieba


def get_path(path):
    directory = os.path.dirname(__file__)
    return os.path.join(directory, path)


class Similarity:
    def __init__(self, category, user_dict_path=None):
        if user_dict_path:
            logging.info('start loading user dictionary')
            jieba.load_userdict(user_dict_path)
            logging.info('end loading user dictionary')
        self.category = category
        self.category_num = len(self.category.list)
        self.stopwords = None
        self.stop_flag = None
        self.dictionary = None
        self.lsi = None
        self.lsi_vector = None
        self.init_stop_words()
        logging.info('start calculate category vector')
        self.init_category()
        logging.info('end calculate category vector')

    def init_stop_words(self):
        stop_words = get_path('./stop_words.txt')
        stopwords = codecs.open(stop_words, 'r', encoding='utf8').readlines()
        self.stopwords = [w.strip() for w in stopwords]
        self.stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']

    def tokenize_with_path(self, filename):
        with open(filename, 'r') as f:
            text = f.read()
            return self.tokenize(text)

    def tokenize(self, text):
        result = []
        words = posseg.cut(text)
        for word, flag in words:
            if flag not in self.stop_flag and word not in self.stopwords:
                result.append(word)
        return result

    def init_category(self):
        corpus = []
        texts_dict = self.category.get_texts_dict()
        for category in self.category.list:
            corpus.append(self.tokenize(texts_dict[category]))
        dictionary = corpora.Dictionary(corpus)
        self.dictionary = dictionary

        doc_vectors = [dictionary.doc2bow(text) for text in corpus]

        tfidf = models.TfidfModel(doc_vectors)
        tfidf_vectors = tfidf[doc_vectors]

        lsi = models.LsiModel(tfidf_vectors, id2word=dictionary, num_topics=len(corpus))
        self.lsi = lsi
        self.lsi_vector = lsi[tfidf_vectors]

    def format_similarity(self, sims):
        sims = list(enumerate(sims))
        sims = sorted(sims, key=operator.itemgetter(1), reverse=True)[:5]

        def parse_similarity_to_string(index, similarity):
            category_name = self.category.list[index]
            return 'name:%s sub:%s sim:%s' % (
                self.category.inverse_words[category_name],
                category_name,
                similarity
            )

        return [parse_similarity_to_string(*item) for item in sims]

    def get_result_category_from_similarity(self, sims):
        if len(sims) == 0:
            return ""
        sims = list(enumerate(sims))
        sims = sorted(sims, key=operator.itemgetter(1), reverse=True)[0]

        def parse_similarity_to_string(index):
            category_name = self.category.list[index]
            return self.category.inverse_words[category_name]

        return parse_similarity_to_string(sims[0])

    def calculate_similarity_lsi(self, query):
        query = self.tokenize(query)
        query_bow = self.dictionary.doc2bow(query)
        query_lsi = self.lsi[query_bow]
        index = similarities.MatrixSimilarity(self.lsi_vector, num_features=len(self.dictionary))
        sims = index[query_lsi]
        return sims
