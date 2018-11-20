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
        self.fileName = ""
        self.folder = ""
        self.fields = []
        self.fieldTypes = []
        self.entries = []
        self.ttest = []
        self.groups = []
        self.order = []
        self.limitedValues = []
        self.rejectedEntries = []
        random.seed(datetime.now())

    def createCopy(self):
        database = Database()
        database.fileName = self.fileName
        database.folder = self.folder
        database.fields = self.fields.copy()
        database.fieldTypes = self.fieldTypes.copy()
        database.ttest = self.ttest.copy()
        database.groups = self.groups.copy()
        database.entries = self.entries.copy()
        database.order = self.order.copy()
        database.limitedValues = self.limitedValues.copy()
        return database

    def create(self):
        fullpath = self.folder + "/" + self.fileName
        self.createWithFullPath(fullpath)


    def createWithFullPath(self, fullpath):
        self.__setFileAndPathFromFullpath__(fullpath)
        if(not os.path.isdir(self.folder)):
            os.mkdir(self.folder)
        self.__checkWritingPath__(fullpath)
        if 'Group' not in self.fields:
            self.addField('Group', 0, 'Hidden')
        with open(fullpath, 'w') as dbInfoFile:
            document = {'databaseFile': self.fileName.replace('db', 'csv'),
                        'order': self.order,
                        'fields': dict(),
                        'groups': self.groups,
                        'rejectedEntries': self.rejectedEntries}
            for field in self.fields:
                document['fields'][field] = dict()
                document['fields'][field]['ttest'] = self.getTtestFromField(field)
                document['fields'][field]['type'] = self.getFieldTypeFromField(field)
                document['fields'][field]['limitedValues'] = self.getLimitedValuesFromField(field)
            yaml.dump(document, dbInfoFile)
        fullpath = self.folder + "/" + self.fileName.replace('db', 'csv')
        with open(fullpath, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fields)
            writer.writeheader()
            for entry in self.entries:
                writer.writerow(entry)

    def __setFileAndPathFromFullpath__(self, fullpath):
        explodedPath = fullpath.split("/")
        self.fileName = explodedPath[len(explodedPath)-1]
        explodedPath[len(explodedPath)-1] = ""
        self.folder = "/".join(explodedPath)

    def __checkWritingPath__(self, fullpath):
        if(self.fileName == ""):
            raise DatabaseError.EmptyFileNameError()

    def loadWithFullPath(self, fullpath):
        self.__setFileAndPathFromFullpath__(fullpath)
        self.__checkReadingPath__(fullpath)
        with open(fullpath, 'r') as dbFile:
            dbInfo = yaml.safe_load(dbFile)
            for field in dbInfo["fields"]:
                self.fields.append(field)
                self.ttest.append(dbInfo["fields"][field]["ttest"])
                self.fieldTypes.append(dbInfo["fields"][field]["type"])
                self.limitedValues.append(dbInfo["fields"][field]["limitedValues"])
            if "rejectedEntries" in dbInfo:
                self.rejectedEntries = dbInfo["rejectedEntries"]
            self.groups = dbInfo['groups']
            self.order = dbInfo['order']
            fullpath = self.folder + "/" + dbInfo["databaseFile"]
            with open(fullpath, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.addEntryWithGroup(row)

    def load(self):
        fullpath = self.folder + "/" + self.fileName
        self.loadWithFullPath(fullpath)

    def getTtestFromField(self, field):
        return self.ttest[self.fields.index(field)]

    def getFieldTypeFromField(self, field):
        return self.fieldTypes[self.fields.index(field)]

    def getLimitedValuesFromField(self, field):
        return self.limitedValues[self.fields.index(field)]

    def __checkReadingPath__(self, fullpath):
        if(self.fileName == ""):
            raise DatabaseError.EmptyFileNameError()
        if(not os.path.exists(fullpath)):
            raise DatabaseError.FileNotExistError(fullpath)

    def destroy(self):
        fullpath = self.folder + "/" + self.fileName
        if(not os.path.exists(fullpath)):
            raise DatabaseError.FileNotExistError(fullpath)
        os.remove(fullpath)
        fullpath = self.folder + "/" + self.fileName.replace('db', 'csv')
        os.remove(fullpath)

    def addField(self, field, ttest, fieldType, limitedValues=''):
        if(field == ""):
            raise DatabaseError.EmptyFieldError()
        self.fields.append(field)
        self.ttest.append(int(ttest))
        self.fieldTypes.append(fieldType)
        self.limitedValues.append(limitedValues)
        self.order.append(field)

    def addFields(self, fields, ttests, fieldTypes):
        fieldIndex = 0
        for field in fields:
            self.addField(field, ttests[fieldIndex], fieldTypes[fieldIndex])
            fieldIndex += 1

    def addEntryWithGroup(self, entry):
        for field in entry.keys():
            if(field not in self.fields):
                print(field)
                raise DatabaseError.EntryWithUnknownFields
        self.entries.append(entry)

    def getPValue(self, field):
        if(field not in self.fields):
            print(field)
            raise DatabaseError.EntryWithUnknownFields
        indexField = self.fields.index(field)
        if self.ttest[indexField] is 0:
            raise DatabaseError.CannotComputeTTestOnField(field)
        groups = ({self.groups[0] : [], self.groups[1] : []})
        pvalue = 0
        entryNumber = 0
        for entry in self.entries:
            if entryNumber+1 not in self.rejectedEntries:
                if self.getFieldTypeFromField(field) == "List":
                    groups[entry["Group"]].append(self.getLimitedValuesFromField(field).index(entry[field]))
                elif self.getFieldTypeFromField(field) == "Number":
                    groups[entry["Group"]].append(int(float(entry[field])))
            entryNumber = entryNumber + 1
        if self.getFieldTypeFromField(field) == "List":
            obs = [groups[self.groups[0]].count(0), groups[self.groups[0]].count(1)]
            obs2 = [groups[self.groups[1]].count(0), groups[self.groups[1]].count(1)]
            _, pvalue = stats.chisquare(obs, obs2)
        elif self.getFieldTypeFromField(field) == "Number":
            _, pvalue = stats.ttest_ind(groups[self.groups[0]],groups[self.groups[1]], equal_var = False)
        return pvalue

    def getGroupsProbabilitiesFromNewEntry(self, newEntry):
        groupCounter = {self.groups[0] : 0, self.groups[1] : 1}
        for entry in self.entries:
            for group in self.groups:
                if entry['Group'] == group:
                    groupCounter[group] = groupCounter[group] + 1
        if abs(groupCounter[self.groups[0]] - groupCounter[self.groups[1]]) >= 4:
            if groupCounter[self.groups[0]] - groupCounter[self.groups[1]] >= 0:
                probas = {self.groups[0] : 0, self.groups[1]: 1}
            else:
                probas = {self.groups[0] : 0, self.groups[1]: 1}
            return probas
        pvalues = dict()
        productsPValues = dict()
        for group in self.groups:
            database = self.createCopy()
            newEntryGroup = dict(newEntry)
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
            pvalues[group] = minPvalue
            productsPValues[group] = productPValue
        probas = dict()
        if pvalues[self.groups[0]] == 0 and pvalues[self.groups[1]] == 0 and productsPValues[self.groups[0]] == 0 and productsPValues[self.groups[1]] == 0:
            probas[self.groups[0]] = 0.5
            probas[self.groups[1]] = 0.5
        elif pvalues[self.groups[0]] == pvalues[self.groups[1]]:
            probas[self.groups[0]] = productsPValues[self.groups[0]] / (productsPValues[self.groups[0]] +
                                          productsPValues[self.groups[1]])
            probas[self.groups[1]] = productsPValues[self.groups[1]] / (productsPValues[self.groups[0]] +
                                          productsPValues[self.groups[1]])
        else:
            probas[self.groups[0]] = pvalues[self.groups[0]] / (pvalues[self.groups[0]] +
                                          pvalues[self.groups[1]])
            probas[self.groups[1]] = pvalues[self.groups[1]] / (pvalues[self.groups[0]] +
                                          pvalues[self.groups[1]])
        return probas

    def getGroupFromNewEntry(self, newEntry):
        probas = self.getGroupsProbabilitiesFromNewEntry(newEntry)
        proba = random.random()
        if proba < probas[self.groups[0]]:
            return self.groups[0]
        return self.groups[1]


    def rejectEntry(self, index):
        self.rejectedEntries.append(index)

    def unrejectEntry(self, index):
        self.rejectedEntries.remove(index)
