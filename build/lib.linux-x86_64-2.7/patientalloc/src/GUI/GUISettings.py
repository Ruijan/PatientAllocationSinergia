#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 02:32:31 2018

@author: cnbi
"""
from pathlib import Path
import yaml
import os


class GUISettings():
    def __init__(self):
        xmlFilePath = str(Path.home()) + "/.cnbitk/cnbimi/xml/"
        xmlFileName = "mi_stroke_prot.xml"
        self.settingsFile = str(Path.home()) + '/.patientalloc/settings.yml'
        self.fileName = "sinergia.db"
        self.folder = str(Path.home()) + '/.patientalloc/SinergiaPatients'
        self.server = ""
        self.saveMode = "local"
        self.subjectCreationType = "BCI"
        self.savingProperties = {"folder": str(Path.home()) + "/data/",
                                 "xmlFilePath": xmlFilePath, "xmlFileName": xmlFileName}

    def createSettingsFile(self):
        if not os.path.exists(os.path.dirname(self.settingsFile)):
            os.mkdir(os.path.dirname(self.settingsFile))
        self.save()

    def save(self):
        with open(self.settingsFile, 'w') as guiInfo:
            document = {'fileName': self.fileName,
                        'folder':  self.folder,
                        'saveMode': self.saveMode,
                        'server': self.server}
            yaml.dump(document, guiInfo)

    def load(self):
        with open(self.settingsFile, 'r') as guiFile:
            guiInfo = yaml.safe_load(guiFile)
            self.fileName = guiInfo['fileName']
            self.folder = guiInfo['folder']
            self.saveMode = guiInfo['saveMode']
            self.server = guiInfo['server']
