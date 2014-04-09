#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import string
import sys

""" This file contains Json transformation methods used by a Flat Searcher."""

def json_transform(json_insides):
    """Transformation of Json into another Json preferred by Solr."""
    insides = json_insides.replace('" ','"')
    insides = edit_as_dict(insides)
    insides = insides.replace('\\n','3ekBXfPdoceTmC58QFez')
    insides = insides.decode('unicode_escape')
    insides = insides.replace('3ekBXfPdoceTmC58QFez', '\\n')
    return insides

def edit_as_dict(insides):
    """Editing inside fields of Json."""
    json_insides = json.loads(insides)
    for ad in json_insides:
        # TODO: What if there's no url? What about id?
        if u"url" in ad:
            ad[u"id"] = ad[u"url"]
        if u"price" in ad:
            ad[u"price"] = re.sub("[^0123456789\.,]","",ad[u"price"])
        if u"rooms" in ad:
            ad[u"rooms"] = re.sub("[^0123456789\.,]","",ad[u"rooms"])
        # If we can delete this entry - uncomment.
        # if len(ad[u"rooms"]) == 0:
        #     del ad[u"rooms"]

    # Place for other operations made on json "insides".

    return json.dumps(json_insides, indent=4)
