#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MODULES

from bs4 import BeautifulSoup
import sys, re

# FUNCTIONS

def format_fn(xml):
	soup = BeautifulSoup(xml)

	if soup.find_all('li', id=re.compile("fn*.")):
		# Iterate through footnotes
		for i, fn in enumerate(soup.find_all('a', id=re.compile("fnref*."))):
			fn_content = soup.find_all('li', id=re.compile("fn*."))[i];
			# clean fn back link (↵)
			fn_content = fn_content.contents[0]
			# remove surrounding <p>?
			fn_content.find('a', href=re.compile("#fnref*.")).extract()
			# encoding problem with <
			fn_content = str(fn_content)
			fn.replace_with("-fn--" + fn_content + "--fn-") # to fit the requirements of ReFoot_mod.js

		#clean footnotes from xml
		fns = soup.find('div', { "class" : "footnotes" })
		fns.extract()
		# remove footnotes title
		fns_title = soup.find('h2', id="notes")
		fns_title.extract()

	return soup

# TEST

if __name__ == '__main__':
  src = str(sys.argv[1])
  f = open(src, 'r+')
  xml = f.read()
  print format_fn(xml)