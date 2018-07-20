# -*- coding: utf-8 -*-

import unittest
import patientalloc
from unittest.mock import MagicMock
from unittest.mock import patch
import git


class testOnlineDatabaseHandler(unittest.TestCase):

    def setUp(self):
        self.gitURL = 'gitRepositoryTest.git'
        self.file = 'fileTest'
        self.folder = 'folder'

    def testOnlineDatabaseHandlerCreation(self):
        self.databaseHandler = patientalloc.OnlineDatabaseHandler(self.gitURL)
        self.assertEqual(self.databaseHandler.database, None)
        self.assertEqual(self.databaseHandler.gitURL, self.gitURL)

    @patch('os.remove')
    @patch('os.path.join')
    @patch('git.Repo.clone_from', return_value=None)
    @patch('patientalloc.src.Database.Database.Database.loadWithFullPath', return_value=None)
    @patch('os.path.exists', return_value=False)
    def testLoadDatabseOnEmptyDirectory(self, existsPaths, databaseCreator, cloneRepo, joinPath, removeFile):
        self.databaseHandler = patientalloc.OnlineDatabaseHandler(self.gitURL)
        self.databaseHandler.loadDatabase(self.folder, self.file)
        existsPaths.assert_called_with(self.folder)
        cloneRepo.assert_called_with(self.gitURL, self.folder, branch='master')
        databaseCreator.assert_called_with(self.databaseHandler.fileName)
        assert joinPath.called
        assert removeFile.called

    @patch('os.remove')
    @patch('os.path.join')
    @patch('git.Repo')
    @patch('patientalloc.src.Database.Database.Database.loadWithFullPath', return_value=None)
    @patch('os.path.exists', return_value=True)
    def testLoadDatabseOnExistingDirectory(self, existsPaths, databaseCreator, repository, joinPath, removeFile):
        repository.return_value = MagicMock()
        self.databaseHandler = patientalloc.OnlineDatabaseHandler(self.gitURL)
        self.databaseHandler.loadDatabase(self.folder, self.file)
        existsPaths.assert_called_with(self.folder)
        repository.assert_called_with(self.folder)
        assert repository.return_value.remotes.origin.pull.called
        repository.return_value.head.reset.assert_called_with(index=True, working_tree=True)
        databaseCreator.assert_called_with(self.databaseHandler.fileName)
        assert joinPath.called
        assert removeFile.called

    @patch('os.path.exists', return_value=False)
    def testGitURLDoesNotExistShouldThrow(self, existsPaths):
        self.databaseHandler = patientalloc.OnlineDatabaseHandler(self.gitURL)
        self.assertRaises(git.exc.GitCommandError, self.databaseHandler.loadDatabase, self.folder, self.file)
        existsPaths.assert_called_with(self.folder)

    @patch('os.remove')
    @patch('os.path.join')
    @patch('git.Repo.clone_from')
    @patch('os.path.exists', return_value=False)
    def testSaveDatabaseOnEmptyGitRepo(self, existsPaths, cloneRepo, joinPath, removeFile):
        databaseMock = MagicMock()
        cloneRepo.return_value = MagicMock()
        self.databaseHandler = patientalloc.OnlineDatabaseHandler(self.gitURL)
        self.databaseHandler.saveDatabase(databaseMock, self.folder, self.file)
        existsPaths.assert_called_with(self.folder)
        cloneRepo.assert_called_with(self.gitURL, self.folder, branch='master')
        assert cloneRepo.return_value.index.add.called
        assert cloneRepo.return_value.index.commit.called
        assert cloneRepo.return_value.remotes.origin.push.called
        assert databaseMock.create.called
        assert joinPath.called
        assert removeFile.called
