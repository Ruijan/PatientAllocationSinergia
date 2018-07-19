# -*- coding: utf-8 -*-

import unittest
import patientalloc
from unittest.mock import MagicMock
from unittest.mock import patch


class testLocalDatabaseHandler(unittest.TestCase):

    def setUp(self):
        self.file = 'fileTest'
        self.folder = 'folder'
        self.databaseHandler = patientalloc.LocalDatabaseHandler()

    def testLocalDatabaseHandlerCreation(self):
        self.assertEqual(self.databaseHandler.database, None)

    @patch('patientalloc.src.Database.Database.Database.loadWithFullPath')
    def testLoadDatabseOnExistingDirectory(self, DatabaseMock):
        DatabaseMock.loadWithFullPath.return_value = None
        self.databaseHandler.loadDatabase(self.folder, self.file)
        assert DatabaseMock.called

    def testSavingDatabseOnExistingDirectory(self):
        database = MagicMock()
        self.databaseHandler.saveDatabase(database, self.folder, self.file)
        assert database.create.called
