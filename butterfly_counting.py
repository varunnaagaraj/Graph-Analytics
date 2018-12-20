"""
This is a piece of code which tries to find the 2,2 bicliques (butterflies) in the Large Network datasets.
Prerequisite: Graphs should be undirected unweighted and bipartite in nature. Preferably should not contain self loops.
"""

import networkx as nx
import matplotlib.pyplot as plt
import datetime as dt
import math

start_time = dt.datetime.now()
fb_data = nx.read_edgelist('board_members.rtf', create_using=nx.Graph())
print(nx.info(fb_data))

edges = fb_data.edges()

top_nodes = set()
for i in edges:
    top_nodes.add(i[0])


def find_butterflies():
    complete_dict_of_butterflies = dict()
    number_of_butterflies = 0
    for i in set(top_nodes):
        complete_dict_of_butterflies.update({i:[]})
        butterfly = dict()
        current_nbrs = fb_data.neighbors(i)
        for nbrs in current_nbrs:
            for w in fb_data.neighbors(nbrs):
                try:
                    butterfly[w] += 1
                except:
                    butterfly[w] = 1
                complete_dict_of_butterflies[i] = list(set(complete_dict_of_butterflies[i] + [w]))
        for w in butterfly.keys():
            total = 0
            if butterfly[w] > 0:
                if butterfly[w] - 2 > 0:
                    total = math.factorial(butterfly[w])/ (2* math.factorial(butterfly[w] - 2))
                number_of_butterflies += total
    return number_of_butterflies, complete_dict_of_butterflies


def vertex_distribution(complete_dict):
    percentage = dict()
    for key, value in complete_dict.items():
        for i in value:
            try:
                percentage[i] += 1
            except:
                percentage[i] = 1
    return percentage


final_bfc, butterfly = find_butterflies()
print("number of butterflies are:{}".format(final_bfc/2))
print("Runtime is :{}".format(dt.datetime.now()-start_time))
v_dist = vertex_distribution(butterfly)
print(v_dist)
names = list(v_dist.keys())
values = list(v_dist.values())

plt.bar(range(len(v_dist)),values,tick_label=names)
plt.savefig('vertex_distribution.png')
plt.show()

