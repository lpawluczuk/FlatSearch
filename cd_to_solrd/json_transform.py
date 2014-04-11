#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import md5
import re
import string
import sys
import uuid

""" This file contains Json transformation methods used by a Flat Searcher."""

def json_transform(json_insides):
    """Transformation of Json into another Json preferred by Solr."""
    insides = json_insides.replace('" ','"')
    # Thanks to all users who use \" in text.
    insides = insides.replace('\\\\\\"', "'")
    insides = insides.replace('\\"', "'")
    insides = insides.replace('\\m', "/m")

    insides = edit_as_dict(insides)
    insides = insides.replace('\\n','3ekBXfPdoceTmC58QFez')
    insides = insides.decode('unicode_escape')
    insides = insides.replace('3ekBXfPdoceTmC58QFez', '\\n')
    return insides

def edit_as_dict(insides):
    """Editing inside fields of Json."""
    json_insides = json.loads(insides)
    for ad in json_insides:
        if u"url" in ad:
            m = md5.new(ad[u"url"])
            ad[u"id"] = str(uuid.UUID(m.hexdigest()))
        if u"area" in ad:
            ad[u"area"] = re.sub("[^0123456789\.,]","",ad[u"area"])
        if u"price" in ad:
            ad[u"price"] = re.sub("[^0123456789\.,]","",ad[u"price"])
        if u"rooms" in ad:
            ad[u"rooms"] = re.sub("[^0123456789\.,]","",ad[u"rooms"])
        if u"desc" in ad:
            ad[u"text"] = ad[u"desc"]
            del ad[u"desc"]
        if u"_version_" not in ad:
            ad[u"_version_"] = 0
        if len(ad[u"rooms"]) == 0:
            del ad[u"rooms"]

    # Place for other operations made on json "insides".

    return json.dumps(json_insides, indent=4)
