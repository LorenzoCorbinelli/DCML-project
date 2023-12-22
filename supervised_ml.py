import pandas
import sklearn.metrics
from sklearn import tree
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, StackingClassifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from Injector import current_ms
import pickle

if __name__ == "__main__":
    data_frame = pandas.read_csv("dataset.csv", sep=',')

    label = data_frame["label"]
    features = data_frame.drop(columns=["timestamp", "label"])

    feat_train, feat_test, lab_train, lab_test = train_test_split(features, label, test_size=0.5, shuffle=False)

    classifiers = [VotingClassifier(estimators=[('lda', LinearDiscriminantAnalysis()),
                                                ('nb', GaussianNB()),
                                                ('dt', tree.DecisionTreeClassifier())]),
                   StackingClassifier(estimators=[('lda', LinearDiscriminantAnalysis()),
                                                  ('nb', GaussianNB()),
                                                  ('dt', tree.DecisionTreeClassifier())],
                                      final_estimator=RandomForestClassifier(n_estimators=10)),
                   tree.DecisionTreeClassifier(), GaussianNB(),
                   LinearDiscriminantAnalysis(), KNeighborsClassifier(n_neighbors=3), KNeighborsClassifier(n_neighbors=20),
                   RandomForestClassifier(n_estimators=20), RandomForestClassifier(n_estimators=10),
                   RandomForestClassifier(n_estimators=3)]

    for cl in classifiers:
        start_train = current_ms()
        cl = cl.fit(feat_train, lab_train)
        end_train = current_ms()

        predicted_labels = cl.predict(feat_test)
        end_time = current_ms()

        accuracy = sklearn.metrics.accuracy_score(lab_test, predicted_labels)
        print("Accuracy is %.4f, train time: %d, test time: %d" % (accuracy, end_train - start_train, end_time - end_train))

    # selected algorithm:
    start_train = current_ms()
    cl = RandomForestClassifier(n_estimators=3).fit(feat_train, lab_train)
    end_train = current_ms()

    predicted_labels = cl.predict(feat_test)
    end_time = current_ms()

    accuracy = sklearn.metrics.accuracy_score(lab_test, predicted_labels)
    print("Accuracy is %.4f, train time: %d, test time: %d" % (accuracy, end_train - start_train, end_time - end_train))
    # save the model
    with open("model.pkl", "wb") as file:
        pickle.dump(cl, file)
