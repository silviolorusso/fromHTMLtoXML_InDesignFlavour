# -*- coding: utf-8 -*-

#############
# footnotes #
#############

### Apertura librerie
from bs4 import BeautifulSoup
import sys

### Variabili
input_file = 'cap03 copia.xml'

tree_doc = open(input_file, 'r').read()
soup = BeautifulSoup(tree_doc, 'xml')

# Iterazioni sulle note sparse per il testo
for i, SUP in enumerate(soup.find_all('SUP')):


	nota = soup.find_all('DIV', ID = 'sdfootnote'+ SUP.string)
	contenuto_nota = nota[0].text.replace('\t', '').replace('\n', '')
	#print contenuto_nota.encode('utf-8')

	SUP.replace_with("'AWSEDRFTGY'" + contenuto_nota + "'YGTFRDESWA'")

print soup