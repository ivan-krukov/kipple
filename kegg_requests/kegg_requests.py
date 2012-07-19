"""
Request reaction descriptions from KEGG based on the EC numbers
"""
import argparse
import requests
import re
from reaction_parse import *
from progress_meter import *
from bs4 import BeautifulSoup
def list_repr(l):
	representation = ""
	for i in l:
		representation+=str(i)+","
	return representation

if __name__=="__main__":
	host = "http://www.genome.jp/"
	reaction_query = host+"dbget-bin/www_bget?ec:{}"
	reaction_list_pattern = re.compile(r"/dbget-bin/www_bget\?reaction\+(?:R\d{5}\+?)+")

	parser = argparse.ArgumentParser()
	parser.add_argument("input_file",type=open,help="File containing EC numbers, one per line")
	parser.add_argument("output_file",type=argparse.FileType("w"),help="Ouput file")
	args = parser.parse_args()
	
	lines = args.input_file.readlines()
	args.input_file.close()
	meter = ProgressMeter(len(lines),update_time=1)
	meter.update(0)
		
	for line in lines:
		ec_number = line.strip()
		ec_page = requests.get(reaction_query.format(ec_number))
		reaction_list_link = reaction_list_pattern.search(ec_page.text)
		if reaction_list_link:
			link = host + reaction_list_link.group(0)
			reactions_page = requests.get(link)
			page_tree = BeautifulSoup(reactions_page.text)
			reaction_tables = page_tree.div.find_all("table", recursive = False)
			for table in reaction_tables:
				r = KReaction(table)
				args.output_file.write(repr(r))
		meter.step()
	args.output_file.close()
