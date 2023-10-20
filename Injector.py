import csv
import os
import tempfile
import time
from multiprocessing import Pool, cpu_count


def current_ms():
    return round(time.time_ns() / 1e+6)


def csv_writer(csv_filename, start_time):
    csvData = {"startTime": start_time, "endTime": current_ms()}
    with open(csv_filename, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvData.keys())
        writer.writeheader()
        writer.writerow(csvData)

def CPUStress(csv_filename):
    '''
    Function for stress the CPU
    :param csv_filename: name of the csv file
    :return:
    '''
    if os.path.exists(csv_filename):
        os.remove(csv_filename)
    print("Starting injection CPU")
    start_time = current_ms()
    pool = Pool(cpu_count())
    pool.map_async(stress_cpu, range(cpu_count()))
    time.sleep((3000 - (current_ms() - start_time)) / 1000.0)
    if pool is not None:
        pool.terminate()

    print("Injection CPU ended")
    csv_writer(csv_filename, start_time)


def stress_cpu(x: int = 1234):
    while True:
        x * x


def memoryStress(csv_filename):
    '''
    Function for stress the memory
    :param csv_filename: name of the csv file
    :return:
    '''
    if os.path.exists(csv_filename):
        os.remove(csv_filename)
    print("Starting injection memory")
    start_time = current_ms()
    list = []
    while True:
        list.append([999 for i in range(0, 12345678)])
        if current_ms() - start_time > 3000:
            break
        else:
            time.sleep(0.001)

    print("Injection memory ended")
    csv_writer(csv_filename, start_time)


def diskStress(csv_filename):
    '''
    Function for stress the disk
    :param csv_filename: name of the csv file
    :return:
    '''
    workers = 10
    if os.path.exists(csv_filename):
        os.remove(csv_filename)
    print("Starting injection disk")
    start_time = current_ms()
    list_pool = []
    pool = Pool(workers)
    pool.map_async(stress_disk, range(workers))
    list_pool.append(pool)
    time.sleep((3000 - (current_ms() - start_time)) / 1000.0)
    if list_pool is not None:
        for pool_disk in list_pool:
            pool_disk.terminate()

    print("Injection disk ended")
    csv_writer(csv_filename, start_time)


def stress_disk():
    block_to_write = 'x' * 1048576
    n_blocks = 50
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


if __name__ == "__main__":
    CPUStress("CPU_injection.csv")
    time.sleep(2)
    memoryStress("memory_injection.csv")
    time.sleep(2)
    diskStress("disk_injection.csv")
