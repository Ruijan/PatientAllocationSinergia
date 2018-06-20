# -*- coding: utf-8 -*-
import os
import DatabaseError
import csv

class Database:
    def __init__(self):
        self.fileName = ""
        self.folder = ""
        self.fields = []
        
    def create(self):
        if(not os.path.isdir(self.folder)):
            os.mkdir(self.folder)
        fullpath = self.folder + "/" + self.fileName
        self.__checkWritingPath(fullpath)
        with open(fullpath, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fields)
            writer.writeheader()
                            
    def __checkWritingPath(self, fullpath):
        if(self.fileName == ""):
            raise DatabaseError.EmptyFileNameError()
        if(os.path.exists(fullpath)):
            raise DatabaseError.FileExistError(fullpath)
            
    def load(self):
        fullpath = self.folder + "/" + self.fileName
        self.__checkReadingPath(fullpath)
        with open(fullpath, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            self.fields = reader.fieldnames
                
    def __checkReadingPath(self, fullpath):
        if(self.fileName == ""):
            raise DatabaseError.EmptyFileNameError()
        if(not os.path.exists(fullpath)):
            raise DatabaseError.FileNotExistError(fullpath)
        
    def destroy(self):
        fullpath = self.folder + "/" + self.fileName
        if(not os.path.exists(fullpath)):
            raise DatabaseError.FileNotExistError(fullpath)
        fullpath = self.folder + "/" + self.fileName
        os.remove(fullpath)
        
    def addField(self, field):
        if(field == ""):
            raise DatabaseError.EmptyFieldError()
        self.fields.append(field)
        
    def addFields(self, fields):
        for field in fields:
            self.addField(field)