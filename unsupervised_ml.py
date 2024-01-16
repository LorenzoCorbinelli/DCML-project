import pandas
import sklearn.metrics
from pyod.models.abod import ABOD
from pyod.models.copod import COPOD
from pyod.models.hbos import HBOS
from sklearn.model_selection import train_test_split
from Injector import current_ms
"""
This file is used for compare different unsupervised machine learning algorithms
based on the generated training set.
Due to a lower accuracy in respect to supervised ML algorithms there's no a model saving procedure (see supervised_ml.py).
"""

if __name__ == "__main__":
    data_frame = pandas.read_csv("dataset.csv", sep=',')

    label = data_frame["label_bin"]
    features = data_frame.drop(columns=["timestamp", "label", "label_bin"])

    feat_train, feat_test, lab_train, lab_test = train_test_split(features, label, test_size=0.5, shuffle=False)

    classifiers = [HBOS(contamination=0.103), ABOD(contamination=0.103), COPOD(contamination=0.103)]

    for cl in classifiers:
        start_train = current_ms()
        cl = cl.fit(feat_train)
        end_train = current_ms()

        predicted_labels = cl.predict(feat_test)
        end_time = current_ms()

        accuracy = sklearn.metrics.accuracy_score(lab_test, predicted_labels)
        mcc = sklearn.metrics.matthews_corrcoef(lab_test, predicted_labels)
        print("Accuracy: %.4f, train time: %d, test time: %d, MCC: %f" % (accuracy, end_train - start_train, end_time - end_train, mcc))
