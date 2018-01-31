import re
import os
import logging
import yaml

from baike import get_word
from utilities import flatten, retry_for_exception_decorator


class Category:
    def __init__(self, category_source_path, category_text_dir_path):
        self.category_text_dir_path = self.append_slash_if_omitted(category_text_dir_path)
        self.texts = None
        with open(category_source_path) as file:
            words = self.parse_categories_yaml(yaml.load(file.read()))
            self.list = sorted(flatten(words.values()))
            self.inverse_words = self.create_inverse_index(words)

    def get_first_category(self, category):
        return self.inverse_words[category]

    def get_texts_dict(self):
        if self.texts is None:
            self.persist_text()
            self.texts = {}
            for category in self.list:
                with open(self.get_category_path(category), 'r') as file:
                    self.texts[category] = file.read()
        return self.texts

    def persist_text(self):
        logging.info('start persisting category ')
        for category in self.list:
            self.persist_category(category)
        logging.info('end persisting category ')

    @retry_for_exception_decorator(TypeError)
    def persist_category(self, category):
        path = self.get_category_path(category)
        if not os.path.exists(path):
            logging.info('%s not exist locally, start crawling it' % category)
            with open(path, 'w') as file:
                file.write(get_word(category).text)

    def get_category_path(self, category):
        return self.category_text_dir_path + category + '.txt'

    @staticmethod
    def append_slash_if_omitted(path):
        return path if path.endswith('/') else path + '/'

    @staticmethod
    def parse_categories(text):
        rows = text.split('\n')
        chinese_number = ['一', '二', '三', '四', '五', '七', '八', '九', '十', ]
        mark = None
        result = {}
        for row in rows:
            if row[0] in chinese_number:
                mark = row
                result[mark] = ''
            else:
                result[mark] += row + '、'
        return result

    @staticmethod
    def parse_categories_dict(categories):
        def is_not_empty(item):
            return item is not ''

        return {key[key.index('、') + 1:]: list(filter(is_not_empty, re.split('[、， ]+', value)))
                for (key, value) in categories.items()}

    @staticmethod
    def create_inverse_index(dictionary):
        return {value: key for key, values in dictionary.items() for value in [key] + values}

    @staticmethod
    def parse_categories_yaml(categories):
        return {category['category_name']: category['sub_category'] for category in categories}
