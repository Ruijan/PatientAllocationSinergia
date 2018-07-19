# -*- coding: utf-8 -*-
from patientalloc.src.Database.Database import Database
import os
import git

class OnlineDatabaseHandler():
    def __init__(self, gitURL):
        self.database = None
        self.gitURL = gitURL
        self.gitRepo = None

    def loadDatabase(self, folder, file):
        self.__loadGitRepo__(folder, file)
        self.file = os.path.join(folder, file)
        database = Database()
        database.loadWithFullPath(self.file)
        self.__secureDatabase__(folder, file)
        return database
        #super(OnlineDatabaseHandler, self).loadDatabase()

    def __loadGitRepo__(self, folder, file):
        if os.path.exists(folder):
            self.gitRepo = git.Repo(folder)
            self.gitRepo.head.reset(index=True, working_tree=True)
            self.gitRepo.remotes.origin.pull()
        else:
            self.gitRepo = git.Repo.clone_from(self.gitURL, folder, branch='master')

    def saveDatabase(self, database, folder, file):
        database.folder = folder
        database.fileName = file
        self.__loadGitRepo__(folder, file)
        database.create()
        self.gitRepo.index.add([os.path.join(folder, file)])
        self.gitRepo.index.add([os.path.join(folder, file.replace('.db', '.csv'))])
        self.gitRepo.index.commit('Updating database')
        self.gitRepo.remotes.origin.push()
        self.__secureDatabase__(folder, file)

    def __secureDatabase__(self, folder, file):
        os.remove(os.path.join(folder, file.replace('.db', '.csv')))