# TemperatureRecords
A Python program that finds the maximum or minimum temperature at a weather station for a user specified timeframe.
# Description
TemperatureRecords.py will obtain user input from either command line arguments or guided input prompts. Then, data will be obtained from the [Iowa State University Iowa Environmental Mesonet](https://mesonet.agron.iastate.edu/request/download.phtml) as a comma-separated values file. Extra data outside of the user specified range will be removed and then a SQL database will be created from the data. Then the program will print and return the maximum or minimum temperature.
# Usage
This Python program supports both command line arguments and arguments added through guided input prompts. Both methods have the same capabilities, however guided input prompts will sometimes warn the user about invalid input. For the command line arguments, please put all 10 arguments in, even if they will be ignored by the program.\
TemperatureRecords.py [weather station identifier] [time zone] [earliest year] [temperature (max or min)] [timeframe] [data_year] [data_month] [data_day] [unit (c or f)]\
station_id - A weather station identifier. A list of valid weather station identifiers can be found at [https://mesonet.agron.iastate.edu/](https://mesonet.agron.iastate.edu/).\
time_zone - A time zone name as it appears in the tz database. A list of TZ database names can be found at [https://en.wikipedia.org/wiki/List_of_tz_database_time_zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).\
year - The earliest year that you want the data from. The earliest allowed year is 1928.\
max_or_min - Enter max for maximum temperature or min for minimum temperature.\
timeframe - The timeframe that you want the data for, choose from the following:
* all - All time
* year - Entire year
* single-month - One month from one year
* every-month - One month from every year
* single-day - One day from one year
* every-day - One day from every year
<!-- -->
data_year = Limit the data to this year (format: YYYY)\
data_month = Limit the data to this month (format: MM)\
data_day = Limit the data to this daty (format: DD)\
If you are not limiting data to all three of the above, put any value in for the ones you are not using.\
unit = Enter c for degrees Celsius or f for degrees Fahrenheit.
# Special Thanks
[Iowa State University Iowa Environmental Mesonet](https://mesonet.agron.iastate.edu/request/download.phtml) for archiving automated airport weather observations from around the world.
