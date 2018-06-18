#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 18:28:32 2018

@author: cnbi
"""

import unittest
import sys
sys.path.insert(0, '../src')
from DatabaseCreator import DatabaseCreator
import os.path

class TestDatabaseCreator(unittest.TestCase):
    def testCreator(self):
        creator = DatabaseCreator()
        creator.fileName = "database.csv"
        creator.folder = "database"
        creator.create()
        self.assertTrue(os.path.isfile(creator.folder + "/" + creator.fileName))

if __name__ == '__main__':
    unittest.main()