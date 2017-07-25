#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""

import os
from system_info import WINDOWS
from system_info import LINUX
from system_info import MACOS
from system_info import get_system_type


XSS_FORK_PATH = "{}/../".format(os.path.dirname(os.path.abspath(__file__)))

TEMPER_PATH = "%stemper/" % (XSS_FORK_PATH)

FUZZ_DIC_PATH = "%sthirdparty/fuzz_dic/payloads.dic" % (XSS_FORK_PATH)

FUZZ_SCRIPT_PATH = "%sthirdparty/fuzz_script/fuzz.js" % (XSS_FORK_PATH)

MACOS_PHANTOMJS_PATH = "%sthirdparty/phantomjs/Darwin/phantomjs" % (XSS_FORK_PATH)

WINDOWS_PHANTOMJS_PATH = "%sthirdparty/phantomjs/Windows/phantomjs.exe" % (XSS_FORK_PATH)

LINUX_PHANTOMJS_PATH = "%sthirdparty/phantomjs/Linux/phantomjs" % (XSS_FORK_PATH)

EXCEPTION_LOG_PATH = "%sdata/exception.log" % (XSS_FORK_PATH)


def get_phantomjs_path():
    system_type = get_system_type()
    if system_type == WINDOWS:
        return WINDOWS_PHANTOMJS_PATH
    elif system_type == LINUX:
        return LINUX_PHANTOMJS_PATH
    elif system_type == MACOS:
        return MACOS_PHANTOMJS_PATH
    else:
        return LINUX_PHANTOMJS_PATH

