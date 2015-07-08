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
import numpy
import pandas
from bs4 import BeautifulSoup
import urllib2
import mecab_direct_connecter
import dic_searcher


def seed_url_generator(stock_num):
    """
    >>> url_generator_without_thread("3318")
    'http://textream.yahoo.co.jp/message/1003318/3318'
    """
    return "http://textream.yahoo.co.jp/message/100" + str(stock_num) + "/" + str(stock_num)


def url_generator_thread_plus(stock_num, thread_num):
    """
    スレッド番号と株式番号からTextreamのホームアドレスを作成
    """
    return "http://textream.yahoo.co.jp/message/100" + str(stock_num) + "/" + str(stock_num) + "/" + str(thread_num)


def targetthreads_urllist_generator(stock_num, start_thread_num, thread_length):
    """
    株式番号・起点となるスレッド番号・必要なスレッドの長さを元に、
    スレッドリストを作成
    >>> target_threads_urllist_generator(1662, 2, 1)

    >>> target_threads_urllist_generator(1662, 2, 2)

    >>> target_threads_urllist_generator(1662, 2, 10)

    """
    target_numbers = range(start_thread_num, start_thread_num - thread_length, -1)

    return [url_generator_thread_plus(stock_num, x) for x in target_numbers if x > 0]


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


class Emotional_Analytics(object):
    """
    文字列を受け取り、極性分析を行います。
    引数: comment(str)
    返り値: 感情点数(float)
    """
    def __init__(self):

        dic_positon = "./opinion_dict_shrinked.dic"

        self.mecab_exe = mecab_direct_connecter.MecabMother()
        self.comment_opinion_teller = dic_searcher.OpinionDictSearcher(dic_positon)

        self.target_part = ["名詞", "動詞", "形容詞", "副詞"]

    def emotional_point(self, comment):
        """
        上記処理をブートストラップに。
        """
        self.mecab_exe.set_text_to_parse(comment)
        self.mecab_exe.unknown_word_buster_by_parts()
        extracted_comment = self.mecab_exe.extract_category_originalshape(self.target_part)

        point_list = [self.comment_opinion_teller.tell_word_score(x) for x in extracted_comment]

        return numpy.mean(point_list)


class DataFetcher(object):
    """
    テキストリームからデータを
    ・URLの特定
    ・ダウンロード
    ・必要要素の抽出
    するクラス
    """
    def __init__(self, args):
        """
        初期化
        ・クラス内プロパティの生成
        """
        # 引数の処理
        self.process_thread_num = args.thread_num
        self.stock_num = args.stock_num
        self.excel_file_name = args.extend_excel_file
        self.output_file_name = args.output_file_name
        self.wait_time = args.wait_time
        self.dump_name = args.dump_name

        # 極性分析処理
        self.emotional_exe = Emotional_Analytics()

        # スレッド現在番号の確認
        self.seed_thread = 0
        # 結果の格納用のデータフレームを初期化
        self.comment_dataframe = pandas.DataFrame()

    def bootstrapper(self):
        """
        一括処理を行うためのブートストラップ
        """
        self.checker()

        seed_list = targetthreads_urllist_generator(self.stock_num, self.seed_thread, self.process_thread_num)

        for seed_url in seed_list:
            self.thread_processor(seed_url)

        cPickle.dump(self.comment_dataframe, file(self.dump_name, 'w'))
        self.comment_dataframe.to_csv(self.output_file_name, index=None)
        if self.excel_file_name is not None:
            self.comment_dataframe.to_excel(self.excel_file_name, str(self.stock_num))

    def thread_processor(self, target_url):
        """
        指定のシードURLから始めて、そのスレッド全体を取得する。
        """
        while True:
            print "target page is %s" % target_url

            site_data_in_loop = BeautifulSoup(urllib2.urlopen(target_url))

            self.comment_dataframe = pandas.concat([self.comment_dataframe, self.comment_parser(site_data_in_loop)])

            # 次の発言を取りに行くために、次ページリンクを抽出
            try:
                target_url = previous_url_parser(site_data_in_loop)
            except AttributeError:  # 処理中のページに「前のページへ」が無くなったとき
                break

            time.sleep(self.wait_time)

    def comment_parser(self, site_data):
        """
        ページ内の発言をパースしてリストにして返す。
        """
        comment_list = list(reversed([x.text.strip().replace('\n', '').replace('\r', '') for x in site_data.findAll("p", class_="comText")]))

        # 要コメント
        contributed_time = list(reversed([x.findAll("a")[-1].text for x in site_data.findAll("p", class_="comWriter")]))
        contributed_time_with_out_time = [x.split(" ")[0] for x in contributed_time]
        contributed_time = contributed_time_with_out_time

        positive_vote = list(reversed([x.a.span.text for x in site_data.findAll("li", class_="positive")]))

        negative_vote = list(reversed([x.a.span.text for x in site_data.findAll("li", class_="negative")]))

        emotional_point = [self.emotional_exe.emotional_point(str(x)) for x in comment_list]

        binding_data = {'comments': comment_list, 'time': contributed_time, 'positive': positive_vote, 'negative': negative_vote, 'emotion_score': emotional_point}

        return pandas.DataFrame(data=binding_data, index=None, columns=["comments", "time", "positive", "negative", "emotion_score"])


    def checker(self):
        """
        ・初期アドレスの実在性確認
        ・スレッド番号の確認
        """
        checking_url = seed_url_generator(self.stock_num)

        try:
            checking_site_data = BeautifulSoup(urllib2.urlopen(checking_url))
        except urllib2.HTTPError as instance:
            if instance.code == 404:
                raise urllib2.HTTPError("You select wrong stock number...Maybe...")
            else:
                raise urllib2.HTTPError("Something wrong...")

        self.seed_thread = find_my_thread_pos(checking_site_data)


def main(args):
    """
    argparser対応を進めるのでメイン関数処理は、こちらに移行させる。
    """
    processor = DataFetcher(args)

    processor.bootstrapper()


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

    PARSER = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="このアプリケーションは、テキストリームから指定の株式番号のスレッド書き込みをダウンロードします。", epilog="Made by pettan0818")
    PARSER.add_argument("stock_num", type=int)
    PARSER.add_argument("output_file_name")
    PARSER.add_argument("-e", "--extend_excel_file", type=str, help="If you want to output file by excel, please input filename like '-e test.xlsx'")
    PARSER.add_argument("-n", "--dump_name", type=str, default="test.dump", help="Set dump name, if you want. default name is test.dump")
    PARSER.add_argument("-s", "--wait_time", type=int, default=5, help="[Do not use] If you have to fetch imaginally high speed, set option small figure")
    PARSER.add_argument("-t", "--thread_num", type=int, default=1, help="if you want to download more than one thread, like '-t 10'")
    PARSER.add_argument("-d", "--debug", action="store_true", help="enter debugmode")

    ARGS = PARSER.parse_args()
    print ARGS

    if ARGS.debug is True:
        debug(ARGS)
    else:
        main(ARGS)
