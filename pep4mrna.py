__doc__="""Given a fasta file of DNA sequences, translate all to peptide in the forward frames.
Find the longest Met to STOP stretch, report it as a peptide
"""

import argparse
import re
from fastaparse import split_fasta

standard = {'ttt': 'F', 'tct': 'S', 'tat': 'Y', 'tgt': 'C',
			'ttc': 'F', 'tcc': 'S', 'tac': 'Y', 'tgc': 'C',
			'tta': 'L', 'tca': 'S', 'taa': 'X', 'tga': 'X',
			'ttg': 'L', 'tcg': 'S', 'tag': 'X', 'tgg': 'W',

			'ctt': 'L', 'cct': 'P', 'cat': 'H', 'cgt': 'R',
			'ctc': 'L', 'ccc': 'P', 'cac': 'H', 'cgc': 'R',
			'cta': 'L', 'cca': 'P', 'caa': 'Q', 'cga': 'R',
			'ctg': 'L', 'ccg': 'P', 'cag': 'Q', 'cgg': 'R',

			'att': 'I', 'act': 'T', 'aat': 'N', 'agt': 'S',
			'atc': 'I', 'acc': 'T', 'aac': 'N', 'agc': 'S',
			'ata': 'I', 'aca': 'T', 'aaa': 'K', 'aga': 'R',
			'atg': 'M', 'acg': 'T', 'aag': 'K', 'agg': 'R',

			'gtt': 'V', 'gct': 'A', 'gat': 'D', 'ggt': 'G',
			'gtc': 'V', 'gcc': 'A', 'gac': 'D', 'ggc': 'G',
			'gta': 'V', 'gca': 'A', 'gaa': 'E', 'gga': 'G',
			'gtg': 'V', 'gcg': 'A', 'gag': 'E', 'ggg': 'G'}

orf_pattern = re.compile(r"M.*?X")
ambiguity_pattern = re.compile(r"N+")

"""Given a DNA sequence, translate in the forward frames, return list of 3 peptide sequences"""
def forward_frame_translate (sequence):

	translations = []
	temp_peptide = []
	
	for frame in range(0,3):
		for i in range(frame, len(sequence) ,3):
			codon = sequence[i:i+3]
			if len(codon) == 3:
				temp_peptide.append(standard[codon])
		# str.join() is faster then str+str
		translations.append("".join(temp_peptide))
		temp_peptide = []

	return translations

def trim_ambiguous_nucleotides (sequence):
	return re.sub(ambiguity_pattern,"",sequence)

def longest_ORF (sequence):
	open_reading_frames = orf_pattern.findall(sequence);
	
	if open_reading_frames:
		#trim M and X
		return max(open_reading_frames,key=len)[1:-1]
	else:
		return ""

if __name__=="__main__":
	parser = argparse.ArgumentParser(__doc__)
	parser.add_argument("input_file",type=str,help="Target fasta file")
	args = parser.parse_args()

	sequences = (seq for seq in split_fasta(args.input_file))

	for seq in sequences:
		data = trim_ambiguous_nucleotides(seq.data.lower())
		header = seq.header
		#keep track of longest ORF for each of 3 forward frames
		peptides = []
		for translation in forward_frame_translate(data):
			peptides.append(longest_ORF(translation))
		print header
		print max(peptides,key=len)
	
