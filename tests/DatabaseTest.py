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
        self.database.folder = "tests/database"
        self.fields = ["SubjectId", "Age", "Group"]
        self.entry = {self.fields[0]: 's01', self.fields[1]: '56', self.fields[2]: 'BCI'}
        self.ttest = [0, 1, 0]
        self.groups = ["BCI", "Sham"]
        self.created = False

    def testCreateDatabase(self):
        self.database.create()
        self.created = True
        self.assertTrue(os.path.isfile(self.database.folder + "/" + self.database.fileName))
    
    def testCreateDatabaseWithEmptyFileNameShouldTrow(self):
        self.database.fileName = ""
        with self.assertRaises(DatabaseError.EmptyFileNameError):
            self.database.create()
        
    def testDestroyFile(self):
        self.database.create()
        self.database.destroy()
        self.assertFalse(os.path.isfile(self.database.folder + "/" + self.database.fileName))
            
    def testDestroyFileDoesNotExistShouldThrow(self):
        with self.assertRaises(DatabaseError.FileNotExistError):
            self.database.destroy()
            
    def testAddField(self):
        self.database.addField(self.fields[0], self.ttest[0])
        self.assertEqual(self.database.fields[0],self.fields[0])
        self.assertEqual(self.database.ttest[0],self.ttest[0])
        
    def testAddEmptyFieldShouldThrow(self):
        with self.assertRaises(DatabaseError.EmptyFieldError):
            self.database.addField("", False)
        
    def testAddFields(self):
        self.database.addFields(self.fields, self.ttest)
        self.assertEqual(self.database.fields, self.fields)
        
    def testLoadFieldsDatabase(self):
        self.database.fileName = "filledDatabase.csv"
        self.database.load()
        self.assertEqual(self.database.fields, self.fields)
        self.assertEqual(self.database.ttest, self.ttest)
        self.assertEqual(self.database.groups, self.groups)
        
    def testLoadDatabaseWithEmptyFileNameShouldTrow(self):
        self.database.fileName = ""
        with self.assertRaises(DatabaseError.EmptyFileNameError):
            self.database.load()
    
    def testLoadDatabaseWithWrongFileName(self):
        self.database.fileName = "wrongDatabase.csv"
        with self.assertRaises(DatabaseError.FileNotExistError):
            self.database.load()
        
    def testFieldsAddedToCSV(self):
        self.database.addFields(self.fields, self.ttest)
        self.database.create()
        self.created = True
        self.database.fields = []
        self.database.ttest = []
        self.database.load()
        self.assertEqual(self.database.fields, self.fields)
        self.assertEqual(self.database.ttest, self.ttest)
        self.assertEqual(self.database.groups, [])
        
    def testEntriesAddedToCSV(self):
        self.database.addFields(self.fields, self.ttest)
        self.database.groups = self.groups
        self.database.addEntryWithGroup(self.entry)
        self.database.create()
        self.database.fields = []
        self.database.ttest = []
        self.database.groups = []
        self.database.entries = []
        self.database.load()
        self.assertEqual(self.database.fields, self.fields)
        self.assertEqual(self.database.ttest, self.ttest)
        self.assertEqual(self.database.groups, self.groups)
        self.assertEqual(self.database.entries[0], self.entry)
        

    def testAddEntryWithGroup(self):
        self.database.addFields(self.fields, self.ttest)
        self.database.addEntryWithGroup(self.entry)
        self.assertEqual(self.database.entries[0], self.entry)
        
    def testAddEntryWithWrongFieldNames(self):
        self.database.addFields(self.fields, self.ttest)
        wrongFieldsEntry = {self.fields[0]: 's01', 'FMA': 56}
        with self.assertRaises(DatabaseError.EntryWithUnknownFields):
            self.database.addEntryWithGroup(wrongFieldsEntry)
            
    def testLoadingEntryFromDatabase(self):
        self.database.fileName = "filledDatabase.csv"
        self.database.load()
        self.assertEqual(self.database.entries[0], self.entry)
        self.assertEqual(len(self.database.entries), 6)
        
    def testGetPValueFromField(self):
        self.database.fileName = "filledDatabase.csv"
        self.database.load()
        self.assertTrue(self.database.getPValue("Age") < 1)
        self.assertTrue(self.database.getPValue("Age") > 0)
        
    def testGetMostProbableGroupFromEntry(self):
        self.database.fileName = "filledDatabase.csv"
        self.database.load()
        newEntry = {self.fields[0]: 's07', self.fields[1]: '65'}
        groups = []
        for index in range(1,200):
            groups.append(self.database.getGroupFromNewEntry(newEntry))
        countGroup1 = groups.count(self.groups[0])
        countGroup2 = groups.count(self.groups[1])
        self.assertEqual(round(countGroup1/(countGroup2 + countGroup1),1), 0.4)
        
    def testAddEntryToBiasedDatabase(self):
        self.database.fileName = "biasedFilledDatabase.csv"
        self.database.load()
        newEntry = {self.database.fields[0]: 's07', self.database.fields[1]: '65', self.database.fields[2]: '2'}
        groups = []
        for index in range(1,200):
            groups.append(self.database.getGroupFromNewEntry(newEntry))
        countGroup1 = groups.count(self.groups[0])
        countGroup2 = groups.count(self.groups[1])
        print(self.groups[0] + str(countGroup1))
        print(self.groups[1] + str(countGroup2))
        self.assertEqual(round(countGroup1/(countGroup2 + countGroup1),1), 0.0)
    
    def tearDown(self):
        if self.created:
            self.database.destroy()
            

if __name__ == '__main__':
    unittest.main()
    