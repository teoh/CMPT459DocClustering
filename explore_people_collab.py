# explore_people_collab.py
# gets distr of # collaborations for a given person

import csv

from funcs_doc_compare import *
from funcs_populate_dicts import *
import time
import numpy as np
import matplotlib.pyplot as plt
import sys

doc2people, people2doc, nums_works = peopleAndDocs()

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
