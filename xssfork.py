#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
import time
import logging
import optparse
from common import log
from common import logo
from common import encode
from common import utils
from common.path import TEMPER_PATH
from taskschedule.task_schedule import TaskSchedule
from taskschedule.payloads import PayLoads
from common.system_time import get_current_time


def help():
    encode.init_encode()
    apiparser = optparse.OptionParser()
    apiparser.add_option("-u", "--url", help="需要测试的链接 eg:http://xssfork.codersec.net/xssdemo.php?id=23",
                         action="store")
    apiparser.add_option("-D", "--destination", help="输出位置链接 eg:http://xssfork.codersec.net/output.php",
                         action="store")
    apiparser.add_option("-l", "--level", help="扫描等级 eg:1-10", action="store", default=1, type=int)
    apiparser.add_option("-c", "--cookie", help="cookie eg:sessid=284EA45D5C14B2A;flag=1", action="store")
    apiparser.add_option("-d", "--data", help="post请求数据 eg:username=admin&pass=admin888", action="store")
    apiparser.add_option("-t", "--temper", help="编码脚本 混合模式或者单个模式 eg:Big ", action="store")
    apiparser.add_option("-m", "--model", help="扫描模式 eg:light | heavy", action="store", default='light')
    apiparser.add_option("--list", help="列出所有编码脚本", action="store_true")
    (args, _) = apiparser.parse_args()
    is_set_url = True if args.url else False
    if args.level < 1 or args.level > 10:
        logger = log.get_logger()
        logger.setLevel(logging.ERROR)
        logger.error(u'错误原因. level范围为 1-10')
        exit()
    if args.list is True:
        print_temper()
    elif is_set_url:
        task_schedule = TaskSchedule(args.url, args.destination, args.level, args.cookie, args.data, args.temper, args.model)
        task_schedule.main()
    else:
        logger = log.get_logger()
        logger.setLevel(logging.DEBUG)
        logger.error(u'错误原因1:url，readfile至少设置一个')
        logger.error(u'错误原因2:url，readfile不能同时设置')
        logger.info(u'查看帮组:python {} -h'.format(__file__))


def print_logo():
    print logo.LOGO


def print_temper():
    logger = log.get_logger()
    logger.setLevel(logging.DEBUG)
    filenames, size = utils.load_pyfiles(TEMPER_PATH)
    logger.debug("总共有{}个编码脚本".format(size))
    i = 0
    for temper in filenames:
        logger.debug('[%s]%s' % (i, temper))
        i += 1

if __name__ == "__main__":
    start_time = time.time()
    print_logo()
    help()
    end_time = time.time()
    print "This task costs {} s".format(end_time - start_time)
    print '[*] shutting down at {}'.format(get_current_time())