#!/usr/local/bin/python3.4
# coding:utf-8

from datetime import datetime
import urllib.request
import json

# liveoorAPI 1.0
# livedoorの天気予報APIからデータを取得
# 2018/4/30 ver 1.0     初版
# 2018/5/1 ver 1.1      複数都市をまとめて取得
# 2018/5/3 weatherfromlivedoor.cgi   CGI版
# 2018/5/3 index.cgiとしてルートディレクトリに配置


# 以下、レンタルサーバーで日本語使うためのおまじない
import cgitb
import sys
sys.stdin =  open(sys.stdin.fileno(),  'r', encoding='UTF-8');
sys.stdout = open(sys.stdout.fileno(), 'w', encoding='UTF-8');
sys.stderr = open(sys.stderr.fileno(), 'w', encoding='UTF-8');
cgitb.enable()
# 以上おまじない終わり

# HTMLヘッダ部
print("Content-Type: text/html; charset=UTF-8\r\n")
print("<html><head><title>ホーム／各種情報</title></head><body>")

print("<h1>{}時点での情報です。</h1>".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S")))

# ここから天気予報取得部
cityIDs = {'千葉':'120010', '東京':'130010', '京都':'260010'}

# ここから各都市ごとのループ
for c, i in cityIDs.items():
    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=' + i
    html = urllib.request.urlopen(url)
    jsonfile = json.loads(html.read().decode('utf-8'))

    print("<h2>{}</h2>".format(jsonfile['title']))
    print("<ul>")
    for d in jsonfile['forecasts']:
        maxtemp = ''
        if d['temperature']['max']:
            maxtemp = '、最高気温は' + d['temperature']['max']['celsius'] + '℃'
        mintemp = ''
        if d['temperature']['min']:
            mintemp = '、最低気温は' + d['temperature']['min']['celsius'] + '℃です。'
        print("<li>{0}の天気は「{1}」{2}{3} </li>".format(d['date'], d['telop'], maxtemp, mintemp))
    print("</ul><hr>")

# ここから鉄道遅延情報
target_line = ['中央･総武各駅停車', '総武快速線',]

# ここからjson取得部
url = 'https://rti-giken.jp/fhc/api/train_tetsudo/delay.json'
html = urllib.request.urlopen(url)
jsonfile = json.loads(html.read().decode('utf-8'))

# ここから検索と出力
print("<h2>{}の電車遅延情報</h2>".format(target_line))
flag = 0
print("<ul>")
for d in jsonfile:
    if d['name'] in target_line:
        print("<li>{}に遅れが発生しています！</li>".format(d['name']))
        flag += 1
if flag == 0:
    print("<li>指定した路線に遅れはありません</li>")
print("</ul><hr>")

# フッタ
print("</body></html>")
