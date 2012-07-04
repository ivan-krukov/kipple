#!/usr/bin/env python

#Quick screen-scrapping for getting a gene description from Ensembl
#Input: file, with a gene name for each line

import requests
import re
import sys

#simple progress meter thingie
class ProgressMeter:
	def __init__(self,job_size):
		self.job_size=float(job_size)
		self.steps_done=float(0)

	def step (self):
		self.steps_done +=1
		self.__show__(self.steps_done)

	def update (self, step):
		self.steps_done = step
		self.__show__(self.steps_done)

	def __show__ (self,complete):
		sys.stderr.write("Working: {:.2%} done\r".format(complete/self.job_size))
		sys.stderr.flush()

	def done(self):
		clear = chr(27) + '[2K' + chr(27) +'[G'
		sys.stderr.write(clear + "Job complete!\n")
		sys.stderr.flush()

input_file = sys.argv[1]
species = "Caenorhabditis_elegans"
query_list = list()
fetch_url = "http://uswest.ensembl.org/{}/Search/Details?species={};idx=Gene;q={}"

"""Example:
<dl class="summary">
  <dt>Description</dt>
  <dd>UDP-GlucuronosylTransferase family member (ugt-13)  [Source:RefSeq peptide;Acc:NP_504317] [Type: protein coding Coding genes]</dd>
</dl>"""

pattern = re.compile(r'<dl class="summary">\n\s+<dt>Description</dt>\n\s+<dd>(?P<info>.*)</dd>\n</dl>')

for line in open(input_file):
	query_list.append(line.strip())

job_size = len(query_list)
meter = ProgressMeter(job_size)
lines_done = 0

for query in query_list:
	url = fetch_url.format(species,species,query)
	r = requests.get(url)
	html = r.text
	entry = pattern.search(html).group("info")
	print "{},{}".format(query,entry)
	
	lines_done += 1
	meter.update(lines_done)


