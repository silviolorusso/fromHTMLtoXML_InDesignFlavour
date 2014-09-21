#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################################
# From HTML to XML - InDesign flavour #
#######################################

### Modules
import re
import sys
from bs4 import BeautifulSoup


### Functions
def delete_head_tags(xml_soup):
	toDelete = ["doctype", "html", "head", "title", "base", "link", "meta", "style", "script", "noscript"]

def clean_linebreaks(html_string):
	"""Return an html string..."""

	cleaned = re.sub(r'(?<!>)\n+',' ', html_string)
	return cleaned


def extract_body_from_html(html_soup):
	"""Return an XML beautiful soup object with the <body> of the input HTML file"""

	body = html_soup.body.extract()
	xml_soup = BeautifulSoup('', 'xml')
	xml_soup.append(body)

	return xml_soup


def convert_footnotes(xml_soup):
	"""Return a beautiful xml soup..."""

	if xml_soup.find_all('li', id=re.compile("fn*.")):

		# Iterate through footnotes
		footnotes = xml_soup.find_all('a', id=re.compile("fnref*."))
		for index_footnote, each_footnote in enumerate(footnotes):
			footnote_content = xml_soup.find_all('li', id=re.compile("fn*."))[index_footnote];
			
			# clean fn back link (↵)
			footnote_content = footnote_content.contents[0]
			
			# remove surrounding <p>?
			footnote_content.find('a', href=re.compile("#fnref*.")).extract()

			# encoding problem with <
			footnote_content = str(footnote_content)
			each_footnote.replace_with("-fn--" + footnote_content + "--fn-") # to fit the requirements of ReFoot_mod.js

		# clean footnotes from xml
		footnotes = xml_soup.find('div', { "class" : "footnotes" })
		footnotes.extract()

		# remove footnotes title
		footnotes_title = xml_soup.find('h2', id="notes")
		footnotes_title.extract()

	return xml_soup


def convert_HTMLtable_to_XMLCALStable(xml_soup, table_width = 300):
	"""Return a Beautiful xml Soup...""" 

	def calc_headerRowsNumber(HTML_table):

		# tbody approach
		thead = HTML_table.find('thead')
		if thead:
			len_header = len(thead.find_all('tr'))
		
		# th approach
		else:
			len_header = 0
			for each_row in HTML_table.find_all('tr'):
				tag_list =[x.name for x in each_row.find_all(True)]
				if 'th' in tag_list:
					len_header +=1

		return len_header


	def calcRowsNumber(xml_soup):
		rows = xml_soup.find_all('tr')
		return len(rows)

	def calcColsNumber(xml_soup):
		cols_number = 0

		# Iterating over the rows of the table
		for each_row in xml_soup.find_all('tr'):
			cells = each_row.find_all('td')

			if cols_number < len(cells):
				cols_number = len(cells)

		return cols_number


	def createTagWithAttributesPlusString(xml_soup, tag_name, dict_attrib, new_string):
		# New tag declaration
		new_tag = xml_soup.new_tag(tag_name)

		# Looking for present attributes to move inside the new tag
		if dict_attrib:
			for k, v in dict_attrib.items():
				new_tag[k] = v

		# New string to put inside the tag
		new_string = xml_soup.new_string(new_string)

		# Appending the string inside the tag
		new_tag.append(new_string)
		
		return new_tag

	# Grab table tag
	HTML_tables = xml_soup.find_all('table')

	for index_table, each_HTML_table in enumerate(HTML_tables):

		# Vars
		table_name = "table_%#03d" % (index_table+1)
		header_rows_number = calc_headerRowsNumber(each_HTML_table)

		# Rows and cols number calculation
		cols_number = calcColsNumber(each_HTML_table)

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
		for i, each_row in enumerate(each_HTML_table.find_all('tr')):

			# Creating tag 'row'
			row_tag = createTagWithAttributesPlusString(CALS_table, 'row', None, '')

			# Iterating over 'td' (HTML cells tags)
			for j, each_col in enumerate(each_row.find_all(['td', 'th'])):

				# Extracting contents from HTML cells
				cell_content = each_col.text.replace('\t', '').replace('\n', ' ').lstrip().rstrip()

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
				entry_tag.string = cell_content

				# Appending cell into row
				row_tag.append(entry_tag)

			if i <= header_rows_number-1:
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

		# Replacement with the new table
		each_HTML_table.replace_with(root_tag)

	return xml_soup


def main():
	# Terminal input
	source_path = str(sys.argv[1])

	# Reading html file
	html_file = open(source_path, 'r+')
	html_doc = html_file.read()

	# Cleaning and calling bs4
	clean_html_doc = clean_linebreaks(html_doc)
	html_soup = BeautifulSoup(clean_html_doc, 'html')

	# Parsing and converting the tree
	xml_soup = extract_body_from_html(html_soup)
	xml_soup = convert_footnotes(xml_soup)
	xml_soup = convert_HTMLtable_to_XMLCALStable(xml_soup)

	# Writing the output
	output_xml = open(source_path[:-4]+'xml', "w+")
	output_xml.write(str(xml_soup))
	output_xml.close()


### Instructions
if __name__ == '__main__':
	main()

