#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""

import sys
import re
import urllib
from __init__ import HTTP_POST_METHOD
from __init__ import HTTP_GET_METHOD
try:
    reload  # Python 2
except NameError:
    from importlib import reload  # Python 3

reload(sys)
sys.setdefaultencoding('utf8')


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
            if len(temp_keys_value) > 0:
                keys = re.findall(r'(\w{1,})=', temp_keys_value, re.S)
                for key in keys:
                    regular = u'{}=([\w\.\'\-\u4e00-\u9fa5]*)'.format(key)
                    value = re.findall(regular, temp_keys_value.decode('utf-8'))[0].encode('utf-8')
                    result[key] = value
        except IndexError, e:
            pass
        return result

    @staticmethod
    def check_is_contain_asterisk(url):
        return True if "*" in url else False

    @staticmethod
    def simplify_url_with_asterisk(url):
        values = re.findall(u'([\w\w\u4e00-\u9fa5]+[*])', url.decode('utf-8'), re.S)
        for value in values:
            url = url.replace("*", UrlClassification.replace_parameter(value))
        return url

    @staticmethod
    def simplify_url_without_asterisk(url, http_method):
        result_parameter = ''
        result_urls_key = None
        have_parameter = False
        for key, value in UrlClassification.remove_same(url, http_method).items():
            result_parameter += "{}={}&".format(key, value)
            have_parameter = True
        if have_parameter:
            if http_method == HTTP_GET_METHOD:
                result_parameter = "?{}".format(result_parameter[:-1])
                result_urls_key = re.subn(u'\?((?:\w*=[\'\.\-\w\-\u4e00-\u9fa5]*&?)*)', result_parameter, url.decode('utf-8'))[0]
            elif http_method == HTTP_POST_METHOD:
                result_parameter = result_parameter[:-1]
                result_urls_key = re.subn(u'\?*((?:\w*=[\'\.\-\w\u4e00-\u9fa5]*&?)*)', result_parameter, url.decode('utf-8'))[0]
        return result_urls_key if result_urls_key is not None else url

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
        if str(value).startswith("'") and str(value).endswith("'"):
            return True, value[1:-1]
        else:
            return False, value

    @staticmethod
    def remove_same(url, http_method=HTTP_GET_METHOD):
        result = {}
        http_parameter = UrlClassification.get_parameter(url, http_method)
        for key, value in http_parameter.items():
            result[key] = value if key == "submit" else UrlClassification.replace_parameter(value)
        return result

    @staticmethod
    def replace_parameter(value):
        is_surround_with_single_quote, value = UrlClassification.surround_with_single_quote(value)
        value_type = UrlClassification.check_type(urllib.quote(value))
        if value_type == UrlClassification.DIGITAL[0]:
            value = UrlClassification.remove_int_same()
        elif value_type == UrlClassification.LETTER[0]:
            value = UrlClassification.remove_str_same()
        elif value_type == UrlClassification.DIGMIXEDLETER[0]:
            value = UrlClassification.remove_mix_same()
        elif value_type == UrlClassification.FLOAT[0]:
            value = UrlClassification.remove_float_same()
        else:
            value = UrlClassification.remove_other_same()
        if is_surround_with_single_quote:
            value = "'{}'".format(value)
        return value

    @staticmethod
    def simplify_url(url, http_method=HTTP_GET_METHOD):
        if UrlClassification.check_is_contain_asterisk(url):
            return UrlClassification.simplify_url_with_asterisk(url)
        return UrlClassification.simplify_url_without_asterisk(url, http_method)

    @staticmethod
    def remove_int_same():
        return UrlClassification.DIGITAL[1]

    @staticmethod
    def remove_str_same():
        return UrlClassification.LETTER[1]

    @staticmethod
    def remove_mix_same():
        return UrlClassification.DIGMIXEDLETER[1]

    @staticmethod
    def remove_other_same():
        return UrlClassification.OTHER[1]

    @staticmethod
    def remove_float_same():
        return UrlClassification.FLOAT[1]
