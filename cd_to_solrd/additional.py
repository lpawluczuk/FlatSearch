#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

""" This file contains additional functions. """

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
