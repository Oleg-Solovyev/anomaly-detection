#!/usr/bin/env python


"""make_model.py: import intervals and marks anomalies.

> python3 test_model.py CELSI-raw-data-reports.csv model_file.csv -10
"""


__author__ = "Oleg Solovyev"
__email__  = "oleg.s.solovyev@gmail.com"
__status__ = "Prototype"


import sys
import datetime
import numpy as np
import pandas as pd


# get input arguments or use testing values
if len(sys.argv) == 1:
    import_data_file      = '/home/q/Downloads/CELSI-raw-data-reports.csv' # test file
    model_file            = 'model_file.csv'
    temperature_threshold = -10
else:
    import_data_file      = sys.argv[1]                                    # file from command line
    model_file            = sys.argv[2]
    temperature_threshold = float(sys.argv[3])


# import data
df = pd.read_csv(import_data_file)
print(str(datetime.datetime.now()) + ' imported file ' + import_data_file)
model_intervals = pd.read_csv(model_file, header=None)
print(str(datetime.datetime.now()) + ' imported file ' + model_file)


# get spikes
df['spike'] = df.Temperature.apply(lambda x: 1 if x > temperature_threshold else 0)
df['change'] = df['spike'].diff()
df['ind'] = df.index
threshold_intervals = df[df['change'] == 1]['ind'].diff()
print(str(datetime.datetime.now()) + ' found ' + str(len(threshold_intervals)) + ' intervals crossing ' + str(temperature_threshold) + ' threshold')


# loop throgh intervals to compare with min, max valies
print(str(datetime.datetime.now()) + ' anomalies with longer intervals' )
print(df.iloc[threshold_intervals[threshold_intervals > float(max(np.array(model_intervals)))].index.to_list(), ])
print(str(datetime.datetime.now()) + ' anomalies with shorter intervals' )
print(df.iloc[threshold_intervals[threshold_intervals < float(min(np.array(model_intervals)))].index.to_list(), ])
