#!/usr/bin/env python


"""moving_average_forecast.py: forecast with moving average

calculates temperature cutoff that is mean of max and min temperature
calculates time intervals when temperature crosses the cutoff
calculates mean of time interval value
loops over SARIMA models and pics the best model
calculates Linux time increment for output
calculates forecast as average of temp values at every mean time interval

> python3 moving_average_forecast.py CELSI-raw-data-reports.csv
"""


__author__ = "Oleg Solovyev"
__email__  = "oleg.s.solovyev@gmail.com"
__status__ = "Prototype"


import sys
import datetime
import numpy as np
import pandas as pd
import itertools
import warnings
import statsmodels.api as sm


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


# loops over SARIMA models and pics the best model
import itertools
p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 36) for x in list(itertools.product(p, d, q))]

warnings.filterwarnings("ignore") 
results = []
best_aic = np.nan
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(endog=df.Temperature,
                                            trend='n',
                                            order=param,
                                            seasonal_order=param_seasonal)
            res = mod.fit()
            results.append([param, param_seasonal, res.aic])
            if np.isnan(best_aic) or best_aic > res.aic:
                best_aic, best_param, best_param_seasonal = res.aic, param, param_seasonal
        except:
            continue

print(str(datetime.datetime.now()) + ' found best SARIMA model with aic=' + str(round(best_aic,2)) + ' params=' + str(best_param) + 'x' + str(best_param_seasonal))
mod = sm.tsa.statespace.SARIMAX(endog=df.Temperature,
                                            trend='n',
                                            order=best_param,
                                            seasonal_order=best_param_seasonal)
res = mod.fit()
forecast = res.forecast(steps = 6)

# calculates Linux time increment for output
time_increment = int(df.LinuxTime.diff().mean())
print(str(datetime.datetime.now()) + ' Linux time increment is ' + str(time_increment))

# calculates forecast as average of temp values at every mean time interval
print(str(datetime.datetime.now()) + ' Temperature forecast ')
for i in range(0, 6):
  print(str(int(df.LinuxTime.tail(1) + (1+i)*time_increment)) + ',' + str(forecast[df.shape[0]+i]))
