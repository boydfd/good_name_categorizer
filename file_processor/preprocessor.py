import logging

import pandas as pd

from file_processor import cut_goods, cut_every_good_name_row
from resources import resource


def delete_duplicity_in_goods(source_path, output_path):
    df = pd.read_csv(source_path)
    df = df.drop_duplicates().dropna()
    df['name'] = df[df.columns[0]]
    df.to_csv(output_path, index=False, columns=['name'])


def delete_english_in_dictionary(source_dict_path, output_path):
    with open(source_dict_path, 'r') as r:
        df = pd.DataFrame(r.read().split('\n'))
    df = df.drop_duplicates().dropna()
    df1 = df[~df[0].str.match('^[^\u4e00-\u9fa5]+$')].dropna().drop_duplicates()
    df1.to_csv(output_path, index=False, header=False)


def pre_process_all():
    logging.info('start delete english in dictionary')
    delete_english_in_dictionary(resource.origin_dict_path, resource.dict_without_english_path)

    logging.info('start delete duplicity in goods')
    delete_duplicity_in_goods(resource.origin_good_name_path, resource.good_name_unique_path)

    logging.info('start cut goods')
    cut_goods(resource.origin_good_name_path,
              resource.good_name_cut_path,
              resource.dict_without_english_path)

    logging.info('start cut good name for every row')
    cut_every_good_name_row(
        resource.good_name_unique_path,
        resource.good_name_row_cut_path,
        resource.user_dict_path
    )
