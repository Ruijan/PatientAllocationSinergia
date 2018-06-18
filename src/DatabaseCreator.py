# -*- coding: utf-8 -*-
import os

class DatabaseCreator:
    def __init__(self):
        self.fileName = ""
        self.folder = ""
        
    def create(self):
        if(not os.path.isdir(self.folder)):
            os.mkdir(self.folder)
        f= open(self.folder + "/" + self.fileName,"w+")
        f.close()