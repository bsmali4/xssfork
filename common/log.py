#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
import logging
import platform
from path import XSS_FORK_PATH

if platform.system() == 'Windows':
    import sys
    reload(sys)
    sys.setdefaultencoding('gbk')

LOGGER = None


def set_level(level):
    global LOGGER
    LOGGER.setLevel(level)


def get_logger():
    global LOGGER
    if not LOGGER:
        init_config()
    return LOGGER


def get_file_handler():
    file_handler = logging.FileHandler('%s/data/xssfork.log' %(XSS_FORK_PATH))
    file_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    file_handler.setFormatter(file_formatter)
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    if platform.system() == 'Windows':
        stream_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")
        stream_handler.setFormatter(stream_formatter)
    else:
        from colorlog import ColoredFormatter
        LOGFORMAT = "%(log_color)s[%(asctime)s]%(reset)s %(log_color)s[%(levelname)s] %(message)s%(reset)s"
        stream_formatter = ColoredFormatter(LOGFORMAT, "%H:%M:%S")
        stream_handler.setFormatter(stream_formatter)
    return stream_handler


def init_config():
    global LOGGER
    LOGGER = logging.getLogger('xssSickleLog')
    file_handler = get_file_handler()
    stream_handler = get_stream_handler()
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(stream_handler)
    return LOGGER