from typing import List
from urllib.parse import quote
from urllib.request import urlopen

import os
from bs4 import BeautifulSoup

import jieba.posseg as pseg
from utilities import retry_for_timeout, get_model


def get_path(path):
    directory = os.path.dirname(__file__)
    return os.path.join(directory, path)


cache_path = get_path('./caches/')


class BaikeResult:
    def __init__(self, origin_name, baike_name, link):
        self.origin_name = origin_name
        self.baike_name = baike_name
        self.link = link
        self.text = None


def search_in_baike_link_by_word(word):
    def get_html_from_baike_search():
        return urlopen('https://baike.baidu.com/search?word=%s' % quote(word),
                       timeout=5).read()

    page = retry_for_timeout(get_html_from_baike_search)
    soup = BeautifulSoup(page, "html.parser")
    try:
        found_result = soup.find(class_='result-title')
        link = found_result['href']
        if link.startswith('/'):
            link = 'https://baike.baidu.com' + link
        return BaikeResult(word, found_result.text[:-5], link)
    except AttributeError:
        return BaikeResult(word, '', '')


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find(class_='main-content').text


def get_baike_html_from_url(url):
    def get_html():
        return urlopen(url, timeout=5).read().decode('utf-8')

    return retry_for_timeout(get_html)


def get_all_noun_form_word(word):
    return [word for word, flag in pseg.cut(word) if
            flag in ["n", "nr", "nr1", "nr2", "nrj", "nrf", "ns",
                     "nsf", "nt", "nz", "nl", "ng"]]


def get_word_with_noun(word) -> List[BaikeResult]:
    nouns = get_all_noun_form_word(word)
    result = []
    if len(nouns) is 0:
        nouns.append(word)
    for noun in nouns:
        result.append(get_word(noun))
    return result


def get_word(word) -> BaikeResult:
    def get():
        baike_result = search_in_baike_link_by_word(word)
        html = get_baike_html_from_url(baike_result.link)
        text = parse_html(html)

        baike_result.text = text
        return baike_result

    return get_model(cache_path + word, get)


def get_word_text(word) -> str:
    baike_results = get_word_with_noun(word)
    return ''.join([baike_result.text for baike_result in baike_results])
