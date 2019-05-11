# -*- coding:utf-8 -*-
import random

grammar = """
sentence => noun_phrase verb_phrase 
noun_phrase => Article Adj* noun
Adj* => null | Adj Adj*
verb_phrase => verb noun_phrase
Article =>  一个 | 这个
noun =>   女人 |  篮球 | 桌子 | 小猫
verb => 看着   |  坐在 |  听着 | 看见
Adj =>   蓝色的 |  好看的 | 小小的
"""


def parse_grammar(grammar_str, sep='=>'):
    grammar = {}
    for line in grammar_str.split('\n'):
        line = line.strip()
        if not line:
            continue

        target, rules = line.split(sep)
        words = rules.split('|')
        grammar[target.strip()] = [i.split(' ') for i in words]
    return grammar


g = parse_grammar(grammar, '=>')
print 1
print g


def generator(grammar_parsed, target='sentence'):
    if target not in grammar_parsed:
        return target
    rules = random.choice(grammar_parsed[target])
    return ''.join(generator(grammar_parsed, target=rule) for rule in rules if rule!='null')


g['sentence']
# print g
print generator(g)
