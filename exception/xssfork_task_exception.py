#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""


class XssforkTaskError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, "执行sql数据失败, {}".format(msg))


class XssforkTaskSaveError(XssforkTaskError):
    def __init__(self, msg):
        Exception.__init__(self, "插入数据失败,{}".format(msg))


class XssforkTaskFindError(XssforkTaskError):
    def __init__(self, msg):
        Exception.__init__(self, "查询数据失败{}".format(msg))