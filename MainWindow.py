#!/bin/env python3
# -*- coding: UTF-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Ui_MainWindow import Ui_MainWindow

def normal2Snake(prefix, text):
    arr = text.split(" ")
    ret = ""
    for word in arr:
        ret += word.lowcase() + "_"
    return ret[:-1]


def normal2Camel(prefix, text):
    pass

def normal2BigSnake(prefix, text):
    pass


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.setupUi(self)
        self.edtReadName.textChanged.connect(self.whenChangeedtReadName)
        self.readLastUIData()

    def readLastUIData(self):
        pass

    def _getRealText(self, edt):
        if len(edt.text()) > 0:
            return edt.text()
        elif
            return edt.text()

    def whenChangeedtReadName(self, text):

        if len(self.edtSnakeID.text()) == 0:
            self.edtSnakeID.setText(normal2Snake(text))
        if len(self.edtCamelID.text()) == 0:
            self.edtCamelID.setText(normal2Camel(text))
        if len(self.edtBigSnakeID.text()) == 0:
            self.edtBigSnakeID.setText(normal2BigSnake(text))