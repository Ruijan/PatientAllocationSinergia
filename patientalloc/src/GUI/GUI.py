# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 14:44:52 2018

@author: cnbi
"""
from appJar import gui
from DatabaseLoaderDisplay import DatabaseLoaderDisplay
from DatabaseCreatorDisplay import DatabaseCreatorDisplay
from WelcomeDisplay import WelcomeDisplay

class GUI():
    def __init__(self, mode):
        self.mode = mode
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
        else:
            pass

    def getFullpathToSaveFromUser(self):
        return self.app.saveBox(title="Save database", fileName=None,
                                  dirName=None, fileExt=".db",
                                  fileTypes=[('Database', '*.db')],
                                  asFile=None, parent=None)
