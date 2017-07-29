#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
from abc import ABCMeta
from abc import abstractproperty


class Temper(object):
    __metaclass__ = ABCMeta
    """
    编码脚本
    """
    def __init__(self):
        self.keywords = ['javascript', '<script>', '</script>', 'script', 'onerror', 'onload', 'onfocus', 'onclick', 'onmove',
                         'onmouseover', 'autofocus', 'onkeypress', ]

    @abstractproperty
    def temper(self, payload, model, **kw):
        pass

    def get_keywords(self):
        return self.keywords

    def get_keyword_count(self):
        """
        获得payload中出现keyword的个数
        eg:<img src="javascript:alert(65534);">  3个 分别是img,javascript script
        """
        count = 0
        for keyword in self.keywords:
            if keyword in self.payload:
                count += 1
        return count

