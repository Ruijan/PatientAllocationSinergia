from patientalloc import Subject
import os
import shutil


class BCISubject(Subject):
    def __init__(self, properties, savingProperties):
        Subject.__init__(self, properties)
        self.savingProperties = savingProperties

    def createDataFolder(self):
        subjectPath = self.savingProperties["folder"] + \
            "/" + self.properties["SubjectId"]
        resourcesPath = subjectPath + "/resources"
        if not os.path.isdir(self.savingProperties["folder"]):
            os.makedirs(self.savingProperties["folder"])
        if not os.path.isdir(subjectPath):
            os.makedirs(subjectPath)
        if not os.path.isdir(resourcesPath):
            os.makedirs(resourcesPath)
        shutil.copyfile(self.savingProperties["xmlFilePath"] + self.savingProperties["xmlFileName"],
                        subjectPath + "/" + self.savingProperties["xmlFileName"])

    def destroy(self):
        if os.path.exists(self.savingProperties["folder"] + "/" + self.properties["SubjectId"]):
            shutil.rmtree(
                self.savingProperties["folder"] + "/" + self.properties["SubjectId"])
