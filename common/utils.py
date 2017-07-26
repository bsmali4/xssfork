#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
from __future__ import print_function
import os


def read_file_to_array(file_path):
    with open(file_path, "r") as lines:
        return [line.replace("\n", "") for line in lines]


def load_pyfiles(path):
    filenames = []
    size = 0
    try:
        for filename in os.listdir(path):
            if filename.endswith(".py") and filename not in ('__init__.py', "temper.py"):
                filenames.append(filename.replace(".py", ""))
        size = len(filenames)
    except Exception as e:
        print(e)
    return filenames, size


def start_with(string, substring):
    try:
        if string.strip().index(substring) == 0:
            return True
    except Exception as e:
        return False


def end_with(string, substring):
    try:
        if string[len(string) - 1] == substring:
            return True
    except Exception as e:
        return False
