#!/bin/env python3
# -*- coding: UTF-8 -*-

import tenjin
tenjin.set_template_encoding('utf-8')
from tenjin.helpers import to_str, echo


class Generator(object):
    def __init__(self, path, data, encoding='utf-8'):
        print('path='+path)
        self.engine = tenjin.Engine(path=[path], escapefunc=to_str)
        self.data = data

    def set(self, name, value):
        self.data[name] = value

    def get(self, name):
        return self.data[name]

    def generate(self, template_file):
        return self.engine.render(template_file,
                                  context=self.data
                                 )
