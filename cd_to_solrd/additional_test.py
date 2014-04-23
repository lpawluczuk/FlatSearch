#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from additional import lower_string as low

class additional_tests(unittest.TestCase):

    def test_lower_1(self):
        self.maxDiff = None
        expected = u"łódź"
        results = low(u"Łódź")
        self.assertEqual(expected, results)

    def test_lower_2(self):
        self.maxDiff = None
        expected = u"łódź"
        results = low(u"ŁÓDŹ")
        self.assertEqual(expected, results)

    def test_lower_3(self):
        self.maxDiff = None
        expected = u"ąęóżźćńłś"
        results = low(u"ĄĘÓŻŹĆŃŁŚ")
        self.assertEqual(expected, results)

if __name__ == '__main__':
    unittest.main()
