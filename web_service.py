#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
import os
import time
import signal
import socket
import logging
import threading
import traceback
import subprocess
from common import log
from json import dumps
from common import encode
from sql.config import init_tables
from thirdparty.bottle.bottle import get
from thirdparty.bottle.bottle import post
from thirdparty.bottle.bottle import run
from thirdparty.bottle.bottle import route
from thirdparty.bottle.bottle import hook
from thirdparty.bottle.bottle import response
from thirdparty.bottle.bottle import request
from thirdparty.bottle.bottle import redirect
from thirdparty.bottle.bottle import template
from thirdparty.bottle.bottle import error as return_error
from common.utils import read_file_to_array
from common.path import AUTHENTICATION_KEY_FILE
from common.utils import make_random_number
from common.path import EXCEPTION_LOG_PATH
from sql.xssfork_task import XssforkTask
from exception.xssfork_task_exception import XssforkTaskSaveError
from exception.xssfork_task_exception import XssforkTaskError
from exception.xssfork_task_exception import XssforkTaskFindError
from common.path import XSS_FORK_SCRIPT_PATH
from sql.config import TASK_DONE
from sql.config import TASK_NOT_START
from sql.config import TASK_WORKKING
from common.system_time import get_current_time
from common.path import XSS_FORK_STDERR_FILE
from common.path import XSS_FORK_STDOUT_FILE
from common.system_info import IS_WIN

AUTHENTICATION_KEY = None
xssfork_process_map = dict()  # XssForkProcess dict
params = ['url', 'cookie', 'data', 'destination']


class XssForkProcess(object):
    def __init__(self, task_id, xssfork_task):
        if isinstance(xssfork_task, XssforkTask):
            self._task_id = task_id
            self._xssfork_task = xssfork_task
        self._process = None

    def engine_start(self):
        command = self.get_command()
        self._process = subprocess.Popen(command, shell=True, close_fds=IS_WIN, bufsize=10000,
                                         stdout=open(XSS_FORK_STDOUT_FILE, 'a'), stderr=open(XSS_FORK_STDERR_FILE, 'a'))
        self._xssfork_task.change(status=TASK_WORKKING)
        threading.Thread(target=self.check_engine_status, args=(1, )).start()

    def check_engine_status(self, sleep_time):
        while True:
            time.sleep(sleep_time)
            if self.engine_has_terminated():
                self._xssfork_task.change(status=TASK_DONE)
                break

    def get_command(self):
        if self._xssfork_task.has_key('url'):
            command = 'python {} -u "{}" --id {} --api'.format(XSS_FORK_SCRIPT_PATH, self._xssfork_task.url, self._task_id)
        if self._xssfork_task.has_key('data'):
            command += ' --data "{}"'.format(self._xssfork_task.data)
        if self._xssfork_task.has_key('cookie'):
            command += ' --cookie "{}"'.format(self._xssfork_task.cookie)
        if self._xssfork_task.has_key('destination'):
            command += ' --destination "{}"'.format(self._xssfork_task.destination)
        return command if command is not None else ""

    def engine_stop(self):
        if self._process:
            self._process.terminate()
            return self._process.wait()
        else:
            return None

    def engine_kill(self):
        if self._process:
            try:
                self._process.stderr.close()
                self._process.stdout.close()
                self._process.kill()
                os.killpg(self._process.pid, signal.SIGTERM)
                return self._process.wait()
            except Exception as e:
                traceback.print_exc(file=open(Exception, 'a'))
        return None

    def engine_get_returncode(self):
        if self._process:
            self._process.poll()
            return self._process.returncode
        else:
            return None

    def engine_has_terminated(self):
        return isinstance(self.engine_get_returncode(), int)

    def engine_process(self):
        return self._process


def get_authentication_key(refresh=False):
    global AUTHENTICATION_KEY
    if refresh:
        AUTHENTICATION_KEY = None
    if AUTHENTICATION_KEY is None:
        try:
            AUTHENTICATION_KEY = read_file_to_array(AUTHENTICATION_KEY_FILE)[0]
        except IndexError:
            traceback.print_exc(file=open(EXCEPTION_LOG_PATH, 'a'))

    return AUTHENTICATION_KEY


def init_authentication_key(refresh=False):
    if refresh or get_authentication_key() is None:
        key = make_random_number(15)
        with open(AUTHENTICATION_KEY_FILE, 'w') as file:
            file.write(key)
    return get_authentication_key()


def check_authentication(func):
    def wrapper(*args, **kargs):
        if kargs.has_key('key') and kargs.get('key') == get_authentication_key():
            return func(**kargs)
        else:
            redirect('/xssfork/401')
    return wrapper


@hook("after_request")
def security_headers(json_header=True):
    response.headers["Server"] = "Server"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Pragma"] = "no-cache"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Expires"] = "0"
    if json_header:
        response.content_type = "application/json; charset=UTF-8"


@route('/xssfork/401')
def error401():
    security_headers(True)
    return dumps({"msg": "Access denied"})


@return_error(404)
def error404():
    security_headers(True)
    return dumps({"msg": "Nothing is there"})


@return_error(405)
def error405():
    security_headers(True)
    return dumps({"msg": "Method not allowed"})


