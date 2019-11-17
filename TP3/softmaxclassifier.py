from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np


class SoftmaxClassifier(BaseEstimator, ClassifierMixin):

    def __init__(self, lr=0.1, alpha=100, n_epochs=1000, eps=1.0e-5, threshold=1.0e-10, early_stopping=True):

        self.lr = lr
        self.alpha = alpha
        self.n_epochs = n_epochs
        self.eps = eps
        self.threshold = threshold
        self.early_stopping = early_stopping
        self.nb_classes = 0
        self.theta_ = None

    """
        In:
        X : l'ensemble d'exemple de taille nb_example x nb_features
        y : l'ensemble d'étiquette de taille nb_example x 1

        Principe:
        Initialiser la matrice de poids
        Ajouter une colonne de bias à X
        Pour chaque epoch
            calculer les probabilités
            calculer le log loss
            calculer le gradient
            mettre à jouer les poids
            sauvegarder le loss
            tester pour early stopping

        Out:
        self, in sklearn the fit method returns the object itself
    """

    def fit(self, X, y=None):
        prev_loss = np.inf
        self.losses_ = []

        m, n = X.shape
        # k = np.max(y)  # TODO: Comment instancier le nombre de classes?
        k = 6

        self.nb_feature = n
        self.nb_classes = k

        bias_column = np.ones((m, 1))  # colonne est remplie de 1
        X_bias = np.hstack((bias_column, X))
        self.theta_ = np.random.rand(n, k)

        for epoch in range(self.n_epochs):

            # logits =
            # probabilities =

            # loss =
            # self.theta_ =

            if self.early_stopping:
                pass

        return self

    def predict_proba(self, X, y=None):
        try:
            getattr(self, "theta_")
        except AttributeError:
            raise RuntimeError("You must train classifer before predicting data!")
        X_bias = np.hstack((np.ones((np.size(X, 0), 1)), X))
        z = X*self.theta_  # TODO: Pas certain que ce soit ce qui est demandé
        # Retourne les probabilités associées à chaque classe pour chacune des instances à prédire
        return self._softmax(z)

    def predict(self, X, y=None):
        try:
            getattr(self, "theta_")
        except AttributeError:
            raise RuntimeError("You must train classifer before predicting data!")
        # Probabilités des différentes classes
        p_x_k = self.predict_proba(X, y)
        # Retourne l'indice (classe) avec la plus grande probabilité pour chacunes des intances à prédire.
        return max(np.arange(len(p_x_k)), key=p_x_k.__getitem__)

    def fit_predict(self, X, y=None):
        self.fit(X, y)
        return self.predict(X,y)

    def score(self, X, y=None):
        pass

    def _cost_function(self, probabilities, y):
        pass

    def _one_hot(self, y):
        y_ohe = np.zeros((len(y), self.nb_classes))
        i = 0
        for x_i in y:
            y_ohe[i, x_i] = 1
            i += 1
        return y_ohe

    def _softmax(self, z):
        return np.exp(z) / np.sum(np.exp(z))

    def _get_gradient(self, X_bias, y, probas):
        pass
