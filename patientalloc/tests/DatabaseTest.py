#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 18:28:32 2018

@author: cnbi
"""

import unittest
import sys
sys.path.insert(0, 'src/Database')
sys.path.insert(0, '../src/Database')
from Database import Database
import DatabaseError
import os.path

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database = Database()
        self.database.fileName = "database.db"
        self.database.folder = "tests/database"
        self.fields = ["SubjectId", "Age", "Group"]
        self.entry = {self.fields[0]: 's01', self.fields[1]: '56', self.fields[2]: 'BCI'}
        self.ttest = [0, 1, 0]
        self.groups = ["BCI", "Sham"]
        self.fieldTypes = ["Entry", "Number", "Hidden"]
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
        self.database.addField(self.fields[0], self.ttest[0], self.fieldTypes[0])
        self.assertEqual(self.database.fields[0],self.fields[0])
        self.assertEqual(self.database.ttest[0],self.ttest[0])

    def testAddEmptyFieldShouldThrow(self):
        with self.assertRaises(DatabaseError.EmptyFieldError):
            self.database.addField("", False, "number")

    def testAddFields(self):
        self.database.addFields(self.fields, self.ttest, self.fieldTypes)
        self.assertEqual(self.database.fields, self.fields)

    def testLoadDatabaseWithEmptyFileNameShouldTrow(self):
        self.database.fileName = ""
        with self.assertRaises(DatabaseError.EmptyFileNameError):
            self.database.load()

    def testLoadDatabaseWithWrongFileName(self):
        self.database.fileName = "wrongDatabase.db"
        with self.assertRaises(DatabaseError.FileNotExistError):
            self.database.load()

    def testFieldsAddedToCSV(self):
        self.database.addFields(self.fields, self.ttest, self.fieldTypes)
        self.database.groups = self.groups.copy()
        self.database.create()
        self.created = True
        self.database.fields = []
        self.database.ttest = []
        self.database.groups = []
        self.database.fieldTypes = []
        self.database.load()
        self.__checkCorrectDBInfo__()
        self.assertEqual(self.database.groups, self.groups)

    def testEntriesAddedToCSV(self):
        self.database.addFields(self.fields, self.ttest, self.fieldTypes)
        self.database.groups = self.groups.copy()
        self.database.addEntryWithGroup(self.entry)
        self.database.create()
        self.created = True
        self.database.fields = []
        self.database.ttest = []
        self.database.groups = []
        self.database.fieldTypes = []
        self.database.entries = []
        self.database.load()
        self.__checkCorrectDBInfo__()
        self.assertEqual(self.database.groups, self.groups)
        self.assertEqual(self.database.entries[0], self.entry)


    def testAddEntryWithGroup(self):
        self.database.addFields(self.fields, self.ttest, self.fieldTypes)
        self.database.addEntryWithGroup(self.entry)
        self.assertEqual(self.database.entries[0], self.entry)

    def testAddEntryWithWrongFieldNames(self):
        self.database.addFields(self.fields, self.ttest, self.fieldTypes)
        wrongFieldsEntry = {self.fields[0]: 's01', 'FMA': 56}
        with self.assertRaises(DatabaseError.EntryWithUnknownFields):
            self.database.addEntryWithGroup(wrongFieldsEntry)

    def testLoadingFromDBFile(self):
        self.database.fileName = "filledDatabase.db"
        self.database.load()
        self.__checkCorrectDBInfo__()
        self.assertEqual(self.database.entries[0], self.entry)
        self.assertEqual(len(self.database.entries), 6)

    def testLoadingEntryFromDatabase(self):
        self.database.fileName = "filledDatabase.db"
        self.database.load()
        self.assertEqual(self.database.entries[0], self.entry)
        self.assertEqual(len(self.database.entries), 6)

    def testGetPValueFromField(self):
        self.database.fileName = "filledDatabase.db"
        self.database.load()
        self.assertTrue(self.database.getPValue("Age") <= 1)
        self.assertTrue(self.database.getPValue("Age") >= 0)

    def testGetMostProbableGroupFromEntry(self):
        self.database.fileName = "filledDatabase.db"
        self.database.load()
        newEntry = {self.fields[0]: 's07', self.fields[1]: '65'}
        self.__checkGroupDistribution__(newEntry, 0.3)

    def testAddEntryToBiasedDatabase(self):
        self.database.fileName = "biasedFilledDatabase.db"
        self.database.load()
        newEntry = {'SubjectId': 's07', 'Age': '65', 'Pre-FMA': '2'}
        self.__checkGroupDistribution__(newEntry, 0.0)

    def __checkCorrectDBInfo__(self):
        fieldIndex = 0
        for field in self.fields:
            self.assertTrue(field in self.database.fields)
            self.assertEqual(self.database.getFieldTypeFromField(field), self.fieldTypes[fieldIndex])
            self.assertEqual(self.database.getTtestFromField(field), self.ttest[fieldIndex])
            fieldIndex += 1

    def __checkGroupDistribution__(self, newEntry, expectedFirstGroupProbability):
        groups = []
        countGroup = dict()
        for _ in range(1,500):
            groups.append(self.database.getGroupFromNewEntry(newEntry))
        countGroup[self.groups[0]] = groups.count(self.groups[0])
        countGroup[self.groups[1]] = groups.count(self.groups[1])
        proba = countGroup[self.groups[0]]/(countGroup[self.groups[1]] + countGroup[self.groups[1]])
        self.assertTrue(abs(proba - expectedFirstGroupProbability) <= 0.1)

    def tearDown(self):
        if self.created:
            self.database.destroy()


if __name__ == '__main__':
    unittest.main()
