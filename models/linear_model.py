from .model_base import Model
import numpy as np

class LinearRegressionModel(Model):
    """
    A model for Linear Regression.
    Arguments:
        input_features (int)
        output_features (int)
    """

    def __init__(self, input_features, output_features):
        self.input_features = input_features
        self.output_features = output_features
        self.weights = np.zeros((input_features + 1, output_features))

    @staticmethod
    def design_matrix(X):
        """Take dataset X and return the design-matrix (dm_X)"""
        return np.c_[np.ones(X.shape[0]), X]

    def predict(self, X):
        """Predict the output after training by given dataset X"""
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
        dm_X = self.design_matrix(X)

        # 'Gradient Descent' method if learn_rate and epochs was given
        if learn_rate and epochs:
            for _ in range(epochs): # Calculate the new weights by vectorization approach
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
    TODO - Implement!
    """

    def predict(self, X):
        pass

    def fit(self, X, y, epochs=None):
        pass

    def loss(self, y_prediction, y_true):
        """ Cross entropy loss i.e. logistic loss."""
        return -np.mean(y_true * np.log(y_prediction) + (1-y_true) * np.log(1-y_prediction))
