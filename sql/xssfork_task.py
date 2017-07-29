#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""

from field import Field
from field import IntegerField
from field import StringField
from xssfork_model import XssforkModel


class XssforkTask(XssforkModel):
    id = IntegerField('id')
    time = StringField('time')
    url = StringField('url')
    cookie = StringField('cookie')
    data = StringField('data')
    destination = StringField('destination')
    status = 0
    __table__ = "xssfork_task"
    __show_sql__ = False