#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
import time


def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())