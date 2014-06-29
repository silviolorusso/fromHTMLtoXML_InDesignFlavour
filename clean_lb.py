#!/usr/bin/env python
# -*- coding: utf-8 -*-

# looks for linebreaks that are not preceded by a '>' and substitutes them with a white space.

# MODULES

import re, sys

# FUNCTIONS

def clean_linebreaks(xml):
  clean = re.sub(r'(?<!>)\n+',' ', xml)
  return clean

# TEST

if __name__ == '__main__':
  src = str(sys.argv[1])
  f = open(src, 'r+')
  xml = f.read()
  print clean_linebreaks(xml)
