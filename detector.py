import pickle
import pandas
import os

writeHeader = True

def loadModel():
    global model
    if os.path.exists("detector.csv"):
        os.remove("detector.csv")
    with open("model.pkl", "rb") as file:
        model = pickle.load(file)


def detect(data):
    global writeHeader
    data_frame = pandas.DataFrame(data, index=[0])
    features = data_frame.drop(columns=["timestamp"])
    predicted_label = model.predict(features)
    data_frame["prediction"] = predicted_label
    data_frame.to_csv("detector.csv", mode="a", index=False, header=writeHeader)
    writeHeader = False
