# -*- coding: utf-8 -*-

import unittest
import patientalloc
from unittest.mock import MagicMock

class testDatabaseHandlerFactory(unittest.TestCase):
    def testCreateLocalDatabaseHandler(self):
        settings = MagicMock()
        settings.saveMode = "local"
        database = patientalloc.DatabaseHandlerFactory.create(settings)
        assert isinstance(database, patientalloc.LocalDatabaseHandler)

    def testCreateOnlineDatabaseHandler(self):
        settings = MagicMock()
        settings.saveMode = "online"
        settings.server = "testGitServer"
        database = patientalloc.DatabaseHandlerFactory.create(settings)
        assert isinstance(database, patientalloc.OnlineDatabaseHandler)
