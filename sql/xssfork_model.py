#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
import traceback
import sqlite3
import config
from field import Field
from field import IntegerField
from field import StringField
from __init__ import EXCEPTION_LOG_PATH
from __init__ import XssforkTaskError
from __init__ import XssforkTaskSaveError
from __init__ import XssforkTaskFindError


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == "XssforkModel":
            return type.__new__(cls, name, bases, attrs)
        mappings = dict()
        for key, value in attrs.iteritems():
            if isinstance(value, Field):
                mappings[key] = value
        for k in mappings.iterkeys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings
        return type.__new__(cls, name, bases, attrs)


class XssforkModel(dict):
    __metaclass__ = ModelMetaclass

    def __init__(self, **kwargs):
        super(XssforkModel, self).__init__(**kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            return None

    def __setattr__(self, key, value):
        self[key] = value

    def set_option(self, option, value):
        self[option] = value

    def save(self):
        fields = list()
        args = list()
        for key, value in self.__mappings__.iteritems():
            column_name = value.name
            column_value = getattr(self, key)
            if column_value is not None:
                fields.append(column_name)
                if isinstance(value, StringField):
                    args.append("'%s'" % column_value)
                elif isinstance(value, IntegerField):
                    args.append(column_value)
        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(self.__table__, ', '.join(fields), ', '.join(args))
        if self.__show_sql__:
            print sql
        try:
            config.execute(sql)
        except XssforkTaskError as e:
            raise XssforkTaskSaveError(e)

    def find(self):
        results = None
        args = list()
        for key, value in self.__mappings__.iteritems():
            column_name = value.name
            column_value = getattr(self, key)
            if column_value is not None:
                if isinstance(value, StringField):
                    column_value = "'{}'".format(column_value)
                elif isinstance(value, IntegerField):
                    column_value = column_value
                args.append("{}={}".format(column_name, column_value))
        sql = "SELECT * FROM {}".format(self.__table__,) if len(args) == 0 else \
            "SELECT * FROM {} WHERE {}".format(self.__table__, " AND ".join(args))
        if self.__show_sql__:
            print sql
        try:
            results = config.execute(sql)
        except XssforkTaskError as e:
            raise XssforkTaskFindError(e)
        return results

    def remove(self):
        args = list()
        for key, value in self.__mappings__.iteritems():
            column_name = value.name
            column_value = getattr(self, key)
            if column_value is not None:
                if isinstance(value, StringField):
                    column_value = "'{}'".format(column_value)
                elif isinstance(value, IntegerField):
                    column_value = column_value
                args.append("{}={}".format(column_name, column_value))
        if len(args) > 0:
            sql = "DELETE FROM {} WHERE {}".format(self.__table__, " AND ".join(args))
            if self.__show_sql__:
                print sql
            config.execute(sql)

    def change(self, **kwargs):
        args = list()
        data = list()
        for key, value in kwargs.iteritems():
            if isinstance(value, int):
                data.append("{}={}".format(key, value))
            elif isinstance(value, str):
                data.append("{}='{}'".format(key, value))

        for key, value in self.__mappings__.iteritems():
            column_name = value.name
            column_value = getattr(self, key)
            if column_value is not None:
                if isinstance(value, StringField):
                    column_value = "'{}'".format(column_value)
                elif isinstance(value, IntegerField):
                    column_value = column_value
                args.append("{}={}".format(column_name, column_value))
        if len(args) > 0 and len(data) > 0:
            sql = "UPDATE {} SET {} WHERE {}".format(self.__table__, ",".join(data), " AND ".join(args))
            if self.__show_sql__:
                print sql
            config.execute(sql)

    def find_lastest_id(self):
        result = None
        sql = "SELECT last_insert_rowid() FROM {}".format(self.__table__)
        if self.__show_sql__:
            print sql
        try:
            result = config.execute(sql)[0][0]
        except XssforkTaskError as e:
            raise XssforkTaskFindError(e)
        return str(result)

    def find_all(self):
        result = None
        sql = "SELECT * FROM {}".format(self.__table__)
        if self.__show_sql__:
            print sql
        try:
            result = config.execute(sql)
        except XssforkTaskError as e:
            raise XssforkTaskFindError(e)
        return result


