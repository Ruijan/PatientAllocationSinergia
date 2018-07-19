# -*- coding: utf-8 -*-

from patientalloc.src.Database.Database import Database
import os

class LocalDatabaseHandler():
    def __init__(self):
        self.database = None

    def loadDatabase(self, folder, fileName):
        database = Database()
        database.loadWithFullPath(os.path.join(folder, fileName))
        return database

    def saveDatabase(self, database, folder, fileName):
        database.folder = folder
        database.fileNameName = fileName
        database.create()
