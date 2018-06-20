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