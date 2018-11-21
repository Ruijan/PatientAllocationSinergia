import unittest
import patientalloc
from unittest.mock import MagicMock
from unittest.mock import patch
from pathlib import Path
import os
import getpass
import xml.etree.ElementTree as ET
import datetime
import json


class testBCISubject(unittest.TestCase):

    def setUp(self):
        self.properties = {"SubjectID": 'testSubject',
                           "Age": '50', "Group": 'Sham'}
        self.matchingSubjectId = "s03"
        xmlFilePath = str(Path.home()) + "/.cnbitk/cnbimi/xml/"
        xmlFileName = "mi_stroke_prot.xml"
        self.savingProperties = {"folder": str(Path.home()) + "/data/test",
                                 "xmlFilePath": xmlFilePath, "xmlFileName": xmlFileName}
        self.dataPath = self.savingProperties["folder"]
        self.subjectPath = self.dataPath + "/" + self.properties["SubjectID"]
        self.resourcesPath = self.subjectPath + "/resources"
        self.subject = patientalloc.BCISubject(
            self.properties, self.savingProperties, self.matchingSubjectId)

    def testCreation(self):
        self.assertEqual(self.subject.properties, self.properties)
        self.assertEqual(self.subject.savingProperties, self.savingProperties)
        self.assertEqual(self.subject.matchingSubjectId,
                         self.matchingSubjectId)

    def testXMLUpdateWithShamGroup(self):
        self.subject.createDataFolder()
        self.subject.updateXML()

        tree = ET.parse(self.savingProperties["folder"] + "/" +
                        self.properties["SubjectID"] + "/" + self.savingProperties["xmlFileName"])
        root = tree.getroot()
        self.__checkXMLValues__(root)

    def __checkXMLValues__(self, root):
        now = datetime.datetime.now()
        self.assertEqual(root.find('subject').find(
            'id').text, self.properties["SubjectID"])
        self.assertEqual(root.find('subject').find(
            'age').text, self.properties["Age"])
        self.assertEqual(root.find('recording').find('date').text, str(
            now.day) + str(now.month) + str(now.year))
        self.assertEqual(root.find('protocol').find(
            'mi').find('fid').text, self.matchingSubjectId)
        self.assertEqual(root.find('classifiers').find(
            'mi').find('ndf').find('exec').text, 'ndf_mi_')

    def testCreateDataFolder(self):
        self.subject.createDataFolder()
        self.assertTrue(os.path.isdir(self.dataPath))
        self.assertTrue(os.path.isdir(self.subjectPath))
        self.assertTrue(os.path.exists(
            self.subjectPath + "/" + self.savingProperties["xmlFileName"]))

    def testCreateResources(self):
        self.subject.createResources()
        files = {"authorized": "AuthorizedMovements.json", "flexion": "flexion.json", "reaching": "extension.json",
                 "lowstimSingle": "lowStimSingle.json", "lowstimDouble": "lowStimDouble.json", "reset": "reset.json"}
        self.assertTrue(os.path.isdir(self.resourcesPath))
        for file in files:
            self.assertTrue(os.path.exists(
                self.resourcesPath + "/" + files[file]))
        with open(self.resourcesPath + "/" + files["authorized"], 'r') as f:
            data = json.load(f)
            for movement in data["Movements"]:
                self.assertEqual(
                    movement["MovementFile"], files[movement["Name"]])

    def tearDown(self):
        self.subject.destroy()
        self.assertTrue(os.path.isdir(self.dataPath))
        self.assertFalse(os.path.isdir(self.subjectPath))
        self.assertFalse(os.path.isdir(self.resourcesPath))
        self.assertFalse(os.path.exists(
            self.subjectPath + "/mi_stroke_prot.xml"))
