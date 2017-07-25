#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
import os


def read_file_to_array(file_path):
    results = []
    with open(file_path, "r") as lines:
        for line in lines:
            results.append(line.replace("\n", ""))
    return results


def load_pyfiles(path):
    filenames = []
    size = 0
    try:
        for filename in os.listdir(path):
            if filename.endswith(".py") and filename != '__init__.py' and filename != "temper.py":
                filenames.append(filename.replace(".py", ""))
        size = len(filenames)
    except Exception as e:
        print e
    return filenames, size


def start_with(string, substring):
    try:
        if string.strip().index(substring) == 0:
            return True
    except Exception, e:
        return False


def end_with(string, substring):
    try:
        if string[len(string) - 1] == substring:
            return True
    except Exception, e:
        return False