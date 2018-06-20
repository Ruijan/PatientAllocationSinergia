# -*- coding: utf-8 -*-

class DatabaseError(Exception):
    """Base class for exceptions in this module."""
    pass

class FileExistError(Exception):
    def __init__(self, fullpath):
        self.message = "File already exists at: " + fullpath
        
class FileNotExistError(Exception):
    def __init__(self, fullpath):
        self.message = "File does not exist at: " + fullpath
        
class EmptyFileNameError(Exception):
    def __init__(self):
        self.message = "Empty file name. Please set it before create the database"
        
class EmptyFieldError(Exception):
    def __init__(self):
        self.message = "Empty field. Please give it a proper name before create the database"
        
class EntryWithUnknownFields(Exception):
    def __init__(self):
        self.message = "Entry has unknown fields. Please check that all fields are filled before adding it to the database"