# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 14:44:52 2018

@author: cnbi
"""

from appJar import gui
app = gui()
app.addLabel("title", "Welcome to appJar")
app.setLabelBg("title", "red")
app.go()