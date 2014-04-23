#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys

SAVE_PATH = ""

def save(content, counter):
    file = codecs.open(SAVE_PATH + "." + str(counter) + ".json", "w", "utf-8")
    for line in content:
        file.write(line)
    file.close()

if __name__ == '__main__':
    """To split big (over 10000 lines) input file:
    python split_files.py input_path.json

    Output will be named input_path.0.json, input_path.1.json, etc."""

    path = "sample.json"
    if len(sys.argv) > 1:
        path = str(sys.argv[1])

    # WARNING! Correct only for *.json files!
    SAVE_PATH = path[:-5:]

    print "Splitting file " + path + ":"

    f = open(path, 'r')
    insides = u""
    l_counter = 1
    f_counter = 0
    for line in f:
        if l_counter % 1000 == 0:
            print str(l_counter/10) + " ads watched."
        insides += line
        if l_counter % 10000 == 0:
            insides = insides[:-2:] + "]"
            save(insides, f_counter)
            insides = u"["
            print "File nr " + str(f_counter) + " created."
            f_counter += 1
        l_counter += 1
    save(insides, f_counter)
    print "File nr " + str(f_counter) + " created.\nThat's all!"
