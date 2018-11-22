#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 18:28:32 2018

@author: cnbi
"""

import unittest
import patientalloc
import os.path
import random


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database = patientalloc.Database()
        dirname, _ = os.path.split(os.path.abspath(__file__))
        self.database.file_name = "database.db"
        self.database.folder = dirname + "/database"
        self.fields = ["SubjectId", "Age", "Group"]
        self.entry = {self.fields[0]: 's01',
                      self.fields[1]: '56', self.fields[2]: 'BCI'}
        self.ttest = [0, 1, 0]
        self.groups = ["BCI", "Sham"]
        self.field_types = ["Entry", "Number", "Hidden"]
        self.created = False
        self.possible_entries = []
        self.possible_entries.append(
            {'SubjectId': 's01', 'Age': '65', 'Group': 'Sham'})
        self.possible_entries.append(
            {'SubjectId': 's02', 'Age': '30', 'Group': 'BCI'})
        self.possible_entries.append(
            {'SubjectId': 's03', 'Age': '40', 'Group': 'BCI'})
        self.possible_entries.append({'SubjectId': 's04', 'Age': '30'})

    def test_create_database(self):
        self.database.create()
        self.created = True
        self.assertTrue(os.path.isfile(
            self.database.folder + "/" + self.database.file_name))

    def test_create_database_with_empty_file_name_should_throw(self):
        self.database.file_name = ""
        with self.assertRaises(patientalloc.DatabaseError.EmptyFileNameError):
            self.database.create()

    def test_destroy_file(self):
        self.database.create()
        self.database.destroy()
        self.assertFalse(os.path.isfile(
            self.database.folder + "/" + self.database.file_name))

    def test_destroy_file_does_not_exist_should_throw(self):
        with self.assertRaises(patientalloc.DatabaseError.FileNotExistError):
            self.database.destroy()

    def test_add_field(self):
        self.database.addField(
            self.fields[0], self.ttest[0], self.field_types[0])
        self.assertEqual(self.database.fields[0], self.fields[0])
        self.assertEqual(self.database.ttest[0], self.ttest[0])

    def test_add_empty_field_should_throw(self):
        with self.assertRaises(patientalloc.DatabaseError.EmptyFieldError):
            self.database.addField("", False, "number")

    def test_add_fields(self):
        self.database.addFields(self.fields, self.ttest, self.field_types)
        self.assertEqual(self.database.fields, self.fields)

    def test_load_database_with_empty_file_name_should_throw(self):
        self.database.file_name = ""
        with self.assertRaises(patientalloc.DatabaseError.EmptyFileNameError):
            self.database.load()

    def test_load_database_with_wrong_file_name(self):
        self.database.file_name = "wrongDatabase.db"
        with self.assertRaises(patientalloc.DatabaseError.FileNotExistError):
            self.database.load()

    def test_fields_added_to_CSV(self):
        self.database.addFields(self.fields, self.ttest, self.field_types)
        self.database.groups = self.groups.copy()
        self.database.create()
        self.created = True
        self.database.fields = []
        self.database.ttest = []
        self.database.groups = []
        self.database.field_types = []
        self.database.load()
        self.__check_correct_DB_Info__()
        self.assertEqual(self.database.groups, self.groups)

    def test_entries_added_to_CSV(self):
        self.database.addFields(self.fields, self.ttest, self.field_types)
        self.database.groups = self.groups.copy()
        self.database.addEntryWithGroup(self.entry)
        self.database.create()
        self.created = True
        self.database.fields = []
        self.database.ttest = []
        self.database.groups = []
        self.database.field_types = []
        self.database.entries = []
        self.database.load()
        self.__check_correct_DB_Info__()
        self.assertEqual(self.database.groups, self.groups)
        self.assertEqual(self.database.entries[0], self.entry)

    def test_add_entry_with_group(self):
        self.database.addFields(self.fields, self.ttest, self.field_types)
        self.database.addEntryWithGroup(self.entry)
        self.assertEqual(self.database.entries[0], self.entry)

    def test_add_entry_with_wrong_field_names(self):
        self.database.addFields(self.fields, self.ttest, self.field_types)
        wrongFieldsEntry = {self.fields[0]: 's01', 'FMA': 56}
        with self.assertRaises(patientalloc.DatabaseError.EntryWithUnknownFields):
            self.database.addEntryWithGroup(wrongFieldsEntry)

    def test_loading_from_DB_file(self):
        self.database.file_name = "filledDatabase.db"
        self.database.load()
        self.__check_correct_DB_Info__()
        self.assertEqual(self.database.entries[0], self.entry)
        self.assertEqual(len(self.database.entries), 6)

    def test_get_entry_group_with_wrong_index_should_throw(self):
        self.database.addFields(self.fields, self.ttest, self.field_types)
        self.database.groups = self.groups.copy()
        with self.assertRaises(patientalloc.DatabaseError.EntryOutOfRange):
            self.database.getEntryGroup(2)

    def test_get_entry_group(self):
        self.database.addFields(self.fields, self.ttest, self.field_types)
        self.database.groups = self.groups.copy()
        self.database.addEntryWithGroup(self.possible_entries[0])
        self.database.addEntryWithGroup(self.possible_entries[1])
        self.database.addEntryWithGroup(self.possible_entries[2])
        self.assertEqual(self.database.getEntryGroup(2),
                         self.possible_entries[2]["Group"])

    def test_loading_entry_from_database(self):
        self.database.file_name = "filledDatabase.db"
        self.database.load()
        self.assertEqual(self.database.entries[0], self.entry)
        self.assertEqual(len(self.database.entries), 6)

    def test_get_PValue_from_field(self):
        self.database.file_name = "filledDatabase.db"
        self.database.load()
        self.assertTrue(self.database.getPValue("Age") <= 1)
        self.assertTrue(self.database.getPValue("Age") >= 0)

    def test_get_most_probable_group_from_entry(self):
        self.database.file_name = "filledDatabase.db"
        self.database.load()
        new_entry = {self.fields[0]: 's07', self.fields[1]: '65'}
        self.__check_group_distribution__(new_entry, 0.3)

    def test_add_entry_to_biased_database(self):
        self.database.file_name = "biasedFilledDatabase.db"
        self.database.load()
        new_entry = {'SubjectId': 's07', 'Age': '65', 'Pre-FMA': '2'}
        self.__check_group_distribution__(new_entry, 0.0)

    def test_add_entry_to_empty_database(self):
        self.database.addFields(self.fields, self.ttest, self.field_types)
        self.database.groups = self.groups.copy()
        new_entry = {'SubjectId': 's01', 'Age': '65'}
        self.__check_group_distribution__(new_entry, 0.5)

    def test_add_entry_to_one_line_database(self):
        self.database.addFields(self.fields, self.ttest, self.field_types)
        self.database.groups = self.groups.copy()
        self.database.addEntryWithGroup(self.possible_entries[0])
        self.__check_group_distribution__(self.possible_entries[1], 0.5)

    def test_add_entry_to_two_lines_database(self):
        self.database.addFields(self.fields, self.ttest, self.field_types)
        self.database.groups = self.groups.copy()
        self.database.addEntryWithGroup(self.possible_entries[0])
        self.database.addEntryWithGroup(self.possible_entries[1])
        self.__check_group_distribution__(self.possible_entries[3], 0.5)

    def test_add_entry_to_three_lines_database(self):
        self.database.addFields(self.fields, self.ttest, self.field_types)
        self.database.groups = self.groups.copy()
        self.database.addEntryWithGroup(self.possible_entries[0])
        self.database.addEntryWithGroup(self.possible_entries[1])
        self.database.addEntryWithGroup(self.possible_entries[2])
        self.__check_group_distribution__(self.possible_entries[3], 0.81)

    def __check_correct_DB_Info__(self):
        field_index = 0
        for field in self.fields:
            self.assertTrue(field in self.database.fields)
            self.assertEqual(self.database.getFieldTypeFromField(
                field), self.field_types[field_index])
            self.assertEqual(self.database.getTtestFromField(
                field), self.ttest[field_index])
            field_index += 1

    def __check_group_distribution__(self, new_entry, expected_first_group_probability):
        groups = []
        count_group = dict()
        for _ in range(1, 600):
            groups.append(self.database.getGroupFromNewEntry(new_entry))
        count_group[self.groups[0]] = groups.count(self.groups[0])
        count_group[self.groups[1]] = groups.count(self.groups[1])
        proba = count_group[self.groups[0]] / \
            (count_group[self.groups[1]] + count_group[self.groups[1]])
        self.assertTrue(abs(proba - expected_first_group_probability) <= 0.15)

    def test_add_rejected_entry(self):
        self.database.addFields(self.fields, self.ttest, self.field_types)
        self.database.groups = self.groups.copy()
        self.database.addEntryWithGroup(self.possible_entries[0])
        self.database.addEntryWithGroup(self.possible_entries[1])
        self.database.addEntryWithGroup(self.possible_entries[2])
        self.database.addEntryWithGroup(self.possible_entries[3])
        self.database.rejectEntry(2)
        self.assertEqual(self.database.rejected_entries[0], 2)
        self.assertEqual(
            self.database.entries[self.database.rejected_entries[0]], self.possible_entries[2])

    def test_add_rejected_entry_should_not_compute_PValue(self):
        self.database.addFields(self.fields, self.ttest, self.field_types)
        self.database.groups = self.groups.copy()
        for x in range(20):
            entry = {'SubjectId': 's0' + str(x), 'Age': str(
                random.randint(20, 90)), 'Group': self.groups[random.randint(0, 1)]}
            self.database.addEntryWithGroup(entry)
        self.database.addEntryWithGroup(self.possible_entries[0])
        self.database.addEntryWithGroup(self.possible_entries[1])
        original_PValue = self.database.getPValue("Age")
        self.database.addEntryWithGroup(self.possible_entries[2])
        rejectedEntry = len(self.database.entries)
        previousPValue = self.database.getPValue("Age")
        self.database.rejectEntry(rejectedEntry)
        currentPValue = self.database.getPValue("Age")
        print(currentPValue)
        print(original_PValue)
        print(previousPValue)
        self.assertEqual(currentPValue, original_PValue)
        self.assertTrue(currentPValue != previousPValue)

    def test_remove_rejected_entry(self):
        self.database.addFields(self.fields, self.ttest, self.field_types)
        self.database.groups = self.groups.copy()
        self.database.addEntryWithGroup(self.possible_entries[0])
        self.database.addEntryWithGroup(self.possible_entries[1])
        self.database.addEntryWithGroup(self.possible_entries[2])
        rejectedEntry = 1
        self.database.rejectEntry(rejectedEntry)
        self.database.unrejectEntry(rejectedEntry)
        self.assertEqual(len(self.database.rejected_entries), 0)

    def test_add_subject_where_max_difference_is_reached(self):
        self.database.addFields(self.fields, self.ttest, self.field_types)
        self.database.groups = self.groups.copy()
        for x in range(0, 5):
            entry = {'SubjectId': 's'
                     + str(x), 'Age': str(random.randint(20, 90)), 'Group': self.groups[0]}
            self.database.addEntryWithGroup(entry)
        entry = {'SubjectId': 's'
                 + str(5), 'Age': str(random.randint(20, 90)), 'Group': self.groups[0]}
        expected_PValues = self.database.getGroupsProbabilitiesFromNewEntry(
            entry)
        self.assertEqual(expected_PValues[self.groups[1]], 1)
        self.assertEqual(expected_PValues[self.groups[0]], 0)

    def tearDown(self):
        if self.created:
            self.database.destroy()
