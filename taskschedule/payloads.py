#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
from __future__ import print_function
import imp
import copy
import traceback
import logging
from __init__ import read_file_to_array
from __init__ import FUZZ_DIC_PATH
from __init__ import FUZZ_API_DIC_PATH
from __init__ import TEMPER_PATH
from __init__ import log
from __init__ import EXCEPTION_LOG_PATH
from __init__ import TemperNotFoundError
from __init__ import LIGHT_MODEL
from __init__ import HEAVY_MODEL


class PayLoads(object):
    single_instance = None
    hook_events = ['alert', 'confirm', 'prompt']
    fuzz_dic_path = FUZZ_DIC_PATH

    @staticmethod
    def get_single_instance():
        if PayLoads.single_instance:
            return PayLoads.single_instance
        PayLoads.single_instance = PayLoads()
        return PayLoads.single_instance

    def __init__(self):
        self.payloads = set()
        self.temper_instances = dict()

    def init_payloads(self, refresh=False):
        if refresh:
            self.payloads = set()
        if not self.payloads:
            temp_payload_list = list()
            for payload in read_file_to_array(PayLoads.fuzz_dic_path):
                for hook_event in PayLoads.hook_events:
                    temp_payload_list.append("{}//".format(payload.replace('alert', hook_event)))
                    temp_payload_list.append("'{}//".format(payload.replace('alert', hook_event)))
                    temp_payload_list.append("'>{}//".format(payload.replace('alert', hook_event)))
                    temp_payload_list.append(">{}//".format(payload.replace('alert', hook_event)))
                    temp_payload_list.append('"{}//'.format(payload.replace('alert', hook_event)))
                    temp_payload_list.append('">{}//'.format(payload.replace('alert', hook_event)))
                    temp_payload_list.append(str(payload.replace('alert', hook_event)).replace("'", "`"))
                    temp_payload_list.append(str(payload.replace('alert', hook_event)).replace("'", "").replace("\"", ""))
            self.payloads = self.payloads|set(temp_payload_list)

    @staticmethod
    def split_payloads(payloads, num):
        wrap_list = []
        count = len(payloads) / num
        remainder = len(payloads) % num
        for i in range(num):
            wrap_list.append(payloads[i * count:count * (i + 1) + remainder] if i == num - 1 else
                             payloads[i * count:count * (i + 1)])
        return wrap_list

    def encode_payload_by_temper_name(self, payload, temper_name, model):
        return self.get_temper_instances_by_name(temper_name).temper(payload, model)

    def get_temper_instances_by_name(self, temper_name):
        try:
            temper_name = temper_name.strip()
            return self.temper_instances[temper_name]
        except KeyError as e:
            raise TemperNotFoundError(e)

    def load_temper_instances(self, temper_names):
        logger = log.get_logger()
        for temper_name in temper_names:
            logger.setLevel(logging.DEBUG)
            logger.debug('check temper {} is existed' .format(temper_name))
            temper_path = "%s%s.py" % (TEMPER_PATH, temper_name)
            temper_instance = None
            try:
                temper_instance = imp.load_source('Temper', temper_path).Temper()
                if temper_instance is not None and not self.temper_instances.has_key(temper_name):
                    self.temper_instances[temper_name] = temper_instance
                logger.setLevel(logging.INFO)
                logger.info('temper {} is existed'.format(temper_name))
            except IOError as e:
                logger.setLevel(logging.ERROR)
                logger.error('temper {} is not existed' .format(temper_name))
                raise TemperNotFoundError(temper_name)

    def encode_payload_single_temper(self, payloads, temper_names, model):
        for temper_name in temper_names:
            for payload in payloads:
                payload = self.encode_payload_by_temper_name(payload, temper_name, model)
                if isinstance(payload, set):
                    self.payloads = copy.deepcopy(self.payloads | payload)
                elif isinstance(payload, str):
                    self.payloads.add(payload)

    def encode_payload_mix_temper(self, payloads, temper_names, model):
        for payload in payloads:
            for temper_name in temper_names:
                payload = self.encode_payload_by_temper_name(payload, temper_name, model)
            if isinstance(payload, set):
                self.payloads = copy.deepcopy(self.payloads | payload)
            elif isinstance(payload, str):
                self.payloads.add(payload)

    def get_payloads(self, temper_names, use_api, model=LIGHT_MODEL):
        if use_api:
            PayLoads.fuzz_dic_path = FUZZ_API_DIC_PATH
        logger = log.get_logger()
        logger.info('loading default paloads')
        self.init_payloads()
        logger.info('loading default paloads success')
        if temper_names:
            temper_names = [temper_name.strip() for temper_name in temper_names.split(",")]
            try:
                logger.setLevel(logging.DEBUG)
                self.load_temper_instances(temper_names)
                temp_payloads = copy.deepcopy(self.payloads)
                # 1.单独编码
                self.encode_payload_single_temper(temp_payloads, temper_names, model)
                # 2.混合编码
                self.encode_payload_mix_temper(temp_payloads, temper_names, model)
            except TemperNotFoundError as e:
                traceback.print_exc(file=open(EXCEPTION_LOG_PATH, 'a'))
                exit()
        logger.setLevel(logging.INFO)
        logger.info("{} payloads loaded".format(len(self.payloads)))
        return self.payloads

if __name__ == "__main__":
    payloads = PayLoads.get_single_instance().get_payloads('addkeywords',)
    for payload in payloads:
        print (payload)