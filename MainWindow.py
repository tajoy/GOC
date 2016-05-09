#!/bin/env python3
# -*- coding: UTF-8 -*-

from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from utils import *
import json

from Ui_MainWindow import Ui_MainWindow

import Interface, Property, Signal, CustomParameter


def getRealText(edt):
    if len(edt.text()) > 0:
        return edt.text()
    else:
        return edt.placeholderText()

def _tr(s):
    return QtCore.QCoreApplication.translate("MainWindow",s)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.readUIData()
        if len(self.edtOutDir.text()) and len(self.edtOutDir.placeholderText()) <= 0:
             self.edtOutDir.setText(getUserDir())
        self._init_widgets()
        self._init_connects()

    def _init_widgets(self):

        self.selectDialog = QtWidgets.QFileDialog(self)
        self.selectDialog.setWindowTitle(_tr("选择输出目录"))
        self.selectDialog.setDirectory(getRealText(self.edtOutDir))
        # self.selectDialog.setFilter(_tr("目录"))
        self.selectDialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        self.selectDialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)

        self.modelInterface = QtGui.QStandardItemModel(1, 1)
        self.modelInterface.setHeaderData(0, QtCore.Qt.Horizontal, QtCore.QVariant(_tr("GType函数/宏")))
        self.modelInterface.itemChanged.connect(self._onInterfaceTableChanged)
        self.delegateInterface = Interface.Delegate()
        self.lstImplInteface.setModel(self.modelInterface)
        self.lstImplInteface.setItemDelegate(self.delegateInterface)


        self.modelProperty = QtGui.QStandardItemModel(1, 2)
        self.modelProperty.setHeaderData(0, QtCore.Qt.Horizontal, QtCore.QVariant(_tr("名称")))
        self.modelProperty.setHeaderData(1, QtCore.Qt.Horizontal, QtCore.QVariant(_tr("类型")))
        self.modelProperty.itemChanged.connect(self._onPropertyTableChanged)
        self.delegateProperty = Property.Delegate()
        self.lstProperties.setModel(self.modelProperty)
        self.lstProperties.setItemDelegate(self.delegateProperty)


        self.modelSignal = QtGui.QStandardItemModel(1, 2)
        self.modelSignal.setHeaderData(0, QtCore.Qt.Horizontal, QtCore.QVariant(_tr("名称")))
        self.modelSignal.setHeaderData(1, QtCore.Qt.Horizontal, QtCore.QVariant(_tr("回调类型")))
        self.modelSignal.itemChanged.connect(self._onSignalTableChanged)
        self.delegateSignal = Signal.Delegate()
        self.lstSignals.setModel(self.modelSignal)
        self.lstSignals.setItemDelegate(self.delegateSignal)


        self.modelCustomParameter = QtGui.QStandardItemModel(1, 2)
        self.modelCustomParameter.setHeaderData(0, QtCore.Qt.Horizontal, QtCore.QVariant(_tr("名称")))
        self.modelCustomParameter.setHeaderData(1, QtCore.Qt.Horizontal, QtCore.QVariant(_tr("值")))
        self.modelCustomParameter.itemChanged.connect(self._onCustomParameterTableChanged)
        self.delegateCustomParameter = CustomParameter.Delegate()
        self.lstCustomParameters.setModel(self.modelCustomParameter)
        self.lstCustomParameters.setItemDelegate(self.delegateCustomParameter)

    def _onInterfaceTableChanged(self, item):
        if item.index().row() == self.modelInterface.rowCount() - 1:
            self.modelInterface.appendRow(None)

    def _onPropertyTableChanged(self, item):
        if item.index().row() == self.modelProperty.rowCount() - 1:
            self.modelProperty.appendRow(None)

    def _onSignalTableChanged(self, item):
        if item.index().row() == self.modelSignal.rowCount() - 1:
            self.modelSignal.appendRow(None)

    def _onCustomParameterTableChanged(self, item):
        if item.index().row() == self.modelCustomParameter.rowCount() - 1:
            self.modelCustomParameter.appendRow(None)

    def _init_connects(self):
        self.edtReadName.textEdited.connect(self._onNameOrPrefixChanged)
        self.edtPrefix.textEdited.connect(self._onNameOrPrefixChanged)
        self.edtSnakeID.textEdited.connect(self._onSnakeIDChanged)
        self.edtCamelID.textEdited.connect(self._onCamelIDChanged)
        self.edtBigSnakeID.textEdited.connect(self._onBigSnakeIDChanged)

        scanSelf(self, QtWidgets.QLineEdit,
                lambda name, value:
                    value.textEdited.connect(self.saveUIData)
            )

        self.btnGenerate.clicked.connect(self.onClickedGenerate)

        self.selectDialog.accepted.connect(self._onClickedSelectDir)
        self.btnSelOutDir.clicked.connect(self.selectDialog.exec)

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
        print("saveUIData")
        data = {}
        def save_cb(name, value):
            data[name] = getRealText(value)
        scanSelf(self, QtWidgets.QLineEdit, save_cb)
        data_str = json.dumps(data)
        f = open(getUserDataDir("uidata.json"), 'w')
        f.write(data_str)
        f.close()

    def _onSnakeIDChanged(self, text):
        if not checkSnakeSyntax(self.edtSnakeID.text()):
            self.edtSnakeID.undo()
            return

    def _onCamelIDChanged(self, text):
        if not checkCamelSyntax(self.edtCamelID.text()):
            self.edtCamelID.undo()
            return

    def _onBigSnakeIDChanged(self, text):
        if not checkBigSnakeSyntax(self.edtBigSnakeID.text()):
            self.edtBigSnakeID.undo()
            return

    def _onNameOrPrefixChanged(self, text):
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

    def _onClickedSelectDir(self):
        self.edtOutDir.setText(self.selectDialog.selectedFiles()[0])
        self.saveUIData()

    def onClickedGenerate(self):
        pass
