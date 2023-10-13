import csv
import os
import time
from multiprocessing import Pool, cpu_count


def current_ms():
    return round(time.time() * 1000)


def CPUStress(csv_filename):
    '''
    Function for stress the CPU
    :return:
    '''
    if os.path.exists(csv_filename):
        os.remove(csv_filename)
    print("Starting injection")
    start_time = current_ms()
    pool = Pool(cpu_count())
    pool.map_async(stress_cpu, range(cpu_count()))
    time.sleep((1000 - (current_ms() - start_time)) / 1000.0)
    if pool is not None:
        pool.terminate()
    csvData = {"startTime": start_time, "endTime": current_ms()}
    print("Injection ended")
    with open(csv_filename, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvData.keys())
        writer.writeheader()
        writer.writerow(csvData)


def stress_cpu(x: int = 1234):
    while True:
        x * x


if __name__ == "__main__":
    CPUStress("CPU_injection.csv")
