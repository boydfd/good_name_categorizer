import logging

from file_processor import pre_process_all
import pandas as pd

from resources import resource
from similarity.processor import save_good_name_to_similarity_vector, process_similarity

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(filename)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO)
    logging.getLogger("gensim").setLevel(logging.WARNING)
    # pre_process_all()

    # df = pd.read_csv(resource.good_name_cut_path)
    # words = df['all'].tolist()
    # save_good_name_to_similarity_vector(words, resource.similarity_output_path)

    process_similarity(resource.good_name_row_cut_path, resource.good_name_similarity_output_path)
