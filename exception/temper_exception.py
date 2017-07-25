#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""


class TemperNotFoundError(Exception):
    def __init__(self, temper_name):
        Exception.__init__(self, "{}插件不存在".format(temper_name))