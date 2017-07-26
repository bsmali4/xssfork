#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
from __future__ import print_function
import copy
import imp
import requests
import logging
import Queue
import traceback
import threading
from __init__ import log
from __init__ import FUZZ_DIC_PATH
from __init__ import get_phantomjs_path
from __init__ import read_file_to_array
from __init__ import TEMPER_PATH
from __init__ import MAX_THREAD_NUM
from __init__ import MAX_LEVEL
from __init__ import EXCEPTION_LOG_PATH
from payloads import PayLoads
from task_thread import FuzzTask
from task_thread import CompletePacket
from abstract_observer import AbstractObserver
from xss_vulnerability import XssVulnerability


class TaskSchedule(AbstractObserver):
    def __init__(self, url, destination, level, cookie, data, tempers, model):
        self._payloads_queue = Queue.Queue()
        self._fuzz_threads = list()
        self._canceled = False
        self._model = model
        self._tempers = tempers
        self._thread_num = TaskSchedule.get_thread_num_by_level(int(level))
        self._complete_packet = CompletePacket(url=url, destination=destination, cookie=cookie, data=data)
        XssVulnerability.add_observer(self)

    def notify(self, xss_status, xss_payloads):
        if xss_status is False:
            logger = log.get_logger()
            logger.setLevel(logging.WARNING)
            logger.warning("[!] xssfork can not find XSS Vulnerability")

    def main(self):
        if self._complete_packet.url is not None:
            self.check_complete_packet_is_alive()
            payloads = PayLoads.get_single_instance().get_payloads(self._tempers, self._model)
            self.create_thread(len(payloads))
            self.add_payloads_queue(payloads)
            try:
                self.monitor_exit(len(payloads))
                self._payloads_queue.join()
                #self.monitor_exit()
                XssVulnerability.notif_all(self.kill_threads)
            except KeyboardInterrupt:
                self._canceled = True
                XssVulnerability.notif_all(self.kill_threads)

    def monitor_exit(self, payloads_len):
        while True:
            alive = False
            stop = False
            for fuzz_thread in self._fuzz_threads:
                alive = alive or fuzz_thread.isAlive()
                stop = stop or fuzz_thread._stop
            if not alive or stop or FuzzTask.working_num >= payloads_len:
                break

    def create_thread(self, payloads_num):
        for _ in range(self._thread_num):
            fuzz_thread = FuzzTask(self._complete_packet, self._payloads_queue, self.kill_threads, payloads_num)
            self._fuzz_threads.append(fuzz_thread)
            XssVulnerability.add_observer(fuzz_thread)
            fuzz_thread.start()

    def check_complete_packet_is_alive(self):
        self.check_complete_url_is_alive()
        self.check_complete_destination_is_alive()

    def check_complete_url_is_alive(self):
        logger = log.get_logger()
        logger.setLevel(logging.DEBUG)
        logger.debug("checking if url is available")
        if TaskSchedule.check_url_is_alive(self._complete_packet.url, self._complete_packet.cookie, self._complete_packet.data):
            logger.setLevel(logging.INFO)
            logger.info("url connection success ")
        else:
            logger.setLevel(logging.ERROR)
            logger.error("url connection fail, please check your input ")
            exit()

    def check_complete_destination_is_alive(self):
        logger = log.get_logger()
        logger.setLevel(logging.DEBUG)
        logger.debug("checking if destination is available")
        if TaskSchedule.check_url_is_alive(self._complete_packet.destination, self._complete_packet.cookie, self._complete_packet.data):
            logger.setLevel(logging.INFO)
            logger.info("destination connection success ")
        else:
            logger.setLevel(logging.ERROR)
            logger.error("destination connection fail, please check your input ")
            exit()

    def kill_threads(self):
        for fuzz_thread in self._fuzz_threads:
            fuzz_thread._stop = True
            fuzz_thread.kill_sub_process()

    def add_payloads_queue(self, payloads):
        for payload in payloads:
            self._payloads_queue.put(payload)

    @staticmethod
    def check_url_is_alive(url, cookie, data=None):
        result = True
        fail_status_codes = [404, 500]
        if url:
            headers = {'Cookie': ''} if cookie is None else {'Cookie': cookie}
            try:
                req = requests.get(url, headers=headers, timeout=5) if data is None else requests.post(url, data=data,
                                                                                                       headers=headers,
                                                                                                       timeout=5)
                result = False if req.status_code in fail_status_codes else True
            except Exception as e:
                traceback.print_exc(file=open(EXCEPTION_LOG_PATH, 'a'))
                result = False
        return result

    @staticmethod
    def get_thread_num_by_level(level):
        return (MAX_THREAD_NUM/MAX_LEVEL)*level

if __name__ == "__main__":
    for pay in PayLoads.get_single_instance().get_payloads(None):
        print(pay)
