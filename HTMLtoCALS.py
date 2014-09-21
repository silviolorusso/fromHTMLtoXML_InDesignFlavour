#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################
# from HTML Table to XML CALS Table #
#####################################

### Open libraries
from bs4 import BeautifulSoup
import sys

### Functions
def calcRowsNumber(soup):
	rows = soup.find_all('tr')
	return len(rows)

def calcColsNumber(soup):
	cols_number = 0

	# Iterating over the rows of the table
	for each_row in soup.find_all('tr'):
		cells = each_row.find_all('td')

		if cols_number < len(cells):
			cols_number = len(cells)

	return cols_number


def createTagWithAttributesPlusString(soup, tag_name, dict_attrib, new_string):
	# New tag declaration
	new_tag = soup.new_tag(tag_name)

	# Looking for present attributes to move inside the new tag
	if dict_attrib:
		for k, v in dict_attrib.items():
			new_tag[k] = v

	# New string to put inside the tag
	new_string = soup.new_string(new_string)

	# Appending the string inside the tag
	new_tag.append(new_string)
	
	return new_tag


### Variables
input_file_path = '/Users/robertoarista/Desktop/conversione/sezioni/tab_finali/tab'+ str(num) +'.html'

table_width = 170.0 #mm

header_row_number = 1

table_name = 'tabella03_'+ str(num)

### Instructions
# Opening source file
table_file = open(input_file_path, 'r').read()
HTML_table = BeautifulSoup(table_file)

# Rows and cols number calculation
cols_number = calcColsNumber(HTML_table)

# New tree
CALS_table = BeautifulSoup('', 'xml')
root_tag = createTagWithAttributesPlusString(CALS_table, table_name, None, '')

# Creating tag 'table'
table_tag_attributes = {'frame':'all'}
table_tag = createTagWithAttributesPlusString(CALS_table, 'table', table_tag_attributes, '')

# Creating tag 'tgroup'
tgroup_tag_attributes = {'cols': cols_number}
tgroup_tag = createTagWithAttributesPlusString(CALS_table, 'tgroup', tgroup_tag_attributes, '')

# Creating tag 'colspec'
for i in xrange(1, cols_number+1):
	colspec_tag_attributes = {
		'colname':"c%01d" % i,
		'colwidth': "%01dmm" % (table_width / cols_number)
		}
	colspec_tag = createTagWithAttributesPlusString(CALS_table, 'colspec', colspec_tag_attributes, '')
	tgroup_tag.append(colspec_tag)

# Creating tag 'thead' e 'tbody'
head_tag = createTagWithAttributesPlusString(CALS_table, 'thead', None, '')
body_tag = createTagWithAttributesPlusString(CALS_table, 'tbody', None, '')

# Iterating over HTML rows
for i, each_row in enumerate(HTML_table.find_all('tr')):

	# Creating tag 'row'
	row_tag = createTagWithAttributesPlusString(CALS_table, 'row', None, '')

	# Iterating over 'td' (HTML cells tags)
	for j, each_col in enumerate(each_row.find_all('td')):

		# Extracting contents from HTML cells
		contenuto_cell = each_col.text.replace('\t', '').replace('\n', ' ').lstrip().rstrip()

		# Attributes for entry tag (CALS cell)
		entry_tag_attributes = {'align':"left", 'valign':"top"}

		# Multiple rows cell
		if 'rowspan' in each_col.attrs:
			entry_tag_attributes['morerows'] = int(each_col.attrs['rowspan'])-1

		# Multiple columns cell
		if 'colspan' in each_col.attrs:
			begin = "c%01d" % (j+1)
			end =  "c%01d" % (j+int(each_col.attrs['colspan']))

			entry_tag_attributes['namest'] = begin
			entry_tag_attributes['nameend'] = end

		# Creating 'entry' tag (CALS cell)
		entry_tag = createTagWithAttributesPlusString(CALS_table, 'entry', entry_tag_attributes, '')
		entry_tag.string = contenuto_cell

		# Appending cell into row
		row_tag.append(entry_tag)

	if i <= header_row_number-1:
		head_tag.append(row_tag)
	else:
		body_tag.append(row_tag)

# Appending header to table
tgroup_tag.append(head_tag)
tgroup_tag.append(body_tag)

# Appending tgroup to table
table_tag.append(tgroup_tag)

# Appending table to root
root_tag.append(table_tag)

# Appending root to soup
CALS_table.append(root_tag)

# Writing table to xml file
with open(input_file_path[:-4]+'xml', "w") as myfile:
	myfile.write(CALS_table.prettify().encode('utf-8'))

