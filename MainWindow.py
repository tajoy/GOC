#!/bin/env python3
# -*- coding: UTF-8 -*-

from PyQt5 import QtWidgets
from utils import *
import json

from Ui_MainWindow import Ui_MainWindow


def getRealText(edt):
    if len(edt.text()) > 0:
        return edt.text()
    else:
        return edt.placeholderText()

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.readUIData()
        self.edtReadName.textEdited.connect(self.whenNameOrPrefixChanged)
        self.edtPrefix.textEdited.connect(self.whenNameOrPrefixChanged)

        self.edtSnakeID.textEdited.connect(self.whenSnakeIDChanged)
        self.edtCamelID.textEdited.connect(self.whenCamelIDChanged)
        self.edtBigSnakeID.textEdited.connect(self.whenBigSnakeIDChanged)

        scanSelf(self, QtWidgets.QLineEdit,
                lambda name, value:
                    value.textEdited.connect(self.saveUIData)
            )
        if len(self.edtOutDir.text()) <= 0:
             self.edtOutDir.setText(getUserDir())

        self.btnGenerate.clicked.connect(self.clickedGenerate)

        

    def readUIData(self):
        filepath = getUserDataDir("uidata.json")
        if not os.path.exists(filepath):
            return
        f = open(filepath, 'r')
        data = json.loads(f.read())
        f.close()
        def read_cb(name, value):
            value.setPlaceholderText(data[name])
        scanSelf(self, QtWidgets.QLineEdit, read_cb)

    def saveUIData(self):
        data = {}
        def save_cb(name, value):
            data[name] = getRealText(value)
        scanSelf(self, QtWidgets.QLineEdit, save_cb)
        data_str = json.dumps(data)
        f = open(getUserDataDir("uidata.json"), 'w')
        f.write(data_str)
        f.close()

    def whenSnakeIDChanged(self, text):
        if not checkSnakeSyntax(self.edtSnakeID.text()):
            self.edtSnakeID.undo()
            return

    def whenCamelIDChanged(self, text):
        if not checkCamelSyntax(self.edtCamelID.text()):
            self.edtCamelID.undo()
            return

    def whenBigSnakeIDChanged(self, text):
        if not checkBigSnakeSyntax(self.edtBigSnakeID.text()):
            self.edtBigSnakeID.undo()
            return

    def whenNameOrPrefixChanged(self, text):
        name = getRealText(self.edtReadName)
        prefix = getRealText(self.edtPrefix)
        if not checkNormalSyntax(name):
            self.edtReadName.undo()
            return
        if not checkNormalSyntax(prefix):
            self.edtPrefix.undo()
            return

        strSnake = normal2Snake(name, prefix)
        strCamel = normal2Camel(name, prefix)
        strBigSnake = normal2BigSnake(name, prefix)

        if len(self.edtSnakeID.text()) == 0:
            self.edtSnakeID.setPlaceholderText(strSnake)
        if len(self.edtCamelID.text()) == 0:
            self.edtCamelID.setPlaceholderText(strCamel)
            self.edtOutFilename.setPlaceholderText(strCamel)
        if len(self.edtBigSnakeID.text()) == 0:
            self.edtBigSnakeID.setPlaceholderText(strBigSnake)

    def clickedGenerate(self):
        pass
