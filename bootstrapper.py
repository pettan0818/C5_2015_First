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

import sys
import pandas
import numpy
import mecab_direct_connecter
import dic_searcher

if __name__ == '__main__':
    try:
        TARGET_FILE_NAME = sys.argv[1]
    except IndexError:
        TARGET_FILE_NAME = "test.list"

    #TEXT_LIST = [text.rstrip('\n') for text in file(TARGET_FILE_NAME, 'r')]
    DATA_LIST = pandas.read_csv(TARGET_FILE_NAME)
    TEXT_LIST = DATA_LIST.comments

    MECAB_EXE = mecab_direct_connecter.MecabMother()
    WORD_OPINION_TELLER = dic_searcher.OpinionDictSearcher("./opinion_dict_shrinked.dic")

    FULL_EXP = []

    for i in TEXT_LIST:
        MECAB_EXE.set_text_to_parse(i)

        MECAB_EXE.unknown_word_buster_by_parts()

        TARGET_WORDS = MECAB_EXE.extract_category_originalshape(["名詞", "動詞", "形容詞", "副詞"])

        opt_list = [WORD_OPINION_TELLER.tell_word_score(word) for word in TARGET_WORDS]

        print opt_list
        print numpy.mean(opt_list)

        FULL_EXP.append(numpy.mean(opt_list))

    print "Total Exp: %s" % str(numpy.mean(numpy.nan_to_num(FULL_EXP)))
