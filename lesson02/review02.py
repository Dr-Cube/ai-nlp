# coding=utf-8
import os
import pandas as pd
import re
from functools import reduce
import jieba
import sys
reload(sys)
sys.setdefaultencoding('utf8')

database = './sqlResult_1558435.csv'
dataframe = pd.read_csv(database, encoding='gb18030')
# 你好
print 1
a='你好'
all_articles = dataframe['content'].tolist()
print len(all_articles)
i = 0
for index, word in enumerate(all_articles):
    if index > 9:
        break
    word = str(all_articles).replace('u\'', '\'')
    word = word.decode("unicode-escape")
    # print word
    print index
# print all_articles[:10]


def token(string):
    return ' '.join(re.findall('[\w|\d+]', string))


string = 'this is a BIGGGGGGGGG thing BI and BIGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGgg'
token('\u3000\u30006月21日，A股纳入MSCI指数尘埃落定，但当天被寄予厚望的券商股并未扛起反弹大旗。22日，在222只纳入MSCI指数的A股股票中，银行股全线飘红，其中招商银行领涨，涨幅达6.66%')
all_articles = [token(str(a)) for a in all_articles]

text = ''
for a in all_articles:
    text += a
print 'length of text: {}'.format(len(text))

TEXT = text
txt_from_reduce = reduce(lambda a1, a2: a1+a2, all_articles[:10])

########
# 爬虫见crawler.py文件。内容为爬取landsat8 cloud cover assignment数据集
########

# Get all tokens


def cut(string):
    temp = list(jieba.cut(string))
    rlt = []
    for word in temp:
        word = word.decode('unicode-escape')
        rlt.append(word)
        # print word
        # print rlt
    return rlt


print cut("你好，我在这里等着你呢")
