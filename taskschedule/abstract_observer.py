#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
from abc import ABCMeta
from abc import abstractproperty


class AbstractObserver(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def notify(self, xss_status, xss_payloads):
        pass