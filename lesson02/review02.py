#coding=utf-8
import os
import pandas as pd
import re
from functools import reduce
import jieba
import sys
import imp
# imp.reload(sys)
# sys.setdefaultencoding('utf8')

database = './sqlResult_1558435.csv'
dataframe = pd.read_csv(database, encoding='gb18030')
# 你好
print(1)
a = '你好'
all_articles = dataframe['content'].tolist()
print(len(all_articles))
i = 0
for index, word in enumerate(all_articles):
    if index > 9:
        break
    word = str(all_articles).replace('u\'', '\'')
    # word = word.decode("unicode-escape")
    # print word
    print(index)
# print all_articles[:10]


def token(string):
    return ' '.join(re.findall('[\w|\d+]', string))


string = 'this is a BIGGGGGGGGG thing BI and BIGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGgg'
token('\\u3000\\u30006月21日，A股纳入MSCI指数尘埃落定，但当天被寄予厚望的券商股并未扛起反弹大旗。22日，在222只纳入MSCI指数的A股股票中，银行股全线飘红，其中招商银行领涨，涨幅达6.66%')
all_articles = [token(str(a)) for a in all_articles]

text = ''
for a in all_articles:
    text += a
print('length of text: {}'.format(len(text)))

TEXT = text
txt_from_reduce = reduce(lambda a1, a2: a1+a2, all_articles[:10])

########
# 爬虫见crawler.py文件。内容为爬取landsat8 cloud cover assignment数据集
########

# Get all tokens


def cut(string):
    return list(jieba.cut(string))
    # temp = list(jieba.cut(string))
    # rlt = []
    # for word in temp:
    #     # word = word.decode('unicode-escape')
    #     rlt.append(word)
    #     # print word
    #     # print rlt
    # return rlt


print(cut("你好，我在这里等着你呢"))
ALL_TOKENS = cut(TEXT)

valida_tokens = [t for t in ALL_TOKENS if t.strip() and t!='\n']
print(re.findall('(?:who)+', 'who are you? who are you!'))
print(1)
print(re.findall('(?:nan)+', 'nannan'))
valida_tokens = [t for t in ALL_TOKENS if not re.findall('(?:nan)+', t)]

valida_tokens = [t for t in valida_tokens if not re.findall('\s+', t)]
print(len(ALL_TOKENS), len(valida_tokens))
# print valida_tokens[:20]

## Get the frequences of words

from collections import Counter
import matplotlib.pylab as plt
import numpy as np
from matplotlib.pyplot import hist
word_count = Counter(valida_tokens)
print(word_count.most_common(10))
frequences = [f for w, f in word_count.most_common(100)]
x = [i for i in range(len(frequences[:100]))]
len(frequences)
plt.plot(x, frequences)
plt.plot(x, np.log(frequences))
frequences_all = [f for w, f in word_count.most_common()]
frequences_sum = sum(frequences_all)
print(frequences_sum, 1/frequences_sum)


def laplace_smooth(counter, c=1):
    N = sum(counter.values())
    Nplus = N + c * (len(counter)+1)
    return lambda word: (counter[word] + c) / Nplus


laplace_prob = laplace_smooth(word_count)
print(laplace_prob('你好'), laplace_prob('手机'), laplace_prob('红外'), laplace_prob('毛主席语录'))

single_word = [w for w in word_count if word_count[w] == 1]
print(len(single_word))

lengths = list(map(len, single_word))
print(Counter(lengths).most_common())

hist(lengths, bins=len(set(lengths)))


def simple_good_turing_version(counter, base=1/26., prior=1e-8):
    N = sum(counter.values())
    lengths = map(len, [w for w in counter if counter[w] == 1])
    ones = Counter(lengths)
    longest = max(ones)

    def _get_prob(w):
        if w in counter:
            prob = counter[w] / N
        elif len(w) in ones:
            prob = prior * ones[len(w)] / N
        else:
            prob = prior * ones[longest] / N * base ** (len(word) - longest)
        return prob
    return _get_prob

