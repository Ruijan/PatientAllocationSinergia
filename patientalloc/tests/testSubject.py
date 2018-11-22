import unittest
import patientalloc


class testSubject(unittest.TestCase):
    def testSubjectCreation(self):
        properties = {"SubjectId", '', "Age", '', "Group", ''}
        self.subject = patientalloc.Subject(properties)
        self.assertEqual(self.subject.properties, properties)
