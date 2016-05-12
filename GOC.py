#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from MainWindow import MainWindow

app = None
mainWindow = None

def main():
    global app
    global mainWindow
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

