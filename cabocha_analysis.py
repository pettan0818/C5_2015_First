# -*- coding: utf-8 -*-
# !/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""
#
# Author:   Noname
# URL:      https://github.com/pettan0818
# License:  MIT License
# Created:  2015-06-03
#

# Usage
#
"""

import CaboCha
from bs4 import BeautifulSoup

cabocha_parser = CaboCha.Parser("-d /usr/local/Cellar/mecab/0.996/lib/mecab/dic/mecab-ipadic-neologd")

tree = cabocha_parser.parse("「疲れる」と感じさせるような友人は、有益なつきあいとは言えないのですから、関係を絶っても問題はありません。")

xml_tree = BeautifulSoup(tree.toString(CaboCha.CABOCHA_FORMAT_XML), "xml")

print xml_tree.findAll("chunk")[1]
