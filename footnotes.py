#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MODULES

from bs4 import BeautifulSoup
import sys, re

# FUNCTIONS

def format_fn(xml):
	soup = BeautifulSoup(xml)

	# Iterate through footnotes
	for i, fn in enumerate(soup.find_all('a', id=re.compile("footnote*."))):
		fn_content = soup.find_all('p', id=re.compile("footnote*."))[i];
		# clean fn back link (↵) by deleting last char
		fn_content = fn_content.text[:-1]
		fn.replace_with("[[NOTE]]" + fn_content + "[[NOTE]]")

	#clean footnotes from xml
	if soup.find_all('p', id=re.compile("footnote*.")):
		fn_old = soup.find_all('p', id=re.compile("footnote*."))[0]
		# remove h3, ol, li, p
		fn_old.parent.parent.previousSibling.previousSibling.extract()
		fn_old.parent.parent.extract()

	return soup

# TEST

if __name__ == '__main__':
  src = str(sys.argv[1])
  f = open(src, 'r+')
  xml = f.read()
  print format_fn(xml)