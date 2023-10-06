import psutil

cpu_t_p = psutil.cpu_times_percent(interval=1, percpu=False)._asdict()
disk_usage = psutil.disk_usage('/')._asdict()

cpu_t_p.update(disk_usage)

dict_test = {"user": "Lorenzo", "pass": "dcml"}
