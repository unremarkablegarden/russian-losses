# import russian-losses.csv, then use the data to create a timeseries forecast
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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

# import linear regression model
from sklearn.linear_model import LinearRegression


# read data from CSV
df = pd.read_csv("russian-losses.csv")

# convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

df2 = df.copy()

# remove the first 60 rows
df2 = df2.iloc[60:]

# first date
first_date = df2["date"].iloc[0]

# last date
last_date = df2["date"].iloc[-1]

# create a linear regression model
model = LinearRegression()

# fit the model
model.fit(df2["date"].values.reshape(-1, 1), df2["personnel"])

# create a new dataframe with the dates we want to predict, starting from the last date in the dataset
df2 = pd.DataFrame({"date": pd.date_range(start=last_date, periods=365)})
df2["date"] = pd.to_datetime(df2["date"])

# # predict the personnel losses
# df2["personnel"] = model.predict(df2["date"].values.reshape(-1, 1))

# # add the new data to the original dataframe
# df = pd.concat([df, df2])

# # create a new column with the forecast
# df["forecast"] = df["personnel"].shift(-365)


# plot the data
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df["date"], df["personnel"], label="Actual")
# ax.plot(df["date"], df["forecast"], label="Forecast")
# ax.plot(df2["date"], df2["personnel"], label="2")

ax.set_xlabel("Date")
ax.set_ylabel("Personnel")
ax.set_title("Russian personnel losses in Ukraine war (GPT-3 projection)")
ax.legend()
plt.show()
