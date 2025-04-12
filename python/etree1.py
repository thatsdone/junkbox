#!/usr/bin/python3
#
# elementtree1.py
#
# Description:
#  A simple example to use xml.etree.ElementTree
#  https://docs.python.org/3/library/xml.etree.elementtree.html#
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2025/03/16 v0.1 Initial version
# Authour:
#   Masanori Itoh <masanori.itoh@gmail.com>
#

import sys
import argparse
import xml.etree.ElementTree as ET


# Returns text content of the first found leaf node with the specified tag
def lookup_one(node, tag=None):

    ret = None

    if node.tag == tag:
        return node.text

    for child in node:
        if len(child) == 0:
            if child.tag == tag:
                return child.text
        else:
            ret = lookup_one(child, tag=tag)
    return ret

def traverse(node, level, cutoff_key=None):
    print(level,
          node.tag,
          len(node.text) if node.text else -1,
          len(node))
    if len(node) > 0:
        if node.tag == cutoff_key: # cutoff_key:
            print('  ',
                  lookup_one(node, tag='item1'),
                  ' / ',
                  lookup_one(node, tag='item3'))
            return
        for child in node:
            traverse(child, level+1, cutoff_key=cutoff_key)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='elementtree.py')
    parser.add_argument('-f', '--input_file', default='etree1-data.xml')
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()
    debug = args.debug

    if args.input_file:
        input_file = args.input_file
    else:
        print('Specify input_file')
        sys.exit()

    with open(input_file, 'rt') as fp:
        data = fp.read()
        root = ET.fromstring(data)

        traverse(root, 0, cutoff_key='entry')


