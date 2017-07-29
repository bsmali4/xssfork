#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""


class CompletePacketException(Exception):
    def __init__(self):
        Exception.__init__(self, "CompletePacket对象必须有设置url")


class CompletePacketNotFoundUrl(Exception):
    def __init__(self):
        Exception.__init__(self, "CompletePacket对象必须有设置url")