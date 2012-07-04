import argparse

parser = argparse.ArgumentParser("Get the sequences of the reads with no qality lines or ids")
parser.add_argument("input_file",type=str,help="Input FASTQ file")
args = parser.parse_args()

sequence_list = list()
entry_line=0
for line in open(args.input_file):
	entry_line += 1
	if entry_line == 1:
		continue
	if entry_line == 2:
		sequence_list.append(line)
	if entry_line == 3:
		continue
	if entry_line == 4:
		entry_line = 0

with open(args.input_file+".sequences","w") as output_file:
	output_file.write("".join(sequence_list))
	
	
	

