# make_graphs_sim_edges.py
# makes 2 graphs: each doc is a node and edges are either based on similarity or common-writer
# outputs those files for viewing in gephi

##################################################
# 
# important structures created:
# adj_mat_sim_edge 		-	adjacency matrix with weights adj_mat_sim_edge[i][j] == similarity(doclist[i],doclist[j])
# docID2index 			- 	maps: docID -> index
# doclist 				- 	doclist[index] -> docID
# NUM_DOCS 				-	number of documents we are dealing with
# 
##################################################

import csv

from funcs_doc_compare import *
from funcs_populate_dicts import *
import time
import numpy as np
import matplotlib.pyplot as plt
import sys

doc2people, people2doc, nums_works = peopleAndDocs()
doc2words_01 = getDoc2Words()
doc2words_02 = dict(doc2words_01)
NUM_DOCS = len(doc2words_01)

simil_lists = [ [0]*NUM_DOCS for i in range(NUM_DOCS) ]
vocab_cnt = getVocabCnts(doc2words_01)

people2collabs = getPeople2Collabs(doc2people)

# similarity based edges graphs:
# goal: n x n matrix M where M[i][j] = similarity between docs i and j

# get a map from docID to index of matrix
docID2index = {}
ind = 0
for docID in doc2words_01.keys():
	assert type(docID) == str
	assert docID not in docID2index.keys()
	docID2index[docID] = ind
	ind += 1
assert NUM_DOCS == ind

# get a list of the document IDs. essentially a map: matrix index -> docID
doclist = [0]*NUM_DOCS 
for docID,ind in docID2index.items():
	doclist[ind] = docID

ctr = 0
# populate simil_lists with the entries
for doc1,words1 in doc2words_01.items():
	for doc2,words2 in doc2words_02.items():
		i = docID2index[doc1]
		j = docID2index[doc2]
		if i > j:
			if shareWriter(doc2people,doc1,doc2):
				simil_lists[i][j] = -100
			else:
				naiveSim = False
				if naiveSim:
					sp, ignore = computeSim(words1,words2)
				else:
					sp = computeIDFWeightedSim(words1,words2,vocab_cnt,NUM_DOCS)
				# print('investigating collaborators')
				doc1_writers = doc2people[doc1]
				doc2_writers = doc2people[doc2]

				assert len(intersect(doc1_writers,doc2_writers)) == 0

				collabsfound = False
				for writer1 in doc1_writers:
					for writer2 in doc2_writers:
						assert writer1 in people2collabs.keys()
						collabs1 = people2collabs[writer1]
						if writer2 in collabs1 and not collabsfound:
							# sp *= 4/3
							collabsfound = True
							ctr+=1
							break
					if collabsfound:
						break
				if not collabsfound:
					sp *= 3/4
				simil_lists[i][j] = sp

adj_mat_sim_edge = np.array(simil_lists)
adj_mat_sim_edge += adj_mat_sim_edge.T



# with open('adj_mat_sim_edge.csv','w') as file:
# 	for i in range(NUM_DOCS):
# 		file.write(';'+doclist[i])
# 	file.write('\n')

# 	for i in range(NUM_DOCS):
# 		file.write(doclist[i])
# 		for j in range(NUM_DOCS):
# 			if adj_mat_sim_edge[i][j] == 0:
# 				file.write(';')
# 			else:
# 				file.write(';'+str(adj_mat_sim_edge[i][j]))
# 		file.write('\n')


print("make_graphs_sim_edges.py is done!")
print(ctr)


