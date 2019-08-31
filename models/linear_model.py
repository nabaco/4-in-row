from .model_base import Model
import numpy as np


class LinearRegressionModel(Model):
    """
    A model for Linear Regression.
    Arguments:
        input_features (int)
        output_features (int)
        normalize (bool)
    """

    def __init__(self, input_features, output_features, normalize=False):
        self.input_features = input_features
        self.output_features = output_features
        self.weights = np.zeros((input_features + 1, output_features))
        self.normalize = normalize
        if normalize:
            self.std = np.zeros(input_features)
            self.mean = np.zeros(input_features)

    @staticmethod
    def design_matrix(X):
        """Take dataset X and return the design-matrix (dm_X)"""
        return np.c_[np.ones(X.shape[0]), X]

    def normalize_matrix(self, X, fit):
        """Take dataset X and return the normalize matrix"""
        if fit:
            self.mean = X.mean(axis=0)
            self.std = X.std(axis=0)
            if 0 in self.std:
                raise ValueError(
                    'The variance of the data is 0, meaning prediction has no meaning.')

        return (X - self.mean) / self.std

    def predict(self, X):
        """Predict the output after training by given dataset X"""
        if self.normalize:
            return self.design_matrix(self.normalize_matrix(X, False)) @ self.weights

        # Predict without normalization
        return self.design_matrix(X) @ self.weights

    def fit(self, X, Y, epochs=None, learn_rate=None):
        """
        Training the model by dataset X and the true values of Y.
        Arguments:
            X (np.ndarray): Dataset.
            Y (np.ndarray): True values.
            Arguments for 'Gradient Descent' method:
                epochs (int): Num of iteration on GD function.
                learn_rate (float): The rate of the learning of the model.
        """
        if self.normalize:  # Normalize the matrix
            dm_X = self.design_matrix(self.normalize_matrix(X, True))
        else:
            dm_X = self.design_matrix(X)

        # 'Gradient Descent' method if learn_rate and epochs was given
        if learn_rate and epochs:
            for _ in range(epochs):  # Calculate the new weights by vectorization approach
                self.weights -= (learn_rate /
                                 Y.shape[0]) * dm_X.T @ (dm_X @ self.weights - Y)

        # 'Normal equation' method if learn_rate or epochs wasn't given
        else:
            self.weights = np.linalg.inv(dm_X.T @ dm_X) @ dm_X.T @ Y

    def loss(self, Y_prediction, Y_true):
        """ Mean Squared Error (MSE) loss.

                      1
        MSE(Y, Y') = --- sum(i=0,N) ||y_i - y_i'||^2
                     2N

        Where ||x|| is the L2 norm of a vector 'x' of dimension C,
        y_i, y_i' are i-th samples from the batches Y, Y' respectively.
        This simplifies to:

                      1
        MSE(Y, Y') = --- sum(i=0,N) sum(k=1,C) (y[i,k] - y'[i,k])^2
                     2N
        """
        batch_size = Y_true.shape[0]
        return 1 / (2*batch_size) * np.sum((Y_true - Y_prediction)**2)


class LogisticRegressionModel(Model):
    """
    A model for Logistic Regression i.e. classification.
    Arguments:
        input_features (int)
        normalize (bool)
    """

    def __init__(self, input_features, normalize=False):
        self.input_features = input_features
        self.weights = np.zeros((input_features + 1, 1))
        self.normalize = normalize
        if normalize:
            self.std = np.zeros(input_features)
            self.mean = np.zeros(input_features)

    @staticmethod
    def design_matrix(X):
        """Take dataset X and return the design-matrix (dm_X)"""
        return np.c_[np.ones(X.shape[0]), X]

    @staticmethod
    def sigmoid_fn(z):
        """Calculate the Sigmoid-function of an array or a scalar"""
        return 1/(1+np.exp(-z))

    def normalize_matrix(self, X, fit):
        """Take dataset X and return the normalize matrix"""
        if fit:
            self.mean = X.mean(axis=0)
            self.std = X.std(axis=0)
            if 0 in self.std:
                raise ValueError(
                    'The variance of the data is 0, meaning prediction has no meaning.')

        return (X - self.mean) / self.std

    def predict(self, X, prob=False):
        """
        Predict the output after training by given dataset X
        Arguments:
            X (np.ndarray): dataset.
            prob (bool):
                True - return the probability of each case to be true (1).
                False - return the prediction of each case 1 or 0.
        """
        if self.normalize:  # Normalize the matrix
            dm_X = self.design_matrix(self.normalize_matrix(X, False))
        else:
            dm_X = self.design_matrix(X)

        # Calculate the probability of each case to be True (1)
        prob_matrix = self.sigmoid_fn(dm_X @ self.weights)
        # Return 1 if probability > 0.5 else 0
        return prob_matrix if prob else np.round(prob_matrix)

    def fit(self, X, y, epochs=None, learn_rate=None):
        """
        Training the model by dataset X and the true values of y.
        Arguments:
            X (np.ndarray): Dataset.
            Y (np.ndarray): True values.
            epochs (int): Num of iteration on GD function.
            learn_rate (float): The rate of the learning of the model.
        """
        if self.normalize:  # Normalize the matrix
            dm_X = self.design_matrix(self.normalize_matrix(X, True))
        else:
            dm_X = self.design_matrix(X)

        # 'Gradient Descent' method
        if learn_rate and epochs:
            for _ in range(epochs):  # Calculate the new weights by vectorization approach
                self.weights -= (learn_rate /
                                 y.shape[0]) * dm_X.T @ (self.sigmoid_fn(dm_X @ self.weights) - y)

    def loss(self, y_prediction, y_true):
        """ Cross entropy loss i.e. logistic loss."""
        return -np.mean(y_true * np.log(y_prediction) + (1-y_true) * np.log(1-y_prediction))
