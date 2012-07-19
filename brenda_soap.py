from SOAPpy import WSDL

client = WSDL.Proxy("http://www.brenda-enzymes.info/soap2/brenda.wsdl"
)
resultString = client.getSubstratesProducts("ecNumber*1.1.1.22#organism*Caenorhabditis elegans")
lines = resultString.split("!")

for line in lines:
	fields = line.split("#")
	for field in fields:
		for entry in field.split("*"):
			print entry," "
	print "\n"
