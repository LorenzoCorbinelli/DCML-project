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
        cpu_t_p = psutil.cpu_times_percent(interval=0.1, percpu=False)._asdict()
       # mem = psutil.virtual_memory()._asdict()
       # cpu_t_p.update(mem)
        with open(csv_filename, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cpu_t_p.keys())
            if n == 0:
                writer.writeheader()
            writer.writerow(cpu_t_p)
        print(round(time.time() * 1000), cpu_t_p)
        exec_time = time.time_ns() - start_time
        time.sleep(1 - exec_time / 1e+9)
        n += 1


if __name__ == "__main__":
    monitor(20, "data.csv")
