"""
Parse a reaction definition from a KEGG entry
"""
from bs4 import BeautifulSoup

class KReaction:
	def __init__(self,entry_html):
		self.__html = entry_html
		self.pathways = list()
		self.reaction_pairs = list()
		self.enzymes = list()
		self.orthology = list()
		
		#parse the page
		page_tree = BeautifulSoup(self.__html)
		for cell in page_tree("tr"):
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


r = KReaction(open("example.html").read())
print r

