#Exports .keg BRITE hierarchy (htext) into a parsable xml format

from argparse import ArgumentParser
from collections import defaultdict
from collections import namedtuple
import re

"""Hierarchy structure:
	A single Entry corresponds to an EC number. 
		EC number has a description and a list of genes.
	Each gene has a unique sequence name, optional common name and a description.
		To each protein, a K number (KEGG ID) is mapped
	A KEGG ID consists of a name and a list of EC numbers that reference that protein
"""

Entry = namedtuple("Entry", ["ec", "description", "genes"])
Gene = namedtuple("Gene", ["sequence_name", "common_name", "description", "kegg_id"])
Kegg_ID = namedtuple("Kegg_ID", ["name", "description", "ec_numbers"])

def between(string, char_a, char_b):
	return string [string.find(char_a)+1 : string.find(char_b)]

if __name__=="__main__":

	parser = ArgumentParser("Exports a .keg BRITE hierarchy file (htext) into XML.")
	parser.add_argument("keg_file",type=str,help="Input .keg file")
	args = parser.parse_args()

	ec_line_pattern = re.compile(r"^D.*$")
	enzyme_line_pattern = re.compile(r"^E.*$")
	#Example: 1.1.1.1  alcohol dehydrogenase
	ec_entry_pattern = re.compile(r"^D\s+(?P<EC>\d+\.\d+\.\d+\.\d+)\s+(?P<description>.*)$")
	#Example: K12G11.3 sodh-1; SOrbitol DeHydrogenase family member (sodh-1)	K13953 alcohol dehydrogenase, propanol-preferring [EC:1.1.1.1]

	#gene entry fields
	sequence_name_pattern = re.compile(r"^E\s+([.A-Z0-9]+)")
	common_name_pattern = re.compile(r"\s([-a-z0-9]+);\s")
	description_pattern = re.compile(r"\s(.+)$")
	
	#kegg entry fields
	id_pattern = r"(?P<kegg_id>K\d{5})\s"
	kegg_description_pattern = r"(?P<kegg_descrition>.*\s)"
	ec_list_pattern = r"\[EC:(?P<EC>\d+\.\d+\.\d+\.\d+?\s)+\]"

	hierarchy = defaultdict(Entry)
	line_buffer = []
	ec_line = ""

	for line in open(args.keg_file):
		if ec_line_pattern.match(line) and not line_buffer:	
			ec_line = line
		elif enzyme_line_pattern.match(line) and ec_line:
			line_buffer.append(line)
		elif ec_line_pattern.match(line) and line_buffer:
			#Record new complete entry
			ec_match = ec_entry_pattern.match(ec_line)
			ec_number = ec_match.group("EC")
			ec_description = ec_match.group("description")
			print "EC:",ec_number,";",ec_description
			
			for description_line in line_buffer:
				protein_entry,kegg_entry = description_line.split("\t")
				
				sequence_name = sequence_name_pattern.search(protein_entry).group(1)

				common_name_match = common_name_pattern.search(protein_entry)
				if common_name_match: 
					common_name = common_name_match.group(1)
				else:
					common_name = ""

				description = description_pattern.search(protein_entry).group(1)

				print sequence_name, common_name, description

			line_buffer = []
			
