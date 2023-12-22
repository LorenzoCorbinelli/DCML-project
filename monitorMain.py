import os.path
import time
import psutil
import csv
import pandas
import random
from threading import Thread
import Injector
import detector


class Monitor(Thread):
    """
    Class for monitoring
    :param max_obs: maximum number of observations
    :param csv_filename: name of the output file csv
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
            else:
                detector.detect(data)

            exec_time = time.time_ns() - start_time
            time.sleep(1 - exec_time / 1e+9)
            n += 1

        # add on csv the label column
        if self.train:      # only for build the training set
            labelColumn()
        print("Monitoring ended")


def labelColumn():
    data_frame = pandas.read_csv("dataset.csv", sep=',')
    CPU_injection = pandas.read_csv("CPU_injection.csv", sep=',')
    memory_injection = pandas.read_csv("memory_injection.csv", sep=',')
    disk_injection = pandas.read_csv("disk_injection.csv", sep=',')

    label = []
    anomaly = False
    for timestamp in data_frame["timestamp"]:
        for i in CPU_injection.index:
            if (CPU_injection["startTime"][i] <= timestamp <= CPU_injection["endTime"][i] or
                    memory_injection["startTime"][i] <= timestamp <= memory_injection["endTime"][i] or
                    disk_injection["startTime"][i] <= timestamp <= disk_injection["endTime"][i]):
                label.append(1)  # during the injection -> anomaly
                anomaly = True
                break
        if not anomaly:
            label.append(0)     # normal
        else:
            anomaly = False

    data_frame["label"] = label
    data_frame.to_csv("dataset.csv", index=False)


def CPUMonitor():
    return psutil.cpu_times_percent(interval=0.1, percpu=False)._asdict()


def virtualMemoryMonitor():
    return psutil.virtual_memory()._asdict()


def diskMonitor():
    return psutil.disk_io_counters()._asdict()


def removeCsvFiles():
    if os.path.exists("CPU_injection.csv"):
        os.remove("CPU_injection.csv")
    if os.path.exists("memory_injection.csv"):
        os.remove("memory_injection.csv")
    if os.path.exists("disk_injection.csv"):
        os.remove("disk_injection.csv")


if __name__ == "__main__":
    removeCsvFiles()
    train = False
    injections = [Injector.CPUStress, Injector.MemoryStress, Injector.DiskStress]
    if train:   # training
        if os.path.exists("dataset.csv"):
            os.remove("dataset.csv")
        threadMonitor = Monitor(500, "dataset.csv", train)
        threadMonitor.start()
        time.sleep(15)
        for i in range(8):
            random.shuffle(injections)
            for inj in injections:
                thread = inj(3000)
                thread.start()
                thread.join()
                time.sleep(5)
            time.sleep(8)
    else:   # detect
        detector.loadModel()
        threadMonitor = Monitor(50, "", train)
        threadMonitor.start()
        time.sleep(5)
        for i in range(2):
            random.shuffle(injections)
            for inj in injections:
                thread = inj(3000)
                thread.start()
                thread.join()
                time.sleep(2)
