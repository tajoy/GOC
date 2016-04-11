#!/bin/env python3.5
# -*- coding: UTF-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.setupUi(self)