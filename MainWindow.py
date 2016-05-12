#!/bin/env python3
# -*- coding: UTF-8 -*-

from PyQt5 import QtWidgets, QtGui, QtCore, Qt
import json

from utils import *
from Ui_MainWindow import Ui_MainWindow
import Interface, Property, Signal, CustomParameter
from Generator import Generator


def getRealText(edt):
    if edt and len(edt.text()) > 0:
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
        ################## 选择目录对话框 #################
        self.selectDialog = QtWidgets.QFileDialog(self)
        self.selectDialog.setWindowTitle(_tr("选择输出目录"))
        self.selectDialog.setDirectory(getRealText(self.edtOutDir))
        # self.selectDialog.setFilter(_tr("目录"))
        self.selectDialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        self.selectDialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)

        ################# 模板列表 #################
        self.cbxTemplate.setEditable(False)
        self.loadTemplateDirs()

        ################# 实现的接口表 #################
        self.modelInterface = QtGui.QStandardItemModel(1, 1)
        self.modelInterface.setHeaderData(0, QtCore.Qt.Horizontal, QtCore.QVariant(_tr("GType函数/宏")))
        self.modelInterface.itemChanged.connect(self._onInterfaceTableChanged)
        self.delegateInterface = Interface.Delegate()
        self.lstImplInteface.setModel(self.modelInterface)
        self.lstImplInteface.setItemDelegate(self.delegateInterface)

        ################# 属性表 #################
        self.modelProperty = QtGui.QStandardItemModel(1, 5)
        self.modelProperty.setHeaderData(0, QtCore.Qt.Horizontal, QtCore.QVariant(_tr("名称")))
        self.modelProperty.setHeaderData(1, QtCore.Qt.Horizontal, QtCore.QVariant(_tr("类型")))
        self.modelProperty.setHeaderData(2, QtCore.Qt.Horizontal, QtCore.QVariant(_tr("默认值")))
        self.modelProperty.setHeaderData(3, QtCore.Qt.Horizontal, QtCore.QVariant(_tr("最大值")))
        self.modelProperty.setHeaderData(4, QtCore.Qt.Horizontal, QtCore.QVariant(_tr("最小值")))
        self.modelProperty.itemChanged.connect(self._onPropertyTableChanged)
        self.delegateProperty = Property.Delegate()
        self.lstProperties.setModel(self.modelProperty)
        self.lstProperties.setItemDelegate(self.delegateProperty)

        ################# 信号表 #################
        self.modelSignal = QtGui.QStandardItemModel(1, 2)
        self.modelSignal.setHeaderData(0, QtCore.Qt.Horizontal, QtCore.QVariant(_tr("名称")))
        self.modelSignal.setHeaderData(1, QtCore.Qt.Horizontal, QtCore.QVariant(_tr("回调类型")))
        self.modelSignal.itemChanged.connect(self._onSignalTableChanged)
        self.delegateSignal = Signal.Delegate()
        self.lstSignals.setModel(self.modelSignal)
        self.lstSignals.setItemDelegate(self.delegateSignal)

        ################# 自定义参数表 #################
        self.modelCustomParameter = QtGui.QStandardItemModel(1, 2)
        self.modelCustomParameter.setHeaderData(0, QtCore.Qt.Horizontal, QtCore.QVariant(_tr("名称")))
        self.modelCustomParameter.setHeaderData(1, QtCore.Qt.Horizontal, QtCore.QVariant(_tr("值")))
        self.modelCustomParameter.itemChanged.connect(self._onCustomParameterTableChanged)
        self.delegateCustomParameter = CustomParameter.Delegate()
        self.lstCustomParameters.setModel(self.modelCustomParameter)
        self.lstCustomParameters.setItemDelegate(self.delegateCustomParameter)

    def _init_connects(self):
        self.cbxTemplate.currentIndexChanged.connect(self._onTemplateComboBoxSelected)
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

        ########### 菜单 ###########
        self.act_open_default_tmpl_dir.triggered.connect(self._onActionOpenDefaultTemplateDir)
        self.act_open_user_tmpl_dir.triggered.connect(self._onActionOpenUserTemplateDir)

    def loadTemplateDirs(self):
        self.cbxTemplate.clear()
        self.allTemplateDirs = []
        self.cbxTemplate.addItem(_tr('默认模板'))
        for root, dirs, files in os.walk(getUserTemplateDir()):
            for d in dirs:
                # 只遍历一级目录
                if len(os.path.split(d)) == 1             \
                    or (                                  \
                        len(os.path.split(d)) == 2        \
                        and (                             \
                            os.path.split(d)[0] == ''     \
                            or os.path.split(d)[1] == '') \
                        ):
                    path = os.path.join(root, d)
                    self.allTemplateDirs.append(path)
        userTemplateDirs = []
        for path in self.allTemplateDirs:
            userTemplateDirs.append(                      \
                    path.replace(getUserTemplateDir(),"") \
                        .replace("/","")                  \
                        .replace("\\","")                 \
                )
        self.cbxTemplate.addItems(userTemplateDirs)
        self.cbxTemplate.setCurrentIndex(0)
        self.selectedTemplateDir = getDefaultTemplateDir()

    def readUIData(self):
        filepath = getUserDataDir("uidata.json")
        if not os.path.exists(filepath):
            return
        f = open(filepath, 'r')
        data = json.loads(f.read())
        f.close()
        def read_cb(name, value):
            if name in data:
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

    def _onTemplateComboBoxSelected(self, index):
        if index == 0 or index == -1:
            self.selectedTemplateDir = getDefaultTemplateDir()
        else:
            if index > 0 and index < len(self.allTemplateDirs):
                self.selectedTemplateDir = self.allTemplateDirs[index]

    def _onInterfaceTableChanged(self, item):
        if item.index().row() == self.modelInterface.rowCount() - 1 \
            and len(item.text()) > 0:
            self.modelInterface.appendRow(None)

    def _onPropertyTableChanged(self, item):
        if item.index().row() == self.modelProperty.rowCount() - 1\
            and len(item.text()) > 0:
            self.modelProperty.appendRow(None)

    def _onSignalTableChanged(self, item):
        if item.index().row() == self.modelSignal.rowCount() - 1\
            and len(item.text()) > 0:
            self.modelSignal.appendRow(None)

    def _onCustomParameterTableChanged(self, item):
        if item.index().row() == self.modelCustomParameter.rowCount() - 1\
            and len(item.text()) > 0:
            self.modelCustomParameter.appendRow(None)

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
            self.edtOutFilename.setPlaceholderText(strCamel.lower())
        if len(self.edtBigSnakeID.text()) == 0:
            self.edtBigSnakeID.setPlaceholderText(strBigSnake)

    def _onClickedSelectDir(self):
        self.edtOutDir.setText(self.selectDialog.selectedFiles()[0])
        self.saveUIData()


    def _onActionOpenDefaultTemplateDir(self):
        dirPath = getDefaultTemplateDir().replace("\\", "/")
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(dirPath))
        print("called _onActionOpenDefaultTemplateDir")

    def _onActionOpenUserTemplateDir(self):
        dirPath = getUserTemplateDir().replace("\\", "/")
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(dirPath))
        print("called _onActionOpenUserTemplateDir")

    def getInterfaceData(self):
        data = []
        cout = self.modelInterface.rowCount()
        for i in range(0, cout):
            if self.modelInterface.item(i, 0):
                data += {
                    "type_macro": self.modelInterface.item(i, 0).text(),
                }
        return data

    def getPropertyData(self):
        data = []
        cout = self.modelProperty.rowCount()
        for i in range(0, cout):
            if self.modelProperty.item(i, 0):
                data += {
                    "name"   : self.modelProperty.item(i, 0).text(),
                    "type"   : self.modelProperty.item(i, 1).text(),
                    "default": self.modelProperty.item(i, 2).text(),
                    "max"    : self.modelProperty.item(i, 3).text(),
                    "min"    : self.modelProperty.item(i, 4).text(),
                }
        return data

    def getSignalData(self):
        data = []
        cout = self.modelSignal.rowCount()
        for i in range(0, cout):
            if self.modelSignal.item(i, 0):
                data += {
                    "name": self.modelSignal.item(i, 0).text(),
                    "type": self.modelSignal.item(i, 1).text(),
                }
        return data

    def getCustomParameterData(self):
        data = []
        cout = self.modelCustomParameter.rowCount()
        for i in range(0, cout):
            if self.modelCustomParameter.item(i, 0):
                data[self.modelCustomParameter.item(i, 0).text()] = self.modelCustomParameter.item(i, 1).text()
        return data

    def errorMsg(self, title, text):
        # QMessageBox::Critical 3 an icon indicating that the message represents a critical problem.
        self.msgBox = QtWidgets.QMessageBox(3, title, text)
        self.msgBox.show()

    def getTemplateBaseName(self):
        if self.rbtnNormalClass.isChecked():
            return "class"
        elif  self.rbtnAbstractClass.isChecked():
            return "abstract"
        elif  self.rbtnInterface.isChecked():
            return "interface"

    def checkParms(self):
        if len(getRealText(self.edtOutFilename).strip()) == 0:
            self.errorMsg(_tr("错误!"), _tr("没有指定输出文件名!"))
            return False
        if len(getRealText(self.edtOutDir).strip()) == 0:
            self.errorMsg(_tr("错误!"), _tr("没有指定输出文件夹!"))
            return False
        if not os.path.isdir(getRealText(self.edtOutDir)):
            self.errorMsg(_tr("错误!"), _tr("输出文件夹不存在或不是文件夹!"))
            return False

        baseName = self.getTemplateBaseName()
        path = os.path.join(self.selectedTemplateDir, baseName + ".c.tmpl")
        if not os.path.isfile(path):
            self.errorMsg(_tr("错误!"), _tr("模板文件不存在: %s") % path)
            return False
        path = os.path.join(self.selectedTemplateDir, baseName + ".h.tmpl")
        if not os.path.isfile(path):
            self.errorMsg(_tr("错误!"), _tr("模板文件不存在: %s") % path)
            return False

        return True

    def onClickedGenerate(self):
        if not self.checkParms():
            return
        outName = getRealText(self.edtOutFilename)
        outDir = getRealText(self.edtOutDir)
        file_base = os.path.join(outDir, outName)

        read_name    = getRealText(self.edtReadName)
        prefix       = getRealText(self.edtPrefix)
        snake_id     = getRealText(self.edtSnakeID)
        camel_id     = getRealText(self.edtCamelID)
        big_snake_id = getRealText(self.edtBigSnakeID)


        data = { 
            #元信息
            "version"              : getVersion(),
            "template_dir"         : self.selectedTemplateDir,
            "file_base"            : outName,

            #名称信息
            "read_name"    : read_name,
            "prefix"       : prefix,
            "snake_id"     : snake_id,
            "camel_id"     : camel_id,
            "big_snake_id" : big_snake_id,

            #继承信息
            "parent_name"       : getRealText(self.edtParentName),
            "parent_prefix"     : getRealText(self.edtParentPrefix),
            "parent_class_name" : getRealText(self.edtParentClassName),
            "parent_type_macro" : getRealText(self.edtParentTypeMacro),

            #实现信息
            "impl_interface" : self.getInterfaceData(),
            "impl_property"  : self.getPropertyData(),
            "impl_signal"    : self.getSignalData(),

            #自定义参数
            "custom" : self.getCustomParameterData(),
        }
        gen = Generator(self.selectedTemplateDir, data)
        f = None
        path = ""
        baseName = self.getTemplateBaseName()

        try:
            path = file_base + ".c"
            f = open(getUserDataDir(path), 'w')
            f.write(gen.generate(os.path.join(self.selectedTemplateDir, baseName + ".c.tmpl")))
            f.close()
            path = file_base + ".h"
            f = open(getUserDataDir(path), 'w')
            f.write(gen.generate(os.path.join(self.selectedTemplateDir, baseName + ".h.tmpl")))
            f.close()
        except Exception as e:
            self.errorMsg(_tr("错误!"), _tr("生成文件时发生错误!\n文件: %s\n错误: %s\n") % (path, e))
            # QMessageBox::Critical 3 an icon indicating that the message represents a critical problem.
            self.msgBox = QtWidgets.QMessageBox(3, _tr("错误!"), _tr("生成文件时发生错误!\n文件: %s\n错误: %s\n") % (path, str(e)))
            self.msgBox.show()
        finally:
            if f:
                f.close()


