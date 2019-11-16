from softmaxclassifier import *


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


if __name__ == '__main__':
    testOneHot()
