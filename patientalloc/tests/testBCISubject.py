import unittest
import patientalloc
from unittest.mock import MagicMock
from pathlib import Path
import os
import getpass
import xml.etree.ElementTree as ET
import datetime
import json


class TestBCISubject(unittest.TestCase):

    def setUp(self):
        self.properties = {"SubjectID": 'testSubject',
                           "Age": '50', "Group": 'Sham'}
        self.matching_subject_id = "s03"
        xml_file_path, _ = os.path.split(os.path.abspath(__file__))
        xml_file_path = xml_file_path + "/database/"
        xml_file_name = "mi_stroke_prot.xml"
        self.savingProperties = {"folder": str(Path.home()) + "/data/test",
                                 "xml_file_path": xml_file_path, "xml_file_name": xml_file_name, "resources": xml_file_path + "resources/"}
        self.dataPath = self.savingProperties["folder"]
        self.subjectPath = self.dataPath + "/" + self.properties["SubjectID"]
        self.resourcesPath = self.subjectPath + "/resources"
        self.subject = patientalloc.BCISubject(
            self.properties, self.savingProperties, self.matching_subject_id)

    def test_creation(self):
        self.assertEqual(self.subject.properties, self.properties)
        self.assertEqual(self.subject.savingProperties, self.savingProperties)
        self.assertEqual(self.subject.matching_subject_id,
                         self.matching_subject_id)

    def test_subject_creation(self):
        self.subject.create()
        self.__check_XML_Values__()
        self.__check_data_folder_creation__()
        self.__check_resources_creation__()

    def __check_XML_Values__(self):
        tree = ET.parse(self.savingProperties["folder"] + "/" +
                        self.properties["SubjectID"] + "/" + self.savingProperties["xml_file_name"])
        root = tree.getroot()
        now = datetime.datetime.now()
        self.assertEqual(root.find('subject').find(
            'id').text, self.properties["SubjectID"])
        self.assertEqual(root.find('subject').find(
            'age').text, self.properties["Age"])
        self.assertEqual(root.find('recording').find('date').text, str(
            now.day) + str(now.month) + str(now.year))
        self.assertEqual(root.find('protocol').find(
            'mi').find('fid').text, self.matching_subject_id)
        self.assertEqual(root.find('classifiers').find(
            'mi').find('ndf').find('exec').text, 'ndf_mi_')

    def __check_data_folder_creation__(self):
        self.assertTrue(os.path.isdir(self.dataPath))
        self.assertTrue(os.path.isdir(self.subjectPath))
        self.assertTrue(os.path.exists(
            self.subjectPath + "/" + self.savingProperties["xml_file_name"]))

    def __check_resources_creation__(self):
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
