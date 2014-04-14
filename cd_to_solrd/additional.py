#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

""" This file contains additional functions. """

def only_numbers(string):
    """ Rip all numbers from string. """
    return re.sub("[^0123456789\.,]", "", string)
