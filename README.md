#Tornask

tornask是一个简单的，使用 `tornado PeriodicCallback` 开发的作为离线任务的脚本管理器。

demo:
        

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


执行： `python demo.py --tasks=task_at,task_callat`  

* ####安装
    pip: `pip install tornask`

* ####TaskManager

	`task_register` : 
		
			task_name: 任务名称
			 callback: 任务执行方法
			 interval: 间隔时间，秒
			  call_at: tuple，每日在指定时间触发,格式：("23:25", "23:35")
			  endtime: 任务结束时间，不给定为永远执行。格式：2014-10-31 16:46:00
