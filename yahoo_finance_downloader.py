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
import pandas
from bs4 import BeautifulSoup
import urllib2


def data_downloader(target_url):
    """
    BeautifulSoupでパースしたHTMLデータを返す。
    """
    return BeautifulSoup(urllib2.urlopen(target_url))


def url_generator_without_thread(seed_num):
    """
    [Deprecated.]
    >>> url_generator_without_thread("3318")
    'http://textream.yahoo.co.jp/message/1003318/3318'
    """
    return "http://textream.yahoo.co.jp/message/100" + seed_num + "/" + seed_num


def url_generator_thread_plus(stock_num, thread_num):
    """
    スレッド番号と株式番号からTextreamのホームアドレスを作成
    """
    return "http://textream.yahoo.co.jp/message/100" + stock_num + "/" + stock_num + "/" + thread_num


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

    # 要コメント
    contributed_time = [x.findAll("a")[-1].text for x in site_data.findAll("p", class_="comWriter")]

    positive_vote = [x.a.span.text for x in site_data.findAll("li", class_="positive")]

    negative_vote = [x.a.span.text for x in site_data.findAll("li", class_="negative")]

    binding_data = {'comments': comment_list, 'time': contributed_time, 'positive': positive_vote, 'negative': negative_vote}

    return pandas.DataFrame(data=binding_data, index=None, columns=["comments", "time", "positive", "negative"])


def main():
    """
    argparser対応を進めるのでメイン関数処理は、こちらに移行させる。
    """
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    COMMENT_DATAFRAME = pandas.DataFrame(columns=["comments", "time", "positive", "negative"])

    STOCK_NUM = sys.argv[1]
    OUTPUT_FILE_NAME = sys.argv[2]

    SEED_URL = url_generator_without_thread(STOCK_NUM)

    FIRST_DATA = data_downloader(SEED_URL)

    COMMENT_DATAFRAME = pandas.concat([COMMENT_DATAFRAME, comment_parser(FIRST_DATA)])

    NEXT_TARGET_URL = previous_url_parser(FIRST_DATA)

    while True:
        SITE_DATA_IN_LOOP = data_downloader(NEXT_TARGET_URL)

        COMMENT_DATAFRAME = pandas.concat([COMMENT_DATAFRAME, comment_parser(SITE_DATA_IN_LOOP)])

        try:
            NEXT_TARGET_URL = previous_url_parser(SITE_DATA_IN_LOOP)
        except AttributeError:
            break

        print "Next page is %s" % NEXT_TARGET_URL

        time.sleep(10)

    cPickle.dump(COMMENT_DATAFRAME, file("test.dump", 'w'))

    COMMENT_DATAFRAME.to_csv(OUTPUT_FILE_NAME, index=None)