@post("/xssfork/create_task/<key>")
@check_authentication
def create_task(key):
    logger = log.get_logger()
    if request.json is None:
        logger.error("sorry,you cann't post empty data")
        return dumps({'status': "fail", 'msg': "you cann't post empty data"})
    xssfork_task = XssforkTask()
    for option, value in request.json.items():
        if option not in params:
            logger.error("sorry,you cann't post {} param".format(option))
            return dumps({'status': 'fail', 'msg': "you cann't post {} param".format(option)})
        xssfork_task.set_option(option, value)
    try:
        xssfork_task.set_option('time', get_current_time())
        xssfork_task.save()
        xssfork_task_id = xssfork_task.find_lastest_id()
        xssfork_process_map[xssfork_task_id] = XssForkProcess(xssfork_task_id, xssfork_task)
        logger.info("task ID {} provided to scan_start()".format(xssfork_task_id))
        return dumps({'status': 'success', 'task_id': xssfork_task_id})
    except XssforkTaskError as e:
        traceback.print_exc(file=open(EXCEPTION_LOG_PATH, 'a'))
    logger.error("sorry, create task fail, See more information in {}".format(EXCEPTION_LOG_PATH))
    return dumps({'status': 'fail', 'msg': 'create task fail, See more information in {}'.format(EXCEPTION_LOG_PATH)})


@get("/xssfork/start_task/<key>/<task_id>")
@check_authentication
def start_task(key, task_id):
    logger = log.get_logger()
    if task_id not in xssfork_process_map:
        logger.error("sorry, task ID {} isn't existed".format(task_id))
        return dumps({"status": "fail", "msg": "task isn't existed"})
    if xssfork_process_map[task_id].engine_process() is None:
        xssfork_process_map[task_id].engine_start()
        logger.info("task ID {} will start scan".format(task_id))
        return dumps({"status": "success", "msg": "task will start"})
    if xssfork_process_map[task_id].engine_has_terminated():
        logger.error("task ID {} has been done".format(task_id))
        return dumps({"status": "fail", "msg": "task has been done"})
    logger.warning("task ID {} is working".format(task_id))
    return dumps({"status": "fail", "msg": "task is working"})


@get("/xssfork/task_status/<key>/<task_id>")
@check_authentication
def task_status(key, task_id):
    logger = log.get_logger()
    if task_id not in xssfork_process_map:
        logger.info("task ID {} isn't existed".format(task_id))
        return dumps({"status": -1, "msg": "task isn’t existed"})
    if xssfork_process_map[task_id].engine_process() is None:
        logger.info("task ID {} isn't started".format(task_id))
        return dumps({"status": TASK_NOT_START, "msg": "task isn't started"})
    if xssfork_process_map[task_id].engine_has_terminated():
        logger.info("task ID {} has been done".format(task_id))
        return dumps({"status": TASK_DONE, "msg": "task has been done"})
    logger.info("task ID {} has is working".format(task_id))
    return dumps({"status": TASK_WORKKING, "msg": "task is working"})


@get("/xssfork/kill_task/<key>/<task_id>")
@check_authentication
def kill_task(key, task_id):
    logger = log.get_logger()
    if task_id not in xssfork_process_map:
        logger.info("task ID {} isn't existed".format(task_id))
        return dumps({"status": "false", "msg": "task isn’t existed"})
    if xssfork_process_map[task_id].engine_process() is None:
        logger.info("task ID {} isn't started".format(task_id))
        return dumps({"status": "false", "msg": "task isn't started"})
    if xssfork_process_map[task_id].engine_has_terminated() is True:
        logger.info("task ID {} has been done".format(task_id))
        return dumps({"status": "false", "msg": "task has been done"})
    xssfork_process_map[task_id].engine_kill()
    logger.info("task ID {} will be killed".format(task_id))
    return dumps({"status": "success", "msg": "task will be killed"})


@get("/xssfork/task_result/<key>/<task_id>")
@check_authentication
def task_result(key, task_id):
    logger = log.get_logger()
    logger.info("task ID [%s] Retrieved scan data and error messages" % task_id)
    try:
        payload = XssforkTask(id=task_id).find()[0][7]
        return dumps({"payload": payload})
    except IndexError as e:
        traceback.print_exc(file=open(EXCEPTION_LOG_PATH, 'a'))
    return dumps({"payload": None})


def server(port, adapter="gevent", refresh=False):
    encode.init_encode()
    logger = log.get_logger()
    try:
        if adapter == "gevent":
            from gevent import monkey
            monkey.patch_all()
        elif adapter == "eventlet":
            import eventlet
            eventlet.monkey_patch()
        logger.setLevel(logging.DEBUG)
        logger.debug("Using adapter '%s' to run bottle" % adapter)
        logger.debug("Using port %s to run bottle" % port)
        init_tables(refresh)
        authentication_key = init_authentication_key(refresh)
        logger.debug(u"authentication_key is '%s'" % authentication_key)
        run(host='localhost', port=port, quiet=True, debug=False, server=adapter)
    except socket.error as e:
        traceback.print_exc(file=open(EXCEPTION_LOG_PATH, 'a'))
        if "already in use" in str(e):
            logger.error(u"端口[{}]早已被占用,请检查".format(port))
    except ImportError:
        traceback.print_exc(file=open(EXCEPTION_LOG_PATH, 'a'))
        error_message = u"系统找不到适配器'{}',你可以尝试执行'sudo apt-get install python-{}'或'sudo pip install {}'".format(adapter, adapter, adapter)
        logger.error(error_message)
