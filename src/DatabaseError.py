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
        DatabaseError.__init__(self, "Empty file name. Please set it before create the database")

class EmptyFieldError(DatabaseError):
    def __init__(self):
        DatabaseError.__init__(self, "Empty field. Please give it a proper name before create the database")

class EntryWithUnknownFields(DatabaseError):
    def __init__(self):
        DatabaseError.__init__(self, "Entry has unknown fields. Please check that all fields are filled before adding it to the database")
