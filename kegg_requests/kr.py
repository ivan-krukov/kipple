"""
Request reaction descriptions from KEGG based on the EC numbers
"""

import requests
import re

reaction_query = "http://www.genome.jp/dbget-bin/get_linkdb?-t+reaction+ec:{}"
reaction_definition = "http://www.genome.jp/dbget-bin/www_bget?rn:{}"

kegg_reaction = re.compile(r"R\d{5}")

reactions_page = requests.get(reaction_query.format("1.1.1.1"))

reactions_list = kegg_reaction.findall(reactions_page.text)

for reaction in reactions_list:
	reaction_page = requests.get(reaction_definition.format(reaction))
	print reaction_page.text
