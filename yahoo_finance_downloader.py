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


def find_my_thread_pos(site_data):
    """
    現在のスレッド番号を検出する
    """
    thread_num = site_data.findAll("li", class_="threadBefore")[0].a.get("href")

    thread_num = int(thread_num.split("/")[-1])

    return thread_num + 1


def comment_parser(site_data):
    """
    ページ内の発言をパースしてリストにして返す。
    """
    comment_list = list(reversed([x.text.strip().replace('\n', '').replace('\r', '') for x in site_data.findAll("p", class_="comText")]))

    # 要コメント
    contributed_time = list(reversed([x.findAll("a")[-1].text for x in site_data.findAll("p", class_="comWriter")]))

    positive_vote = list(reversed([x.a.span.text for x in site_data.findAll("li", class_="positive")]))

    negative_vote = list(reversed([x.a.span.text for x in site_data.findAll("li", class_="negative")]))

    binding_data = {'comments': comment_list, 'time': contributed_time, 'positive': positive_vote, 'negative': negative_vote}

    return pandas.DataFrame(data=binding_data, index=None, columns=["comments", "time", "positive", "negative"])


def main(args):
    """
    argparser対応を進めるのでメイン関数処理は、こちらに移行させる。
    """
    # 引数の処理
    stock_num = args.stock_num
    output_file_name = args.output_file_name

    # 結果の格納用のデータフレームを初期化
    comment_dataframe = pandas.DataFrame(columns=["comments", "time", "positive", "negative"])

    # 株式番号を元に初回処理対象URLを決定
    target_url = url_generator_without_thread(stock_num)

    while True:
        print "target page is %s" % target_url

        # ページデータのダウンロード
        site_data_in_loop = data_downloader(target_url)

        # 結果格納用のデータフレームに格納
        comment_dataframe = pandas.concat([comment_dataframe, comment_parser(site_data_in_loop)])

        # 次の発言を取りに行くために、次ページリンクを抽出
        try:
            target_url = previous_url_parser(site_data_in_loop)
        except AttributeError:  # 処理中のページに「前のページへ」が無くなったとき
            break

        time.sleep(10)

    cPickle.dump(comment_dataframe, file("test.dump", 'w'))
    comment_dataframe.to_csv(output_file_name, index=None)


def debug(args):
    """
    Loggingを有効化する。
    """
    import logging
    import doctest

    doctest.testmod()

    logging.basicConfig(filename="debug.log", level=logging.DEBUG)

    main(args)


if __name__ == '__main__':
    import argparse

    PARSER = argparse.ArgumentParser(description="このアプリケーションは、テキストリームから指定の株式番号のスレッド書き込みをダウンロードします。", epilog="Made by pettan0818")
    PARSER.add_argument("stock_num", type=str)
    PARSER.add_argument("output_file_name")
    PARSER.add_argument("-t", nargs=1, type=int, default=1)
    PARSER.add_argument("-d", "--debug", action="store_true", help="enter debugmode")

    ARGS = PARSER.parse_args()

    if ARGS.debug is True:
        debug(ARGS)
    else:
        main(ARGS)
