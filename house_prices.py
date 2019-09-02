import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from models.linear_model import LinearRegressionModel
from datetime import datetime


DATES = ['Date']
PRICES = ['Price (All)', 'Price (New)', 'Price (Modern)', 'Price (Older)']


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
linear_reg = LinearRegressionModel(1, 4)
linear_reg.fit(X2, Y)

# Predict the dataset X by our model
Y_predict = linear_reg.predict(X2)
prediction = pd.DataFrame(Y_predict, index=data.index, columns=PRICES)

# Print the result
print(data)
print(prediction)
print(linear_reg.loss(Y_predict, Y))
