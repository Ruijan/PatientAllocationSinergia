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
from pathlib import Path
import os
import yaml


class GUI():
    def __init__(self, mode):
        self.mode = mode
        self.__createSettings__()
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
        self.settings = SettingsDisplay(self.app)

    def __createSettings__(self):
        settingsPath = str(Path.home()) + '/.patientalloc'
        if not os.path.exists(settingsPath):
            os.makedirs(settingsPath)
        fullpath = str(Path.home()) + '/.patientalloc/settings.yml'
        if not os.path.exists(fullpath):
            with open(fullpath, 'w') as guiInfo:
                document = {'fileName' : 'sinergia.db',
                            'folder':  str(Path.home()) + '/.patientalloc/SinergiaPatients',
                            'saveMode': 'local',
                            'server': ''}
                yaml.dump(document, guiInfo)

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
            self.settings.display()
        else:
            pass

    def getFullpathToSaveFromUser(self):
        return self.app.saveBox(title="Save database", fileName=None,
                                  dirName=None, fileExt=".db",
                                  fileTypes=[('Database', '*.db')],
                                  asFile=None, parent=None)
