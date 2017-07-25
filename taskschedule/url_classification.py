#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
import urllib
from __init__ import start_with
from __init__ import end_with
from __init__ import HTTP_POST_METHOD
from __init__ import HTTP_GET_METHOD


class UrlClassification(object):
    result_urls = {}
    DIGITAL = (1, 'bsmali4_int')
    LETTER = (2, 'bsmali4_str')
    DIGMIXEDLETER = (3, 'bsmali4_mix')
    OTHER = (4, 'bsmali4_other')
    FLOAT = (5, 'bsmali4_float')

    @staticmethod
    def get_parameter(url, http_method=HTTP_GET_METHOD):
        result = {}
        try:
            if http_method == HTTP_GET_METHOD:
                temp_keys_value = re.findall(u'\?((?:\w*=[\'\.\-\w\u4e00-\u9fa5]*&?)*)', url.decode('utf-8'), re.S)[0].\
                    encode('utf-8')
            elif http_method == HTTP_POST_METHOD:
                temp_keys_value = re.findall(u'\?*((?:\w*=[\'\.\-\w\u4e00-\u9fa5]*&?)*)', url.decode('utf-8'), re.S)[0].encode('utf-8')
            if len(temp_keys_value):
                keys = re.findall(r'(\w{1,})=', temp_keys_value, re.S)
                for key in keys:
                    regular = u'{}=([\w\.\'\-\u4e00-\u9fa5]*)'.format(key)
                    value = re.findall(regular, temp_keys_value.decode('utf-8'))[0].encode('utf-8')
                    result[key] = value
        except IndexError, e:
            pass
        return result

    @staticmethod
    def check_type(value):
        if sum([n.isdigit() for n in value.strip().split('.')]) == 2:
            return UrlClassification.FLOAT[0]
        if value.isdigit():
            return UrlClassification.DIGITAL[0]
        elif value.isalpha():
            return UrlClassification.LETTER[0]
        elif value.isalnum():
            return UrlClassification.DIGMIXEDLETER[0]
        else:
            return UrlClassification.OTHER[0]

    @staticmethod
    def surround_with_single_quote(value):
        if start_with(value, "'") and end_with(value, "'"):
            return True, value[1:-1]
        else:
            return False, value

    @staticmethod
    def remove_same(url, http_method=HTTP_GET_METHOD):
        result = {}
        http_parameter = UrlClassification.get_parameter(url, http_method)
        for key, value in http_parameter.items():
            # 判断value的类型，如果字段是submit,就不做处理
            temp_value = value
            is_surround_with_single_quote, value = UrlClassification.surround_with_single_quote(value)
            value_type = UrlClassification.check_type(urllib.quote(value))
            if value_type == UrlClassification.DIGITAL[0]:
                value = UrlClassification.remove_int_same(value)
            elif value_type == UrlClassification.LETTER[0]:
                value = UrlClassification.remove_str_same(value)
            elif value_type == UrlClassification.DIGMIXEDLETER[0]:
                value = UrlClassification.remove_mix_same(value)
            elif value_type == UrlClassification.FLOAT[0]:
                value = UrlClassification.remove_float_same(value)
            else:
                value = UrlClassification.remove_other_same(value)
            if is_surround_with_single_quote:
                value = "'{}'".format(value)
            if key == "submit":
                result[key] = temp_value
            else:
                result[key] = value
        return result

    # 统计最后的结果
    @staticmethod
    def simplify_url(url, http_method=HTTP_GET_METHOD):
        result_urls = {}
        result_parameter = ''
        result_urls_key = None
        have_parameter = False
        for key, value in UrlClassification.remove_same(url, http_method).items():
            result_parameter += "{}={}&".format(key, value)
            have_parameter = True
        # 对有无参数进行判断
        if have_parameter:
            if http_method == HTTP_GET_METHOD:
                result_parameter = "?" + result_parameter[:-1]
                result_urls_key = re.subn(u'\?((?:\w*=[\'\.\-\w\-\u4e00-\u9fa5]*&?)*)', result_parameter, url.decode('utf-8'))[0]
            elif http_method == HTTP_POST_METHOD:
                result_parameter = result_parameter[:-1]
                result_urls_key = re.subn(u'\?*((?:\w*=[\'\.\-\w\-\u4e00-\u9fa5]*&?)*)', result_parameter, url.decode('utf-8'))[0]
            if not result_urls.has_key(result_urls_key):
                result_urls[result_urls_key] = url
        return result_urls_key if result_urls_key else url

    @staticmethod
    def remove_int_same(value):
        return UrlClassification.DIGITAL[1]

    @staticmethod
    def remove_str_same(value):
        return UrlClassification.LETTER[1]

    @staticmethod
    def remove_mix_same(value):
        return UrlClassification.DIGMIXEDLETER[1]

    @staticmethod
    def remove_other_same(value):
        return UrlClassification.OTHER[1]

    @staticmethod
    def remove_float_same(value):
        return UrlClassification.FLOAT[1]