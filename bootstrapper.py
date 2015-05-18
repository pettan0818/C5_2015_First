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
import mecab_direct_connecter
import dic_reader


if __name__ == '__main__':
    TARGET_FILE_NAME = "test.list"
#     TARGET_FILE_NAME = sys.argv[1]

    TEXT_LIST = [text.rstrip('\n') for text in file(TARGET_FILE_NAME, 'r')]

    mecab_exe = mecab_direct_connecter.MecabMother()

    mecab_exe.set_text_to_parse(TEXT_LIST[0])

    mecab_exe.unknown_word_buster_by_parts()

    word_gen = mecab_exe.word_generator()

    print word_gen.next()

    print word_gen.next()

    print word_gen.next()

    for i in word_gen.next():
        print i

