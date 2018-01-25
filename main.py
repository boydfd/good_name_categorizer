from file_processor import pre_process_all
import pandas as pd

from resources import resource
from similarity.processor import save_good_name_to_similarity_vector

if __name__ == '__main__':
    pre_process_all()

    df = pd.read_csv(resource.good_name_cut_path)
    words = df['all'].tolist()
    save_good_name_to_similarity_vector(words, resource.similarity_vector_path)
