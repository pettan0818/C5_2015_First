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

def data_downloader(url):
    """
    """
    pass

def url_generator_thread(seed_url):
    """
    """
    pass

def previous_url_parser(site_data):
    """
    """
    pass

def comment_parser():
    """
    """
    pass


if __name__ == '__main__':
    URL = sys.argv[1]

    SITE_DATA = BeautifulSoup(urllib2.urlopen(URL))

    COMMENT_LIST = [x.text.strip().replace('\n', '') for x in SITE_DATA.findAll("p", class_="comText")]

    for x in COMMENT_LIST:
        print x

    print SITE_DATA.findAll("li", class_="prev")[0].a.get("href")

