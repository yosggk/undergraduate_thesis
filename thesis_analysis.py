import MeCab as mc
from collections import Counter
import pandas as pd

import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt
% matplotlib inline

# 1.mecabを用いて単語に分けます。
def mecab_analysis(text):
    t = mc.Tagger("-Ochasen")
    t.parse('')
    node = t.parseToNode(text) 
    output = []
    while node:
        if node.surface != "":  # ヘッダとフッタを除外
            word_type = node.feature.split(",")[0]
            if word_type in ["形容詞", "動詞","名詞", "副詞"]:
                output.append(node.surface)
        node = node.next
        if node is None:
            break
    return output

def add_count_to_dict(words):
    for k, v in words.items():
        if k not in stop_words and k in counts:
            counts[k] += v
        elif k not in stop_words:
            counts[k] = v

df = pd.read_csv('df_blockchain.csv')

#titleをわかち書き
df['wakachi_title'] = df.title.map(mecab_analysis)
#abstractをわかち書き
df['wakachi_abstract'] = df.abstract.map(mecab_analysis)
#count title words
df['title_count'] = df.wakachi_title.map(Counter)
#count abstract words
df['abstract_count'] = df.wakachi_abstract.map(Counter)

#date型から年、クォーター、月を出す
df.date = pd.to_datetime(df.date, format = '%Y/%m/%d %H:%M')
df['year']     = df.date.map(lambda x: x.year)
df['quarter'] = df.date.map(lambda x: x.quarter)
df['month']    = df.date.map(lambda x: x.month)


#各新聞社に分ける
df_nk = df.loc[df.company == 'NK']
df_ft = df.loc[df.company == 'FT']
df_ws = df.loc[df.company == 'WS']

#ストップワードの設定
stop_words = [ u'てる', u'いる', u'なる', u'れる', u'する', u'ある', u'こと', u'これ', u'さん', u'して', \
             u'くれる', u'やる', u'くださる', u'そう', u'せる', u'した',  u'思う',  \
             u'それ', u'ここ', u'ちゃん', u'くん', u'', u'て',u'に',u'を',u'は',u'の', u'が', u'と', u'た', u'し', u'で', \
             u'ない', u'も', u'な', u'い', u'か', u'ので', u'よう', u'',\
                'the', 'a', 'to', 'of', 's', 'for', 'it', 'at', 'as', 'up', 'on', 'from','with','or', 'in', 'and', 'that', 'be', 'an' ,'.',',',\
             '-','"',"'",'...', 'is','the', 'The', 'its','You','has', 'are']

#月ごとにまとめる
year = range(2013, 2019)
month = range(1, 13)
for y in year:
    for m in month:
        counts = {}
        df_ws[(df_ws.year == y) & (df_ws.month == m)]["abstract_count"].map(add_count_to_dict)
        if counts.keys() not in stop_words:
     
           print(str(y) + "年" + str(m) + "月: ",sorted(counts.items(), key=lambda x: x[1], reverse=True)[:11])

#quarter
year = range(2013, 2019)
#month = range(1, 13)
quarter = range(1, 5)
for y in year:
    for q in quarter:
        counts = {}
        df_ws[(df_ws.year == y) & (df_ws.quarter == q)]["abstract_count"].map(add_count_to_dict)
        if counts.keys() not in stop_words:
     
           print(str(y) + "年" + str(q) + "Q: ",sorted(counts.items(), key=lambda x: x[1], reverse=True)[:11])
           
# Year
year = range(2013, 2019)
#month = range(1, 13)
quarter = range(1, 5)
for y in year:
    #for q in quarter:
        counts = {}
        df_ws[(df_ws.year == y)]["abstract_count"].map(add_count_to_dict)
        if counts.keys() not in stop_words:
     
           print(str(y) + "年" ,sorted(counts.items(), key=lambda x: x[1], reverse=True)[:11])