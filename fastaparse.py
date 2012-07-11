"""Simple fasta parse module
"""

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


def split_fasta(input_file, count=0):
	
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
			if (count and len(sequences) == count):
				break
			
			seq_buffer=list()
			header = line.strip()

		#skip the ID line
		elif ">" in line and not seq_buffer:
			header = line.strip()
		
		#add next line to sequence buffer
		else:
			seq_buffer.append(line.strip())

	#dont forget the last sequence
	if (sequences and len(sequences) < count):
		sequences.append(Sequence(header,"".join(seq_buffer)))
  	return sequences

