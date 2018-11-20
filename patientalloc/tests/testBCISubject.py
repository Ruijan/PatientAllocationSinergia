import unittest
import patientalloc
from unittest.mock import MagicMock
from unittest.mock import patch
import os
import getpass


class testBCISubject(unittest.TestCase):

    def setUp(self):
        self.properties = {"SubjectId": 'testSubject', "Age": '', "Group": ''}
        user = getpass.getuser()
        xmlFilePath = "/home/" + user + "/.cnbitk/cnbimi/xml/"
        xmlFileName = "mi_stroke_prot.xml"
        self.savingProperties = {"folder": "/home/" + user + "/data/test",
                                 "xmlFilePath": xmlFilePath, "xmlFileName": xmlFileName}
        self.dataPath = self.savingProperties["folder"]
        self.subjectPath = self.dataPath + "/" + self.properties["SubjectId"]
        self.resourcesPath = self.subjectPath + "/resources"
        self.subject = patientalloc.BCISubject(
            self.properties, self.savingProperties)

    def testBCISubjectCreation(self):
        self.assertEqual(self.subject.properties, self.properties)
        self.assertEqual(self.subject.savingProperties, self.savingProperties)

    def testBCISubjectSave(self):
        self.subject.createDataFolder()
        self.assertTrue(os.path.isdir(self.dataPath))
        self.assertTrue(os.path.isdir(self.subjectPath))
        self.assertTrue(os.path.isdir(self.resourcesPath))
        self.assertTrue(os.path.exists(
            self.subjectPath + "/" + self.savingProperties["xmlFileName"]))

    def tearDown(self):
        self.subject.destroy()
        self.assertTrue(os.path.isdir(self.dataPath))
        self.assertFalse(os.path.isdir(self.subjectPath))
        self.assertFalse(os.path.isdir(self.resourcesPath))
        self.assertFalse(os.path.exists(
            self.subjectPath + "/mi_stroke_prot.xml"))
