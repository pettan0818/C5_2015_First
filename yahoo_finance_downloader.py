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
    comment_dataframe = pandas.DataFrame(columns=["comments", "time", "positive", "negative"])

    stock_num = sys.argv[1]
    output_file_name = sys.argv[2]

    seed_url = url_generator_without_thread(stock_num)

    first_data = data_downloader(seed_url)

    comment_dataframe = pandas.concat([comment_dataframe, comment_parser(first_data)])

    next_target_url = previous_url_parser(first_data)

    while True:
        site_data_in_loop = data_downloader(next_target_url)

        comment_dataframe = pandas.concat([comment_dataframe, comment_parser(site_data_in_loop)])

        try:
            next_target_url = previous_url_parser(site_data_in_loop)
        except AttributeError:
            break

        print "next page is %s" % next_target_url

        time.sleep(10)

    cPickle.dump(comment_dataframe, file("test.dump", 'w'))

    comment_dataframe.to_csv(output_file_name, index=None)

def debug():
    """
    Doctestを走らせるための関数
    ArgParseで--debugオプション時に発動。
    """
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    import argparse

    main()
