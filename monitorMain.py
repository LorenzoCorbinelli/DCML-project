import time
import psutil

# dict_test = {"user": "Lorenzo", "pass": "dcml"}
# cpu_t_p = psutil.cpu_times_percent(interval=1, percpu=False)._asdict()
# disk_usage = psutil.disk_usage('/')._asdict()
# cpu_t_p.update(disk_usage)

n = 10
while n > 0:
    start_time = time.time_ns()
    mem = psutil.virtual_memory()._asdict()
    exec_time = time.time_ns() - start_time
    time.sleep(1 - exec_time * pow(10,-9))
    print(mem)
    n -= 1
