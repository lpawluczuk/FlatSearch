#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import md5
import re
import string
import sys
import uuid

from additional import only_numbers as num

""" This file contains Json transformation methods used by a Flat Searcher. """

def json_transform(json_insides):
    """Transformation of Json into another Json preferred by Solr. """
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
    """Editing inside fields of Json. """
    json_insides = json.loads(insides)
    for ad in json_insides:
        if u"url" in ad:
            m = md5.new(ad[u"url"])
            ad[u"id"] = str(uuid.UUID(m.hexdigest()))
        if u"desc" in ad:
            ad[u"text"] = ad[u"desc"]
            del ad[u"desc"]
        if u"area" in ad:
            ad[u"area"] = num(ad[u"area"])
        if u"price" in ad:
            ad[u"price"] = num(ad[u"price"])
        if u"rooms" in ad:
            ad[u"rooms"] = num(ad[u"rooms"])
            if len(ad[u"rooms"]) == 0:
                del ad[u"rooms"]
        if u"rooms" not in ad:
            regex = re.compile(r"((\d)+ (.+){0,1}pok(oi|oj|" + u"ój))")
            match_r = regex.search(ad[u"text"])
            if match_r != None:
                ad[u"rooms"] = num(match_r.group(0))
        if u"_version_" not in ad:
            ad[u"_version_"] = 0

    return json.dumps(json_insides, indent=4)
