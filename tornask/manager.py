#!/usr/bin/env python
# -*- coding: utf-8  -*-
# Created by mqingyn on 2015/1/15.
"""
tornado task manager
"""
import datetime, time, functools
from tornado.options import define, options, parse_command_line
from tornado.log import app_log
from tornado.ioloop import PeriodicCallback, IOLoop

define("tasks", default=None, help="tasks name list ,eg:task1,task2,task3")
define("startrun", default=True, type=bool, help="immediately run task when start.")


class ArgumentError(Exception):
    """Arguments error"""


class ConfigError(Exception):
    """Arguments error"""


class DiligentPeriodicCallback(PeriodicCallback):
    def run_once(self):
        if not self._running:
            return
        try:
            self.io_loop.call_later(2, self.callback)
        except Exception, ex:
            app_log.error(ex)
            self.io_loop.handle_callback_exception(self.callback)


class TaskManager(object):
    def __init__(self):
        self._task_pool = {}

    def task_register(self, task_name, callback, interval=1, call_at=(), endtime=None):
        """
        任务注册
        :param task_name: 任务名
        :param callback: 任务执行方法
        :param interval: 间隔时间(单位：分钟)
        :param call_at: 每日周期性定时调用时间，如：(8:00,14:00,18:00)
        :param endtime: 结束日期，格式：2015-01-01 12:12:12
        :return:
        """
        print("task register: %s" % task_name)
        if callable(callback):
            try:
                call = functools.partial(self._run, task_name, callback, call_at, endtime)
                self._task_pool.update(
                    {
                        task_name: DiligentPeriodicCallback(call, 1000 * 60 * float(interval))
                    })
            except Exception, ex:
                app_log.exception(ex)
        else:
            raise ArgumentError("%s not a function. " % (callback,))

    def _run(self, task_name, callback, call_at, endtime):
        now = datetime.datetime.now()
        if endtime and time.time() > time.mktime(time.strptime(endtime, "%Y-%m-%d %H:%M:%S")):
            app_log.info('Stop task %s at %s' % (
                task_name, now,))
            self.task_stop(task_name)
            return
        else:
            app_log.info('Run task %s at %s' % (
                task_name, now,))
            if call_at:
                task = self._task_pool[task_name]
                call_list = []
                for dtstr in call_at:
                    dt = datetime.datetime.strptime(dtstr, "%H:%M")
                    run_dt = datetime.datetime(now.year, now.month, now.day, dt.hour, dt.minute, dt.second)
                    call_list.append(run_dt)
                    call_list.append(run_dt + datetime.timedelta(1))

                call_list.sort()

                for c in call_list:
                    if c >= now:
                        task.stop()
                        task.callback_time = (c - now).total_seconds() * 1000
                        task.start()
                        break

            return callback()

    def task_start(self, task_name, ioloop=None):

        task = self._task_pool.get(task_name, None)
        if task:
            if ioloop:
                task.io_loop = ioloop
            task.start()
            if options.startrun:
                task.run_once()
        else:
            raise ConfigError("task %s not found." % task_name)

    def task_stop(self, task_name):
        task = self._task_pool.get(task_name, None)
        if task:
            task.stop()
        else:
            raise ConfigError("task %s not found." % task_name)

    def start_all(self, ioloop=None):
        for k in self._task_pool.keys():
            self.task_start(k, ioloop)

    def stop_all(self):
        for k in self._task_pool.keys():
            self.task_stop(k)


taskmgr = TaskManager()


def run_tasks():
    """
    start tasks
    :return:
    """
    parse_command_line()
    loop = IOLoop.instance()

    t_name = options.tasks
    if t_name:
        t_list = t_name.split(',')
        for t in t_list:
            taskmgr.task_start(t, loop)
    else:
        taskmgr.start_all(loop)

    loop.start()
