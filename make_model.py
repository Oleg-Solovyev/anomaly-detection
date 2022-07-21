#!/usr/bin/env python


"""make_model.py: Calculates intervals between the data crossing temp cutoff.

> python3 make_model.py CELSI-raw-data-reports.csv model_file.csv -10
"""


__author__ = "Oleg Solovyev"
__email__  = "oleg.s.solovyev@gmail.com"
__status__ = "Prototype"


import sys
import datetime
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


# get spikes
df['spike'] = df.Temperature.apply(lambda x: 1 if x > temperature_threshold else 0)
df['change'] = df['spike'].diff()
df['ind'] = df.index
threshold_intervals = df[df['change'] == 1]['ind'].diff()
print(str(datetime.datetime.now()) + ' found ' + str(len(threshold_intervals)) + ' intervals crossing ' + str(temperature_threshold) + ' threshold')


# save intervals into model file
threshold_intervals[~threshold_intervals.isnull()].to_csv(model_file, index=False, header=False)
print(str(datetime.datetime.now()) + ' saved intervales in ' + model_file)


