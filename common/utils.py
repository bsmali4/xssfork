#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
from __future__ import print_function
import os
import traceback
import string
from random import choice
from common.path import EXCEPTION_LOG_PATH
from common.path import TEMPER_PATH


def read_file_to_array(file_path):
    results = []
    try:
        files = open(file_path, 'r')
        results = [line.replace("\n", "") for line in files.readlines()]
    except IOError as e:
        traceback.print_exc(file=open(EXCEPTION_LOG_PATH, 'a'))
    return results


def load_pyfiles(path):
    filenames = []
    size = 0
    try:
        filenames = [filename.replace(".py", "") for filename in os.listdir(path)
                     if filename.endswith(".py") and filename not in['__init__.py', 'temper.py']]
        size = len(filenames)
    except Exception:
        traceback.print_exc(file=open(EXCEPTION_LOG_PATH, 'a'))
    return filenames, size
    

def make_random_number(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])
