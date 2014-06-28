#!/usr/bin/env python
# -*- coding: utf-8 -*-

# looks for linebreaks that are not preceded by a '>' and substitutes them with a white space.

# MODULES

import re, sys

# FUNCTIONS

def clean_linebreaks(html):
  clean = re.sub(r'(?<!>)\n+',' ', html)
  return clean

# TEST

if __name__ == '__main__':
  src = str(sys.argv[1])
  f = open(src, 'r+')
  html = f.read()
  print clean_linebreaks(html)
