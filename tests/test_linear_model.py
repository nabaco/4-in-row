import pytest
import numpy as np
from models.linear_model import LinearRegressionModel, LogisticRegressionModel
from sklearn.linear_model import LinearRegression as SKLinearRegression
from sklearn.metrics import mean_squared_error

BATCH_SIZE = 1000
ACCEPTABLE_BASIC_ERROR = 1e-10
ACCEPTABLE_GD_ERROR = 1e-3
ACCEPTABLE_BASIC_LOSS = 1e-10
ACCEPTABLE_GD_LOSS = 0.1
ACCEPTABLE_NUMERIC_ERROR = 1e-6


@pytest.mark.parametrize(
    "input_shape, output_shape, epochs, learn_rate, acceptable_r_squared",
    [
        (1, 1, None, None, 1.0),      # basic single dimensional linear regression
        (1, 1, 10000, 0.01, 0.999),   # single dimensional GD
        (32, 1, None, None, 1.0),     # multi input/single channel basic
        (32, 1, 10000, 0.1, 0.999),   # multi input/single channel GD
        (32, 5, None, None, 1.0),     # multi input/multi channel basic
        (32, 5, 10000, 0.1, 0.999)    # multi input/multi channel gd
    ],
    ids=[
        'basic/single_dim',
        'gd/single_dim',
        'basic/multi_in/single_c',
        'gd/multi_in/single_c',
        'basic/multi_in/multi_c',
        'gd/multi_in/multi_c'
    ]
)
def test_linear_regression(input_shape, output_shape, epochs, learn_rate, acceptable_r_squared):
    model = LinearRegressionModel(input_shape, output_shape)
    sk_model = SKLinearRegression()
    X = np.random.rand(BATCH_SIZE, input_shape)
    w, b = np.random.rand(input_shape, output_shape), np.random.rand(output_shape)
    y = X @ w + b
    model.fit(X, y, epochs, learn_rate)
    sk_model.fit(X, y)
    r_squared = sk_model.score(X, model.predict(X))
    assert r_squared >= acceptable_r_squared
    is_gd = epochs is not None and learn_rate is not None
    acceptable_error = ACCEPTABLE_GD_ERROR if is_gd else ACCEPTABLE_BASIC_ERROR
    acceptable_loss = ACCEPTABLE_GD_LOSS if is_gd else ACCEPTABLE_BASIC_LOSS
    y_pred = model.predict(X)
    y_sk_pred = sk_model.predict(X)
    assert abs(y_pred-y).max() < acceptable_error
    assert abs(y_pred - y_sk_pred).max() < acceptable_error
    assert abs(model.loss(y_pred, y) - mean_squared_error(y, y_pred)) < ACCEPTABLE_NUMERIC_ERROR
    assert model.loss(y_pred, y) < acceptable_loss


