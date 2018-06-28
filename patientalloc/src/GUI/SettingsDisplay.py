# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from pathlib import Path
import yaml


class SettingsDisplay():
    def __init__(self, app):
        guiInfo = dict()
        fullpath = str(Path.home()) + "/.patientalloc/settings.yml"
        with open(fullpath, 'r') as guiFile:
            guiInfo = yaml.safe_load(guiFile)
        self.app = app
        self.app.startSubWindow('Settings')
        self.app.addLabel("Settings Title","Settings", 0, 0, colspan=2)
        self.app.setFont(size=14)
        self.app.startLabelFrame("File Details", 1, 0)
        self.app.addLabelEntry("Filename Database")
        self.app.setEntry("Filename Database", guiInfo["fileName"])
        self.app.addDirectoryEntry("Folder Database")
        self.app.setEntry("Folder Database", guiInfo["folder"])
        self.app.stopLabelFrame()
        self.app.startLabelFrame("Save Details", 1, 1)
        self.app.addRadioButton("saveMode", "Local")
        self.app.addRadioButton("saveMode", "Git (ssh c4Science)")
        if guiInfo['saveMode'] == 'local':
            self.app.setRadioButton("saveMode", "Local", callFunction=False)
        elif guiInfo['saveMode'] == 'online':
            self.app.setRadioButton("saveMode", "Git (ssh c4Science)", callFunction=False)
        self.app.addLabelEntry("Server Address")
        self.app.setEntry("Server Address", guiInfo["server"])
        self.app.stopLabelFrame()
        self.app.addButton("Save Settings", self.__saveSetting__, 2,0)
        self.app.addButton("Cancel", self.__cancel__,2,1)
        self.app.stopSubWindow()
        self.app.hideSubWindow('Settings')

    def display(self):
        self.app.showSubWindow('Settings')

    def __saveSetting__(self):
        fullpath = str(Path.home()) + '/.patientalloc/settings.yml'
        saveMode = self.app.getRadioButton("saveMode")
        if saveMode == 'Git (ssh c4Science)':
            saveMode = 'online'
        else:
            saveMode = 'local'
        with open(fullpath, 'w') as guiInfo:
            document = {'fileName' : self.app.getEntry('Filename Database'),
                        'folder':  self.app.getEntry('Folder Database'),
                        'saveMode': saveMode,
                        'server': self.app.getEntry('Server Address')}
            yaml.dump(document, guiInfo)
        self.__cancel__()

    def __cancel__(self):
        self.app.hideSubWindow('Settings')
