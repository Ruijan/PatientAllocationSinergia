# -*- coding: utf-8 -*-
from patientalloc.src.Database.Database import Database
import os
import git

class OnlineDatabaseHandler():
    def __init__(self, gitURL):
        self.database = None
        self.gitURL = gitURL
        self.gitRepo = None

    def loadDatabase(self, folder, fileName):
        self.__loadGitRepo__(folder, fileName)
        self.fileName = os.path.join(folder, fileName)
        database = Database()
        database.loadWithFullPath(self.fileName)
        self.__secureDatabase__(folder, fileName)
        return database
        #super(OnlineDatabaseHandler, self).loadDatabase()

    def __loadGitRepo__(self, folder, fileName):
        if os.path.exists(folder):
            self.gitRepo = git.Repo(folder)
            self.gitRepo.head.reset(index=True, working_tree=True)
            self.gitRepo.remotes.origin.pull()
        else:
            self.gitRepo = git.Repo.clone_from(self.gitURL, folder, branch='master')

    def saveDatabase(self, database, folder, fileName):
        database.folder = folder
        database.fileNameName = fileName
        self.__loadGitRepo__(folder, fileName)
        database.create()
        self.gitRepo.index.add([os.path.join(folder, fileName)])
        self.gitRepo.index.add([os.path.join(folder, fileName.replace('.db', '.csv'))])
        self.gitRepo.index.commit('Updating database')
        self.gitRepo.remotes.origin.push()
        self.__secureDatabase__(folder, fileName)

    def __secureDatabase__(self, folder, fileName):
        os.remove(os.path.join(folder, fileName.replace('.db', '.csv')))
