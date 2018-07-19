# -*- coding: utf-8 -*-

from patientalloc.src.Database.LocalDatabaseHandler import LocalDatabaseHandler
from patientalloc.src.Database.OnlineDatabaseHandler import OnlineDatabaseHandler


class DatabaseHandlerFactory():
    @staticmethod
    def create(settings):
        if settings.saveMode == "local":
            return LocalDatabaseHandler()
        elif settings.saveMode == "online":
            return OnlineDatabaseHandler(settings.server)
