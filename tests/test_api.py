# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 18:00:46 2012

@author: Max Lang
"""

import unittest
from shoppersherpa.api import api

class TestApi(unittest.TestCase):
    def test_badQuery(self):
        badJson = "this isn't a json string"
        emptyJson = ""
        self.assertRaises(ValueError,api.query,badJson)
        self.assertRaises(ValueError,api.query,emptyJson)

if __name__ == '__main__':
    unittest.main(verbosity=2,buffer=True)