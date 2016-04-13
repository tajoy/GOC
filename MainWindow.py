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
        self.edtReadName.textChanged.connect(self.whenNameOrPrefixChanged)
        self.edtPrefix.textChanged.connect(self.whenNameOrPrefixChanged)

        scanSelf(self, QtWidgets.QLineEdit,
                lambda name, value:
                    value.textChanged.connect(self.saveUIData)
            )

    def listenUIDataChanged(self):
        pass

    def readUIData(self):
        pass

    def saveUIData(self):
        data = {}
        def scan_cb(name, value):
            data[name] = getRealText(value)
        scanSelf(self, QtWidgets.QLineEdit, scan_cb)
        data_str = json.dumps(data)
        f = open(getDataDir("uidata.json"))
        f.write(data_str)
        f.close()



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


