#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import solr

# from files import save_file as save

""" This file contains logic of network connections. """

def send_file_to_solr(content, solr_core_address):
    """ Sending content to a solr server and returning number of sent ads. """
    # Create a connection to a solr server
    s = solr.Solr(solr_core_address)

    # save(content, "debug_n.tmp")
    jsons = json.loads(content)

    counter = 0

    for ad in jsons:
        counter += 1
        s.add(ad)
        print str(counter) + " of " + str(len(jsons))

    return counter
