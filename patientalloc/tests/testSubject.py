import unittest
import patientalloc
from unittest.mock import MagicMock
from unittest.mock import patch
import git


class testSubject(unittest.TestCase):
	def testSubjectCreation(self):
		properties = {"SubjectId", '', "Age", '', "Group", ''}
		self.subject = patientalloc.Subject(properties)
		self.assertEqual(self.subject.properties, properties)
