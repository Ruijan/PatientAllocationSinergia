# -*- coding: utf-8 -*-

import unittest
import patientalloc
from unittest.mock import MagicMock


class testGuiDatabaseHandler(unittest.TestCase):
    def setUp(self):
        self.appMock = MagicMock()
        self.databaseHandlerMock = MagicMock()
        self.databaseHandler = patientalloc.GuiDatabaseHandler(self.appMock, self.databaseHandlerMock)

    def testGuiDatabaseHandlerCreation(self):
        self.assertEqual(self.databaseHandler.databaseHandler, self.databaseHandlerMock)
        self.assertEqual(self.databaseHandler.app, self.appMock)



    def testLoadDatabase(self):
        self.appMock.setStatusbar = MagicMock()
        self.databaseHandlerMock.loadDatabase = MagicMock()
        self.databaseHandler.loadDatabase('testFolder', 'testFilename')
        self.assertTrue(self.appMock.setStatusbar.called)
        self.assertEqual(self.appMock.setStatusbar.call_count, 2)
        self.assertTrue(self.databaseHandlerMock.loadDatabase.called)

    def testSaveDatabase(self):
        self.appMock.setStatusbar = MagicMock()
        self.databaseHandlerMock.saveDatabase = MagicMock()
        self.databaseHandler.saveDatabase(None, 'testFolder', 'testFilename')
        self.assertTrue(self.appMock.setStatusbar.called)
        self.assertEqual(self.appMock.setStatusbar.call_count, 2)
        self.assertTrue(self.databaseHandlerMock.saveDatabase.called)