gt_prob = simple_good_turing_version(word_count)

print(gt_prob('测试'), gt_prob('我们'))


def get_prob(word):
    esp = 1/frequences_sum
    if word in word_count:
        return word_count[word]/frequences_sum
    else:
        return esp


def product(numbers):
    return reduce(lambda n1, n2: n1 * n2, numbers)


def language_model_one_gram(string):
    words = cut(string)
    return product([get_prob(w) for w in words])


print(get_prob('我们'))
print(language_model_one_gram('上海车展下月举办'))

# 2-Gram
valid_tokens = [str(t) for t in valida_tokens]
all_2_gram_words = [''.join(valid_tokens[i:i+2]) for i in range(len(valid_tokens[:-2]))]
_2_gram_sum = len(all_2_gram_words)
_2_gram_counter = Counter(all_2_gram_words)


def get_combination_prob(w1, w2):
    if w1+w2 in _2_gram_counter:
        return _2_gram_counter[w1+w2] / _2_gram_sum
    else:
        return 1/_2_gram_sum


def get_pro_2_gram(w1, w2):
    return get_combination_prob(w1, w2) / get_prob(w1)


print('去北京', get_combination_prob('去', '北京'), '喝可乐', get_combination_prob('喝', '可乐'))
print('prob:', get_pro_2_gram('去', '北京'), get_pro_2_gram('去', '上海'))


def language_model_2_gram(sentence):
    sentence_prob = 1
    words = cut(sentence)
    for i, word in enumerate(words):
        if i == 0:
            prob = get_prob(word)
        else:
            previous = words[i-1]
            prob = get_pro_2_gram(previous, word)
        sentence_prob *= prob
    return sentence_prob


print(language_model_2_gram('小明今天抽奖抽到一台苹果手机'))


# Problem using 2-gram

need_compared = [
    "今天晚上请你吃大餐，我们一起吃日料 明天晚上请你吃大餐，我们一起吃苹果",
    "真事一只好看的小猫 真是一只好看的小猫",
    "今晚我去吃火锅 今晚火锅去吃我",
    "洋葱奶昔来一杯 养乐多绿来一杯"
]

grammar = """
sentence => noun_phrase verb_phrase 
noun_phrase => Article Adj* noun belong 
belong => de property
de => 的
property => 眼睛 | 裙子 | 胳膊 | 尾巴
Adj* => null | Adj Adj*
verb_phrase => verb noun_phrase
Article =>  一个 | 这个
noun =>   女人 |  篮球 | 桌子 | 小猫
verb => 看着   |  坐在 |  听着 | 看见
Adj =>   蓝色的 |  好看的 | 小小的
"""

for s in need_compared:
    s1, s2 = s.split()
    p1, p2 = language_model_2_gram(s1), language_model_2_gram(s2)
    better = s1 if p1 > p2 else s2

    print('{} is more possible'.format(better))
    print('-' * 4 + ' {} with probility {}'.format(s1, p1))
    print('-' * 4 + ' {} with probility {}'.format(s2, p2))

import random


def parse_grammar(grammar_str, sep='=>'):
    grammar = {}
    for line in grammar_str.split('\n'):
        line = line.strip()
        if not line:
            continue
        target, rules = line.split(sep)
        grammar[target.strip()] = [r.split() for r in rules.split('|')]
    return grammar


def gene(grammar_parsed, target='sentence'):
    if target not in grammar_parsed:
        return target
    rule = random.choice(grammar_parsed[target])
    return ''.join(gene(grammar_parsed, target=r) for r in rule if r!='null')


g = parse_grammar(grammar)
random_generated = [gene(g) for _ in range(100)]
s1 = {1, 2, 3}
s2 = {4, 5, 2}
print('s1|s2', s1 | s2)

print('language model 2-gram', sorted(random_generated, key=language_model_2_gram, reverse=True))

