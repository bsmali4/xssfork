#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
from __future__ import print_function
import os
import re
import sys
import time
import json
import signal
import logging
import subprocess
import threading
import traceback
from __init__ import log
from __init__ import get_phantomjs_path
from __init__ import FUZZ_SCRIPT_PATH
from __init__ import CompletePacketNotFoundUrl
from __init__ import url_encode
from __init__ import EXCEPTION_LOG_PATH
from __init__ import IS_WIN
from __init__ import XSS_FORK_STDERR_FILE
from __init__ import XSS_FORK_STDOUT_FILE
from __init__ import XssforkTask
from __init__ import hook_list
from __init__ import HTTP_GET_METHOD
from __init__ import HTTP_POST_METHOD
from payloads import PayLoads
from __init__ import EXCEPTION_LOG_PATH
from url_classification import UrlClassification
from abstract_observer import AbstractObserver
from xss_vulnerability import XssVulnerability


class CompletePacket(dict):

    def __init__(self, **kw):
        for eachkw in kw:
            self[eachkw] = kw[eachkw]
        if not self.has_key('url'):
            raise CompletePacketNotFoundUrl()

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            return None

    def __setattr__(self, key, value):
        self[key] = value


class FuzzTask(threading.Thread, AbstractObserver):

    working_num = 0
    working_num_thread_lock = threading.Lock()
    notify_num = 0
    working_num_thread_lock = threading.Lock()

    def __init__(self, complete_packet, payloads_queue, payloads_num):
        super(FuzzTask, self).__init__()
        self._complete_packet = complete_packet
        self._payloads_queue = payloads_queue
        self._stop = False
        self._child_process_list = []
        self.classificat_complete_packet()
        self._payloads_num = payloads_num
        self.daemon = True

    def is_call_xssfork_api(self):
        return True if self._complete_packet.id is not None else False

    def classificat_complete_packet(self):
        url = self._complete_packet.url
        data = self._complete_packet.data
        if self._complete_packet.data is not None:
            self._complete_packet['key_data'] = UrlClassification.simplify_url(data, HTTP_POST_METHOD)
        else:
            self._complete_packet['key_url'] = UrlClassification.simplify_url(url, HTTP_GET_METHOD)

    def __del__(self):
        self.kill_sub_process()

    def replace_url_to_payload(self, payload):
        url_payload = self._complete_packet.key_url if self._complete_packet.key_url is not None else self._complete_packet.url
        url_payload = re.subn(r'bsmali4_(?:int|mix|other|str|float)', payload, url_payload)[0]
        url_payload = url_encode(url_payload)
        return url_payload

    def replace_data_to_payload(self, payload):
        data_payload = url_encode(re.subn(r'bsmali4_(?:int|mix|other|str|float)', payload, self._complete_packet.key_data)[0])
        return data_payload

    def get_cmd(self, payload):
        data_payload = None
        destination_command = None
        url_payload = self.replace_url_to_payload(payload)

        request_command = "{} {} \"{}\"".format(get_phantomjs_path(), FUZZ_SCRIPT_PATH, url_payload)
        request_command = "{} \"{}\"".format(request_command, self._complete_packet.cookie) if self._complete_packet.cookie is not None\
            else "{} \"\"".format(request_command,)
        request_command = "{} \"{}\"".format(request_command, self._complete_packet.ua)
        if self._complete_packet.data:
            # 有post数据
            data_payload = self.replace_data_to_payload(payload)
            request_command = "{} \"{}\"".format(request_command, data_payload)

        if self._complete_packet.destination:
            destination_command = "{} {} \"{}\"".format(get_phantomjs_path(), FUZZ_SCRIPT_PATH, self._complete_packet.destination)
            if self._complete_packet.cookie:
                destination_command = "{} \"{}\"".format(destination_command, self._complete_packet.cookie)

        payload = {'url': url_payload, 'data': data_payload}
        return request_command, payload, destination_command

    def sub_process_open(self, payload):
        child_process = None
        try:
            request_command, url_payload, destination_command = self.get_cmd(payload)
            child_request_process = subprocess.Popen(request_command, bufsize=10000, stdout=subprocess.PIPE,
                                                     stderr=subprocess.PIPE, shell=True, close_fds=IS_WIN)
            self._child_process_list.append(child_request_process)
            if destination_command is not None:
                child_process = subprocess.Popen(destination_command, bufsize=10000, stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE, shell=True, close_fds=IS_WIN)
                self._child_process_list.append(child_process)
            else:
                child_process = child_request_process
        except OSError:
            self.kill_sub_process()

        return child_process, url_payload

    def check_xss(self, payload):
        if self._stop is False:
            try:
                child_process = None
                while child_process is None:
                    child_process, payload_dic = self.sub_process_open(payload)
                response = self.get_exec_result(child_process)
                FuzzTask.print_fuzz_progress(self._payloads_num)
                for hook_string in hook_list:
                    if hook_string in response:
                        XssVulnerability.add_xss_payload(payload_dic)
                        self._stop = True
                        break
            except OSError as e:
                traceback.print_exc(file=open(EXCEPTION_LOG_PATH, 'a'))

    def kill_sub_process(self):
        for temp_child_process in self._child_process_list:
            try:
                temp_child_process.stderr.close()
                temp_child_process.stdout.close()
                temp_child_process.kill()
                self._child_process_list.remove(temp_child_process)
                os.killpg(temp_child_process.pid, signal.SIGTERM)
            except (OSError, IOError) as e:
                pass

    def get_exec_result(self, child_process):
        result = ""
        try:
            result = child_process.stdout.readlines()[0]
        except IndexError as e:
            pass
        return result

    def run(self):
        while True:
            try:
                payload = self._payloads_queue.get()
                self.check_xss(payload)
            except Exception, e:
                traceback.print_exc(file=open(EXCEPTION_LOG_PATH, 'a'))
            finally:
                self._payloads_queue.task_done()

    def notify(self, xss_status, xss_payloads):
        with FuzzTask.working_num_thread_lock:
            FuzzTask.notify_num += 1
            if xss_status is True:
                if FuzzTask.notify_num == 1:
                    logger = log.get_logger()
                    logger.setLevel(logging.CRITICAL)
                    logger.critical("[!] xssfork find XSS Vulnerability")
                try:
                    payload = xss_payloads.pop()
                    print ("---")
                    print ("    Status: Vulnerable")
                    print ("    payload_url: {}".format(payload.get('url')))
                    if payload.get('data') is not None:
                        print ("    payload_data: {}".format(payload.get('data')))
                    print ("---")
                    if self.is_call_xssfork_api():  # 调用api则保存数据到数据
                        xssfork_task = XssforkTask(id=self._complete_packet.id)
                        xssfork_task.change(payload=json.dumps(payload))
                except Exception as e:
                    traceback.print_exc(file=open(EXCEPTION_LOG_PATH, 'a'))

    @staticmethod
    def print_fuzz_progress(total_num):
        with FuzzTask.working_num_thread_lock:
            FuzzTask.working_num += 1
            sys.stdout.write("\r[xssfork] {}/{} payloads injected...\r".format(FuzzTask.working_num, total_num))
            sys.stdout.flush()
