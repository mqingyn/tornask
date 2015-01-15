#!/usr/bin/env python
# -*- coding: utf-8  -*-
# Created by mqingyn on 2015/1/15.


from tornask.manager import TaskManager, run_tasks
import time


def task_func():
    """
    任务执行方法，可以是异步方法。
    :return:
    """
    print time.time()

# 注册任务
TaskManager.task_register("func", task_func, 10)

if __name__ == '__main__':
    run_tasks()