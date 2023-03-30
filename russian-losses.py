# import JSON from URL and draw a graph
# format:
# {
#   date: "2022-02-25",
#   day: 2,
#   personnel: 2800,
#   personnel*: "about",
#   POW: 0
# },

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import json
import urllib.request
import datetime

# open the file projection-feb-16.csv
with open("projection-feb-16.csv", "r") as f:
    lines = f.readlines()
    lines = lines[1:]
    projected_dates = []
    projected_personnel = []
    for line in lines:
        line = line.split(",")
        projected_dates.append(datetime.datetime.strptime(line[0], "%Y-%m-%d"))
        projected_personnel.append(int(line[1]))

# open the file russian-losses-mar-29-gpt4
with open("russian-losses-mar-29-gpt4.csv", "r") as f:
    lines = f.readlines()
    lines = lines[1:]
    projected_dates2 = []
    projected_personnel2 = []
    for line in lines:
        line = line.split(",")
        projected_dates2.append(datetime.datetime.strptime(line[0], "%Y-%m-%d"))
        projected_personnel2.append(int(line[1]))

# open the file projection-feb-16-gpt4.csv
with open("projection-feb-16-gpt4.csv", "r") as f:
    lines = f.readlines()
    lines = lines[1:]
    projected_dates3 = []
    projected_personnel3 = []
    for line in lines:
        line = line.split(",")
        projected_dates3.append(datetime.datetime.strptime(line[0], "%Y-%m-%d"))
        projected_personnel3.append(int(line[1]))

# open the file projection-2023.csv
with open("projection-2023.csv", "r") as f:
    lines = f.readlines()
    lines = lines[1:]
    projected_dates_2023 = []
    projected_personnel_2023 = []
    for line in lines:
        line = line.split(",")
        projected_dates_2023.append(datetime.datetime.strptime(line[0], "%Y-%m-%d"))
        projected_personnel_2023.append(int(line[1]))


# get data from URL
url = "https://raw.githubusercontent.com/PetroIvaniuk/2022-Ukraine-Russia-War-Dataset/main/data/russia_losses_personnel.json"

with urllib.request.urlopen(url) as url:
    data = json.loads(url.read().decode())
    
# get data from JSON
real_dates = []
real_personnel = []
for i in range(len(data)):
    real_dates.append(datetime.datetime.strptime(data[i]["date"], "%Y-%m-%d"))
    real_personnel.append(data[i]["personnel"])

# save data to a CSV file
with open("russian-losses.csv", "w") as f:
    f.write("date,personnel\n")
    for i in range(len(real_dates)):
        # remove time from date
        date = real_dates[i].strftime("%Y-%m-%d")
        f.write(f"{date},{real_personnel[i]}\n")

# draw a graph
fig, ax = plt.subplots(figsize=(20, 10))

ax.plot(real_dates, real_personnel, color="red", label="Reported (Ministry of Defence of Ukraine)")
ax.plot(projected_dates, projected_personnel, color="blue", label="Projected from 16/2 (davinci-003)")
# ax.plot(projected_dates3, projected_personnel3, color="orange", label="Projected from 16/2 (GPT-4)")
ax.plot(projected_dates2, projected_personnel2, color="green", label="Projected from 29/3 (GPT-4)")

# ax.plot(projected_dates_2023, projected_personnel_2023, color="green", label="Projected for 2023 of 2022")

ax.set_title("Russian personnel losses in Ukraine war (GPT projections)")
# ax.set_xlabel("Date")
ax.set_ylabel("Personnel")
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
# ax.xaxis.set_minor_locator(mdates.DayLocator())
# ax.xaxis.set_minor_formatter(mdates.DateFormatter("%d"))
ax.xaxis.set_tick_params(which="major", pad=15)
ax.xaxis.set_tick_params(which="minor", pad=5)
ax.yaxis.set_major_locator(ticker.MultipleLocator(10000))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(5000))
ax.yaxis.set_tick_params(which="major", pad=15)
ax.yaxis.set_tick_params(which="minor", pad=5)
ax.grid(which="major", axis="both", linestyle="dashed")
ax.grid(which="minor", axis="both", linestyle="dotted")    

# set a marker for when the Y plot passes 200,000
# ax.axhline(y=200000, color="black", linestyle="dashed", label="200,000")

# set a marker for May 3rd 2023
# ax.axvline(x=datetime.datetime.strptime("2023-05-04", "%Y-%m-%d"), color="black", linestyle="dashed", label="May 4th 2023")

# set a marker for the last date in real_dates
# ax.axvline(x=real_dates[-1], color="pink", linestyle="dotted", label="Last date in real data")
ax.axvline(x=real_dates[-1], color="black", linestyle="dotted", label="Last date in real data")

# set a marker for the first date of projected_dates
# ax.axvline(x=projected_dates[0], color="lightblue", linestyle="dotted", label="First date of projection")
ax.axvline(x=projected_dates[0], color="black", linestyle="dotted", label="First date of projection")

ax.set_facecolor((0.97, 0.97, 0.97))

ax.legend()
plt.show()
