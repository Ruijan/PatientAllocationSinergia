#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 18:28:32 2018

@author: cnbi
"""

import unittest
import sys
sys.path.insert(0, 'src')
sys.path.insert(0, '../src')
from Database import Database
import DatabaseError
import os.path

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database = Database()
        self.database.fileName = "database.csv"
        self.database.folder = "database"
        self.fields = ["SubjectId", "Age"]
        self.entry = {self.fields[0]: 's01', self.fields[1]: 56}
        
        
    def testCreateDatabase(self):
        self.database.create()
        self.assertTrue(os.path.isfile(self.database.folder + "/" + self.database.fileName))
        self.database.destroy()
    
    def testCreateDatabaseWithEmptyFileNameShouldTrow(self):
        self.database.fileName = ""
        with self.assertRaises(DatabaseError.EmptyFileNameError):
            self.database.create()
        
    def testCreateDatabaseFileExistShouldThrow(self):
        self.database.create()
        with self.assertRaises(DatabaseError.FileExistError):
            self.database.create()
        self.database.destroy()
        
    def testDestroyFile(self):
        self.database.create()
        self.database.destroy()
        self.assertFalse(os.path.isfile(self.database.folder + "/" + self.database.fileName))
            
    def testDestroyFileDoesNotExistShouldThrow(self):
        with self.assertRaises(DatabaseError.FileNotExistError):
            self.database.destroy()
            
    def testAddField(self):
        self.database.addField(self.fields[0])
        self.assertEqual(self.database.fields[0],self.fields[0])
        
    def testAddEmptyFieldShouldThrow(self):
        with self.assertRaises(DatabaseError.EmptyFieldError):
            self.database.addField("")
        
    def testAddFields(self):
        self.database.addFields(self.fields)
        self.assertEqual(self.database.fields, self.fields)
        
    def testLoadDatabase(self):
        self.database.fileName = "filledDatabase.csv"
        self.database.load()
        self.assertEqual(self.database.fields, self.fields)
        
    def testFieldsAddedToCSV(self):
        self.database.addFields(self.fields)
        self.database.create()
        self.database.fields = []
        self.database.load()
        self.assertEqual(self.database.fields, self.fields)
        self.database.destroy()
        
    def testAddEntry(self):
        self.database.addFields(self.fields)
    
    def tearDown(self):
        pass        

if __name__ == '__main__':
    unittest.main()