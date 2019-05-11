from .model_base import Model
import numpy as np


class LinearRegressionModel(Model):
    """
    A model for Linear Regression.
    TODO - Implement!
    """
    def predict(self, X):
        pass

    def fit(self, X, y, epochs=None):
        pass

    def loss(self, y_prediction, y_true):
        """ Mean Squared Error (MSE) loss."""
        return np.mean((y_prediction - y_true)**2)


class LogisticRegressionModel(Model):
    """
    A model for Logistic Regression i.e. classification.
    TODO - Implement!
    """
    def predict(self, X):
        pass

    def fit(self, X, y, epochs=None):
        pass

    def loss(self, y_prediction, y_true):
        """ Cross entropy loss i.e. logistic loss."""
        return -np.mean(y_true * np.log(y_prediction) + (1-y_true) * np.log(1-y_prediction))
