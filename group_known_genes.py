#!/usr/bin/env python

"""
Given a list of C elegans genes, count each group
"""

import re
import sys
from operator import itemgetter
from collections import defaultdict, OrderedDict

gene_groups = defaultdict(int)
input_file = sys.argv[1]
name_pattern = re.compile(r"^(?P<class>\w+)\-\d")

for line in open(input_file):
	line = line.strip()
	match = name_pattern.match(line)
	if match:
		gene_groups[match.group("class")] += 1	

gene_groups = OrderedDict(sorted(gene_groups.iteritems(),key=itemgetter(1),reverse=True))

for key,value in gene_groups.items():
	print "{},{}".format(key,value)
