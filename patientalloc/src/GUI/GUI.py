# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 14:44:52 2018

@author: cnbi
"""
from appJar import gui
from patientalloc.src.GUI.DatabaseLoaderDisplay import DatabaseLoaderDisplay
from patientalloc.src.GUI.DatabaseCreatorDisplay import DatabaseCreatorDisplay
from patientalloc.src.GUI.WelcomeDisplay import WelcomeDisplay
from patientalloc.src.GUI.SettingsDisplay import SettingsDisplay
from patientalloc.src.GUI.GUISettings import GUISettings
from patientalloc.src.Database.DatabaseHandler import DatabaseHandler

import os


class GUI():
    def __init__(self, mode):
        self.mode = mode
        self.settings = GUISettings()
        self.databaseHandler = DatabaseHandler(self)
        if not os.path.exists(self.settings.settingsFile):
            self.settings.createSettingsFile()
        else:
            self.settings.load()
        self.app = gui("Patient allocation")
        if self.mode == 'admin':
            self.fileMenus = ["Load", "Save", "Save as", "Create", "-", "Settings", "-", "Close"]
        elif self.mode == 'user':
            self.fileMenus = ["Load", "Save", "-", "Close"]
        self.app.addMenuList("File", self.fileMenus, self.__menuPress__)

        self.currentFrame = WelcomeDisplay(self.app, self)
        self.currentFrame.display()
        self.app.addStatusbar(fields=1, side="LEFT")
        self.app.setStatusbarWidth(120, 0)
        self.app.setStretch("COLUMN")
        self.settingsDisplay = SettingsDisplay(self.app, self.settings)

    def start(self):
        self.app.go()

    def switchFrame(self, newFrame):
        self.currentFrame.removeFrame()
        del self.currentFrame
        self.currentFrame = newFrame
        self.currentFrame.display()

    def enableSaveMenu(self):
        if self.mode == 'admin':
            self.app.enableMenuItem("File", "Save as")
        self.app.enableMenuItem("File", "Save")

    def disableSaveMenu(self):
        if self.mode == 'admin':
            self.app.disableMenuItem("File", "Save as")
        self.app.disableMenuItem("File", "Save")

    def __menuPress__(self, menu):
        if menu == "Close":
            self.currentFrame.removeFrame()
            self.app.stop()
        elif menu == "Load":
            self.switchFrame(DatabaseLoaderDisplay(self))
        elif menu == "Create":
            self.switchFrame(DatabaseCreatorDisplay(self))
        elif menu == "Save":
            self.currentFrame.handleCommand("Save")
        elif menu == "Save as":
            self.currentFrame.handleCommand("Save as")
        elif menu == "Settings":
            self.settingsDisplay.display()
        else:
            pass

    def getFullpathToSaveFromUser(self):
        return self.app.saveBox(title="Save database", fileName=None,
                                  dirName=None, fileExt=".db",
                                  fileTypes=[('Database', '*.db')],
                                  asFile=None, parent=None)
