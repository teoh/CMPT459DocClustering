# gen_res_commdet_sim.py
# will create a graph
# nodes: documents
# edges: if two docs are suspected similar. similarity is the intersect div by union
# will run some community detection algo on it

import csv

from funcs_doc_compare import *
from funcs_populate_dicts import *
from igraph import *
import numpy as np

# runs make_graphs_writer_sim_edges.py so that we have:
# doclist, adj_mat_sim_edge, docID2index, NUM_DOCS

from make_graphs_sim_edges import *

# some conversions
doclist = [int(docID) for docID in doclist]
docID2index = {int(docID): index for (docID,index) in docID2index.items()}

# construct the graph, igraph style

# make the vertex list
vertices = doclist
assert len(vertices) == NUM_DOCS


# make the edge list
edges = []
weights = []
for i in range(NUM_DOCS):
	for j in range(NUM_DOCS):
		# only add an edge once
		if i < j and adj_mat_sim_edge[i][j] != 0:
			# assert adj_mat_sim_edge[i][j] > 0, "Why the negative edge weight?"
			edges.append((i,j))
			weights.append(adj_mat_sim_edge[i][j])

g = Graph(directed=False)
g.add_vertices(NUM_DOCS)
g.vs["docID"] = doclist
g.add_edges(edges)
g.es["weight"] = weights


method = 'community_spinglass'
print('Method: '+method)

if method == 'community_multilevel':
	communities = g.community_multilevel("weight")
	clusters = communities 
	membership = [c+1 for c in clusters.membership] 
elif method == 'community_edge_betweenness': # takes forever
	communities = g.community_edge_betweenness(clusters=4,directed=False,weights="weight")
	print("hello")
	clusters = communities.as_clustering()
	membership = [c+1 for c in clusters.membership] 
elif method == 'community_spinglass':
	communities = g.community_spinglass(weights="weight",spins=4)
	clusters = communities
	membership = [c+1 for c in clusters.membership] 


with open('res_'+method+'.txt','w') as file:
	for i in range(NUM_DOCS):
		file.write(str(doclist[i])+','+str(membership[i])+'\n')


summary(g)
