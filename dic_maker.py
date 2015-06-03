# -*- coding: utf-8 -*-
# !/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""
#
# Author:   Noname
# URL:      https://github.com/pettan0818
# License:  MIT License
# Created:  2015-05-18
#

# Usage
#
"""
import pandas


def merge_category_dummy(original):
    """
    pandasのダミー変数作成関数により、
    ダミー変数を辞書データにくっつける
    """
    dummy_data = pandas.get_dummies(original['eval'])

    merged_df = pandas.concat([original['word'], dummy_data], axis=1)

    return merged_df


def shrink_dic(dic_data):
    """
    ダミーデータつき辞書のサイズを軽減する。
    e = 1の行を削除し、返す。
    """
    pn_dic = dic_data[dic_data.e == 0]
    del pn_dic['e']
    return pn_dic


if __name__ == '__main__':
    # 辞書の名前
    PN_DIC_NAME = "opinion_dict.csv"
    SCORED_DIC_NAME = "pn_ja.dic.txt"

    # 数値の設定
    NEGATIVE_DIVISION_SCORE = -0.5
    POSITIVE_DIVISION_SCORE = -0.2

    # 評価辞書からの品詞抽出用評価式
    EXTRACT_PARTS = 'part == u"副詞" | part == u"形容詞"'

    # Pandaによる読みこみ
    DIC_PN = pandas.read_csv(PN_DIC_NAME, sep='\t', header=None)
    DIC_EXPAND_SCORED = pandas.read_csv(SCORED_DIC_NAME, sep=':', header=None, encoding='cp932')

    # データフレームの列命名
    DIC_PN.columns = ['word', 'eval', 'usecase']
    DIC_EXPAND_SCORED.columns = ['word', 'yomi', 'part', 'score']

    # 用言・名詞辞書の処理
    DIC_WITH_DUMMY = merge_category_dummy(DIC_PN)
    SHRINKED_DIC = shrink_dic(DIC_WITH_DUMMY)

    # 小林の評価表現辞書
    SUPECIFIED_PARTS = DIC_EXPAND_SCORED.query(EXTRACT_PARTS)

    # 小林の辞書で、DIVISION SCOREに沿って、PNを割り当てる。
    NEGATIVE_WORD = SUPECIFIED_PARTS.query('score < @NEGATIVE_DIVISION_SCORE')
    POSITIVE_WORD = SUPECIFIED_PARTS.query('score > @POSITIVE_DIVISION_SCORE')

    # Concatの準備(Indexを初期化・評価を含んだデータフレームの作成)
    NEGATIVE_WORD.index = range(0, len(NEGATIVE_WORD))
    POSITIVE_WORD.index = range(0, len(POSITIVE_WORD))
    INIT_WITH_N = pandas.DataFrame(['n' for x in range(0, len(NEGATIVE_WORD))])
    INIT_WITH_P = pandas.DataFrame(['p' for x in range(0, len(POSITIVE_WORD))])
    NEGATIVE_WORD_DIC = pandas.concat([NEGATIVE_WORD.word, INIT_WITH_N], axis=1)
    POSITIVE_WORD_DIC = pandas.concat([POSITIVE_WORD.word, INIT_WITH_P], axis=1)

    RESULT_DIC = pandas.concat([NEGATIVE_WORD_DIC, POSITIVE_WORD_DIC], axis=0)

    RESULT_DIC.columns = ['word', 'eval']

    DUMMYED_RESULT_DICT = merge_category_dummy(RESULT_DIC)

    FOUR_PARTS_DICTIONARY = pandas.concat([SHRINKED_DIC, DUMMYED_RESULT_DICT], axis=0)
    FOUR_PARTS_DICTIONARY.index = range(0, len(FOUR_PARTS_DICTIONARY))

    # 辞書の出力
    FOUR_PARTS_DICTIONARY.to_pickle("opinion_dict_shrinked.dic")
