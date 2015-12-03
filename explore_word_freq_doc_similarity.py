# explore_word_freq_doc_similarity.py
# makes plots for the distribution of similarities between doc and distr of word freqencies

import csv

from funcs_doc_compare import *
from funcs_populate_dicts import *
import time
import numpy as np
import matplotlib.pyplot as plt
import sys

doc2people, people2doc, nums_works = peopleAndDocs()

doc2words_01 = getDoc2Words()
NUM_DOCS = len(doc2words_01)

vocab_cnt = getVocabCnts(doc2words_01)
vocab_freq = [c for c in vocab_cnt.values()]

times = []
simprops = []
simmags = []

count = 0
cnt_set_0 = 0

doc2words_02 = dict(doc2words_01)
#  for two differnt documents...
for key1, val1 in doc2words_01.items():
	for key2, val2 in doc2words_02.items():
		# make sure that pair of documents we are examining haven't been examined yet
		if(key1 > key2):
			# print(key1, key2)
			count = count + 1
			start = time.time()
			# if these two documents share an author, they CANNOT be similar at all
			if shareWriter(doc2people,key1,key2): #( len(intersect(doc2people[key1],doc2people[key2])) != 0 ):
				simprop = 0
				simmag = 0
				cnt_set_0 += 1
			else:
				# otherwise, compute the similarity between the documents
				# print("hello hello")
				simprop, simmag = computeSim(val1,val2)
				simprop = computeIDFWeightedSim(val1,val2,vocab_cnt,NUM_DOCS)
			simprops.append(simprop)
			simmags.append(simmag)
			end = time.time()
			elapsed = end-start
			times.append(elapsed)

print("count: ",count)
print("cnt_set_0: ",cnt_set_0)



#  plotting all the results 

# plot the frequencies of the numworks
plt.figure(1)
plt.hist(nums_works,bins = 300)
plt.title("Histogram")
plt.xlabel("nums_works")
plt.ylabel("Frequency")
plt.xlim([min(nums_works),max(nums_works)])


# plot the frequencies of similarities computed
plt.figure(2)
plt.hist(simprops,bins = 300)
plt.title("Histogram")
plt.xlabel("simprops")
plt.ylabel("Frequency")
plt.xlim([min(simprops),max(simprops)])

# plt.figure(3)
# plt.hist(simmags,bins = 300)
# plt.title("Histogram")
# plt.xlabel("simmags")
# plt.ylabel("Frequency")
# plt.xlim([min(simmags),max(simmags)])

plt.figure(4)
plt.plot( range(0,len(vocab_freq)) ,sorted(vocab_freq),'ro')
plt.title("Histogram")
plt.xlabel("Ordinal")
plt.ylabel("Frequency of a vocab word")
plt.ylim([min(vocab_freq),max(vocab_freq)])

plt.show()