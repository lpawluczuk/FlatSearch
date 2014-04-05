#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from files import open_file as open_f
from files import save_file as save_f
from json_transform import json_transform as transform

""" This file contains main method correcting json file returned by a crawler.
"""

if __name__ == '__main__':
    """To transform file with JSONs call:
    "python __init__.py input_path.json output_path.json" """
    path = "sample.json"
    # TODO: When dirs structure will be settled - change default path!
    if len(sys.argv) > 1:
        path = str(sys.argv[1])
    save_path = path + ".out"
    if len(sys.argv) > 2:
        save_path = str(sys.argv[2])
    file_insides = open_f(path)
    output = transform(file_insides)
    save_f(output, save_path)
    