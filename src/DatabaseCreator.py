# -*- coding: utf-8 -*-
import os
import DatabaseError
import csv

class DatabaseCreator:
    def __init__(self):
        self.fileName = ""
        self.folder = ""
        self.fields = []
        
    def create(self):
        if(not os.path.isdir(self.folder)):
            os.mkdir(self.folder)
        fullpath = self.folder + "/" + self.fileName
        if(self.fileName == ""):
            raise DatabaseError.EmptyFileNameError()
        if(os.path.exists(fullpath)):
            raise DatabaseError.FileExistError(fullpath)
        with open(fullpath, 'wb') as csvfile:
            database = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
    def destroy(self):
        fullpath = self.folder + "/" + self.fileName
        if(not os.path.exists(fullpath)):
            raise DatabaseError.FileNotExistError(fullpath)
        fullpath = self.folder + "/" + self.fileName
        os.remove(fullpath)
        
    def addField(self, field):
        self.fields.append(field)