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
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

from sklearn.metrics import mean_squared_error

import seaborn as sns

plt.style.use('fivethirtyeight')
color_pal = sns.color_palette()

# import XGBoost
import xgboost as xgb



# read data from CSV
df = pd.read_csv("russian-losses.csv")

# convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# set the date column as the index
df = df.set_index("date")

# train test split
traintestoffset = 45
train = df.iloc[:-traintestoffset]
test = df.iloc[-traintestoffset:]

# features
features = ["personnel"]

reg = xgb.XGBRegressor(n_estimators=1000, 
                      early_stopping_rounds=50)
                      # learning_rate=0.05) 

target = 'personnel'

X_train = train[features]
Y_train = train[target]

X_test = test[features]
Y_test = test[target]

reg.fit(X_train, Y_train, 
        eval_set=[(X_train, Y_train), (X_test, Y_test)],
        verbose=100)
        
# forecast on test
test['prediction'] = reg.predict(X_test)

df = df.merge(test[['prediction']], how='left', left_index=True, right_index=True)
ax = df[['personnel']].plot(figsize=(16, 9))
df[['prediction']].plot(ax=ax)
plt.legend(['Truth', 'Prediction'])
ax.set_title("Russian Personnel Losses")
plt.show()

# # plot
# fig, ax = plt.subplots(figsize=(16, 9))
# train.plot(ax=ax, label="Train")
# test.plot(ax=ax, label="Test")
# ax.axvline(test.index[0], color="black", linestyle="--")
# ax.legend(['Train', 'Test', 'Prediction', 'Test Start'])
# plt.show()