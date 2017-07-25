#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""

import platform

WINDOWS = "Windows"
LINUX = "Linux"
MACOS = "Darwin"


def get_system_type():
    return platform.system()