import unittest


from baike.baike import search_in_baike_link_by_word, parse_html, get_all_noun_form_word


class BaikeTest(unittest.TestCase):
    def test_searchBakeLink_nameExistInBaike_returnBaikeResultWithBaikeNameAndLink(self):
        word = '百度百科'
        baike_result = search_in_baike_link_by_word(word)
        self.assertEquals(
            '百度百科',
            baike_result.origin_name
        )
        self.assertEquals(
            '百度百科',
            baike_result.baike_name
        )
        self.assertEquals(
            'http://baike.baidu.com/item/%E7%99%BE%E5%BA%A6%E7%99%BE%E7%A7%91',
            baike_result.link
        )

    def test_searchBaikeLink_nameNotExistInBaike_returnBaikeResultWithEmptyBaikeNameAndLink(self):
        word = '阿斯蒂芬接口'
        baike_result = search_in_baike_link_by_word(word)
        self.assertEquals(
            '阿斯蒂芬接口',
            baike_result.origin_name
        )
        self.assertEquals(
            '',
            baike_result.baike_name
        )
        self.assertEquals(
            '',
            baike_result.link
        )

    def test_parseBaikeWord_withHtml_returnTextContainsMainSection(self):
        with open('./test_html', 'r') as html, open('./test_word_text', 'r') as text:
            self.assertEquals(
                text.read(),
                parse_html(html.read())
            )

    def test_getNounFromWord_withWordContainNoun_returnListOfNoun(self):
        word = '时尚产品'
        self.assertEquals(
            [
                '时尚',
                '产品',
            ],
            get_all_noun_form_word(word)
        )
