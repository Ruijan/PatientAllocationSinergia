import patientalloc
import random
import math


class SubjectFactory:
    def __init__(self, database, settings):
        self.database = database
        self.settings = settings

    def createSubject(self, properties):
        properties['Group'] = self.database.getGroupFromNewEntry(properties)
        subject = None
        if self.settings.subjectCreationType == 'Simple':
            subject = patientalloc.Subject(properties)
        elif self.settings.subjectCreationType == 'BCI':
            matchingSubjectId = self.getMatchingSubjectId()
            subject = patientalloc.BCISubject(
                properties, self.settings.savingProperties, matchingSubjectId)
        return subject

    def getMatchingSubjectId(self):
        nbOfEntries = len(self.database.entries) - 1
        matchingSubjectIndex = random.randint(0, nbOfEntries)
        while matchingSubjectIndex in self.database.rejectedEntries or self.database.getEntryGroup(matchingSubjectIndex) != "BCI":
            matchingSubjectIndex = random.randint(0, nbOfEntries)
        return self.database.getEntryId(matchingSubjectIndex)
