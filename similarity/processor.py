from baike import get_word_text
from resources import get_similarity
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
