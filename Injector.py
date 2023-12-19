import csv
import os
import tempfile
import time
from multiprocessing import Pool, cpu_count
from threading import Thread


def current_ms():
    return round(time.time_ns() / 1e+6)


def csv_writer(csv_filename, start_time):
    csvData = {"startTime": start_time, "endTime": current_ms()}
    with open(csv_filename, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvData.keys())
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
        if os.path.exists(self.csv_filename):
            os.remove(self.csv_filename)
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
        if os.path.exists(self.csv_filename):
            os.remove(self.csv_filename)
        print("Starting injection memory")
        start_time = current_ms()
        list = []
        while True:
            list.append([99999 for i in range(0, 123456789)])
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
        if os.path.exists(self.csv_filename):
            os.remove(self.csv_filename)
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
    block_to_write = 'x' * 1048576
    n_blocks = 300
    while True:
        filehandle = tempfile.TemporaryFile(dir='./')
        for _ in range(n_blocks):
            filehandle.write(block_to_write)
        filehandle.seek(0)
        for _ in range(n_blocks):
            content = filehandle.read(1048576)
        filehandle.close()
        del content
        del filehandle
