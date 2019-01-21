from patientalloc import Subject
import os
import shutil
import xml.etree.ElementTree as ET
import datetime
from pathlib import Path
import json


class BCISubject(Subject):
    def __init__(self, properties, savingProperties, matching_subject_id):
        Subject.__init__(self, properties)
        self.savingProperties = savingProperties
        self.matching_subject_id = matching_subject_id

    def create(self):
        self.create_data_folder()
        self.update_xml()
        self.create_resources()

    def create_data_folder(self):
        subjectPath = self.__get_subject_path__()
        if not os.path.isdir(self.savingProperties["folder"]):
            os.makedirs(self.savingProperties["folder"])
        if not os.path.isdir(subjectPath):
            os.makedirs(subjectPath)
        shutil.copyfile(self.savingProperties["xml_file_path"] + self.savingProperties["xml_file_name"],
                        subjectPath + "/" + self.savingProperties["xml_file_name"])

    def update_xml(self):
        now = datetime.datetime.now()
        xmlFile = self.__get_subject_path__() + "/" + \
            self.savingProperties["xml_file_name"]
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        root.find('subject').find('id').text = self.properties["SubjectID"]
        root.find('subject').find('age').text = str(self.properties["Age"])
        root.find('recording').find('date').text = str(
            now.day) + str(now.month) + str(now.year)
        root.find('protocol').find('mi').find(
            'fid').text = self.matching_subject_id
        if self.properties['Group'] == "Sham":
            root.find('classifiers').find('mi').find(
                'ndf').find('exec').text = "ndf_mi_"
        elif self.properties['Group'] == "BCI":
            root.find('classifiers').find('mi').find(
                'ndf').find('exec').text = "ndf_mi"
        tree.write(xmlFile)

    def create_resources(self):
        resourcesPath = self.__get_subject_path__() + "/resources"
        if not os.path.isdir(resourcesPath):
            os.makedirs(resourcesPath)
        files = {"authorized": "AuthorizedMovements.json", "flexion": "flexion.json", "reaching": "extension.json",
                 "lowstimSingle": "lowStimSingle.json", "lowstimDouble": "lowStimDouble.json", "reset": "reset.json"}
        for file in files:
            pathToFile = resourcesPath + "/" + files[file]
            if not os.path.isfile(resourcesPath + "/" + files[file]):
                shutil.copyfile(
                    self.savingProperties['resources'] + files[file], pathToFile)
        with open(resourcesPath + "/" + files["authorized"], 'r') as f:
            data = json.load(f)
            for movement in data["Movements"]:
                movement["MovementFile"] = resourcesPath + \
                    "/" + files[movement["Name"]]
        with open(resourcesPath + "/" + files["authorized"], 'w') as f:
            json.dump(data, f, indent=4)

    def __get_subject_path__(self):
        return self.savingProperties["folder"] + \
            self.properties["SubjectID"]

    def destroy(self):
        if os.path.exists(self.savingProperties["folder"] + "/" + self.properties["SubjectID"]):
            shutil.rmtree(
                self.savingProperties["folder"] + "/" + self.properties["SubjectID"])
