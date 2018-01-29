import pandas as pd
import re
import numpy as np
import operator
import jieba as jieba

letter2good = {
    'M': '邮件',
    'V': '贵重物品',
    'S': '急件',
    'P': '普货',
    'L': '活体动物',
    'X': '海鲜',
    'G': '果蔬',
    'H': '鲜花',
    'D': '鲜冻品',
    'O': '其他',
    'A': '所有',
}


def cut_good_name(word):
    word = word.upper()
    words = list(jieba.cut(word))
    if words[0] in letter2good:
        words[0] = letter2good[words[0]]
    if len(words) > 1 and words[0] == words[1]:
        words.pop(0)
    return words


def normalize(inventory):
    result_inventory = {}
    for item in inventory.items():
        if not item[0]:
            continue
        item_name = item[0]
        item_names = cut_good_name(item_name)

        for name in item_names:
            if name not in result_inventory:
                result_inventory[name] = 0
            result_inventory[name] += item[1]
    return result_inventory


def cut_every_good_name_row(source_good_path, output_path, user_dict):
    df = pd.read_csv(source_good_path)

    if user_dict:
        jieba.load_userdict(user_dict)

    def cut_with_comma(word):
        return ','.join([item for item in cut_good_name(word) if item != '' and item != ' '])

    pattern = re.compile('[ \\\\/,;；，、|()（）.]')
    df['cut_name'] = df['name'].map(lambda row: re.sub(pattern, ' ', row)).dropna().map(
        cut_with_comma)

    df.to_csv(output_path, index=False, columns=['cut_name', 'name'])


def cut_goods(source_goods_path,
              output_path,
              user_dict=None,
              frequency_limit=2):
    """
    this method can use jieba to cut words and calculate the word frequency
    ---
    :param user_dict: use customized dictionary to cut words
    :param source_goods_path: file like this:
        title
        word1
        word2
        word3
    :param output_path: file like this:
        'all' all_words_frequency
        cut_word1 frequency
        cut_word2 frequency
    :param frequency_limit: filter the word which has less limit frequency
    ---
    """
    if not user_dict:
        jieba.load_userdict(user_dict)
    print('loaded')
    df = pd.read_csv(source_goods_path)

    splited = df[df.columns[0]].dropna().map(lambda row: re.split('[ \\\\/,;；，、|()（）.]',
                                                                  row)).dropna()

    inventory = {}

    def insert_items(items):
        for item in items:
            inventory[item] = 1 if item not in inventory else inventory[item] + 1

    splited.apply(insert_items)

    inventory = normalize(inventory)

    sorted_inventory = sorted(inventory.items(), key=operator.itemgetter(1), reverse=True)

    pattern = re.compile('^[a-zA-Z0-9]{2,}$')
    filtered_inventory = list(
        filter(lambda item: item[1] > frequency_limit and (pattern.match(item[0]) or 0 <
                                                           len(item[0])
                                                           <= 4),
               sorted_inventory))
    inventory_count = np.asarray([value for _, value in filtered_inventory]).sum()
    filtered_inventory.insert(0, ('all', inventory_count))
    pd.DataFrame(np.asarray(filtered_inventory)).to_csv(output_path, index=False,
                                                        header=False)
