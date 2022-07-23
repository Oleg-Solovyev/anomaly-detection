moving_average_forecast.py forecast with moving average
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
1657939800,-17.866666666666664
1657940400,-17.73333333333333
1657941000,-17.85
1657941600,-17.75
1657942200,-17.816666666666666
1657942800,-17.766666666666666

```
