class Model:
    """
    Base class for all machine learning models.
    """
    def __repr__(self):
        """
        Returns a pretty representation of the model.
        Note:
             DO NOT OVERRIDE THIS. You may override `extra_repr` instead.
        """
        return '%s(%s)' % (self.__class__.__name__, self.extra_repr())

    def extra_repr(self):
        return ''

    def predict(self, X):
        """
        Returns the model prediction fot the data X.
        """
        raise NotImplementedError

    def fit(self, X, y, epochs=None):
        """
        Trains the model on the given data X and ground-truth labels y.
        """
        raise NotImplementedError

    def loss(self, y_prediction, y_true):
        """
        Returns the loss defined for the model/data.
        """
        raise NotImplementedError
