import os.path
import time
import psutil
import csv


def monitor(max_obs, csv_filename):
    '''
    Function for monitoring
    :param max_obs: maximum number of observations
    :param csv_filename: name of the output file csv
    :return: nothing
    '''

    if os.path.exists(csv_filename):
        os.remove(csv_filename)
    n = 0
    while n < max_obs:
        start_time = time.time_ns()
        data = {}

        # Elements to monitoring
        cpu = CPUMonitor()
        mem = virtualMemoryMonitor()
        disk = diskMonitor()

        data.update(cpu)
        data.update(mem)
        data.update(disk)
        with open(csv_filename, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data.keys())
            if n == 0:
                writer.writeheader()
            writer.writerow(data)
        print(round(start_time / 1e+6), data)
        exec_time = time.time_ns() - start_time
        time.sleep(1 - exec_time / 1e+9)
        n += 1


def CPUMonitor():
    return psutil.cpu_times_percent(interval=0.1, percpu=False)._asdict()


def virtualMemoryMonitor():
    return psutil.virtual_memory()._asdict()


def diskMonitor():
    return psutil.disk_io_counters()._asdict()


if __name__ == "__main__":
    monitor(15, "data.csv")
