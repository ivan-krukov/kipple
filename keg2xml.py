#Exports .keg BRITE hierarchy (htext) into a parsable xml format

from argparse import ArgumentParser
from cgi import escape

top = '<?xml version="1.0" encoding="UTF-8"?>\n<KEGG>'
bottom = "</KEGG>"

"""KEGG htext stores level of hierarchy as a capital letter, starting at A
	This returns a numerical value corresponding to the level of hierarchy
"""
def hierarchy_level(htext_line):
	return ord(htext_line[:1])-65

def hierarchy_char(level):
	return chr(level+65)

def print_with_header(string, header):
	print "<{}>".format(header)
	print string
	print "</{}>".format(header)

if __name__=="__main__":
	parser = ArgumentParser("Parses a .keg BRITE hierarchy file (htext)")
	parser.add_argument("keg_file",type=str,help="Input .keg file")
	args = parser.parse_args()

	print top
	for line in open(args.keg_file):
		level = hierarchy_level(line)


		#TODO: resolve comments and other things - need to look up more htext files
		if level >= 0:

			content = escape(line[1:].strip())
			if content:
				print "<"+hierarchy_char(level)+">"
				#if we have a data line
				if "\t" in content:
					common,kegg = content.split("\t") 
					print_with_header(common,"commonData")
					print_with_header(kegg,"keggData")
				else:
					print content
				print "</"+hierarchy_char(level)+">"
	print bottom
					
