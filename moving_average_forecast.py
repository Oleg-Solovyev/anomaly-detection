#!/usr/bin/env python


"""moving_average_forecast.py: forecast with moving average

calculates temperature cutoff that is mean of max and min temperature
calculates time intervals when temperature crosses the cutoff
calculates mean of time interval value
calculates Linux time increment for output
calculates forecast as average of temp values at every mean time interval

> python3 moving_average_forecast.py CELSI-raw-data-reports.csv
"""


__author__ = "Oleg Solovyev"
__email__  = "oleg.s.solovyev@gmail.com"
__status__ = "Prototype"


import sys
import datetime
import pandas as pd


# get input arguments or use testing values
if len(sys.argv) == 1:
    import_data_file      = '4peeks-short.csv' # test file
else:
    import_data_file      = sys.argv[1]                                    # file from command line


# import data
df = pd.read_csv(import_data_file)
print(str(datetime.datetime.now()) + ' imported file ' + import_data_file)


# calculates temperature cutoff that is mean of max and min temperature.
temp_cutoff = (min(df.Temperature) + max(df.Temperature))/2
print(str(datetime.datetime.now()) + ' temperature cutoff is ' + str(temp_cutoff))


# calculates time intervals when temperature crosses the cutoff
df['spike'] = df.Temperature.apply(lambda x: 1 if x > temp_cutoff else 0)
df['change'] = df['spike'].diff()
df['ind'] = df.index
cutoff_intervals = df[df['change'] == 1]['ind'].diff()
print(str(datetime.datetime.now()) + ' found ' + str(len(cutoff_intervals)) + ' intervals crossing ' + str(temp_cutoff) + ' cutoff')


# calculates mean of time interval value
mean_cutoff_intervals = cutoff_intervals.mean().round()
print(str(datetime.datetime.now()) + ' mean time interval ' + str(mean_cutoff_intervals))


# calculates Linux time increment for output
time_increment = int(df.LinuxTime.diff().mean())
print(str(datetime.datetime.now()) + ' Linux time increment is ' + str(time_increment))

# calculates forecast as average of temp values at every mean time interval
print(str(datetime.datetime.now()) + ' Temperature forecast ')
for i in range(0, 6):
  print(str(int(df.LinuxTime.tail(1) + i*time_increment)) + ',' + str(df.Temperature[range(df.shape[0]%36+i, df.shape[0], 36)].mean()))

