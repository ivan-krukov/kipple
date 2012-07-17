#!/usr/bin/env python

"""
Given a list of EC numbers, produce a frequency for each
"""

import re
import sys
import argparse
from operator import itemgetter
from collections import defaultdict, OrderedDict


parser = argparse.ArgumentParser("Count frequencies of EC numbers in a file")
parser.add_argument("target_file",type=open,help="File with a column list of EC numbers")
parser.add_argument("-ec_class",type=int,choices=range(1,4),default=4,help="Use N digits for counting EC numbers (default 4 - complete EC nubmer)")

args = parser.parse_args()

ec_groups = defaultdict(int)
ec_pattern = re.compile(r"(\d+\.){3}\d+")

for line in args.target_file:
	line = line.strip()
	match = ec_pattern.match(line)
	if match:
		ec_number = match.group(0)
		ec_digits = ec_number.split(".")
		ec_id = ".".join(ec_digits[:args.ec_class])
		ec_groups[ec_id] += 1	

ec_groups = OrderedDict(sorted(ec_groups.iteritems(),key=itemgetter(1),reverse=True))

for key,value in ec_groups.items():
	print "{},{}".format(key,value)
