# -*- coding: utf-8 -*-
class DatabaseError(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message


class FileExistError(DatabaseError):
    def __init__(self, fullpath):
        DatabaseError.__init__(self, "File already exists at: " + fullpath)


class FileNotExistError(DatabaseError):
    def __init__(self, fullpath):
        DatabaseError.__init__(self, "File does not exist at: " + fullpath)


class EmptyFileNameError(DatabaseError):
    def __init__(self):
        DatabaseError.__init__(
            self, "Empty file name. Please set it before create the database")


class EntryOutOfRange(DatabaseError):
    def __init__(self, index):
        DatabaseError.__init__(self, "Entry at index " +
                               str(index) + " is out of boundaries")


class EmptyFieldError(DatabaseError):
    def __init__(self):
        DatabaseError.__init__(
            self, "Empty field. Please give it a proper name before create the database")


class EntryWithUnknownFields(DatabaseError):
    def __init__(self):
        DatabaseError.__init__(
            self, "Entry has unknown fields. Please check that all fields are filled before adding it to the database")


class CannotComputeTTestOnField(DatabaseError):
    def __init__(self, field):
        DatabaseError.__init__(self, "Field " + field +
                               " is set to be not testable through ttest.")
