#!/bin/env python3
# -*- coding: UTF-8 -*-


from PyQt5 import QtWidgets, QtCore, Qt

from utils import *

class Delegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        #createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex) -> QWidget
        editor = QtWidgets.QLineEdit(parent)
        return editor

    def setEditorData(self, editor, index):
        #setEditorData(self, QWidget, QModelIndex)
        value = index.model().data(index, QtCore.Qt.EditRole)
        editor.setText(value)

    def setModelData(self, editor, model, index):
        #setModelData(self, QWidget, QAbstractItemModel, QModelIndex)
        if not checkNormalSyntax(editor.text()):
            return
        model.setData(index, editor.text(), QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        #updateEditorGeometry(self, QWidget, QStyleOptionViewItem, QModelIndex)
        editor.setGeometry(option.rect)