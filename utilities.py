from _socket import timeout

from bs4 import BeautifulSoup
import numpy as np
import jieba as jieba
import pickle
import os.path


# with open('./htmls/上衣', 'r') as f:
#     html_doc = f.read()
#     soup = BeautifulSoup(html_doc, 'html.parser')
#
#     print(soup.find_all(class_ = 'para'))
#     '\n'.join([tag.text for tag in soup.find_all(class_ = 'para')])
#     soup.find(class_='basic-info').text
#     soup.find(class_='lemma-catalog').text
#     pass

def get_content_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find(class_='main-content').text


def parse_html(word, path='./htmls'):
    with open('%s/%s' % (path, word), 'r') as f:
        # html_doc = f.read()
        # soup = BeautifulSoup(html_doc, 'html.parser')
        with open('./jd_items/%s' % word, 'w') as r:
            print(word + '\n')
            r.write(get_content_from_html(f.read()))
            r.flush()


def get_words(path):
    with open(path, 'r') as file:
        return list(set([row.split(' ')[0] for row in file.read().split('\n')[1:]
                         if row.split(' ')[0] is not '']))


def get_standard_words():
    return get_words('./output/standard_words_link.txt')


def get_jd_words():
    path = './output/jd_words'
    return get_words(path)


def get_model(path, callback):
    if not os.path.isfile(path):
        result = callback()
        pickle_out = open(path, "wb")
        pickle.dump(result, pickle_out)
        pickle_out.close()
    else:
        result = pickle.load(open(path, "rb"))
    return result


def get_jieba_with_filtered_dict():
    path = './model/jieba_with_filtered_dict.pikle'

    def callback():
        jieba.load_userdict('./sources/filtered_dict.txt')
        return jieba

    return get_model(path, callback)


def get_jieba_with_dict():
    path = './model/jieba_with_dict.pikle'

    def callback():
        jieba.load_userdict('./sources/dict.txt')
        return jieba

    return get_model(path, callback)


def retry_for_exception(exception, function, times=5):
    for i in range(times):
        try:
            return function()
        except exception:
            if i + 1 == times:
                raise exception


def append_slash_if_omitted(path):
    return path if path.endswith('/') else path + '/'


def get_saved_similarities():
    with open('./output/similarities/standard_result.txt') as f:
        return {
            w[0]: np.asarray(w[1:], np.float32)
            for word in f.read().split('\n') if word is not '' for w in [word.split(' ')]
        }


def flatten(l):
    return [item for sublist in l for item in sublist]


def get_filtered_dictionary():
    path = './sources/filtered_dict.txt'
    vectors = open(path, 'r')
    return vectors.read().split('\n')


# get_saved_similarities()

if __name__ == '__main__':
    words = get_words('./output/standard_words_link.txt')
    for word in words:
        parse_html(word)
