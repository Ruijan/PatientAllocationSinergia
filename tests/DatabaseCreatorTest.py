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
import DatabaseError
import os.path

class TestDatabaseCreator(unittest.TestCase):
    def setUp(self):
        self.creator = DatabaseCreator()
        self.creator.fileName = "database.csv"
        self.creator.folder = "database"
        
    def testAddField(self):
        self.creator.addField("SubjectId")
        self.assertEqual(self.creator.fields[0],"SubjectId")
        self.creator.addField("Age")
        self.assertEqual(self.creator.fields[1],"Age")
        
    def testCreator(self):
        self.creator.create()
        self.assertTrue(os.path.isfile(self.creator.folder + "/" + self.creator.fileName))
        self.creator.destroy()
    
    def testCreatorWithEmptyFileNameShouldTrow(self):
        self.creator.fileName = ""
        with self.assertRaises(DatabaseError.EmptyFileNameError):
            self.creator.create()
        
    def testCreatorFileExistShouldThrow(self):
        self.creator.create()
        with self.assertRaises(DatabaseError.FileExistError):
            self.creator.create()
        self.creator.destroy()
        
    def testDestroyFile(self):
        self.creator.create()
        self.creator.destroy()
        self.assertFalse(os.path.isfile(self.creator.folder + "/" + self.creator.fileName))
            
    def testDestroyFileDoesNotExistShouldThrow(self):
        with self.assertRaises(DatabaseError.FileNotExistError):
            self.creator.destroy()
    
    def tearDown(self):
        pass        

if __name__ == '__main__':
    unittest.main()