#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MODULES

import sys
from bs4 import BeautifulSoup
#from BeautifulSoup import BeautifulStoneSoup

from clean_lb import clean_linebreaks
from footnotes import format_fn

# FUNCTIONS

def main():
  # open file and read html
  try:
    src = str(sys.argv[1])
  except IndexError:
    print '\nNo file provided. Usage: main.py filename\n'
    return
  f = open(src, 'r+')
  html = f.read()
  # if there's a body, extract its content, otherwise use it as it is
  soup = BeautifulSoup(html)
  body = ''
  if soup.body:
    # a bit annoying that you loose indents and you get comments
    for t in soup.body.contents:
      body += str(t)
      xml = body
  else:
    xml = str(soup)

  # do stuff

  # clean linebreaks
  xml = clean_linebreaks(xml)

  # format footnotes
  xml = format_fn(xml)

  return xml

# TEST

if __name__ == '__main__':
  print(main()) 