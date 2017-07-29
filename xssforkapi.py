#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
from __future__ import print_function
import time
import logging
import optparse
import web_service
from common import log
from common import logo
from common import encode
from common import utils
from common.path import TEMPER_PATH
from taskschedule.task_schedule import TaskSchedule
from taskschedule.payloads import PayLoads
from common.system_time import get_current_time
from common.system_info import DEFAULT_UA

try:
    reload  # Python 2
except NameError:
    from importlib import reload  # Python 3


def help():
    encode.init_encode()
    apiparser = optparse.OptionParser()
    apiparser.add_option("-p", "--port", help="开启服务的端口", default=2333)
    apiparser.add_option("-a", "--adapter", help="适配器 eg gevent or eventlet", default="gevent")
    apiparser.add_option("-r", "--refresh", help="更新服务器key并将原有扫描记录清空", default="False",)
    (args, _) = apiparser.parse_args()
    if args.refresh not in ['True', 'False']:
        logger = log.get_logger()
        logger.setLevel(logging.DEBUG)
        logger.error(u'refresh只能设置为True或者False')
        logger.info(u'查看帮组:python {} -h'.format(__file__))
        exit()
    refresh = True if args.refresh == "True" else False
    web_service.server(int(args.port), args.adapter, refresh)

if __name__ == "__main__":
    start_time = time.time()
    help()