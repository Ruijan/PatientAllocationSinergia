# -*- coding: utf-8 -*-

import sys
from patientalloc.src.GUI.GUI import GUI
from patientalloc.src.Database.Database import Database
from patientalloc.src.Database.Subject.Subject import Subject
from patientalloc.src.Database.Subject.BCISubject import BCISubject
from patientalloc.src.Database.Subject.SubjectFactory import SubjectFactory
import patientalloc.src.Database.DatabaseError as DatabaseError
from patientalloc.src.GUI.GUISettings import GUISettings
from patientalloc.src.Database.OnlineDatabaseHandler import OnlineDatabaseHandler
from patientalloc.src.Database.LocalDatabaseHandler import LocalDatabaseHandler
from patientalloc.src.GUI.GuiDatabaseHandler import GuiDatabaseHandler
from patientalloc.src.GUI.DatabaseLoaderDisplay import DatabaseLoaderDisplay
from patientalloc.src.Database.DatabaseHandlerFactory import DatabaseHandlerFactory

import argparse


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--mode', required=False, nargs='?', default='user',
                        choices=['user', 'admin'],
                        help='launch the allocator in admin mode. Gives access to more information from the database')
    args = parser.parse_known_args()
    if args[0].mode is not None:
        del sys.argv[1:len(sys.argv)]
    app = GUI(args[0].mode)
    app.start()
