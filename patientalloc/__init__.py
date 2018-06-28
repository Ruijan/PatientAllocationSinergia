# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'patientalloc/src/Database')
sys.path.insert(0, 'patientalloc/src/GUI')
from GUI import GUI
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
