#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import string
import sys

""" This file contains Json transformation methods used by a Flat Searcher."""

def json_transform(json_insides):
    """Transformation of Json into another Json preferred by Solr."""
    insides = json_insides.replace('" ','"')
    insides = insides.replace('\\n','3ekBXfPdoceTmC58QFez')
    insides = insides.decode('unicode_escape')
    return insides.replace('3ekBXfPdoceTmC58QFez', '\\n')
