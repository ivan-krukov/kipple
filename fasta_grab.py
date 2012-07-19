"""
Given a fasta reference, only print requested sequences (search by identifiers)
"""

import argparse
import fastaparse

parser = argparse.ArgumentParser()

parser.add_argument("reference_file",type=str,help="Reference fasta database")
parser.add_argument("id_file",type=str,help="File containing references to sequences")
args = parser.parse_args()

sequences = fastaparse.split_fasta(args.reference_file)

results = list()

for seq_id in open(args.id_file):
	for seq in sequences:
		if seq_id.strip() in seq.header:
			results.append(seq.fasta())

for seq in results:
	print seq
