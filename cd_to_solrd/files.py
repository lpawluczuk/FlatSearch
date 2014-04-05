#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

""" This file contains logic of file IN/OUT operations. """

def open_file(path):
    """ Opening a file specified by a path. Returns a file content."""
    f = open(path, 'r')
    insides = u""
    for line in f:
    	insides += line
    return insides.decode('unicode_escape')
