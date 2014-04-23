#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from files import open_file as open_f
from files import save_file as save_f
from json_transform import json_transform as transform
from network import send_file_to_solr as send_f

""" This file contains main method correcting json file returned by a crawler.
"""

SOLR_SERVER = ""

if __name__ == '__main__':
    """To transform file with JSONs call:
    python __init__.py input_path.json output_path.json

    If You prefer - just use this programme to send it to your solr:
    python __init__.py input_path.json -w http://server.address.com/solr/collection1/

    Default it's saving input file into output file."""

    path = "sample.json"
    # TODO: When dirs structure will be settled - change default path!
    if len(sys.argv) > 1:
        path = str(sys.argv[1])
    save_path = path + ".out"

    print "Opening file " + path + " .."

    file_insides = open_f(path)

    print "File opened!"

    output = transform(file_insides)

    print "Input file transformation completed!"

    if len(sys.argv) == 3:
        save_path = str(sys.argv[2])
        save_f(output, save_path)
        print "Success! Output file: " + save_path
    elif len(sys.argv) == 4:
        if str(sys.argv[2])[1] == 'w':
            solr_server = str(sys.argv[3])
            mess = str(send_f(output, solr_server))
            print "Success! All " + mess + " ads sent to the server!"
        else:
            print "ERROR! No -w in args!"
    else:
        save_f(output, save_path)
        print "Success! Output file: " + save_path
