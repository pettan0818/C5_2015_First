# -*- coding: utf-8 -*-
# !/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""
#
# Author:   Noname
# URL:      https://github.com/pettan0818
# License:  MIT License
# Created:  2014-10-15
#

# Usage
#
"""


def flatten_list(nested_list):
    """
    入れ子になったリストをたたみ込んで、
    入れ子のない状態に戻す。
    引数: リスト(入れ子あり)
    返値: リスト(入れ子なし)
    >>> flatten_list([1, 2, 3])
    [1, 2, 3]
    >>> flatten_list([[1, 2],[1, 4, 2],1,[0]])
    [1, 2, 1, 4, 2, 1, 0]
    >>> flatten_list([[[1, 2], 2],[1, 2, 3],[[[[1, 2, 3, 4], 3, 2, 1]], 2, 1]])
    [1, 2, 2, 1, 2, 3, 1, 2, 3, 4, 3, 2, 1, 2, 1]
    """
    flat_list = []
    fringe = [nested_list]

    while len(fringe) > 0:
        node = fringe.pop(0)
        # If node is list, then add this to fringe.
        # If node is not list, then just kick to flat_list.
        if isinstance(node, list):
            fringe = node + fringe
        else:
            flat_list.append(node)

    return flat_list


def duplicate_remover(duplicated_list):
    """
    リスト内の重複要素を削除して、リストで返す(順番維持)
    引数: リスト
    返り値: ダブりがなくなったリスト
    >>> duplicate_remover([1, 1, 2, 2, 3, 3])
    [1, 2, 3]
    >>> duplicate_remover([1, 2, 3, 4])
    [1, 2, 3, 4]
    """
    list_no_duplicated = sorted(set(duplicated_list), key=duplicated_list.index)

    return list_no_duplicated


def str_to_utf(str_object):
    """
    Str型のオブジェクトをユニコード(UTF-8)に変換し、結果を表示する。
    引数: STR型のオブジェクト
    返値: Unicode型のオブジェクト
    """
    unicode_object = str_object.decode('utf-8')

    return unicode_object


def dic_keys_extractor(dic_object, extract_opt):
    """
    辞書型のオブジェクトを含んだリストのそれぞれキーをリストにして返す。
    引数: 辞書型(以下のテストを参照)
    引数2: 取得したい辞書中のキーを指定。(順番)
    返値: キーの値だけを持ったリスト
    >>> dic_keys_extractor([{"test":75, "key":45}, {"test":61, "key":44}, {"test":10000, "key":111111}], 0)
    [75, 61, 10000]
    >>> dic_keys_extractor([{"test":90, "key":100}, {"test":111, "yo":0}], 0)
    [90, 111]
    """
    return_list = []

    for terms in dic_object:
        return_list.append(terms.values()[extract_opt])

    return return_list


if __name__ == '__main__':
    import doctest
    doctest.testmod()
