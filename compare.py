#!/usr/bin/env python
#coding=utf-8

"""
Project: Chinese Segmentation Comparison
Author: log0
Date: 4/24/2013
"""
from mmseg import mmseg
import jieba

def utf8(value):
    if isinstance(value, unicode):
        return value.encode("utf-8")
    assert isinstance(value, str)
    return value

def _unicode(value):
    if isinstance(value, str):
        return value.decode("utf-8")
    assert isinstance(value, unicode)
    return value

def seg_by_mmseg(text):
    text = utf8(text)
    algor = mmseg.Algorithm(text)
    return [_unicode(tok.text) for tok in algor]

def seg_by_jieba(text):
    text = utf8(text)
    return jieba.cut(text)

def segment(text):
    results = {}
    results['mmseg'] = seg_by_mmseg(text)
    results['jieba'] = seg_by_jieba(text)

    for algo, result in results.iteritems():
        result = [ '\\' + item for item in result ]
        results[algo] = ' '.join(result)

    return results

raw_text = \
"""
我现在在北京
歧义识别指一个字符串有多种分词方法，计算机难以给出到底哪一种分词算法才是正确的分词系列。如”表面的”可以分为”表面/的”或”表/面的”。计算机无法判断哪一种才是准确的分词系列。
"""

if __name__ == '__main__':
    mmseg.dict_load_defaults()

    texts = raw_text.strip().split('\n')

    for text in texts:
        print '%12s : %s' % ('original', text)
        for algo, result in segment(text).iteritems():
            print '%12s : %s' % (algo, result)
