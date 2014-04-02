#!/usr/bin/env python
# -*- coding: utf-8 -*-

class json_transform_tests(unittest.TestCase):

    def test_empty_one(self):
        self.maxDiff = None
        expected = True
        results = True
        self.assertEqual(expected, results)

if __name__ == '__main__':
    unittest.main()
