"""
This is a piece of code which tries to find the 2,2 bicliques (butterflies) in the Large Network datasets.
Prerequisite: Graphs should be undirected unweighted and bipartite in nature. Preferably should not contain self loops.
"""

import networkx as nx
import matplotlib.pyplot as plt

fb_data = nx.read_edgelist('facebook_combined.txt', create_using=nx.Graph())
print(nx.info(fb_data))

edges = fb_data.edges()

top_nodes = []
bottom_nodes = []
for i in edges:
    top_nodes.append(i[0])
    bottom_nodes.append(i[1])
    
def uniq(lst):
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item

def sort_and_deduplicate(l):
    return list(uniq(sorted(l, reverse=True)))
    
butterfly = list()


def second_level_neighbors(second_level_nbrs):
    for l in second_level_nbrs:
        if l == j:
            continue
        if i in fb_data.neighbors(l):
            print("adding a butterfly")
            butterfly_content = sorted([str(i), str(j), str(k), str(l)])
            butterfly.append(butterfly_content)


def current_node_neighbors(current_nbrs):
    global j, k, second_level_nbrs
    for j in set(current_nbrs):
        bottom_node_nbrs = fb_data.neighbors(j)
        for k in bottom_node_nbrs:
            if k == i:
                continue
            second_level_nbrs = fb_data.neighbors(k)
            second_level_neighbors(second_level_nbrs)


def find_butterflies():
    for i in set(top_nodes):
        current_nbrs = fb_data.neighbors(i)
        current_node_neighbors(current_nbrs)

find_butterflies()
print("The butterflies are: ",sort_and_deduplicate(butterfly))

nx.draw(fb_data, with_labels=True)
plt.show()