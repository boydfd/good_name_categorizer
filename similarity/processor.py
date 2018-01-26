import numpy as np
import pandas as pd

from baike import get_word_text, get_word
from resources import get_similarity
from resources import resource
from utilities import append_slash_if_omitted


def save_good_name_to_similarity_vector(good_names, output_path):
    output_path = append_slash_if_omitted(output_path)
    vector_path = output_path + 'vectors.txt'
    error_path = output_path + 'errors.txt'
    error_list_path = output_path + 'error_name_list.txt'
    with open(vector_path, 'w') as vector_output, \
            open(error_path, 'w') as error_output, \
            open(error_list_path, 'w') as error_name_output:
        for index, good_name in enumerate(good_names):
            try:
                good_text = get_word_text(good_name)
                similarities = get_similarity().calculate_similarity_lsi(good_text)
                similarity_vector = ' '.join(list(similarities.astype(str)))
                output_row = '%s %s\n' % (good_name, similarity_vector)
                vector_output.write(output_row)
            except Exception as e:
                error_row = 'name: %s, error: %s\n' % (good_name, str(e))
                error_name_output.write(good_name + '\n')
                error_output.write(error_row)

            if index % 10 == 0:
                error_name_output.flush()
                vector_output.flush()
                error_output.flush()


class SimilarityCalculator:
    def __init__(self, saved_similarities_dict, similarity):
        self.saved_similarities_dict = saved_similarities_dict
        self.similarity = similarity

    def process(self, names):
        saved_similarities = self._get_saved_similarities(names)
        names_unsaved = self._get_names_unsaved(names)

        all_similarities = self._get_unsaved_similarities(names_unsaved)
        return all_similarities + saved_similarities

    def _get_unsaved_similarities(self, names):
        all_similarities = []
        for name in names:
            try:
                baike = get_word(name).text
                similarity = self.similarity.calculate_similarity_lsi(baike)
                all_similarities.append(similarity)
                self.saved_similarities_dict[name] = similarity
            except:
                pass
        return all_similarities

    def _get_names_unsaved(self, names):
        return [name for name in names if name not in self.saved_similarities_dict]

    def _get_saved_similarities(self, names):
        return [self.saved_similarities_dict[name] for name in names if name in
                self.saved_similarities_dict]


def calculate_similarity(similarity_callback, good_names):
    saved_similarities_dict = resource.get_saved_similarity()
    similarity_calculator = SimilarityCalculator(saved_similarities_dict, get_similarity())
    for index, names in enumerate(good_names):
        names = names.split(',')
        similarity = similarity_calculator.process(names)
        similarity_callback(names, similarity, index)


def process_similarity(good_name_path, output_path):
    with open(output_path, 'w') as f:
        def process(name, sims, index):
            similarity = get_similarity()
            sims = average_similarity(sims)
            sims = similarity.format_similarity(sims)
            f.write('%s %s\n' % (name, str(sims)))
            if index % 10 == 0:
                f.flush()

        df = pd.read_csv(good_name_path)
        calculate_similarity(process, df[df.columns[0]].values)


def average_similarity(all_similarities):
    if len(all_similarities) == 0:
        return all_similarities
    all_similarities = np.asarray(all_similarities)
    return np.mean(all_similarities, axis=0)
