# -*- coding: utf-8 -*-
from patientalloc.src.Database.Database import Database
from patientalloc.src.GUI.WelcomeDisplay import WelcomeDisplay
import os
import git

class DatabaseHandler():
    def __init__(self, gui):
        self.gui = gui
        self.database = None
        self.gitRepo = None
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
            self.gui.app.setStatusbar("Loading database...", field=0)
            self.__loadGitRepo__()
            self.file = os.path.join(self.gui.settings.folder, self.gui.settings.fileName)
        if self.file is None:
            self.gui.app.setStatusbar("Operation Canceled", field=0)
            self.gui.switchFrame(WelcomeDisplay(self.gui.app, self.gui))
        else:
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
            self.__loadGitRepo__()
            self.database.create()
            self.gitRepo.index.add([os.path.join(self.database.folder, self.database.fileName)])
            self.gitRepo.index.add([os.path.join(self.database.folder, self.database.fileName.replace('.db', '.csv'))])
            self.gitRepo.index.commit('Updating database')
            self.gitRepo.remotes.origin.push()
            self.secureDatabase()
            self.gui.app.setStatusbar("Database saved", field=0)

    def secureDatabase(self):
        os.remove(os.path.join(self.database.folder, self.database.fileName.replace('.db', '.csv')))

    def __loadGitRepo__(self):
        if os.path.exists(self.gui.settings.folder):
                self.gitRepo = git.Repo(self.gui.settings.folder)
                self.gitRepo.head.reset(index=True, working_tree=True)
                self.gitRepo.remotes.origin.pull()
        else:
            self.gitRepo = git.Repo.clone_from(self.gui.settings.server, self.gui.settings.folder, branch='master')


    def getFullpathToSaveFromUser(self):
        return self.app.saveBox(title="Save database", fileName=None,
                                  dirName=None, fileExt=".db",
                                  fileTypes=[('Database', '*.db')],
                                  asFile=None, parent=None)

    def isDatabaseLoaded(self):
        if self.database is None:
            return False
        return True
