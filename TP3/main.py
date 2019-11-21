from softmaxclassifier import *
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def testOneHot():
    softmax = SoftmaxClassifier()
    softmax.nb_classes = 6  # les classes possibles sont donc 0-5

    y1 = np.array([0, 1, 2, 3, 4, 5])
    y1.shape = (6, 1)
    print('Premier test')
    print(softmax._one_hot(y1))

    y2 = np.array([5, 5, 5, 5])
    y2.shape = (4, 1)
    print('\nDeuxième test')
    print(softmax._one_hot(y2))

    y3 = np.array([0, 0, 0, 0])
    y3.shape = (4, 1)
    print('\nTroisième test')
    print(softmax._one_hot(y3))

    softmax.fit(np.zeros((3, 4)))


def testSol():
    # load dataset
    data, target = load_iris().data, load_iris().target

    # split data in train/test sets
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.33, random_state=42)

    # standardize columns using normal distribution
    # fit on X_train and not on X_test to avoid Data Leakage
    s = StandardScaler()
    X_train = s.fit_transform(X_train)
    X_test = s.transform(X_test)

    cl = SoftmaxClassifier()

    # train on X_train and not on X_test to avoid overfitting
    train_p = cl.fit_predict(X_train, y_train)
    test_p = cl.predict(X_test)

    from sklearn.metrics import precision_recall_fscore_support

    # display precision, recall and f1-score on train/test set
    print("train : " + str(precision_recall_fscore_support(y_train, train_p, average="macro")))
    print("test : " + str(precision_recall_fscore_support(y_test, test_p, average="macro")))


if __name__ == '__main__':
    # testOneHot()
    testSol()
