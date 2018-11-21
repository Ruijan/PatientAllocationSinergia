import unittest
import patientalloc
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import PropertyMock


class TestSubjectFactory(unittest.TestCase):
    def setUp(self):
        self.properties = {'Group': 'Sham'}
        self.database = patientalloc.Database()
        self.entries = PropertyMock(return_value={1, 2, 3})
        type(self.database).entries = self.entries
        self.database.getGroupFromNewEntry = MagicMock(
            return_value=self.properties['Group'])
        self.database.getEntryGroup = MagicMock()
        self.settings = MagicMock()
        self.subjectCreationType = PropertyMock(return_value='Simple')
        type(self.settings).subjectCreationType = self.subjectCreationType
        self.subjectFactory = patientalloc.SubjectFactory(
            self.database, self.settings)

    def testSubjectFactoryCreation(self):
        self.assertEqual(self.subjectFactory.database, self.database)
        self.assertEqual(self.subjectFactory.settings, self.settings)

    def testSimpleSubjectCreation(self):
        subject = self.subjectFactory.createSubject(self.properties)
        self.assertEqual(subject.properties, self.properties)
        self.assertIsInstance(subject, patientalloc.Subject)
        self.database.getGroupFromNewEntry.assert_called_with(self.properties)
        self.subjectCreationType.assert_called_with()

    def testBCISubjectCreation(self):
        self.subjectCreationType = PropertyMock(return_value='BCI')
        self.database.getEntryGroup.side_effect = ['Sham', 'BCI']
        self.database.getEntryId = MagicMock(return_value='s04')

        type(self.settings).subjectCreationType = self.subjectCreationType
        subject = self.subjectFactory.createSubject(self.properties)

        self.assertIsInstance(subject, patientalloc.BCISubject)
        self.assertEqual(subject.properties, self.properties)
        self.database.getGroupFromNewEntry.assert_called_with(self.properties)
        self.subjectCreationType.assert_called_with()
        self.assertEqual(subject.matchingSubjectId, 's04')

    def testGetMatchingSubjectId(self):
        self.database.getEntryGroup.side_effect = ['Sham', 'BCI']
        self.database.getEntryId = MagicMock(return_value='s03')
        matchingSubjectId = self.subjectFactory.getMatchingSubjectId()
        self.assertEqual(matchingSubjectId, 's03')
        self.assertEqual(self.database.getEntryId.call_count, 1)
        self.entries.assert_called_once_with()
        self.assertEqual(self.database.getEntryGroup.call_count, 2)
