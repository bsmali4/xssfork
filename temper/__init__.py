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
from temper import Temper
from common.path import EXCEPTION_LOG_PATH
from common.system_config import LIGHT_MODEL
from common.system_config import HEAVY_MODEL