# -*- coding: utf-8 -*-
import os
import patientalloc.src.Database.DatabaseError as DatabaseError
import csv
import yaml
from scipy import stats
import math
import random
from datetime import datetime


class Database:
    def __init__(self):
        self.file_name = ""
        self.folder = ""
        self.fields = []
        self.field_types = []
        self.entries = []
        self.ttest = []
        self.groups = []
        self.group_counter = dict()
        self.order = []
        self.limited_values = []
        self.rejected_entries = []
        random.seed(datetime.now())

    def createCopy(self):
        database = Database()
        database.file_name = self.file_name
        database.folder = self.folder
        database.fields = self.fields.copy()
        database.field_types = self.field_types.copy()
        database.ttest = self.ttest.copy()
        database.groups = self.groups.copy()
        database.entries = self.entries.copy()
        database.order = self.order.copy()
        database.limited_alues = self.limited_values.copy()
        database.rejected_entries = self.rejected_entries.copy()
        database.group_counter = self.group_counter.copy()
        return database

    def create(self):
        fullpath = self.folder + "/" + self.file_name
        self.createWithFullPath(fullpath)

    def createWithFullPath(self, fullpath):
        self.__set_file_and_path_from_full_path__(fullpath)
        if(not os.path.isdir(self.folder)):
            os.mkdir(self.folder)
        self.__check_writing_path__(fullpath)
        if 'Group' not in self.fields:
            self.addField('Group', 0, 'Hidden')
        self.__fill_info_database_file__(fullpath)
        self.__fill_database_csv_file__()

    def __fill_info_database_file__(self, path_to_info_db_file):
        with open(path_to_info_db_file, 'w') as db_info_file:
            document = {'databaseFile': self.file_name.replace('db', 'csv'),
                        'order': self.order,
                        'fields': dict(),
                        'groups': self.groups,
                        'rejectedEntries': self.rejected_entries}
            for field in self.fields:
                document['fields'][field] = dict()
                document['fields'][field]['ttest'] = self.getTtestFromField(
                    field)
                document['fields'][field]['type'] = self.getFieldTypeFromField(
                    field)
                document['fields'][field]['limitedValues'] = self.getLimitedValuesFromField(
                    field)
            yaml.dump(document, db_info_file)

    def __fill_database_csv_file__(self):
        fullpath = self.folder + "/" + self.file_name.replace('db', 'csv')
        with open(fullpath, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fields)
            writer.writeheader()
            for entry in self.entries:
                writer.writerow(entry)

    def __set_file_and_path_from_full_path__(self, fullpath):
        exploded_path = fullpath.split("/")
        self.file_name = exploded_path[len(exploded_path) - 1]
        exploded_path[len(exploded_path) - 1] = ""
        self.folder = "/".join(exploded_path)

    def __check_writing_path__(self, fullpath):
        if(self.file_name == ""):
            raise DatabaseError.EmptyFileNameError()

    def loadWithFullPath(self, fullpath):
        self.__set_file_and_path_from_full_path__(fullpath)
        self.__check_reading_path__(fullpath)
        with open(fullpath, 'r') as dbFile:
            db_info = yaml.safe_load(dbFile)
            for field in db_info["fields"]:
                self.fields.append(field)
                self.ttest.append(db_info["fields"][field]["ttest"])
                self.field_types.append(db_info["fields"][field]["type"])
                self.limited_values.append(
                    db_info["fields"][field]["limitedValues"])
            if "rejectedEntries" in db_info:
                self.rejected_entries = db_info["rejectedEntries"]
            self.groups = db_info['groups']
            self.order = db_info['order']
            for group in self.groups:
                self.group_counter[group] = 0
            fullpath = self.folder + "/" + db_info["databaseFile"]
            with open(fullpath, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.addEntryWithGroup(row)

    def load(self):
        fullpath = self.folder + "/" + self.file_name
        self.loadWithFullPath(fullpath)

    def getEntryGroup(self, index):
        if index > len(self.entries):
            raise DatabaseError.EntryOutOfRange(index)
        return self.entries[index]["Group"]

    def getEntryId(self, index):
        if index > len(self.entries):
            raise DatabaseError.EntryOutOfRange(index)
        return self.entries[index]["SubjectID"]

    def getTtestFromField(self, field):
        return self.ttest[self.fields.index(field)]

    def getFieldTypeFromField(self, field):
        return self.field_types[self.fields.index(field)]

    def getLimitedValuesFromField(self, field):
        return self.limited_values[self.fields.index(field)]

    def __check_reading_path__(self, fullpath):
        if(self.file_name == ""):
            raise DatabaseError.EmptyFileNameError()
        if(not os.path.exists(fullpath)):
            raise DatabaseError.FileNotExistError(fullpath)

    def destroy(self):
        fullpath = self.folder + "/" + self.file_name
        if(not os.path.exists(fullpath)):
            raise DatabaseError.FileNotExistError(fullpath)
        os.remove(fullpath)
        fullpath = self.folder + "/" + self.file_name.replace('db', 'csv')
        os.remove(fullpath)

    def addField(self, field, ttest, field_type, limited_values=''):
        if(field == ""):
            raise DatabaseError.EmptyFieldError()
        self.fields.append(field)
        self.ttest.append(int(ttest))
        self.field_types.append(field_type)
        self.limited_values.append(limited_values)
        self.order.append(field)

    def addFields(self, fields, ttests, field_types):
        fieldIndex = 0
        for field in fields:
            self.addField(field, ttests[fieldIndex], field_types[fieldIndex])
            fieldIndex += 1

    def addEntryWithGroup(self, entry):
        for field in entry.keys():
            if(field not in self.fields):
                print(field)
                raise DatabaseError.EntryWithUnknownFields
        self.entries.append(entry)
        if entry["Group"] not in self.group_counter:
            self.group_counter[entry["Group"]] = 0
        self.group_counter[entry["Group"]] += 1

    def setGroups(self, groups):
        self.groups = groups
        for group in self.groups:
            self.group_counter[group] = 0

    def getPValue(self, field):
        if(field not in self.fields):
            print(field)
            raise DatabaseError.EntryWithUnknownFields
        index_field = self.fields.index(field)
        if self.ttest[index_field] is 0:
            raise DatabaseError.CannotComputeTTestOnField(field)
        groups = ({self.groups[0]: [], self.groups[1]: []})
        pvalue = 0
        entry_number = 0
        for entry in self.entries:
            if entry_number + 1 not in self.rejected_entries:
                if self.getFieldTypeFromField(field) == "List":
                    groups[entry["Group"]].append(
                        self.getLimitedValuesFromField(field).index(entry[field]))
                elif self.getFieldTypeFromField(field) == "Number":
                    groups[entry["Group"]].append(int(float(entry[field])))
            entry_number = entry_number + 1
        if self.getFieldTypeFromField(field) == "List":
            obs = [groups[self.groups[0]].count(
                0), groups[self.groups[0]].count(1)]
            obs2 = [groups[self.groups[1]].count(
                0), groups[self.groups[1]].count(1)]
            _, pvalue = stats.chisquare(obs, obs2)
        elif self.getFieldTypeFromField(field) == "Number":
            _, pvalue = stats.ttest_ind(
                groups[self.groups[0]], groups[self.groups[1]], equal_var=False)
        return pvalue

    def get_groups_probabilities_from_new_entry(self, new_entry):
        if self.__is_group_size_difference_significant__():
            if self.group_counter[self.groups[0]] - self.group_counter[self.groups[1]] >= 0:
                probas = {self.groups[0]: 0, self.groups[1]: 1}
            else:
                probas = {self.groups[0]: 1, self.groups[1]: 0}
            return probas
        else:
            [pvalues, products_pvalues] = self.__create_pvalues_for_all_groups__(
                new_entry)
            return self.__get_allocation_probability_from_pvalues__(pvalues, products_pvalues)

    def __create_pvalues_for_all_groups__(self, new_entry):
        pvalues = dict()
        products_pvalues = dict()
        for group in self.groups:
            minPvalue, productPValue = self.__get_pvalues_for_group__(
                group, new_entry)

            pvalues[group] = minPvalue
            products_pvalues[group] = productPValue
        return pvalues, products_pvalues

    def __get_pvalues_for_group__(self, group, new_entry):
        database = self.createCopy()
        newEntryGroup = dict(new_entry)
        newEntryGroup["Group"] = group
        database.addEntryWithGroup(newEntryGroup)
        minPvalue = 1
        productPValue = 1
        for field in database.fields:
            try:
                pvalue = database.getPValue(field)
                if math.isnan(pvalue):
                    pvalue = 1
                if pvalue < minPvalue:
                    minPvalue = pvalue
                productPValue *= pvalue
            except DatabaseError.CannotComputeTTestOnField:
                pass
        return minPvalue, productPValue

    def __get_allocation_probability_from_pvalues__(self, pvalues, products_pvalues):
        probas = dict()
        if pvalues[self.groups[0]] == 0 and pvalues[self.groups[1]] == 0 and products_pvalues[self.groups[0]] == 0 and products_pvalues[self.groups[1]] == 0:
            probas[self.groups[0]] = 0.5
            probas[self.groups[1]] = 0.5
        elif pvalues[self.groups[0]] == pvalues[self.groups[1]]:
            probas[self.groups[0]] = products_pvalues[self.groups[0]] / (products_pvalues[self.groups[0]] +
                                                                         products_pvalues[self.groups[1]])
            probas[self.groups[1]] = products_pvalues[self.groups[1]] / (products_pvalues[self.groups[0]] +
                                                                         products_pvalues[self.groups[1]])
        else:
            probas[self.groups[0]] = pvalues[self.groups[0]] / (pvalues[self.groups[0]] +
                                                                pvalues[self.groups[1]])
            probas[self.groups[1]] = pvalues[self.groups[1]] / (pvalues[self.groups[0]] +
                                                                pvalues[self.groups[1]])
        return probas

    def __is_group_size_difference_significant__(self):
        return abs(self.group_counter[self.groups[0]] - self.group_counter[self.groups[1]]) >= 4

    def getGroupFromNewEntry(self, new_entry):
        probas = self.get_groups_probabilities_from_new_entry(new_entry)
        proba = random.random()
        if proba < probas[self.groups[0]]:
            return self.groups[0]
        return self.groups[1]

    def rejectEntry(self, index):
        self.rejected_entries.append(index)

    def unrejectEntry(self, index):
        self.rejected_entries.remove(index)
