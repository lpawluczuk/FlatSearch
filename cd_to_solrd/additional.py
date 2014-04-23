#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

""" This file contains additional functions. """

def found_city(address, url):
    """ Return city from address with a help of url. """
    page = url.split("/")[2].replace(u"www.", "").replace(u".pl", "")
    if (page == u"gumtree" or page == u"regiodom"):
        return address.split(u",")[1]
    elif page == u"otodom":
        return address.split(u"miejscowo")[1].split(u",")[0].split(u":")[1]
    elif (page == u"olx" or page == u"morizon"):
        return address.split(u",")[0]

def lower_string(string):
    """ Polish string to lower case polish string. """
    string = string.lower()
    string = string.replace(u"Ą", u"ą")
    string = string.replace(u"Ę", u"ę")
    string = string.replace(u"Ó", u"ó")
    string = string.replace(u"Ż", u"ż")
    string = string.replace(u"Ź", u"ź")
    string = string.replace(u"Ć", u"ć")
    string = string.replace(u"Ń", u"ń")
    string = string.replace(u"Ł", u"ł")
    string = string.replace(u"Ś", u"ś")
    return string

def only_numbers(string):
    """ Rip all numbers from string. """
    return re.sub("[^0123456789\.,]", "", string)
