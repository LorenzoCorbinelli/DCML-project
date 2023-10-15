import csv
import os
import time
from multiprocessing import Pool, cpu_count


def current_ms():
    return round(time.time_ns() / 1e+6)


def CPUStress(csv_filename):
    '''
    Function for stress the CPU
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
    csvData = {"startTime": start_time, "endTime": current_ms()}
    print("Injection CPU ended")
    with open(csv_filename, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvData.keys())
        writer.writeheader()
        writer.writerow(csvData)


def stress_cpu(x: int = 1234):
    while True:
        x * x


def memoryStress(csv_filename):
    '''
    Function for stress the memory
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

    csvData = {"startTime": start_time, "endTime": current_ms()}
    print("Injection memory ended")
    with open(csv_filename, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvData.keys())
        writer.writeheader()
        writer.writerow(csvData)


if __name__ == "__main__":
    CPUStress("CPU_injection.csv")
    memoryStress("memory_injection.csv")
