#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MODULES

import sys
import xml.etree.ElementTree as ET

# FUNCTIONS

def main():
  # open file and read html
  try:
    src = str(sys.argv[1])
  except IndexError:
    print '\nNo file provided. Usage: main.py filename\n'
    return
  # is it possible to parse html with ElementTree???
  tree = ET.parse(src)
  return tree

# TEST

if __name__ == '__main__':
   main() 