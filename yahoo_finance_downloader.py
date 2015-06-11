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
import time
import cPickle
from bs4 import BeautifulSoup
import urllib2


def data_downloader(target_url):
    """
    BeautifulSoupでパースしたHTMLデータを返す。
    """
    return BeautifulSoup(urllib2.urlopen(target_url))


def url_generator_thread(seed_num):
    """
    >>> url_generator_thread("3318")
    'http://textream.yahoo.co.jp/message/1003318/3318'
    """
    return "http://textream.yahoo.co.jp/message/100" + seed_num + "/" + seed_num


def previous_url_parser(site_data):
    """
    より前の発言のURLを取得
    """
    prev_url = site_data.findAll("li", class_="prev")[0].a.get("href")

    return prev_url


def comment_parser(site_data):
    """
    ページ内の発言をパースしてリストにして返す。
    """
    comment_list = [x.text.strip().replace('\n', '').replace('\r', '') for x in site_data.findAll("p", class_="comText")]

    return comment_list


def output_file_maker(result_list, output_file_name):
    """
    出力用コード
    """
    output_con = file(output_file_name, 'w')

    [output_con.writelines([line + '\n' for line in x]) for x in result_list]


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    COMMENT_RESULT = []

    STOCK_NUM = sys.argv[1]
    OUTPUT_FILE_NAME = sys.argv[2]

    SEED_URL = url_generator_thread(STOCK_NUM)

    FIRST_DATA = data_downloader(SEED_URL)

    COMMENT_RESULT.append(comment_parser(FIRST_DATA))

    NEXT_TARGET_URL = previous_url_parser(FIRST_DATA)

    while True:
        SITE_DATA_IN_LOOP = data_downloader(NEXT_TARGET_URL)

        COMMENT_RESULT.append(comment_parser(SITE_DATA_IN_LOOP))

        try:
            NEXT_TARGET_URL = previous_url_parser(SITE_DATA_IN_LOOP)
        except AttributeError:
            break

        print COMMENT_RESULT

        print NEXT_TARGET_URL

        time.sleep(10)

    cPickle.dump(COMMENT_RESULT, file("test.dump", 'w'))

    output_file_maker(COMMENT_RESULT, OUTPUT_FILE_NAME)
