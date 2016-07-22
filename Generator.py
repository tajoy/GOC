#!/bin/env python3
# -*- coding: UTF-8 -*-

import tenjin
tenjin.set_template_encoding('utf-8')
from tenjin.helpers import *
import config

class Generator(object):
    def __init__(self, path, data, encoding='utf-8'):
        print('path='+path)
        self.engine = tenjin.Engine(path=[path], postfix='.tmpl', trace=False)
        self.data = data

    def set(self, name, value):
        self.data[name] = value

    def get(self, name):
        return self.data[name]

    def generate(self, template_file):
        if config.debug:
            print('template_file:\n'+str(template_file))
            print('data:\n'+str(self.data))
        ret = self.engine.render(template_file,
                                  context=self.data
                                 )
        if config.debug:
            print('ret:\n'+ret)

        return ret
