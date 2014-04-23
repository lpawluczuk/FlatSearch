#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import md5
import re
import string
import sys
import uuid

from additional import found_city as city_found
from additional import lower_string as low
from additional import only_numbers as num

# from files import save_file as save

""" This file contains Json transformation methods used by a Flat Searcher. """

def json_transform(json_insides):
    """Transformation of Json into another Json preferred by Solr. """
    insides = json_insides.replace('" ','"')

    # print "Pre-replaces started.."

    # Thanks to all users who use \" in text.
    insides = insides.replace('\\\\\\"', "'")
    insides = insides.replace('\\"', "'")
    insides = insides.replace('\\m', "/m")
    insides = insides.replace('\\\\', "/")
    insides = insides.replace('\\t', " ")
    insides = insides.replace('\t', " ")

    print "Pre-replaces completed!"

    # save(insides, "debug_t.tmp")
    insides = edit_as_dict(insides)

    print "Disctionary conversion completed!"

    insides = insides.replace('\\n','3ekBXfPdoceTmC58QFez')
    insides = insides.decode('unicode_escape')
    insides = insides.replace('3ekBXfPdoceTmC58QFez', '\\n')

    print "Unicode escape completed!"

    return insides

def edit_as_dict(insides):
    """Editing inside fields of Json. """
    json_insides = json.loads(insides)
    for ad in json_insides:
        if u"url" in ad:
            m = md5.new(ad[u"url"])
            ad[u"id"] = str(uuid.UUID(m.hexdigest()))
        if u"address" in ad:
            ad[u"address"] = low(ad[u"address"])
            ad[u"city"] = city_found(ad[u"address"], ad[u"url"])
        if u"desc" in ad:
            ad[u"text"] = ad[u"desc"].replace("\\quot;", "").replace("\\'", "'")
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
