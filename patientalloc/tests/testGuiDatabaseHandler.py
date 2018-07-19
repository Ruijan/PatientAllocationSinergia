# -*- coding: utf-8 -*-

import unittest
import patientalloc
from unittest.mock import MagicMock


class testGuiDatabaseHandler(unittest.TestCase):
    def testGuiDatabaseHandlerCreation(self):
        appMock = MagicMock()
        databaseHandlerMock = MagicMock()
        self.databaseHandler = patientalloc.GuiDatabaseHandler(appMock, databaseHandlerMock)
        self.assertEqual(self.databaseHandler.databaseHandler, databaseHandlerMock)
        self.assertEqual(self.databaseHandler.app, appMock)
