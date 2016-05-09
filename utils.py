#!/bin/env python3
# -*- coding: UTF-8 -*-
import os
import re
import config

from PyQt5 import QtCore

def normal2Snake(text, prefix):
    arr = text.split(" ")
    ret = ""
    for word in arr:
        ret += word.lower() + "_"
    if prefix == None:
        return ret[:-1]
    else:
        return normal2Snake(prefix, None) + "_" + ret[:-1]


def normal2Camel(text, prefix):
    arr = text.split(" ")
    ret = ""
    for word in arr:
        ret += word[0:1].upper() + word.lower()[1:]
    if prefix == None:
        return ret
    else:
        return normal2Camel(prefix, None) + ret

def normal2BigSnake(text, prefix):
    arr = text.split(" ")
    ret = ""
    for word in arr:
        ret += word.upper() + "_"
    if prefix == None:
        return ret[:-1]
    else:
        return normal2BigSnake(prefix, None) + ret

def checkNormalSyntax(text):
    arr = text.split(" ")
    index = 0
    for word in arr:
        word = word.strip()
        if word == "":
            index +=1
            continue
        if index == 0:
            if not re.match(r"[a-zA-Z_][a-zA-Z0-9_]*", word):
                return False
        else:
            if not re.match(r"[a-zA-Z0-9_]+", word):
                return False
        index += 1
    return True

def checkSnakeSyntax(text):
    arr = text.split(" ")
    index = 0
    for word in arr:
        word = word.strip()
        if word == "":
            index +=1
            continue
        if index == 0:
            if not re.match(r"[a-z][a-z0-9_]*", word):
                return False
        else:
            if not re.match(r"[a-z0-9_]+", word):
                return False
        index += 1
    return True

def checkCamelSyntax(text):
    arr = text.split(" ")
    index = 0
    for word in arr:
        word = word.strip()
        if word == "":
            index +=1
            continue
        if index == 0:
            if not re.match(r"[A-Z][a-zA-Z0-9]*", word):
                return False
        else:
            if not re.match(r"[a-zA-Z0-9]+", word):
                return False
        index += 1
    return True

def checkBigSnakeSyntax(text):
    arr = text.split(" ")
    index = 0
    for word in arr:
        word = word.strip()
        if word == "":
            index +=1
            continue
        if index == 0:
            if not re.match(r"[A-Z][A-Z0-9_]*", word):
                return False
        else:
            if not re.match(r"[A-Z0-9_]+", word):
                return False
        index += 1
    return True

def checkIdentifySyntax(text):
    return re.match(r"[a-zA-Z_][a-zA-Z0-9_]*", text)

def getDataDir():
    return config.dataDir

def getUserDir():
    return os.path.expanduser('~')

def getVersion():
    return config.version

def getUserTemplateDir():
    path = getUserDataDir('templates')
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def getDefaultTemplateDir():
    path = os.path.join(getDataDir, 'default')
    if not os.path.exists(path):
        os.mkdir(path)
    return path

def getUserDataDir(path):
    dataDir = os.path.join(getUserDir(), '.GOC')
    if not os.path.exists(dataDir):
        os.mkdir(dataDir)
    if path and len(path) > 0:
        dataDir = os.path.join(dataDir, path)
    return dataDir

def scanSelf(self, klass, func):
    for name,value in vars(self).items():
        if issubclass(value.__class__, klass):
            func(name, value)