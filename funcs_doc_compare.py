from math import *

def computeSim(vec1, vec2):
	inter = intersect(vec1,vec2)
	unio = union(vec1,vec2)
	return len(inter)/len(unio), len(inter)

def computeIDFWeightedSim(vec1,vec2,vocab_cnt,NUM_DOCS):
	inter = intersect(vec1,vec2)
	return sum( [ log(NUM_DOCS/vocab_cnt[vocab],10) for vocab in inter ] )
	# return sum( [ (vocab_cnt[vocab]/NUM_DOCS) for vocab in inter ] )
	# assert n_t != 0
	# return log(NUM_DOCS/n_t,10)

def completeComputeSim(vec1,vec2):
	assert False, "implement this!"


def shareWriter(doc2people,doc1,doc2):
	return (len(intersect(doc2people[doc1],doc2people[doc2])) != 0)

def unique(a):
    return list(set(a))

def intersect(a, b):
    return list(set(a) & set(b))

def union(a, b):
    return list(set(a) | set(b))