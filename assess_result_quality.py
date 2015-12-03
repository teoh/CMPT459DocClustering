# assess_result_quality.py
# checks the quality of the given results file

import csv
from funcs_doc_compare import *
from funcs_populate_dicts import *
import numpy as np

doc2people, people2doc, nums_works = peopleAndDocs()
doc2words_01 = getDoc2Words()
doc2words_02 = dict(doc2words_01)
NUM_DOCS = len(doc2words_01)

simil_lists = [ [0]*NUM_DOCS for i in range(NUM_DOCS) ]
vocab_cnt = getVocabCnts(doc2words_01)

people2collabs = getPeople2Collabs(doc2people)


# maps: docID -> clusterID
doc2cluster = {}
# maps: clusterID -> [(list of docID)]
cluster2doc = {}
with open('./fire/res_community_spinglass.txt','r') as file:
	reader = csv.reader(file)
	for row in reader:
		assert len(row) == 2;
		docID = row[0]
		clusterID = row[1]

		assert docID not in doc2cluster.keys()
		doc2cluster[docID] = clusterID

		if clusterID not in cluster2doc.keys():
			cluster2doc[clusterID] = [docID]
		else:
			cluster2doc[clusterID].append(docID)

# check that any pair of docs that share a writer do not appear in the same cluster
numSameWriters = 0
numSameClustersBad = 0
for doc1,words1 in doc2words_01.items():
	for doc2,words2 in doc2words_02.items():
		if doc1 > doc2:
			if shareWriter(doc2people,doc1,doc2):
				numSameWriters += 1
				if doc2cluster[doc1] == doc2cluster[doc2]:
					numSameClustersBad += 1 
					print(doc1+' AND '+doc2)

size_c1 = len(cluster2doc['1'])
size_c2 = len(cluster2doc['2'])
size_c3 = len(cluster2doc['3'])
size_c4 = len(cluster2doc['4'])

print('numSameWriters: ' + str(numSameWriters))
print('numSameClustersBad: ' + str(numSameClustersBad))

print('size_c1: ' + str(size_c1))
print('size_c2: ' + str(size_c2))
print('size_c3: ' + str(size_c3))
print('size_c4: ' + str(size_c4))