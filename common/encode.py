#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
import platform
import sys
from system_info import WINDOWS


def init_encode():
    if platform.system() == WINDOWS:
        reload(sys)
        sys.setdefaultencoding('gbk')
    else:
        reload(sys)
        sys.setdefaultencoding('utf8')


def url_encode(url):
    return url.replace("'", "%27").replace("\"", "%22").replace(" ", "%20")