# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 14:44:52 2018

@author: cnbi
"""
from appJar import gui
from pathlib import Path
import sys
sys.path.insert(0, '..')
from Database import Database
import DatabaseError

class GUI():
    def __init__(self):
        self.database = None
        self.file = None
        self.app = gui("Patient allocation")
        self.databaseDisplayed = False
        self.fileMenus = ["Load", "Save", "Save as", "Create", "-", "Settings", "-", "Close"]
        self.__initGUI__()
        
    def __initGUI__(self):
        self.app.addMenuList("File", self.fileMenus, self.menuPress)
        self.app.addLabel("Welcome Title","Welcome to Patient Allocation")
        self.app.setLabelFont("Welcome Title", size=42)
        self.app.disableMenuItem("File", "Save")
        self.app.disableMenuItem("File", "Save as")
        self.app.addStatusbar(fields=1, side="LEFT")
        self.app.setStatusbarWidth(120, 0)
        self.app.setStretch("COLUMN")
        
    def start(self):
        self.app.go()

    def menuPress(self, menu):
        self.app.setFont(size=14)
        if menu == "Close":
            self.app.stop()
        elif menu == "Load":
            path = str(Path.home()) + "/dev/PatientAllocationSinergia/tests/database"
            self.file = self.app.openBox(title="Load database file", 
                                             dirName=path, 
                                             fileTypes=[('Spreadsheet', '*.csv')], 
                                             asFile=True,
                                             parent=None)
            self.file = self.file.name

            self.__tryLoadingDatabase__()
        elif menu == "Create":
            self.app.enableMenuItem("File", "Save")
            self.app.enableMenuItem("File", "Save as")
            self.database = Database()
            self.__displayCreateDatabasePanel__()
        elif menu == "Save":
            if self.database.fileName == "":
                self.file = self.app.saveBox(title="Save database", fileName=None, 
                                  dirName=None, fileExt=".csv", 
                                  fileTypes=[('Spreadsheet', '*.csv')], 
                                  asFile=None, parent=None)
                self.database.createWithFullPath(self.file)
            else:
                self.database.create()
        elif menu == "Save as":
            self.file = self.app.saveBox(title="Save database", fileName=None, 
                              dirName=None, fileExt=".csv", 
                              fileTypes=[('Spreadsheet', '*.csv')], 
                              asFile=None, parent=None)
            self.database.createWithFullPath(self.file)
        else:
            pass
        
    def __displayCreateDatabasePanel__(self):
        self.app.startFrame("Information", row=0, colspan=5)
        self.app.addLabel("Title", "Database Creation",0,0,colspan=4)
        self.app.setStretch("column")
        self.app.addLabelEntry("Group 1", 1, 0, colspan=2)
        self.app.addLabelEntry("Group 2", 1, 2, colspan=2)
        self.app.addLabelEntry("Add new field", 2, 0, colspan=2)
        self.app.addNamedCheckBox("Use for t-test", "ttest", 2, 2)
        self.app.setStretch("none")
        self.app.addImageButton("Add", self.__addField__, "../../res/add.png", 2, 3)
        self.app.stopFrame()
        self.app.startFrame("emptyFrame", row=1, column=4)
        self.app.stopFrame()
        self.app.startFrame("Create Button", row=4, colspan=5)
        self.app.addButton("Create", self.__createDatabase__)
        self.app.stopFrame()

    def __addField__(self, button):
        field = self.app.getEntry("Add new field")
        if field not in self.database.fields:
            ttest = self.app.getCheckBox("ttest")
            self.app.startFrame("field_"+str(len(self.database.fields)), row=int(1+len(self.database.fields)/5),
                                column=(len(self.database.fields) % 5))
            self.app.addLabel(field, field)
            self.app.addImageButton("Remove_field_"+str(len(self.database.fields)), self.__addField__, "../../res/delete.png")
            self.app.stopFrame()
            self.database.addField(field, ttest)
            self.app.clearEntry("Add new field", callFunction=False)
        else:
            self.app.setStatusbar("Operation Canceled: Field already exists", field=0)
        
    def __createDatabase__(self):
        self.database.groups.append(self.app.getEntry("Group 1"))
        self.database.groups.append(self.app.getEntry("Group 2"))
        self.file = self.app.saveBox(title="Save database", fileName=None, 
                                  dirName=None, fileExt=".csv", 
                                  fileTypes=[('Spreadsheet', '*.csv')], 
                                  asFile=None, parent=None)
        self.database.createWithFullPath(self.file)
        self.app.removeAllWidgets()
        self.__initGUI__()
        self.__tryLoadingDatabase__()

    def __tryLoadingDatabase__(self):
        try:
            print(self.file)
            if self.file is None:
                self.app.setStatusbar("Operation Canceled", field=0)
            else:
                self.__loadDatabase__()
        except DatabaseError.DatabaseError as error:
            self.app.setStatusbar(error.message, field=0)
            print(error.message)

    def __loadDatabase__(self):
        self.database = Database()
        self.database.loadWithFullPath(self.file)
        self.app.setFg("green")
        self.app.enableMenuItem("File", "Save")
        self.app.enableMenuItem("File", "Save as")
        self.app.setStatusbar("File " + self.file + " loaded", field=0)
        self.app.setFg("black")
        self.__displayDatabase__()

    def __displayDatabase__(self):
        fieldIndex = 0
        self.app.startFrame("DatabaseDisplay")
        self.app.startFrame("IndicesFrame", row=0, column=fieldIndex)
        self.app.addLabel("Indices", "Indices") 
        entryIndex = 1
        for entry in self.database.entries:
            self.app.addLabel("Indices_" + str(entryIndex), str(entryIndex))
            entryIndex += 1
        self.app.addLabel("PValues", "PValues")
        self.app.addLabel("New Entry", "New Entry")
        self.app.stopFrame()
        fieldIndex += 1
        for field in self.database.fields:
            self.app.startFrame(field, row=0, column=fieldIndex)
            fieldIndex += 1
            self.app.setSticky("NEW")
            self.app.setStretch("COLUMN")
            self.app.addLabel(field, field)
            entryIndex = 0
            for entry in self.database.entries:
                self.app.addLabel(field + "_ " + str(entryIndex), entry[field])
                entryIndex += 1
            try:
                self.app.addLabel("PValue_" + field, str(round(self.database.getPValue(field),2)))
            except Database.CannotComputeTTestOnField as error:
                self.app.addLabel("PValue_" + field, "")
                pass
            if field != "Group":
                self.app.addEntry("New " + field)
            self.app.stopFrame()
        self.app.startFrame("AddSubject", row=1, column=0, colspan=fieldIndex)
        self.app.addButton("AddEntry",self.__addSubject__)
        self.app.stopFrame()
        self.app.stopFrame()
        self.databaseDisplayed = True
        
    def __addSubject__(self):
        subject = dict()
        for field in self.database.fields:
            subject["field"] = self.app.getEntry("New " + field)
        self.database.addEntry(subject)

if __name__ == '__main__':
    app = GUI()
    app.start()