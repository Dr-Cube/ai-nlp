# -*- coding:utf-8 -*

# 问题1
# 编写一个程序, get_response(saying, response_rules)
# 输入是一个字符串 + 我们定义的 rules，
# 例如上边我们所写的 pattern，
# 输出是一个回答。


def is_variable(pat):
    return pat.startswith('?') and all(s.isalpha() for s in pat[1:])


def pat_match(pattern, saying):
    if is_variable(pattern[0]):
        return pattern[0], saying[0]
    else:
        if pattern[0] != saying[0]:
            return False
        else:
            return pat_match(pattern[1:], saying[1:])


print pat_match('I have ?X'.split(), "I have pen".split())
print pat_match('I have ?X'.split(), "I want pen".split())

