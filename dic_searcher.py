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


class OpinionDictSearcher(object):
    """
    評価辞書を高速に検索するためのクラス
    >>> searcher = OpinionDictSearcher("./opinion_dict_shrinked.dic")

    >>> searcher.tell_word_score("死刑")
    -1
    >>> searcher.tell_word_score("特別")
    0
    >>> searcher.tell_word_score("割高")
    -1
    >>> searcher.tell_word_score("最高")
    1
    """
    def __init__(self, dic_name):
        self.dic = pandas.read_pickle(dic_name)

    def tell_word_score(self, word):
        score_base = self.dic.query('word == @word')

        dic_data_size = len(score_base.index)

        if dic_data_size == 0:
            return 0
        elif dic_data_size == 1:
            return int(score_base['n'] * -1 + score_base['p'] * 1)
        else:
            raise IndexError("I receive illegal data from dictionary")



if __name__ == '__main__':
    import doctest
    doctest.testmod()
