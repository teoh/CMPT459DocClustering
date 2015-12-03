# freqitem_k_means.py
# this script uses k means to partition the documents
# feature vector for a documents has 1s where the words is present

from funcs_doc_compare import *
from funcs_populate_dicts import *
import csv
import numpy as np
import pprint

from pymining import itemmining 
from sklearn.cluster import KMeans

# get the data from DocumentWords.txt and put it in a dict<docID,featureVec>
docIDlist = []
docwordlist = []
with open('.\data\DocumentWords.txt','r') as file:
	reader = csv.reader(file)
	for row in reader: # [docID numWords words.........]
		docID = int(row[0])
		numwords = int(row[1])
		end_ind = len(row)
		
		docIDlist.append(docID)
		docwordlist.append(row[2:])
		assert ( numwords == len(row[2:]) )

transactions = docwordlist
relim_input = itemmining.get_relim_input(transactions)
report = itemmining.relim(relim_input, min_support=75)
sortRpt = sorted( report.items(), key=lambda x: (-x[1], sorted( map(int, list(x[0]) ) ) ) )

with open('freqitems','w') as file:
	for item in sortRpt:
		if len(item[0]) > 2:
			file.write(str(item))
			file.write('\n')

# make the list of frequent patterns
fplist = [list(item) for item in report.keys() if len(item) > 2]
NUM_FP = len(fplist)

# make the feature vector for each document
docfeatlist = []
# features: docfeatlist[i][j] = 1 iff fplist[j] a subset of docwordlist[i]
for docwords in docwordlist:
	docfeatlist.append([ int( set(fp).issubset( docwords ) ) for fp in fplist])

# for feats in docfeatlist:
# 	print(feats)

featMtx = np.array(docfeatlist)
est = KMeans(n_clusters=4)
est.fit(featMtx)
labels = est.labels_.astype(int) + 1
# print(labels)

assert len(labels)==len(docIDlist)

NUM_DOCS = len(docIDlist)

with open('freqitem_k_means_301165239.txt','w') as file:
	for i in range(len(labels)):
		file.write(str(docIDlist[i])+','+str(labels[i])+'\n')