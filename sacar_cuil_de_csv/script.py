#pdfs augusto:
#numero de inscripcion
#cuit
# ---- ---- ----
# primero convertir los pdf a xml en bash con el sig comando:
	# for file in *.pdf; do pdftohtml -xml $file; done

import csv
from os import listdir
from xml.dom import minidom

mypath = "."
files = [ f for f in listdir(mypath) if f.endswith(".xml") ]

path = "output.csv"
ofile = open(path, "wb")
writer = csv.writer(ofile, delimiter=',')
writer.writerow(['archivo', 'inscripcion', 'cuit'])

for f in files:
	xmldoc = minidom.parse(f)
	archivo = f.split('.')[0] + ".pdf"
	inscripcion = xmldoc.childNodes[1].childNodes[1].childNodes[35].firstChild.firstChild.nodeValue
	cuit = xmldoc.childNodes[1].childNodes[1].childNodes[37].firstChild.firstChild.nodeValue
	writer.writerow([archivo, inscripcion, cuit])

ofile.close()
