import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates
import datetime as dt
import glob
import os

# NOTE
# Make sure that the values in the csv file are number-like!
#   Measurements should be like "0.4", and NOT "0,4"

#IF YOU HAVE MULTIPLE FILES...
#GET THE CSVs LIKE THIS:
# path = r"C:\Users\Alexandra\Documents\WatchPlant\DataToPlot\weather"
# all_files = glob.glob(os.path.join(path, "*.csv"))

# files_list = []

# for filename in all_files:
#     temp = pd.read_csv(filename, index_col=None, header=0)
#     files_list.append(temp)
#     print(filename)

# combine all the files into one big file
# df = pd.concat(files_list, axis=0)

#For only reading 1 file
df = pd.read_csv('newgoogle-2024-07.csv', index_col=None, header=0)

#get rid of all empty rows
df.dropna(how='all', inplace=True)

#correct the time columns from 24:00:00 to 23:59:00 (24:00:00 is not valid datetime)
df = df.replace("24:00:00", "23:59:59")

#connect the time and date columns
df['Station:'] =df['Station:'] + " " + df['Unnamed: 1']
df.drop(columns='Unnamed: 1', inplace=True)

#get rid of extra columns (only keep the measurement ones)
numrows = len(df.index)-3
df.dropna(axis='columns', thresh=numrows, inplace=True)
df.dropna(axis='index', how='any', inplace=True)
df.drop(labels=5, axis=0, inplace=True)
df = df.reset_index(drop=True)

#convert the first column to datetime
df['Station:'] = pd.to_datetime(df['Station:'], format="%d.%m.%Y %H:%M:%S")

#rename all columns to their correct values
df.rename(columns={"Station:":"Timestamp", "DLx Met":"Wind speed", "DLx Met.1":"Wind direction",
    "DLx Met.2":"Air temperature", "DLx Met.3":"Relative humidity", "DLx Met.4":"Solar irradiance",
    "DLx Met.5":"Precipitation", "DLx Met.6":"Dew point temperature"}, inplace=True)

#convert all the columns into correct data type
df['Wind speed'] = df['Wind speed'].astype(float)               # m/s
df['Wind direction'] = df['Wind direction'].astype(int)         # degrees
df['Air temperature'] = df['Air temperature'].astype(float)     # degrees Celcius
df['Relative humidity'] = df['Relative humidity'].astype(float) # %
df['Solar irradiance'] = df['Solar irradiance'].astype(float)   # W/m^2 (Watts per meter^2)
df['Precipitation'] = df['Precipitation'].astype(float)         # mm
df['Dew point temperature'] = df['Dew point temperature'].astype(float) # degrees Celcius
#Note: the last value (Verdunstung Haude/Evaporation) has almost no data, so not included
#print(df.types)

#create a dataframe that only has the measurement columns
df = df[['Timestamp','Wind speed','Wind direction','Relative humidity','Solar irradiance',
    'Precipitation','Air temperature','Dew point temperature']]

print(df.head())

timecol = 'Timestamp'
#ycol0 = 'Wind speed'            # m/s
#ycol1 = 'Wind direction'        # degrees
#ycol2 = 'Relative humidity'     # %
#ycol3 = 'Solar irradiance'      # W/m^2
#ycol4 = 'Precipitation'         # mm
#ycol5 = 'Air temperature'       # degrees Celcius
#ycol6 = 'Dew point temperature' # degrees Celcius

print("working...")

#~~~ WIP ~~~
# do not plot data that has "ungültig" (not valid)
# how to plot only from a certain timeframe?

ax = df.plot(x=timecol, subplots=True, kind="line", figsize=(10,6))
#label the units for each subplot
ax[0].set_ylabel('m/s')
ax[1].set_ylabel('°')
ax[2].set_ylabel('%')
ax[3].set_ylabel('W/m²')
ax[4].set_ylabel('mm')
ax[5].set_ylabel('°C')
ax[6].set_ylabel('°C')

# auto formate the timestamps to be readable
plt.gcf().autofmt_xdate()

print("done")
plt.show()