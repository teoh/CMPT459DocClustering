import csv

def peopleAndDocs():
	# doc2people: docID -> [ people (IDs) ]
	# people2doc: person (ID) -> [ docIDs ]
	# nums_works: [ (length of list of docs done by a person) ]
	doc2people = {}
	people2doc = {}

	# map document id to list of people who wrote it
	with open('./data/Collaboration.txt','r') as file:
		reader = csv.reader(file)
		for row in reader:
			assert(len(row) == 3)
			p = list(set(row[0:2]))
			doc = row[2]
			doc2people[doc] = p
			# populate the person 2 doc map
			for person in p:
				if person not in people2doc.keys():
					people2doc[person] = [doc]
				else:
					people2doc[person].append(doc)

	# look at numbers of docs people have worked on
	nums_works = []
	for person, docs in people2doc.items():
		# print(person)
		assert len(people2doc[person]) <= 4
		nums_works.append(len(people2doc[person]))

	return doc2people, people2doc, nums_works

def getDoc2Words():
	# doc2words_01: docID -> [ (wordIDs appearing in that doc) ] 
	doc2words_01 = {}
	# map document id to the list of words it contains
	with open('./data/DocumentWords.txt','r') as file:
		reader = csv.reader(file)
		for row in reader:
			doc_i = row[0]
			end_ind = len(row)
			doc2words_01[doc_i] = row[2:end_ind]
			assert ( int(row[1]) == len(doc2words_01[doc_i]) )
			assert ( len(doc2words_01[doc_i])-len(row) == -2 )
	return doc2words_01

def getPeople2Collabs(doc2people):
	# people2collabs: person (ID) -> [ (list of people (IDs) that person worked with) ]
	people2collabs = {}
	# get dict of: person -> list of people they worked with
	for v in doc2people.values():
		assert len(v) >= 1
		if len(v)  == 2:
			person1 = v[0]
			person2 = v[1]
			if person1 not in people2collabs.keys():
				people2collabs[person1] = [person2]
			else:
				people2collabs[person1].append(person2)
			if person2 not in people2collabs.keys():
				people2collabs[person2] = [person1]
			else:
				people2collabs[person2].append(person1)
		else:
			person1 = v[0]
			if person1 not in people2collabs.keys():
				people2collabs[person1] = []



	return people2collabs

def getVocabCnts(doc2words_01):
	# vocab_cnt: wordID -> number of documents (docIDs) it appears in
	vocab_cnt = {}
	# get a count of the occurrences of the different words across the vocabulary
	# first get all of the vocab words in the dict
	with open('./data/Vocabulary.txt','r') as file:
		reader = csv.reader(file)
		for row in reader:
			doc = row[0]
			vocab_cnt[doc] = 0;
	for doc, words in doc2words_01.items():
		for word in words:
			assert(word in vocab_cnt.keys())
			vocab_cnt[word] += 1
	return vocab_cnt
