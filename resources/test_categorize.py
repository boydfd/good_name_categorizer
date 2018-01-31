import unittest
import yaml

import resources


class CategoryParserTest(unittest.TestCase):
    def setUp(self):
        self.category = resources.Category('./category.txt', '', yml_path='./category.yml')

    def test_test(self):
        with open('./category.yml', 'r') as f:
            categories = yaml.load(f)
            self.assertIsInstance(categories, list)

    def test_parseCategory_withYamlDictionary_shouldConvertToFirstSubPair(self):
        categories = [{
            'category_name': 'cate1',
            'sub_category': [
                'sub11',
                'sub12',
            ],
        }, {
            'category_name': 'cate2',
            'sub_category': [
                'sub21',
                'sub22',
            ],
        }
        ]
        self.assertEquals({
            'cate1': ['sub11', 'sub12'],
            'cate2': ['sub21', 'sub22'],
        }, self.category.parse_categories_yaml(categories))

    def test_parseCategory_withChineseNumberStarted_shouldBeCategorizedToOneSection(self):
        categories = '''一、第一个类别
1类1，1类
2、1类3、1类4
二、第二个类别
2类1、
2类2，
2类3'''
        self.assertEquals({
            '一、第一个类别': '1类1，1类、2、1类3、1类4、',
            '二、第二个类别': '2类1、、2类2，、2类3、'
        }, self.category.parse_categories(categories))

    def test_parseCategory_withDictionaryType_shouldRemoveCategoryNumberAndCutSubCategories(self):
        categories = {
            '一、第一个类别': '1类1，1类2、、1类3、1类4',
            '二、第二个类别': '2类1、2类2，2类3、',
        }

        self.assertEquals({
            '第一个类别': ['1类1', '1类2', '1类3', '1类4'],
            '第二个类别': ['2类1', '2类2', '2类3'],
        }, self.category.parse_categories_dict(categories))

    def test_createInverseIndex_withDictionary_shouldReturnCorrectIndex(self):
        categories = {
            '第一个类别': ['1类1', '1类2', '1类3', '1类4'],
            '第二个类别': ['2类1', '2类2', '2类3'],
        }

        self.assertEquals({
            '第一个类别': '第一个类别',
            '1类1': '第一个类别',
            '1类2': '第一个类别',
            '1类3': '第一个类别',
            '1类4': '第一个类别',
            '第二个类别': '第二个类别',
            '2类1': '第二个类别',
            '2类2': '第二个类别',
            '2类3': '第二个类别',
        }, self.category.create_inverse_index(categories))

    def test_getFirstCategory_fromSecondCategory_shouldReturnCorrectCategory(self):
        category = '蟹类'
        self.assertEquals('海鲜', self.category.get_first_category(category))

        category = '空气净化器'
        self.assertEquals('家电', self.category.get_first_category(category))

        category = '手机'
        self.assertEquals('手机', self.category.get_first_category(category))
