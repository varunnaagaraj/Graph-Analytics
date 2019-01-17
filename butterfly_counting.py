"""
This is a piece of code which tries to find the 2,2 bicliques (butterflies) in the Large Network datasets.
Prerequisite: Graphs should be undirected unweighted and bipartite in nature. Preferably should not contain self loops.
"""
import networkx as nx
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd


start_time = dt.datetime.now()
data = pd.read_csv('board_members.txt', sep=" ", header=None, dtype=str)
data=data.dropna(how='all')
data = data.dropna()
max_value = 0
for item in data[0]:
    if int(item) > max_value:
        max_value = int(item)

vert_L = set()
vert_R = set()
for i, j in data.iterrows():
    if j[0] == '}' or j[1] == '}':
        continue
    vert_L.add(j[0])
    vert_R.add(str(int(j[1])+ max_value))

B = nx.Graph()
B.add_nodes_from(vert_L, bipartite=0)
B.add_nodes_from(vert_R, bipartite=1)
for row in data.iterrows():
    B.add_edge(row[1][0], str(int(row[1][1])+ max_value))

max = 0
for i in vert_L:
    if i > max:
        max = int(i)

max2 = 0
for i in vert_R:
    if i > max2:
        max2 = int(i)

hashmap_c = [0]* (max+max2)
aux_array = [0]* (max+max2)


def exact_bfc():
    complete_dict_of_butterflies = dict()
    bf_count = 0
    edge_list = list()
    for v in vert_L:
        complete_dict_of_butterflies.update({v:0})
        index = 0
        for neighbor in B.neighbors(v):
            two_hop_neighbors = B.neighbors(neighbor)
            for thn in two_hop_neighbors:
                if int(v) > int(thn):
                    bf_count += hashmap_c[int(thn)]
                    hashmap_c[int(thn)] += 1
                    if hashmap_c[int(thn)] == 1:
                        aux_array[index] = int(thn)
                        index += 1
                        temp = sorted([int(v), int(neighbor)])
                        temp = (str(temp[0]), str(temp[1]))
                        temp1 = sorted([int(neighbor), int(thn)])
                        temp1 = (str(temp1[0]), str(temp1[1]))
                        edge_list.append((temp))
                        edge_list.append((temp1))
                else:
                    break
        complete_dict_of_butterflies[v] = index
        for j in range(index+1):
            hashmap_c[aux_array[j]] = 0
    return sum(complete_dict_of_butterflies.values())/2, complete_dict_of_butterflies, edge_list

bf_counted, complete_bfc, edge_dist = exact_bfc()
print("Number of Butterflies counted is {}".format(bf_counted))


names = list(complete_bfc.keys())
values = list(complete_bfc.values())
#
fig1, ax1 = plt.subplots()
result_occurrences = {i:complete_bfc.values().count(i) for i in complete_bfc.values()}
result_occurrences.pop(0)
ax1.bar(result_occurrences.keys(), result_occurrences.values(), color='g')
plt.title('Vertex Distribution')
plt.xlabel('Vertex Occurrences')
plt.ylabel('Number of Butterflies associated with vertices')
plt.savefig('vertex_distribution.png')

fig2, ax2 = plt.subplots()
edge_occurrences = {i:edge_dist.count(i) for i in edge_dist}
edge_result_occurrences = {i:edge_occurrences.values().count(i) for i in edge_occurrences.values()}
ax2.bar(edge_result_occurrences.keys(), edge_result_occurrences.values(), color='b')
plt.title('Edge Distribution')
plt.xlabel('Edge Occurrences')
plt.ylabel('Number of Butterflies associated with edges')
plt.savefig('edge_distribution.png')

print("Time taken is {}".format(dt.datetime.now() - start_time))