import csv
import tempfile
import time
import os
from multiprocessing import Pool, cpu_count
from threading import Thread

"""
This file is used for inject some anomalies during monitoring.
It's used in the monitorMain.py file
"""


def current_ms():
    return round(time.time_ns() / 1e+6)


def csv_writer(csv_filename, start_time):
    csvData = {"startTime": start_time, "endTime": current_ms()}
    header = False
    if not os.path.exists(csv_filename):
        header = True
    with open(csv_filename, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvData.keys())
        if header:
            writer.writeheader()
        writer.writerow(csvData)


class CPUStress (Thread):
    """
    Class for stress the CPU
    :param duration: duration of the injection
    :return:
    """
    def __init__(self, duration):
        Thread.__init__(self)
        self.csv_filename = "CPU_injection.csv"
        self.duration = duration

    def run(self):
        print("Starting injection CPU")
        start_time = current_ms()
        pool = Pool(cpu_count())
        pool.map_async(stress_cpu, range(cpu_count()))
        time.sleep((self.duration - (current_ms() - start_time)) / 1000.0)
        if pool is not None:
            pool.terminate()

        print("Injection CPU ended")
        csv_writer(self.csv_filename, start_time)


def stress_cpu(x: int = 1234):
    while True:
        x * x


class MemoryStress(Thread):
    """
    Class for stress the memory
    :param duration: duration of the injection
    :return:
    """
    def __init__(self, duration):
        Thread.__init__(self)
        self.csv_filename = "memory_injection.csv"
        self.duration = duration

    def run(self):
        print("Starting injection memory")
        start_time = current_ms()
        list = []
        while True:
            list.append([555555 for i in range(0, 123456789)])
            if current_ms() - start_time > self.duration:
                break
            else:
                time.sleep(0.001)

        print("Injection memory ended")
        csv_writer(self.csv_filename, start_time)


class DiskStress(Thread):
    """
    Class for stress the disk
    :param duration: duration of the injection
    :return:
    """
    def __init__(self, duration):
        Thread.__init__(self)
        self.csv_filename = "disk_injection.csv"
        self.duration = duration

    def run(self):
        workers = 10
        print("Starting injection disk")
        start_time = current_ms()
        list_pool = []
        pool = Pool(workers)
        pool.map_async(stress_disk, range(workers))
        list_pool.append(pool)
        time.sleep((self.duration - (current_ms() - start_time)) / 1000.0)
        if list_pool is not None:
            for pool_disk in list_pool:
                pool_disk.terminate()

        print("Injection disk ended")
        csv_writer(self.csv_filename, start_time)


def stress_disk():
    block_to_write = 'x' * 1234567
    n_blocks = 500
    while True:
        filehandle = tempfile.TemporaryFile(dir='./')
        for _ in range(n_blocks):
            filehandle.write(block_to_write)
        filehandle.seek(0)
        for _ in range(n_blocks):
            content = filehandle.read(1234567)
        filehandle.close()
        del content
        del filehandle
