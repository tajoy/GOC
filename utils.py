#!/bin/env python3
# -*- coding: UTF-8 -*-
import os
import re

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

def checkIdentifySyntax(text):
    return re.match(r"[a-zA-Z_][a-zA-Z0-9_]*", text)

def getDataDir(path):
    dataDir = os.path.join(os.path.expanduser('~'), '.GOC')
    if not os.path.isdir(dataDir):
        os.mkdir(dataDir)
    if path and len(path) > 0:
        os.path.join(dataDir, path)
    return dataDir


def scanSelf(self, klass, func):
    for name,value in vars(self).items():
        if issubclass(value.__class__, klass):
            func(name, value)