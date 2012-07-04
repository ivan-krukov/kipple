#!/usr/bin/env python

from collections import defaultdict
import sys

peptides = defaultdict(tuple)

input_file = sys.argv[1]

for line in open(input_file):
	(seq_id,ec,probability) = line.strip().split(",")
	#check if entry exists
	if len(peptides[seq_id]) == 0:
		peptides[seq_id] = (ec,probability)
	else:
		if probability > peptides[seq_id][1]:
			peptides[seq_id] = (ec,probability)

for entry in peptides.items():
	print "{},{},{}".format(entry[0],entry[1][0],entry[1][1])
