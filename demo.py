#!/usr/bin/env python
# -*- coding: utf-8  -*-
# Created by mqingyn on 2015/1/15.
import time
from datetime import datetime
from tornask.manager import taskmgr, run_tasks
from tornado.concurrent import run_on_executor
from tornado.netutil import ThreadedResolver, IOLoop
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import coroutine


class Task(object):
    def __init__(self):
        self.executor = ThreadedResolver().executor
        self.io_loop = IOLoop.current()

    @run_on_executor
    def task_interval(self):
        print 'start at', datetime.now()
        time.sleep(3)
        print 'end at', datetime.now()

    @coroutine
    def task_callat(self):
        response = yield AsyncHTTPClient().fetch("http://www.baidu.com")
        print response.body


if __name__ == '__main__':
    tasks = Task()
    taskmgr.task_register("task_at", tasks.task_interval, interval=1)
    taskmgr.task_register("task_callat", tasks.task_callat, call_at=("23:25", "23:35"))
    run_tasks()
