from resources.category import Category
import os
import numpy as np
import pickle

from similarity.main import Similarity
from utilities import get_model


def get_path(path):
    directory = os.path.dirname(__file__)
    return os.path.join(directory, path)


category_texts_path = get_path('./category_texts/')

category = Category(get_path('./category.yml'), category_texts_path)

user_dict_path = get_path('./dictionaries/filtered_dict_without_english.csv')

similarity = None

similarity_model_path = get_path('./model/standard_similarity.pickle')

origin_good_name_path = get_path('./good_name/goods.csv')
good_name_unique_path = get_path('./good_name/unique_goods.csv')
good_name_row_cut_path = get_path('./good_name/row_cut_goods.csv')
good_name_cut_path = get_path('./good_name/cut_goods.csv')

origin_dict_path = get_path('./dictionaries/filtered_dict.txt')
dict_without_english_path = get_path('./dictionaries/filtered_dict_without_english.csv')

similarity_output_path = get_path('./similarities/')
good_name_similarity_output_path = similarity_output_path


def get_similarity() -> Similarity:
    global similarity
    if not similarity:
        path = similarity_model_path
        similarity = get_model(path, lambda: Similarity(category, user_dict_path))
    return similarity


def get_saved_similarity():
    with open(similarity_output_path + '/vectors.txt', 'r') as f:
        return {
            w[0]: np.asarray(w[1:], np.float32)
            for word in f.read().split('\n') if word is not '' for w in [word.split(' ')]
        }
