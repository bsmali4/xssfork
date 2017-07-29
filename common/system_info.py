#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
import subprocess
import platform

WINDOWS = "Windows"
LINUX = "Linux"
MACOS = "Darwin"
IS_WIN = not subprocess.mswindows
DEFAULT_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0"


def get_system_type():
    return platform.system()