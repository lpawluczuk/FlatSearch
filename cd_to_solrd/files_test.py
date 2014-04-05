#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from files import open_file

class pta_files_tests(unittest.TestCase):

    def test_opening_of_correct_txt(self):
        self.maxDiff = None
        results = open_file("sample_text_to_test.txt")
        expected = u"test\nof\nfiles\nIs it proper?\nKraków\nPOKÓJ\npiętrze w garażu"
        self.assertEqual(expected, results)

if __name__ == '__main__':
    unittest.main()

