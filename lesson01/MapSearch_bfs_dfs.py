# -*- coding:utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt
print 1
BEIJING, CHANGCHUN, WULUMUQI, WUHAN, GUANGZHOU, SHENZHEN, BANGKOK, SHANGHAI, NEWYORK = """
BEIJING
CHANGCHUN
WULUMUQI
WUHAN
GUANGZHOU
SHENZHEN
BANGKOK
SHANGHAI
NEWYORK
""".split()
dictionary = {}
crt_connection = {
    CHANGCHUN: [BEIJING],
    WULUMUQI: [BEIJING],
    BEIJING: [WULUMUQI, CHANGCHUN, WUHAN, SHENZHEN, NEWYORK, GUANGZHOU, SHANGHAI],
    NEWYORK: [BEIJING, SHANGHAI],
    SHANGHAI: [NEWYORK, WUHAN, BEIJING],
    WUHAN: [SHANGHAI, BEIJING, GUANGZHOU],
    GUANGZHOU: [WUHAN, BANGKOK, BEIJING],
    SHENZHEN: [WUHAN, BANGKOK],
    BANGKOK: [SHENZHEN, GUANGZHOU]
}
crt_graph = crt_connection
draw_graph = nx.Graph(crt_graph)
nx.draw(draw_graph, with_labels=True)
# print crt_connection[CHANGCHUN]
# plt.show()
# plt.close()


def navigator_bfs(start, destination, connection):
    path_que = [start]
    seen = set()
    print 'bfs result is as follow:'
    while path_que:  # path_que not null
        que_front = path_que.pop(0)
        if que_front in seen:
            continue
        flags = connection[que_front]
        print 'start is {}, going to {}'.format(que_front, flags)
        path_que += flags
        seen.add(que_front)


def navigator_dfs(start, destination, connection):
    path_que = [start]
    seen = set()
    print 'dfs result is as follow:'
    while path_que:
        que_front = path_que.pop(0)
        if que_front in seen:
            continue
        flags = connection[que_front]
        print 'start is {}, going to {}'.format(que_front, flags)
        path_que = flags + path_que
        seen.add(que_front)


navigator_bfs(NEWYORK, SHANGHAI, crt_connection)
navigator_dfs(NEWYORK, SHANGHAI, crt_connection)
plt.show()
