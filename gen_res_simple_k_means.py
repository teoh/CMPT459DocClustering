# simple_k_means.py
# this script uses k means to partition the documents
# feature vector for a documents has 1s where the words is present

from funcs_doc_compare import *
from funcs_populate_dicts import *
import csv
import numpy as np
import pprint

from sklearn.cluster import KMeans


def zerolistmaker(n):
	listofzeros = [0] * n
	return listofzeros


# get data from Vocabulary.txt so that we can map docID -> index; index -> docID
vocab_list = []
vocab_to_ind = {}
with open('./data/Vocabulary.txt','r') as file:
	reader = csv.reader(file)
	for row in reader:
		assert len(row) == 1
		vocab_list.append(int(row[0]))

vocab_list = sorted(vocab_list)
for i in range(len(vocab_list)) :
	vocab_to_ind[vocab_list[i]] = i

# print(vocab_to_ind)
# print(vocab_list)

# get the data from DocumentWords.txt and put it in a dict<docID,featureVec>
NUM_VOCAB = len(vocab_list)
docID_to_feat = {}
docIDlist = []
docfeatlist = []
with open('./data/DocumentWords.txt','r') as file:
	reader = csv.reader(file)
	for row in reader: # [docID numWords words.........]
		docID = int(row[0])
		numwords = int(row[1])
		end_ind = len(row)
		feat = zerolistmaker(NUM_VOCAB)
		for i in range(2,end_ind):
			vocab = int(row[i])
			ind = vocab_to_ind[ vocab ]
			feat[ ind ] = 1
		
		docIDlist.append(docID)
		docfeatlist.append(feat)
		assert sum(feat) == numwords

featMtx = np.array(docfeatlist)
est = KMeans(n_clusters=4)
est.fit(featMtx)
labels = est.labels_.astype(int) + 1
# print(labels)

assert len(labels)==len(docIDlist)

NUM_DOCS = len(docIDlist)

with open('simple_k_means_301165239.txt','w') as file:
	for i in range(len(labels)):
		file.write(str(docIDlist[i])+','+str(labels[i])+'\n')

doc2people, people2doc, nums_works = peopleAndDocs()
