#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
import sys
import platform
from system_info import WINDOWS
from system_info import get_system_type


try:
    reload  # Python 2
except NameError:
    from importlib import reload  # Python 3


def init_encode():
    reload(sys)
    if get_system_type() == WINDOWS:
        sys.setdefaultencoding('gbk')
    else:
        sys.setdefaultencoding('utf8')


def url_encode(url):
    return url.replace("'", "%27").replace("\"", "%22").replace(" ", "%20")