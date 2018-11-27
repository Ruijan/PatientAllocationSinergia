import unittest
import patientalloc
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import PropertyMock


class TestDatabaseLoaderDisplay(unittest.TestCase):
    def setUp(self):
        self.gui = MagicMock()
        self.gui.getDatabaseFolder = MagicMock(return_value='path')
        self.gui.getDatabaseFilename = MagicMock(return_value='file')
        self.app = PropertyMock(return_value=None)
        type(self.gui).app = self.app
        self.databaseHandler = MagicMock()
        self.databaseHandler.saveDatabase = MagicMock()
        type(self.gui).databaseHandler = self.databaseHandler
        self.gui.getFullpathToSaveFromUser = MagicMock(return_value='fullpath')
        self.database = MagicMock()
        self.database.createWithFullPath = MagicMock()

        self.frame = patientalloc.DatabaseLoaderDisplay(self.gui)

    def test_creation(self):
        self.assertEqual(self.frame.app, self.gui.app)
        self.assertEqual(self.frame.gui, self.gui)

    def test_handle_save_command(self):
        self.frame.handleCommand('Save')
        self.gui.getDatabaseFolder.assert_called_once_with()
        self.gui.getDatabaseFilename.assert_called_once_with()
        self.databaseHandler.saveDatabase.assert_called_once_with(
            None, 'path', 'file')

    def test_handle_save_as_command(self):
        self.frame.database = self.database
        self.frame.handleCommand('Save as')
        self.gui.getFullpathToSaveFromUser.assert_called_once_with()
        self.database.createWithFullPath.assert_called_once_with('fullpath')
