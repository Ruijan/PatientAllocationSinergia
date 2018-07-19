# -*- coding: utf-8 -*-

from patientalloc.src.Database.Database import Database
import os

class LocalDatabaseHandler():
    def __init__(self):
        self.database = None

    def loadDatabase(self, folder, file):
        database = Database()
        database.loadWithFullPath(os.path.join(folder, file))
        return database

    def saveDatabase(self, database, folder, file):
        database.folder = folder
        database.fileName = file
        database.create()