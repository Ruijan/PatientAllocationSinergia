# -*- coding: utf-8 -*-
import os
import DatabaseError
import csv
from scipy import stats
import random
from datetime import datetime

class Database:
    def __init__(self):
        self.fileName = ""
        self.folder = ""
        self.fields = []
        self.entries = []
        self.ttest = []
        self.groups = []
        random.seed(datetime.now())

        
    def createCopy(self):
        database = Database()
        database.fileName = self.fileName
        database.folder = self.folder
        database.fields = self.fields.copy()
        database.ttest = self.ttest.copy()
        database.groups = self.groups.copy()
        database.entries = self.entries.copy()
        return database

    def create(self):
        fullpath = self.folder + "/" + self.fileName
        self.createWithFullPath(fullpath)
        
            
    def createWithFullPath(self, fullpath):
        self.__setFileAndPathFromFullpath__(fullpath)
        if(not os.path.isdir(self.folder)):
            os.mkdir(self.folder)
        self.__checkWritingPath__(fullpath)
        with open(fullpath, 'w') as csvfile:
            header = self.fields + ["ttest"] + self.ttest + ["Groups"] + self.groups
            writer = csv.DictWriter(csvfile, fieldnames=header)
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
        with open(fullpath, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            indexForTtest = reader.fieldnames.index("ttest")
            indexForGroups = reader.fieldnames.index("Groups")
            ttestValues = reader.fieldnames[indexForTtest+1:indexForGroups]
            self.groups = reader.fieldnames[indexForGroups+1:len(reader.fieldnames)]
            del reader.fieldnames[indexForTtest:len(reader.fieldnames)]
            self.addFields(reader.fieldnames, ttestValues)
            for row in reader:
                del row[None]
                self.addEntryWithGroup(row)
                
    def load(self):
        fullpath = self.folder + "/" + self.fileName
        self.loadWithFullPath(fullpath)
        

    def __checkReadingPath__(self, fullpath):
        if(self.fileName == ""):
            raise DatabaseError.EmptyFileNameError()
        if(not os.path.exists(fullpath)):
            raise DatabaseError.FileNotExistError(fullpath)

    def destroy(self):
        fullpath = self.folder + "/" + self.fileName
        if(not os.path.exists(fullpath)):
            raise DatabaseError.FileNotExistError(fullpath)
        fullpath = self.folder + "/" + self.fileName
        os.remove(fullpath)

    def addField(self, field, ttest):
        if(field == ""):
            raise DatabaseError.EmptyFieldError()
        self.fields.append(field)
        self.ttest.append(int(ttest))

    def addFields(self, fields, ttests):
        fieldIndex = 0
        for field in fields:
            self.addField(field, ttests[fieldIndex])
            fieldIndex += 1

    def addEntryWithGroup(self, entry):
        for field in entry.keys():
            if(field not in self.fields):
                raise DatabaseError.EntryWithUnknownFields
        self.entries.append(entry)
        
    def getPValue(self, field):
        if(field not in self.fields):
            raise DatabaseError.EntryWithUnknownFields
        indexField = self.fields.index(field)
        if self.ttest[indexField] is 0:
            raise DatabaseError.CannotComputeTTestOnField(field)
        groups = ({self.groups[0] : [], self.groups[1] : []})
        for entry in self.entries:
            groups[entry["Group"]].append(int(entry[field]))
        tvalue, pvalue = stats.ttest_ind(groups[self.groups[0]],groups[self.groups[1]], equal_var = False)
        return pvalue
         
    def getGroupFromNewEntry(self, newEntry):
        pvalues = dict()
        for group in self.groups:
            database = self.createCopy()
            newEntryGroup = dict(newEntry)
            newEntryGroup["Group"] = group
            database.addEntryWithGroup(newEntryGroup)
            minPvalue = 1
            for field in database.fields:
                try:
                    pvalue = database.getPValue(field)
                    if pvalue < minPvalue:
                        minPvalue = pvalue
                except DatabaseError.CannotComputeTTestOnField:
                    pass
            pvalues[group] = minPvalue
        thresholdProbability = pvalues[self.groups[0]] / (pvalues[self.groups[0]] + pvalues[self.groups[1]])
        proba = random.random()
        if proba < thresholdProbability:
            return self.groups[0]
        return self.groups[1]
        