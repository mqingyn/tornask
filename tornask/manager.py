#!/usr/bin/env python
# -*- coding: utf-8  -*-
# Created by mqingyn on 2015/1/15.
"""
tornado 离线任务管理
"""
import datetime, time
from tornado.options import define, options, parse_command_line
from tornado.log import app_log
from tornado.ioloop import PeriodicCallback, IOLoop

define("tasks", default='', help="tasks name list ,eg:task1,task2,task3")


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


_TASK_POOL = {}


class TaskManager(object):
    @staticmethod
    def task_register(task_name, callback, interval, endtime=None):
        """
        任务注册
        :param task_name: 任务名
        :param callback: 任务执行方法
        :param interval: 间隔时间(单位：second)
        :param interval: 结束时间，当时间超过这个时间后，任务将自动stop
        :return:
        """

        def run_():
            if endtime and time.time() > time.mktime(time.strptime(endtime, "%Y-%m-%d %H:%M:%S")):
                TaskManager.task_stop(task_name)
                app_log.info('PeriodicCallback ==> Stop %s at %s' % (
                    task_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
                return
            else:
                app_log.info('PeriodicCallback ==> Run %s at %s' % (
                    task_name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
                return callback()

        if callable(callback):
            try:
                _TASK_POOL.update(
                    {
                        task_name: {'callback': DiligentPeriodicCallback(run_, 1000 * float(interval))}
                    })
            except Exception, ex:
                app_log.exception(ex)
                pass
        else:
            raise ArgumentError("need a callable func callback. now %s " % (callback,))

    @staticmethod
    def task_start(task_name, ioloop=None):

        task = _TASK_POOL.get(task_name, None)
        if task:
            if ioloop:
                task['callback'].io_loop = ioloop
            task['callback'].start()
            task['callback'].run_once()
        else:
            raise ConfigError("task %s not found." % task_name)

    @staticmethod
    def task_stop(task_name):
        task = _TASK_POOL.get(task_name, None)
        if task:
            task['callback'].stop()
        else:
            raise ConfigError("task %s not found." % task_name)

    @staticmethod
    def start_all(ioloop=None):
        for k, task in _TASK_POOL.keys():
            TaskManager.task_start(k, ioloop)

    @staticmethod
    def stop_all():
        for k, task in _TASK_POOL.keys():
            TaskManager.task_stop(k)


def run_tasks():
    """
    启动定时任务 ,目前未启用
    :return:
    """
    parse_command_line()
    loop = IOLoop.instance()

    t_name = options.tasks
    if t_name:
        t_list = t_name.split(',')
        for t in t_list:
            TaskManager.task_start(t, loop)

        loop.start()
    else:
        print 'task not found.'

