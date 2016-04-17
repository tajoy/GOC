#!/bin/env python3
# -*- coding: UTF-8 -*-


from PyQt5 import QtWidgets, Qt

class Delegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        #createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex) -> QWidget
        editor = QtWidgets.QSpinBox(parent)
        editor.setFrame(False)
        editor.setMinimum(0)
        editor.setMaximum(100)
        return editor

    def setEditorData(self, editor, index):
        #setEditorData(self, QWidget, QModelIndex)
        value = index.model().data(index, Qt.ItemDataRole.EditRole).toInt()
        spinBox = editor
        spinBox.setValue(value)

    def setModelData(self, editor, model, index):
        #setModelData(self, QWidget, QAbstractItemModel, QModelIndex)
        spinBox = editor
        spinBox.interpretText()
        value = spinBox.value()
        model.setData(index, value, Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        #updateEditorGeometry(self, QWidget, QStyleOptionViewItem, QModelIndex)
        editor.setGeometry(option.rect)