import patientalloc
import random


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
            matching_subject_id = self.getMatchingSubjectId()
            subject = patientalloc.BCISubject(
                properties, self.settings.savingProperties, matching_subject_id)
        return subject

    def getMatchingSubjectId(self):
        nb_of_entries = len(self.database.entries) - 1
        matching_subject_index = random.randint(0, nb_of_entries)
        while matching_subject_index + 1 in self.database.rejected_entries or self.database.getEntryGroup(matching_subject_index) != "BCI":
            matching_subject_index = random.randint(0, nb_of_entries)
        return self.database.getEntryId(matching_subject_index)
