from resources import resource
from similarity.processor import save_good_name_to_similarity_vector
import pandas as pd

if __name__ == '__main__':
    names = ['服装', 'SCARF', '~~~~~~']
    save_good_name_to_similarity_vector(names, './')

    df = pd.read_csv(resource.good_name_cut_path)
    words = df['all'].tolist()
    save_good_name_to_similarity_vector(words, resource.similarity_vector_path)
