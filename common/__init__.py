#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
import os
import sys
XSS_FORK_PATH = "{}/../".format(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, XSS_FORK_PATH)
from taskschedule.task_schedule import CompletePacket