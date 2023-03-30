# import russian-losses.csv
# example:
# date,personnel
# 2022-02-25,2800
# 2022-02-26,4300
# 2022-02-27,4500
# 2022-02-28,5300
# 2022-03-01,5710
# 2022-03-02,5840
# 2022-03-03,9000
# 2022-03-04,9166
# ...

# using XGBoost for regression, predict the personnel losses for the next 365 days

# import libraries
import numpy as np
import pandas as pd
from sklearn.svm import SVR

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

dates = []
personnel = []

# read the csv file with pd
df = pd.read_csv('russian-losses.csv')

# get the dates and personnel losses
dates = df.iloc[:, 0].values
personnel = df.iloc[:, 1].values

# convert the dates to matplotlib dates
dates = [mdates.datestr2num(d) for d in dates]

def predict_personnel(dates, personnel, x):
    # convert the dates to numpy arrays
    dates = np.reshape(dates, (len(dates), 1))

    # create the SVR model
    svr_lin = SVR(kernel='linear', C=1e3)
    svr_poly = SVR(kernel='poly', C=1e3, degree=2)
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)

    # fit the model
    svr_lin.fit(dates, personnel)
    svr_poly.fit(dates, personnel)
    svr_rbf.fit(dates, personnel)

    # predict the next 365 days
    plt.plot(dates, personnel, color='black', label='Data')
    plt.plot(dates, svr_rbf.predict(dates), color='red', label='RBF model')
    plt.plot(dates, svr_lin.predict(dates), color='green', label='Linear model')
    plt.plot(dates, svr_poly.predict(dates), color='blue', label='Polynomial model')
    plt.xlabel('Date')
    plt.ylabel('Personnel')
    plt.title('Support Vector Regression')
    plt.legend()
    plt.show()

    return svr_rbf.predict(x)[0], svr_lin.predict(x)[0], svr_poly.predict(x)[0]
    
predict_personnel(dates, personnel, 29)