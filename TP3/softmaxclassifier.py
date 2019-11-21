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

    def add_bias(self, X):
        return np.hstack((np.ones((np.size(X, 0), 1)), X))

    def fit(self, X, y=None):
        prev_loss = np.inf
        self.losses_ = []

        m, n = X.shape
        self.nb_feature = n
        k = np.max(y) + 1
        self.nb_classes = k
        y = self._one_hot(y)


        X_bias = self.add_bias(X)
        self.theta_ = np.random.rand(n+1, k)

        for epoch in range(self.n_epochs):

            logits = X_bias @ self.theta_
            probabilities = self._softmax(logits)

            loss = self._cost_function(probabilities, y)
            self.theta_ = self.theta_ - self.lr*self._get_gradient(X_bias, y, probabilities)

            if self.early_stopping:
                if prev_loss - loss < self.threshold:
                    break
                prev_loss = loss

        return self

    def predict_proba(self, X, y=None):
        try:
            getattr(self, "theta_")
        except AttributeError:
            raise RuntimeError("You must train classifer before predicting data!")
        X_bias = self.add_bias(X)
        z = X_bias @ self.theta_  # TODO: Pas certain que ce soit ce qui est demandé
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
        # return max(np.arange(len(p_x_k)), key=p_x_k.__getitem__)
        return np.argmax(p_x_k, axis=1)

    def fit_predict(self, X, y=None):
        self.fit(X, y)
        return self.predict(X,y)

    def score(self, X, y=None):
        return (self.predict(X, y) == y).sum() / y.shape[0]

    def _cost_function(self, probabilities, y):
        m, K = y.shape
        # Permet de s'assurer que les prob sont comprises entre epsilon et epsilon - 1
        np.clip(probabilities, self.eps, 1 - self.eps)
        return -np.sum(y * np.log(probabilities))/m

    def _one_hot(self, y):
        y_ohe = np.zeros((len(y), self.nb_classes))
        for i in range(len(y)):
            y_ohe[i, y[i]] = 1
        return y_ohe

    def _softmax(self, z, axis=1):
        z_p = z - np.max(z, axis=axis)[:, None]  # Pour la stabilité du softmax (translation-invariant)
        exp = np.exp(z_p)
        return exp / np.sum(exp, axis=axis)[:, None]

    def _get_gradient(self, X_bias, y, probas):
        m, K = y.shape
        return X_bias.T@(probas - y)/m
