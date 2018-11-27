# -*- coding: utf-8 -*-
import patientalloc
import getpass
import os
from shutil import copyfile
import xml.etree.ElementTree as ET
from appJar import appjar
import patientalloc.src.Database.DatabaseError as DatabaseError
import json
import datetime
import random
import math


class DatabaseLoaderDisplay():
    def __init__(self, currentGui):
        self.gui = currentGui
        self.app = currentGui.app
        self.database = None
        self.loaded = False
        self.dataPath = "/home/" + getpass.getuser() + "/data"
        self.labelsToRemove = []
        self.buttonsToRemove = []
        self.checkboxesToRemove = []
        self.optionBoxToRemove = []
        self.entriesToRemove = []
        self.subjectFactory = None

    def display(self):
        if self.database is None:
            self.__tryLoadingDatabase__()
        if self.loaded:
            self.__displayDatabase__()

    def handleCommand(self, command):
        if command == "Save":
            self.__saveDatabase__()
        elif command == "Save as":
            self.file = self.gui.getFullpathToSaveFromUser()
            self.database.createWithFullPath(self.file)

    def __saveDatabase__(self):
        self.gui.databaseHandler.saveDatabase(
            self.database, self.gui.getDatabaseFolder(), self.gui.getDatabaseFilename())

    def __tryLoadingDatabase__(self):
        try:
            self.database = self.gui.databaseHandler.loadDatabase(
                self.gui.getDatabaseFolder(), self.gui.getDatabaseFilename())
            if self.database is not None:
                self.loaded = True
                self.subjectFactory = patientalloc.SubjectFactory(
                    self.database, self.gui.settings)
                self.gui.enableSaveMenu()
        except DatabaseError.DatabaseError as error:
            print("==============================================")
            print(error.message)
            print("==============================================")
            self.app.setStatusbar(error.message, field=0)

    def __displayDatabase__(self):
        self.app.setFont(size=14)
        fieldIndex = 0
        self.app.setStretch("column")
        self.app.startFrame("DatabaseDisplay", row=0, colspan=5)
        self.app.addLabel("Indices", "Indices", row=0, column=fieldIndex)
        self.labelsToRemove.append("Indices")
        entryIndex = 1
        for _ in self.database.entries:
            self.app.addLabel("Indices_" + str(entryIndex),
                              str(entryIndex), row=entryIndex, column=0)
            self.labelsToRemove.append("Indices_" + str(entryIndex))
            entryIndex += 1
        self.app.addLabel("PValues", "PValues", row=entryIndex, column=0)
        self.labelsToRemove.append("PValues")
        self.app.addLabel("New Entry", "New Entry",
                          row=entryIndex + 1, column=0)
        self.labelsToRemove.append("New Entry")
        fieldIndex += 1
        for field in self.database.order:
            self.__createFieldFrame__(field, fieldIndex)
            fieldIndex += 1
        self.app.addLabel("Reject", "Reject", row=0, column=fieldIndex)
        self.labelsToRemove.append("Reject")
        entryIndex = 1
        for entry in self.database.entries:
            self.app.addNamedCheckBox(
                "", "Reject_" + str(entryIndex), row=entryIndex, column=fieldIndex)
            self.checkboxesToRemove.append("Reject_" + str(entryIndex))
            if entryIndex in self.database.rejectedEntries:
                self.app.setCheckBox("Reject_" + str(entryIndex), True, False)
            else:
                self.app.setCheckBox("Reject_" + str(entryIndex), False, False)
            self.app.setCheckBoxChangeFunction(
                "Reject_" + str(entryIndex), self.__rejectEntry__)
            entryIndex = entryIndex + 1
        fieldIndex += 2
        entryIndex += 2
        self.app.addButton("Add Patient", self.__addSubject__,
                           row=entryIndex, column=0, colspan=math.floor(fieldIndex / 2))
        self.buttonsToRemove.append("Add Patient")
        if self.gui.mode == 'admin':
            self.app.addButton("Check Probabilities",
                               self.__checkProbabilityGroups__)
            self.buttonsToRemove.append("Check Probabilities")
        self.app.addButton("Save", self.__saveDatabase__, row=entryIndex, column=math.floor(
            fieldIndex / 2), colspan=math.floor(fieldIndex / 2))
        self.buttonsToRemove.append("Save")
        self.app.setButtonBg("Save", "green")
        self.app.stopFrame()
        self.databaseDisplayed = True

    def __rejectEntry__(self, entry):
        entryIndex = int(entry[7:len(entry)])
        if entryIndex in self.database.rejectedEntries:
            self.database.unrejectEntry(entryIndex)
        else:
            self.database.rejectEntry(entryIndex)
        for field in self.database.order:
            if self.gui.mode == 'admin' or field != 'Group':
                try:
                    self.app.setLabel(
                        "PValue_" + field, str(round(self.database.getPValue(field), 2)))
                except DatabaseError.CannotComputeTTestOnField:
                    self.app.setLabel("PValue_" + field, "")

    def __createFieldFrame__(self, field, fieldIndex):
        if self.gui.mode == 'admin' or field != 'Group':
            self.app.addLabel(field, field, row=0, column=fieldIndex)
            self.labelsToRemove.append(field)
            entryIndex = 0
            for entry in self.database.entries:
                self.app.addLabel(field + "_ " + str(entryIndex),
                                  entry[field], row=entryIndex + 1, column=fieldIndex)
                self.labelsToRemove.append(field + "_ " + str(entryIndex))
                entryIndex += 1
            entryIndex += 1
            try:
                self.app.addLabel("PValue_" + field, str(
                    round(self.database.getPValue(field), 2)), row=entryIndex, column=fieldIndex)
            except DatabaseError.CannotComputeTTestOnField:
                self.app.addLabel("PValue_" + field, "",
                                  row=entryIndex, column=fieldIndex)
            self.labelsToRemove.append("PValue_" + field)
            entryIndex += 1
            if field != "Group":
                if self.database.getFieldTypeFromField(field) == "List":
                    self.app.addOptionBox("New " + field, self.database.getLimitedValuesFromField(
                        field), row=entryIndex, column=fieldIndex)
                    self.optionBoxToRemove.append("New " + field)
                elif self.database.getFieldTypeFromField(field) == "Number":
                    self.app.addNumericEntry(
                        "New " + field, row=entryIndex, column=fieldIndex)
                    self.entriesToRemove.append("New " + field)
                else:
                    self.app.addEntry(
                        "New " + field, row=entryIndex, column=fieldIndex)
                    self.entriesToRemove.append("New " + field)
            else:
                self.app.addLabel("New " + field, "",
                                  row=entryIndex, column=fieldIndex)
                self.labelsToRemove.append("New " + field)

    def __addSubject__(self):
        subjectProperties = self.__createSubjectPorpertiesFromFormValues__()
        subject = self.subjectFactory.createSubject(subjectProperties)
        subject.create()
        self.removeFrame()
        self.database.addEntryWithGroup(subjectProperties)
        print(subjectProperties["SubjectID"])
        self.__displayDatabase__()

    def __checkProbabilityGroups__(self):
        self.__tryRemovingCheckProbabilityFrame__()
        subject = self.__createSubjectPorpertiesFromFormValues__()
        probabilities = self.database.getGroupsProbabilitiesFromNewEntry(
            subject)
        indexKey = 0
        for key in probabilities.keys():
            self.app.startFrame("Probas_" + str(indexKey),
                                row=2 + indexKey, column=0, colspan=5)
            self.app.addLabel("key_" + str(indexKey), key, 0, 0)
            self.app.addLabel("proba_" + str(indexKey),
                              round(probabilities[key], 2), 0, 1)
            indexKey += 1
            self.app.stopFrame()

    def __createSubjectPorpertiesFromFormValues__(self):
        subject = dict()
        for field in self.database.fields:
            if field != "Group":
                fieldType = self.database.getFieldTypeFromField(field)
                if fieldType == "List":
                    subject[field] = self.app.getOptionBox("New " + field)
                elif fieldType == "Entry" or fieldType == "Number":
                    subject[field] = self.app.getEntry("New " + field)
        return subject

    def removeFrame(self):
        if self.loaded:
            self.__tryRemovingCheckProbabilityFrame__()
            for label in self.labelsToRemove:
                self.app.removeLabel(label)
            for entry in self.entriesToRemove:
                self.app.removeEntry(entry)
            for checkbox in self.checkboxesToRemove:
                self.app.removeCheckBox(checkbox)
            for button in self.buttonsToRemove:
                self.app.removeButton(button)
            for box in self.optionBoxToRemove:
                self.app.removeOptionBox(box)
            self.app.removeFrame("DatabaseDisplay")
            del self.labelsToRemove[:]
            del self.entriesToRemove[:]
            del self.checkboxesToRemove[:]
            del self.buttonsToRemove[:]
            del self.optionBoxToRemove[:]

    def __removeFieldColumn__(self, field):
        if self.gui.mode == 'admin' or field != 'Group':
            self.app.removeLabel("PValue_" + field)
            if field == "Group":
                self.app.removeLabel("New " + field)
            else:
                if self.database.getFieldTypeFromField(field) == "List":
                    self.app.removeOptionBox("New " + field)
                else:
                    self.app.removeEntry("New " + field)
            self.app.removeLabel(field)
            for entryIndex in range(0, len(self.database.entries)):
                self.app.removeLabel(field + "_ " + str(entryIndex))
            self.app.removeFrame(field)

    def __tryRemovingCheckProbabilityFrame__(self):
        try:
            for indexKey in range(0, len(self.database.groups)):
                self.app.removeLabel("key_" + str(indexKey))
                self.app.removeLabel("proba_" + str(indexKey))
                self.app.removeFrame("Probas_" + str(indexKey))
        except appjar.ItemLookupError:
            pass
