# README #

### Description

Freezer temperature anomaly detector. Calculates time intervals when the temperature crossess predefined threshold on the training data.

make_model.py calculates time intervals when the temperature crossess predefined threshold on the training data.
test_model.py marks anomalies in the data where time intervals are shorter or longer then the intervals in the training data.
moving_average_forecast.py forecast with moving average
SARIMA_forecast.py forecast with SARIMA model


### Test
Download CSV file with data into the same folder as the repository files.
Run make_model.py script to calculate time intervals:
```
> python3 make_model.py CELSI-raw-data-reports.csv model_file.csv -10
2022-07-21 19:57:26.429139 imported file CELSI-raw-data-reports.csv
2022-07-21 19:57:26.437832 found 9 intervals crossing -10.0 threshold
2022-07-21 19:57:26.439307 saved intervales in model_file.csv

```
Double check new file model_file.csv in the same folder.
Run test_model.py to get anomalies in the data

```
> python3 test_model.py CELSI-raw-data-reports.csv model_file.csv -10
2022-07-21 20:00:44.002761 imported file CELSI-raw-data-reports.csv
2022-07-21 20:00:44.004783 imported file model_file.csv
2022-07-21 20:00:44.014641 found 9 intervals crossing -10.0 threshold
2022-07-21 20:00:44.014679 anomalies with longer intervals
Empty DataFrame
Columns: [DateTime, Date, Time, Time24, ISOdateTime, LinuxTime, Temperature, Humidity, spike, change, ind]
Index: []
2022-07-21 20:00:44.016339 anomalies with shorter intervals
Empty DataFrame
Columns: [DateTime, Date, Time, Time24, ISOdateTime, LinuxTime, Temperature, Humidity, spike, change, ind]
Index: []
```
There are no anomalies because we are using the same data file for training and testing.
Remove smallest value 138.0 from the model_file.csv file and run the test_model.py again.
```
2022-07-21 20:04:22.178098 imported file CELSI-raw-data-reports.csv
2022-07-21 20:04:22.179431 imported file model_file.csv
2022-07-21 20:04:22.188506 found 9 intervals crossing -10.0 threshold
2022-07-21 20:04:22.188541 anomalies with longer intervals
Empty DataFrame
Columns: [DateTime, Date, Time, Time24, ISOdateTime, LinuxTime, Temperature, Humidity, spike, change, ind]
Index: []
2022-07-21 20:04:22.189923 anomalies with shorter intervals
                    DateTime        Date         Time    Time24               ISOdateTime   LinuxTime  Temperature  Humidity  spike  change   ind
6919  7/12/2022, 11:19:00 AM  2022-07-12  11:19:00 AM  11:19:00  2022-07-12T07:19:00.000Z  1657610340         -9.7        51      1     1.0  6919
```
There is a data set row reported where temperature crossed the threshold and time interval was less then the shortest interval in the model_file.csv file.

Run python3 moving_average_forecast.py 4peeks-short.csv
```
> python3 moving_average_forecast.py 4peeks-short.csv
2022-07-23 21:34:21.705278 imported file 4peeks-short.csv
2022-07-23 21:34:21.705508 temperature cutoff is -15.4
2022-07-23 21:34:21.707792 found 6 intervals crossing -15.4 cutoff
2022-07-23 21:34:21.708019 mean time interval 36.0
2022-07-23 21:34:21.708349 Linux time increment is 600
2022-07-23 21:34:21.708369 Temperature forecast 
1657940400,-17.866666666666664
1657941000,-17.73333333333333
1657941600,-17.85
1657942200,-17.75
1657942800,-17.816666666666666
1657943400,-17.766666666666666
```
Run python3 SARIMA_forecast.py 4peeks-short.csv
```
> python3 SARIMA_forecast.py 4peeks-short.csv
2022-07-25 17:01:31.322512 imported file 4peeks-short.csv
2022-07-25 17:01:31.322804 temperature cutoff is -15.4
2022-07-25 17:01:31.325234 found 6 intervals crossing -15.4 cutoff
2022-07-25 17:01:31.325408 mean time interval 36.0
RUNNING THE L-BFGS-B CODE
...
CONVERGENCE: REL_REDUCTION_OF_F_<=_FACTR*EPSMCH             
2022-07-25 17:03:14.681297 found best SARIMA model with aic=41.57 params=(1, 0, 1)x(1, 1, 1, 36)
RUNNING THE L-BFGS-B CODE
...
CONVERGENCE: REL_REDUCTION_OF_F_<=_FACTR*EPSMCH             
2022-07-25 17:03:20.825332 Linux time increment is 600
2022-07-25 17:03:20.825854 Temperature forecast 
1657940400,-17.550353958500153
1657941000,-18.06113014552193
1657941600,-17.660904347833668
1657942200,-17.832430238422294
1657942800,-17.903417088591198
1657943400,-17.58495752638998
```

