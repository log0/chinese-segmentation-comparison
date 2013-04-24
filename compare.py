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

def format_as_html(results):
    html = '''
<!DOCTYPE html>
<html lang="en" id="chinese_segmentation_comparison" class="no_js">
<head>
<meta charset="utf-8" /><title id="pageTitle">Chinese Segmentation Comparison</title>
<style>
body {
    font-family: Courier New, monospace;
}
</style>
</head>
    '''
    html += '<table border="1">'
    html += '<tr>'
    html += '<th>Original</th>'

    for algo in results[0].iterkeys():
        if algo == 'original': continue
        html += '<th>%s</th>' % (algo)

    html += '</tr>'

    for result in results:
        html += '<tr>'
        html += '<td>' + result['original'] + '</td>'
        for algo, output in result.iteritems():
            if algo == 'original': continue
            html += '<td>' + output + '</td>'
        html += '</tr>'

    html += '</table>'
    html += '</html>'

    return html

if __name__ == '__main__':
    mmseg.dict_load_defaults()

    raw_text = _unicode(file('text.in').read())
    texts = raw_text.strip().split('\n')

    results = []
    for text in texts:
        result = segment(text)
        result['original'] = text
        results.append(result)
        """
        print '%12s : %s' % ('original', text)
        for algo, output in result.iteritems():
            print '%12s : %s' % (algo, output)
        """

    html = format_as_html(results)
    print utf8(html)
