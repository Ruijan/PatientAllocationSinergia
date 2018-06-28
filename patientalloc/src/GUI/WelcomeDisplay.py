# -*- coding: utf-8 -*-
from appJar import appjar

class WelcomeDisplay():
    def __init__(self, app, gui):
        self.app = app
        self.gui = gui

    def display(self):
        self.app.addLabel("Welcome Title","Welcome to Patient Allocation")
        self.app.setLabelFont("Welcome Title", size=42)
        self.gui.disableSaveMenu()

    def removeFrame(self):
        try:
            self.app.removeLabel("Welcome Title")
        except appjar.ItemLookupError:
            pass
