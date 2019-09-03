import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from models.linear_model import LinearRegressionModel
from datasets import import_dataset


DATES = ['Date']
PRICES = ['Price (All)', 'Price (New)', 'Price (Modern)', 'Price (Older)']
INPUT_FEATURES = 1
OUTPUT_FEATURES = 4


def date2years(date):
    """Convert date str to float number of years"""
    data = datetime.strptime(date, '%Y-%m-%d')
    return data.year + (data.month - 1)/12


# Import the dates and prices data from 'hose_prices_data.csv' file
data = pd.read_csv('house_prices_data.csv', index_col=0,
                   usecols=(DATES + PRICES))

# Clean missing data
data = data[data > 0]
data = data.dropna()

# Create datasets X and Y
x = [date2years(date) for date in data.index]
X2 = np.array([[date, date**2] for date in x])
Y = data.loc[:, PRICES].to_numpy()

# Create LinearRegression model and training by given data
linear_reg = LinearRegressionModel(INPUT_FEATURES, OUTPUT_FEATURES)
linear_reg.fit(X2, Y)

# Predict the dataset X by our model
Y_predict = linear_reg.predict(X2)
prediction = pd.DataFrame(Y_predict, index=data.index, columns=PRICES)

# Plot the prices and the pur prediction
fig, plots = plt.subplots(2, 2, figsize=(7, 5))
plots_list = plots.ravel().tolist()

for i in range(OUTPUT_FEATURES):
    plots_list[i].plot(x, Y[:,i], label = PRICES[i])
    plots_list[i].plot(x, Y_predict[:,i], label = "Prediction")
    plots_list[i].legend()
    plots_list[i].set_xlabel("Year")
    plots_list[i].set_ylabel("Price")

plt.show()


# Print the original data, prediction and the loss
print("The original data:")
print(data)
print("--------------------")
print("The prediction data:")
print(prediction)
print("--------------------")
print(f"Loss: {linear_reg.loss(Y_predict, Y)}")
