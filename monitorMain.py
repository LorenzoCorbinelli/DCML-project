import os.path
import sys
import time
import psutil
import csv
import pandas
import random
from threading import Thread
import Injector
import detector
"""
This is the main file and the only one to execute even if you want to build the training set 
(execute this file with -t or -train argument)
or if you just want to do monitoring (execute this file without any argument)
"""


class Monitor(Thread):
    """
    Class for monitoring
    :param max_obs: maximum number of observations
    :param csv_filename: name of the output file csv (only when train=True)
    :param train: True only for build the training set
    :return: nothing
    """
    def __init__(self, max_obs, csv_filename, train):
        Thread.__init__(self)
        self.max_obs = max_obs
        self.csv_filename = csv_filename
        self.train = train

    def run(self):
        n = 0
        print("Starting monitoring...")
        while n < self.max_obs:
            start_time = time.time_ns()
            data = {"timestamp": round(start_time / 1e+6)}

            # Elements to monitoring
            cpu = CPUMonitor()
            mem = virtualMemoryMonitor()
            disk = diskMonitor()

            data.update(cpu)
            data.update(mem)
            data.update(disk)

            if self.train:  # only for build the training set
                with open(self.csv_filename, "a", newline="") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=data.keys())
                    if n == 0:
                        writer.writeheader()
                    writer.writerow(data)
            else:   # for monitoring: call to the ML algorithm for prediction
                detector.detect(data)

            exec_time = time.time_ns() - start_time
            time.sleep(1 - exec_time / 1e+9)
            n += 1

        # add on csv the label column
        if self.train:      # only for build the training set
            labelColumn(self.csv_filename)
        print("Monitoring ended")


def labelColumn(csv_filename):
    data_frame = pandas.read_csv(csv_filename, sep=',')
    CPU_injection = pandas.read_csv("CPU_injection.csv", sep=',')
    memory_injection = pandas.read_csv("memory_injection.csv", sep=',')
    disk_injection = pandas.read_csv("disk_injection.csv", sep=',')

    label = []
    label_bin = []
    anomaly = False
    for timestamp in data_frame["timestamp"]:
        for i in CPU_injection.index:
            if (CPU_injection["startTime"][i] <= timestamp <= CPU_injection["endTime"][i] or
                    memory_injection["startTime"][i] <= timestamp <= memory_injection["endTime"][i] or
                    disk_injection["startTime"][i] <= timestamp <= disk_injection["endTime"][i]):
                label.append("anomaly")  # during the injection -> anomaly
                label_bin.append(1)
                anomaly = True
                break
        if not anomaly:
            label.append("normal")     # normal
            label_bin.append(0)
        else:
            anomaly = False

    data_frame["label"] = label
    data_frame["label_bin"] = label_bin
    data_frame.to_csv(csv_filename, index=False)


def CPUMonitor():
    data = psutil.cpu_times_percent(interval=0.1, percpu=False)._asdict()
    indicators = ["user", "system"]     # indicators that I'm interested in monitoring
    return filterIndicators(data, indicators)


def virtualMemoryMonitor():
    data = psutil.virtual_memory()._asdict()
    indicators = ["total", "available", "percent", "used", "free"]  # indicators that I'm interested in monitoring
    return filterIndicators(data, indicators)


def diskMonitor():
    data = psutil.disk_io_counters()._asdict()
    # indicators that I'm interested in monitoring
    indicators = ["read_count", "write_count", "read_bytes", "write_bytes", "read_time", "write_time"]
    return filterIndicators(data, indicators)


def filterIndicators(data, indicators):
    # Return only the indicators that I want to monitor
    return {key: data[key] for key in indicators}


def removeCsvFiles():
    if os.path.exists("CPU_injection.csv"):
        os.remove("CPU_injection.csv")
    if os.path.exists("memory_injection.csv"):
        os.remove("memory_injection.csv")
    if os.path.exists("disk_injection.csv"):
        os.remove("disk_injection.csv")


if __name__ == "__main__":
    removeCsvFiles()
    injections = [Injector.CPUStress, Injector.MemoryStress, Injector.DiskStress]
    if len(sys.argv) > 1:   # training
        if sys.argv[1] not in ["-t", "-train"]:
            sys.exit("Acceptable arguments: -t or -train")
        if os.path.exists("dataset.csv"):
            os.remove("dataset.csv")
        threadMonitor = Monitor(1000, "dataset.csv", True)
        threadMonitor.start()
        time.sleep(30)
        for i in range(10):
            random.shuffle(injections)
            for inj in injections:
                thread = inj(3000)
                thread.start()
                thread.join()
                time.sleep(20)
            time.sleep(15)
    else:   # detect
        detector.loadModel()
        threadMonitor = Monitor(50, "", False)
        threadMonitor.start()
        time.sleep(5)
        for i in range(2):
            random.shuffle(injections)
            for inj in injections:
                thread = inj(3000)
                thread.start()
                thread.join()
                time.sleep(2)
        # add the right label for check if the ml algorithm works fine
        threadMonitor.join()
        labelColumn("detector.csv")
