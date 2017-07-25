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
from common import log
from common.path import FUZZ_DIC_PATH
from common.path import get_phantomjs_path
from common.utils import read_file_to_array
from common.path import TEMPER_PATH
from common.system_config import MAX_THREAD_NUM
from common.system_config import MAX_LEVEL
from common.path import EXCEPTION_LOG_PATH
from exception.temper_exception import TemperNotFoundError
from common.path import FUZZ_SCRIPT_PATH
from exception.complete_packet_exception import CompletePacketNotFoundUrl
from common.encode import url_encode
from common.hook_string import hook_list
from common.utils import start_with
from common.utils import end_with
from common.system_time import get_current_time
from common.system_config import LIGHT_MODEL
from common.system_config import HEAVY_MODEL
from common.system_config import HTTP_GET_METHOD
from common.system_config import HTTP_POST_METHOD
