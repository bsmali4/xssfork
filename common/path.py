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

TEMPER_PATH = "{}temper/".format(XSS_FORK_PATH)

FUZZ_DIC_PATH = "{}thirdparty/fuzz_dic/payloads.dic".format(XSS_FORK_PATH)

FUZZ_API_DIC_PATH = "{}thirdparty/fuzz_dic/payload.dic".format(XSS_FORK_PATH)

FUZZ_SCRIPT_PATH = "{}thirdparty/fuzz_script/fuzz.js".format(XSS_FORK_PATH)

MACOS_PHANTOMJS_PATH = "{}thirdparty/phantomjs/Darwin/phantomjs".format(XSS_FORK_PATH)

WINDOWS_PHANTOMJS_PATH = "{}thirdparty/phantomjs/Windows/phantomjs.exe".format(XSS_FORK_PATH)

LINUX_PHANTOMJS_PATH = "{}thirdparty/phantomjs/Linux/phantomjs".format(XSS_FORK_PATH)

EXCEPTION_LOG_PATH = "{}data/exception.log".format(XSS_FORK_PATH)

AUTHENTICATION_KEY_FILE = "{}authentication.key".format(XSS_FORK_PATH)

XSS_FORK_DB = "{}data/xssfork.db".format(XSS_FORK_PATH)

XSS_FORK_SCRIPT_PATH = "{}xssfork.py".format(XSS_FORK_PATH)

XSS_FORK_STDERR_FILE = "{}data/stderr.out".format(XSS_FORK_PATH)

XSS_FORK_STDOUT_FILE = "{}data/stdout.out".format(XSS_FORK_PATH)


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

