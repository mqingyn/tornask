#Tornask

tornask是一个简单的，使用 `tornado PeriodicCallback` 开发的作为离线任务的脚本管理器。

demo:
        
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
		#TaskManager.task_register("func2", task_func, 20)
		#TaskManager.task_register("func3", task_func, 30)
        
        if __name__ == '__main__':
            run_tasks()

* ####TaskManager

	`task_register` : 
		
			task_name: 任务名称
			callback： 任务执行方法
			interval： 间隔时间，秒
			endtime：  任务结束时间，不给定为永远执行。格式：2014-10-31 16:46:00