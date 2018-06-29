# -*- coding: utf-8 -*-

import unittest
import patientalloc
from unittest.mock import MagicMock

class testDatabaseHandler(unittest.TestCase):
    def testDatabaseHandlerCreation(self):
        mock = MagicMock()
        self.databaseHandler = patientalloc.DatabaseHandler(mock)
        self.assertEqual(self.databaseHandler.gui, mock)
        self.assertEqual(self.databaseHandler.database, None)