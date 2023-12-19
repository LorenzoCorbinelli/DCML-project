import os.path
import time
import psutil
import csv
import pandas


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
        data = {"timestamp": round(start_time / 1e+6)}

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
        print(data)
        exec_time = time.time_ns() - start_time
        time.sleep(1 - exec_time / 1e+9)
        n += 1

    # add on csv the label column
    data_frame = pandas.read_csv("data.csv", sep=',')
    CPU_injection = pandas.read_csv("CPU_injection.csv", sep=',')
    memory_injection = pandas.read_csv("memory_injection.csv", sep=',')
    disk_injection = pandas.read_csv("disk_injection.csv", sep=',')

    label = []
    for timestamp in data_frame["timestamp"]:
        if (CPU_injection["startTime"][0] <= timestamp <= CPU_injection["endTime"][0] or
                memory_injection["startTime"][0] <= timestamp <= memory_injection["endTime"][0] or
                disk_injection["startTime"][0] <= timestamp <= disk_injection["endTime"][0]):
            label.append(1)  # during the injection -> anomaly
        else:
            label.append(0)  # normal

    data_frame["label"] = label
    data_frame.to_csv("data.csv", index=False)


def CPUMonitor():
    return psutil.cpu_times_percent(interval=0.1, percpu=False)._asdict()


def virtualMemoryMonitor():
    return psutil.virtual_memory()._asdict()


def diskMonitor():
    return psutil.disk_io_counters()._asdict()


if __name__ == "__main__":
    monitor(20, "data.csv")
