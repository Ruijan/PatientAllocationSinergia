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
        self.fileMenus = ["Load", "Save", "Create", "-", "Settings", "-", "Close"]
        self.app.addMenuList("File", self.fileMenus, self.menuPress)
        self.app.disableMenuItem("File", "Save")
        self.app.addStatusbar(fields=1, side="LEFT")
        self.app.setStatusbarWidth(120, 0)
        self.app.setStretch("COLUMN")
        
    def start(self):
        self.app.go()

    def menuPress(self, menu):
        if menu == "Close":
            self.app.stop()
        elif menu == "Load":
            path = str(Path.home()) + "/dev/PatientAllocationSinergia/tests/database"
            self.file = self.app.openBox(title="Load database file", 
                                             dirName=path, 
                                             fileTypes=[('Spreadsheet', '*.csv')], 
                                             asFile=True,
                                             parent=None)

            self.__tryLoadingDatabase__()
        elif menu == "Create":
            self.database = Database()
            self.app.startFrame("Information", row=0, colspan=5)
            self.app.addLabel("Title", "Database Creation")
            self.app.addHorizontalSeparator()
            self.app.addLabelEntry("Field")
            self.app.addImageButton("Add", self.__addField__, "../../res/add.png")
            self.app.stopFrame()
        else:
            pass

    def __addField__(self, button):
        field = self.app.getEntry("Field")
        self.app.startFrame("field_"+str(len(self.database.fields)), row=int(1+len(self.database.fields)/5),
                            column=(len(self.database.fields) % 5))
        self.app.addLabel(field, field)
        self.app.addImageButton("Remove_field_"+str(len(self.database.fields)), self.__addField__, "../../res/delete.png")
        self.app.stopFrame()
        self.database.addField(field)

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
        self.database.loadWithFullPath(self.file.name)
        self.app.setFg("green")
        self.app.enableMenuItem("File", "Save")
        self.app.setStatusbar("File " + self.file.name + " loaded", field=0)
        self.app.setFg("black")
        self.__displayDatabase__()

    def __displayDatabase__(self):
        fieldIndex = 0
        self.app.startFrame("DatabaseDisplay")
        for field in self.database.fields:
            self.app.startFrame(field, row=0, column=fieldIndex)
            fieldIndex += 1
            self.app.setSticky("NEW")
            self.app.setStretch("COLUMN")
            self.app.addLabel(field, field)
            for entry in self.database.entries:
                self.app.addLabel(entry[field], entry[field])
            self.app.stopFrame()
        self.app.stopFrame()
        self.databaseDisplayed = True

if __name__ == '__main__':
    app = GUI()
    app.start()