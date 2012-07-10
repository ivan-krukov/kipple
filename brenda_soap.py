from SOAPpy import WSDL

client = WSDL.Proxy("http://www.brenda-enzymes.info/soap2/brenda.wsdl"
)
resultString = client.getReaction("ecNumber*1.1.1.1#organism#Caenorhabditis Elegans")
lines = resultString.split("!")

for line in lines:
	fields = line.split("#")
	for field in fields:
		print field.split("*")," "
	print "\n"
