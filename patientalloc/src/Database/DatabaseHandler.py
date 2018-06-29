# -*- coding: utf-8 -*-
from patientalloc.src.Database.Database import Database
from patientalloc.src.GUI.WelcomeDisplay import WelcomeDisplay
import os

class DatabaseHandler():
    def __init__(self, gui):
        self.gui = gui
        self.database = None
        self.file = ''

    def loadDatabase(self):
        if self.gui.settings.saveMode == "local":
            self.file = self.gui.app.openBox(title="Load database file",
                                             dirName=None,
                                             fileTypes=[('Database', '*.db')],
                                             asFile=True,
                                             parent=None)
            if self.file is not None:
                self.file = self.file.name
        elif self.gui.settings.saveMode == "online":
            self.file = os.path.join(self.gui.settings.folder, self.gui.settings.fileName)
            os.system("git clone " + self.gui.settings.server + " " + self.gui.settings.folder)
        if self.file is None:
            self.gui.app.setStatusbar("Operation Canceled", field=0)
            self.gui.switchFrame(WelcomeDisplay(self.gui.app, self.gui))
        else:
            self.gui.app.setStatusbar("Loading database...", field=0)
            self.database = Database()
            self.database.loadWithFullPath(self.file)
            self.gui.app.setStatusbar("File " + self.file + " loaded", field=0)

    def saveDatabase(self):
        if self.gui.settings.saveMode == "local":
            if self.gui.mode == 'admin':
                if self.database.fileName == "":
                    self.file = self.getFullpathToSaveFromUser()
                    self.database.createWithFullPath(self.file)
                else:
                    self.database.create()
            elif self.gui.mode == 'user':
                self.database.create()
        elif self.gui.settings.saveMode == "online":
            self.gui.app.setStatusbar("Saving database...", field=0)
            self.database.folder = self.gui.settings.folder
            self.database.fileName = self.gui.settings.fileName
            os.system("git clone -v " + self.gui.settings.server + ' ' + self.database.folder)
            self.database.create()
            os.system("cd " + self.database.folder + " ; git add . ; git commit -m 'saving database' ; git push")
            self.secureDatabase()
            self.gui.app.setStatusbar("Database saved", field=0)

    def secureDatabase(self):
        os.system("rm -rf " + self.database.folder)

    def getFullpathToSaveFromUser(self):
        return self.app.saveBox(title="Save database", fileName=None,
                                  dirName=None, fileExt=".db",
                                  fileTypes=[('Database', '*.db')],
                                  asFile=None, parent=None)

    def isDatabaseLoaded(self):
        if self.database is None:
            return False
        return True