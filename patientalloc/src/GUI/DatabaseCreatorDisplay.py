# -*- coding: utf-8 -*-

from patientalloc.src.Database.Database import Database
from patientalloc.src.GUI.DatabaseLoaderDisplay import DatabaseLoaderDisplay
import os

class DatabaseCreatorDisplay():
    def __init__(self, currentGui):
        self.gui = currentGui
        self.app = currentGui.app
        self.database = Database()
        self.resPath = os.path.dirname(os.path.realpath(__file__))
        self.resPath = os.path.split(self.resPath)
        self.resPath = os.path.split(self.resPath[0])
        self.resPath = os.path.join(self.resPath[0],'res')

    def display(self):
        self.__displayCreateDatabasePanel__()
        self.gui.disableSaveMenu()

    def __displayCreateDatabasePanel__(self):
        self.app.setFont(size=14)
        self.app.startFrame("Information", row=0, colspan=5)
        self.app.addLabel("Title", "Database Creation",0,0,colspan=4)
        self.app.setStretch("column")
        self.app.addLabelEntry("Group 1", 1, 0, colspan=2)
        self.app.addLabelEntry("Group 2", 1, 2, colspan=2)
        self.app.addLabelOptionBox("Add new field", ["Entry", "Hidden", "List", "Number"], 2, 0)
        self.app.addButton("Choose", self.__chooseFieldType__,2,2)

        self.app.stopFrame()
        self.app.startFrame("emptyFrame", row=1, column=4)
        self.app.stopFrame()
        self.app.startFrame("Create Button", row=4, colspan=5)
        self.app.addButton("Create", self.__createDatabase__)
        self.app.stopFrame()

    def __createDatabase__(self):
        self.database.groups.append(self.app.getEntry("Group 1"))
        self.database.groups.append(self.app.getEntry("Group 2"))
        self.gui.databaseHandler.saveDatabase(self.database, self.gui.getDatabaseFolder(), self.gui.getDatabaseFilename())
        databaseDisplayer = DatabaseLoaderDisplay(self.gui)
        self.gui.switchFrame(databaseDisplayer)

    def __chooseFieldType__(self):
        self.app.startSubWindow("Create New Field", modal=True)
        self.app.setStretch("column")
        self.app.setSticky("new")

        message = ""
        if self.app.getOptionBox("Add new field") == "Entry":
            message = "Enter text or number."
        elif self.app.getOptionBox("Add new field") == "Number":
            message = "Enter a number only"
        elif self.app.getOptionBox("Add new field") == "Hidden":
            message = "Enter text or number. The field will be hidden from user"
        elif self.app.getOptionBox("Add new field") == "List":
            message = "Enter text or number. Separate rows with a comma: Male, Female"
            self.app.addLabelEntry("Limited Values", 1, 2, colspan=2)
        self.app.addLabel("Message", message,0, 0, colspan=4)

        self.app.addLabelEntry("Field Name", 1, 0, colspan=2)
        self.app.addNamedCheckBox("Use for t-test", "ttest", 2, 0)
        self.app.setStretch("none")
        self.app.addButton("Cancel Field", self.__removeAddFieldWindow__, 3, 0, colspan=2)
        self.app.addButton("Add Field", self.__addField__, 3, 2, colspan=2)
        self.app.stopSubWindow()
        self.app.showSubWindow("Create New Field")

    def __addField__(self, button):
        field = self.app.getEntry("Field Name")
        fieldType = self.app.getOptionBox("Add new field")
        limitedValues = []
        if fieldType == "List":
            limitedValues = self.app.getEntry("Limited Values").split(",")
            print(limitedValues)
            newLimitedValues = []
            for value in limitedValues:
                value = value.replace(' ','')
                newLimitedValues.append(value)
            limitedValues = newLimitedValues
            print(newLimitedValues)
        ttest = self.app.getCheckBox("ttest")
        self.__removeAddFieldWindow__()
        if field not in self.database.fields:
            self.app.startFrame("frame_"+field,
                                row=int(1+len(self.database.fields)/5),
                                column=(len(self.database.fields) % 5))
            self.app.addLabel(field, field)
            self.app.addImageButton("Remove_field_"+field,
                                    self.__addField__, self.resPath + "/delete.png")
            self.app.stopFrame()
            self.database.addField(field, ttest, fieldType, limitedValues)
        else:
            self.app.setStatusbar("Operation Canceled: Field already exists", field=0)


    def __removeAddFieldWindow__(self):
        if self.app.getOptionBox("Add new field") == "List":
            self.app.removeEntry("Limited Values")
        self.app.removeEntry("Field Name")
        self.app.removeButton("Cancel Field")
        self.app.removeButton("Add Field")
        self.app.removeCheckBox("ttest")
        self.app.destroySubWindow("Create New Field")

    def removeFrame(self):
        #try:
        self.app.removeLabel("Title")
        self.app.removeEntry("Group 1")
        self.app.removeEntry("Group 2")
        self.app.removeOptionBox("Add new field")
        for field in self.database.fields:
            if field != "Group":
                self.app.removeLabel(field)
                self.app.removeButton("Remove_field_"+field)
                self.app.removeFrame("frame_"+field)
        self.app.removeButton("Choose")
        self.app.removeButton("Create")
        self.app.removeFrame("Create Button")
        self.app.removeFrame("emptyFrame")
        self.app.removeFrame("Information")
        #except appjar.ItemLookupError:
            #pass
