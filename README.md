# Anomaly detector for laptop
The goal of this project is to develop an anomaly detector for laptop with the use of machine learning algorithms.

In particular, the software monitors some system indicator (memory, disk and CPU) and with a machine learning algorithm decides if the system is in a normal behaviour or there are some anomalies.

# How to run the program
If you want to build the training set:
```
py monitorMain.py -t
```
or
```
py monitorMain.py -train
```
If you just want to do monitoring:
```
py monitorMain.py
```
At the end in the file `detector.csv` you can see the prediction of the machine learning algorithm.
