#!/bin/env python3
# -*- coding: UTF-8 -*-

import platform
import os
import sys


installPrefix = '/usr/local'

     
if platform.system() == 'Linux':
    dataDir = os.path.join(installPrefix, '/share', 'GOC')
elif platform.system() == 'Windows':
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(sys.path[0]):
        dataDir = os.path.join(sys.path[0], 'data')
    elif os.path.isfile(sys.path[0]):
        dataDir = os.path.join(os.path.dirname(sys.path[0]), 'data')
elif platform.system() == 'MacOS':
    dataDir = os.path.join(installPrefix, '/share', 'GOC')


version = '0.1.0'


# 测试所需, 以后该为安装路径
defaultModelDir = os.path.join(dataDir, 'default')
