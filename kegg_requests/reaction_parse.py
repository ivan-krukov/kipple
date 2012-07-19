"""
Parse a reaction definition from a KEGG entry
"""
from bs4 import BeautifulSoup

#Curency metabolite list as defined by Huss and Holme, 2007
__currency_metabolites = set(["C00001",	#water
							"C00002",	#ATP
							"C00003",	#NAD+
							"C00004",	#NADH
							"C00005",	#NADPH
							"C00006",	#NADP+
							"C00007",	#O2
							"C00008",	#ADP
							"C00011",	#CO2
							"C00080"])	#H+
class KReaction:

	def __init__(self,entry_tree):
		self.pathways = list()
		self.reaction_pairs = list()
		self.enzymes = list()
		self.orthology = list()
		
		#parse the page
		for cell in entry_tree("tr"):
			title = cell.find("nobr")
			if title:
				if "Entry" in title.text:
					self.kegg_id = cell.code.text.strip().split()[0]
				elif "Name" in title.text:
					self.name = cell.div.text.strip()
				elif "Equation" in title.text:
					self.equation = cell.div.text.strip()
				elif "RPair" in title.text:
					for subcell in cell.find_all("tr"):
						pair_entry = self.__split_unicode(subcell.text)
						self.reaction_pairs.append(pair_entry)
				elif "Enzyme" in title.text:
					self.enzymes = self.__split_unicode(cell.div.text)
				elif "Pathway" in title.text:
					for subcell in cell.find_all("tr"):
						pathway_entry = self.__split_unicode(subcell.text)
						self.pathways.append(pathway_entry)
				elif "Orthology" in title.text:
					for subcell in cell.find_all("tr"):
						orthology_entry = self.__split_unicode(subcell.text)
						self.orthology.append(orthology_entry)

		#parse substrates and products
		sub, prod = self.equation.strip().split(" <=> ")
		self.substrates = set(sub.split(" + "))
		self.products = set(prod.split(" + "))

	def __split_unicode(self,string):
		return [token for token in string.strip().split(u"\xa0") if not token == ""]

	def __table_repr(self,unicode_list):
		representation = ""
		for row in unicode_list:
			representation+="\t"
			for column in row:
				representation += column+" "
			representation+="\n"
		return representation

	def __list_repr(self,unicode_list):
		representation = ""
		for column in unicode_list:
			representation+="\t"
			representation += column+"\n"
		return representation

	def __repr__(self):
		return unicode("KEGG ID:\t"+self.kegg_id+"\n"+\
		"Name:\t\t"+self.name+"\n"+\
		"Equation:\t"+self.equation+"\n"+\
		"RPairs:\n"+self.__table_repr(self.reaction_pairs)+\
		"Enzyme(s):\n"+self.__list_repr(self.enzymes)+\
		"Pathways:\n"+self.__table_repr(self.pathways)+\
		"Orthology:\n"+self.__table_repr(self.orthology)).encode("utf-8")

def exclude_currency (metabolites):
	return metabolites.difference(__currency_metabolites)

