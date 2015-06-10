# -*- coding: utf-8 -*-
# !/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""
#
# Author:   Noname
# URL:      https://github.com/pettan0818
# License:  MIT License
# Created:  2015-06-10
#

# Usage
#
"""

import sys
from bs4 import BeautifulSoup
import urllib2

url = sys.argv[1]

site_data = BeautifulSoup(urllib2.urlopen(url))

comment_list = [x.text.strip().replace('\n','') for x in site_data.findAll("p", class_="comText")]

for x in comment_list:
    print x

