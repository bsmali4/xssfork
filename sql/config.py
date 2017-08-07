#! /usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2017 xssfork developers (http://xssfork.codersec.net/)
See the file 'doc/COPYING' for copying permission
"""
import traceback
import sqlite3
from __init__ import XSS_FORK_DB
from __init__ import EXCEPTION_LOG_PATH
from __init__ import XssforkTaskSaveError
from __init__ import XssforkTaskFindError
from __init__ import XssforkTaskError


TASK_NOT_START = 0  # 未开始
TASK_WORKKING = 1  # 工作中
TASK_DONE = 2  # 工作完成


CONNECTION = None


def get_connection(refresh=False):
    global CONNECTION
    if refresh:
        CONNECTION = None
    if CONNECTION is None:
        CONNECTION = sqlite3.connect(XSS_FORK_DB)
    return CONNECTION


def execute(sql):
    results = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if sql.lower().strip().startswith("select"):
            results = cursor.execute(sql).fetchall()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
    except (sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
        traceback.print_exc(file=open(EXCEPTION_LOG_PATH, 'a'))
        raise XssforkTaskError(e)
    return results


def init_tables(refresh=False):
    if refresh:
        open(XSS_FORK_DB, 'w')
    conn = sqlite3.connect(XSS_FORK_DB)
    cursor = conn.cursor()
    sql = '''CREATE TABLE "xssfork_task" (
            "id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL DEFAULT 1,
            "time"  TEXT,
            "url"  TEXT,
            "cookie"  TEXT,
            "data"  TEXT,
            "destination"  TEXT,
            "status"  INTEGER DEFAULT 0,
            "payload"  TEXT
            );
    '''
    try:
        execute(sql)
    except XssforkTaskError:
        traceback.print_exc(file=open(EXCEPTION_LOG_PATH, 'a'))

if __name__ == "__main__":
    init_tables(True)
