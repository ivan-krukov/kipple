#!/usr/bin/env python

"""
Parse fasta sequence file and break in up in smaller chunks"""

import argparse
from os.path import splitext

def split_fasta(input_file):
	
	#resultant array of peptide sequences
	sequences=list()

	#temporary array of lines for each sequence as it is being read
	seq_buffer=list()
	
	header = ""
	for line in open(input_file):
			
		#if we find a header line and there are already lines in sequence buffer
		if ">" in line and seq_buffer:
			
			#flush lines from the buffer to the sequences array
			sequences.append(Sequence(header,"".join(seq_buffer)))
			seq_buffer=list()
			header = line.strip()

		#skip the ID line
		elif ">" in line and not seq_buffer:
			header = line.strip()
		
		#add next line to sequence buffer
		else:
			seq_buffer.append(line.strip())

	#dont forget the last sequence
	sequences.append(Sequence(header,"".join(seq_buffer)))
  	return sequences

class Sequence: 
	"""Represents a FASTA sequence string with its header"""
	def __init__(self, header, data):
		self.header=header
		self.data=data

	"""Return an indetifier from the fasta sequence
	First non-whitespace string, excluding the first character (>)"""
	def name (self):
		return self.header.split()[0][1:]

	"""Return the complete FASTA sequence with both header and sequence data
	"""
	def fasta (self):
		return "\n".join([self.header,self.data])

if __name__=="__main__":
	parser = argparse.ArgumentParser("Create N smaller files from a fasta sequence file")

	parser.add_argument("input_file",type=str,help="Input fasta file")
	parser.add_argument("n",type=int,help="Number of files to be produced")

	args = parser.parse_args()

	name,extension = splitext(args.input_file)

	sequences = split_fasta(args.input_file)

	length = len(sequences)
	print "Found {} sequences".format(length)

	n = length/args.n

	for i,j in enumerate(range(0,length,n)):
		file_handle = open("{}_{}{}".format(name,i,extension),"w")
		chunk = sequences[j:j+n]
		for seq in chunk:
			file_handle.write(seq.fasta()+"\n")
		file_handle.close()



