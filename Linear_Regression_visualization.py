from models.linear_model import LogisticRegressionModel
import matplotlib.pyplot as plt
import numpy as np

# Data
x = list(range(1,11))       # x data [1, 2, ... , 9, 10]
y = [0,0,0,0,1,0,1,0,1,1]   # y data [0, 0, ... , 1,  1]

X = np.array([x]).T         # Convert x data to column vector X
Y = np.array([y]).T         # Convert y data to column vector Y


# Logistic Regression Model
logistic_reg = LogisticRegressionModel(1) # Create Logistic Regression Model with 1 input argument
logistic_reg.fit(X, Y, 10000, 0.1) # Train Model by data
theta0, theta1 = logistic_reg.weights # Get the weights
y_p = logistic_reg.predict(X)


# Print results
print(f"Theta 0: {theta0[0]}, Theta 1: {theta1[0]}")
print("True Values")
print(Y)
print("Prediction Value")
print(logistic_reg.predict(X))

# Plot the data
plt.scatter(x, y, label="True points") # True points


sigmoid_fn = logistic_reg.sigmoid_fn(theta0 + theta1 * x)
plt.plot(x, sigmoid_fn, label="Probability") # Probability Sigmoid Function

decision = -theta0[0] / theta1[0]
plt.plot([decision, decision], [0, 1], color='r', linestyle='-', linewidth=2, label="Decision Boundary") # Decision Boundary


plt.legend()
plt.show()