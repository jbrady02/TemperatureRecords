#!/usr/bin/python3
"""Find the maximum or minimum temperature at a weather station for a user
specified timeframe.

TemperatureRecords.py [weather station identifier] [time zone]
[earliest year] [temperature (max or min)] [timeframe] [data_year]
[data_month] [data_day] [unit (c or f)]
Read README.md for more information about the parameters.
"""

import urllib.request
import datetime
import sqlite3
import re
import sys


def remove_year(data_year, date_time, temperature) -> None:
    """
    If the index of date_time contains a year not in data_year, pop the
    index from data_time and temperature.
    """
    size = len(date_time)
    index = 0
    while index < size:
        if data_year not in date_time[index]:
            date_time.pop(index)
            temperature.pop(index)
            size -= 1
        else:
            index += 1


def remove_month(data_month, date_time, temperature) -> None:
    """
    If the index of date_time contains a month not in data_month, pop the
    index from data_time and temperature.
    """
    size = len(date_time)
    index = 0
    while index < size:
        if "-" + data_month + "-" not in date_time[index]:
            date_time.pop(index)
            temperature.pop(index)
            size -= 1
        else:
            index += 1


def remove_day(data_day, date_time, temperature) -> None:
    """
    If the index of date_time contains a day not in data_day, pop the
    index from data_time and temperature.
    """
    size = len(date_time)
    index = 0
    while index < size:
        if "-" + data_day + " " not in date_time[index]:
            date_time.pop(index)
            temperature.pop(index)
            size -= 1
        else:
            index += 1


def remove_null(date_time, temperature) -> None:
    """
    If the index of date_time or temperature contains null, pop the
    index from data_time and temperature.
    """
    size = len(date_time)
    index = 0
    while index < size:
        if "null" in date_time[index] or "null" in temperature[index]:
            date_time.pop(index)
            temperature.pop(index)
            size -= 1
        else:
            index += 1


def main() -> None:
    """
    Get the user arguments, make the URL, format the data, make the database,
    and print the result.
    """
    # If all 10 command line arguments exists, assign them to variables
    if len(sys.argv) == 10:
        station_id = sys.argv[1]
        time_zone = sys.argv[2]
        year = sys.argv[3]
        max_or_min = sys.argv[4]
        timeframe = sys.argv[5]
        data_year = sys.argv[6]
        data_month = sys.argv[7]
        data_day = sys.argv[8]
        unit = sys.argv[9]
    # If all 10 command line arguments do not exist, ask the user
    # for the information to request
    else:
        station_id = input("Please enter a weather station identifier.\n"
                           "A list of valid weather station identifiers"
                           "can be found at\n"
                           "https://mesonet.agron.iastate.edu/"
                           "request/download.phtml\n")
        time_zone = input("Please enter a time zone name as it "
                          "appears in the tz database.\n"
                          "A list of TZ database names can be found at\n"
                          "https://en.wikipedia.org/wiki/List_of_tz_"
                          "database_time_zones\n")
        year = input("Please enter the earliest year that you "
                     "want the data from."
                     "\nThe earliest allowed and default year is 1928.\n")
        if year == "":
            year = "1928"
        invalid_max_or_min = True
        while invalid_max_or_min:
            max_or_min = input("Please enter max for maximum temperature "
                               "or min for minimum temperature.\n")
            if max_or_min.lower() == 'max' or max_or_min.lower() == 'min':
                invalid_max_or_min = False
        invalid_timeframe = True
        while invalid_timeframe:
            timeframe = input("What timeframe do you want the " + max_or_min +
                              " temperature for?\n"
                              "all - All time\nyear - Entire year"
                              "\nsingle-month - One month from one year\n"
                              "every-month - One month from every year\n"
                              "single-day - One day from one year\n"
                              "every-day - One day from every year\n").lower()
            if (timeframe == "all" or timeframe == "year" or
                timeframe == "single-month" or timeframe == "every-month" or
                    timeframe == "single-day" or timeframe == "every-day"):
                invalid_timeframe = False
        if (timeframe == "year" or timeframe == "single-month" or
                timeframe == "single-day"):
            data_year = str(input("What year do you want the data for? "
                                  "(format: YYYY)\n"))
        if (timeframe == "single-month" or timeframe == "every-month" or
                timeframe == "single-day" or timeframe == "every-day"):
            data_month = input("What month do you want the "
                               "data for? (format: MM)\n")
        if timeframe == "single-day" or timeframe == "every-day":
            data_day = input(
                "What day do you want the data for? (format: DD)\n")
        unit = input("Please enter c for degrees Celsius "
                     "or f for degrees Fahrenheit.\n")

    # Get the current year and request the data
    datetime.date.today()
    max_year = datetime.date.today().year
    if timeframe == "single_day":
        url = ("https://mesonet.agron.iastate.edu/cgi-bin/request/"
               "asos.py?station=" + station_id + "&data=tmp" + unit +
               "&year1=" + data_year + "&month1=" + data_month + "&day1=" +
               data_day + "&year2=" + data_year + "&month2=" + data_month +
               "&day2=" + data_day + "&tz=" + time_zone +
               "&format=onlycomma&latlon=no&elev=no&missing=null"
               "&trace=T&direct=no&report_type=3&report_type=4")
    else:
        url = ("https://mesonet.agron.iastate.edu/cgi-bin/request/"
               "asos.py?station=" + station_id + "&data=tmp" + unit +
               "&year1=" + year + "&month1=1&day1=1&year2=" +
               str(max_year + 1) + "&month2=1&day2=3&tz=" + time_zone +
               "&format=onlycomma&latlon=no&elev=no&missing=null"
               "&trace=T&direct=no&report_type=3&report_type=4")
    try:
        site = urllib.request.urlopen(url)
    except Exception as error:
        print("An error occured with your request. Please try again\n"
              "and make sure that your data is formatted correctly.\n")
        main()
        sys.exit(0)

    # Format the data
    raw_data = site.read()
    date_time = str(raw_data)
    date_time = date_time.replace("b'station,valid,tmpc\\n", "")
    date_time = date_time.replace("b'station,valid,tmpf\\n", "")
    date_time = date_time.replace("\\n", "newline")
    date_time = re.sub("[A-Z]+,", "", date_time)
    date_time = re.sub(",", ", ", date_time)
    date_time = re.sub("newline", "', '", date_time)
    date_time = re.sub("(, [-]?[0-9]{1,2}.[0-9]{2})|(, null)", "", date_time)
    date_time = date_time.replace("'", "")
    date_time = date_time.split(", ")
    date_time.pop()  # Remove last element, which is empty
    temperature = str(raw_data)
    temperature = temperature.replace("b'station,valid,tmpc\\n", "'")
    temperature = temperature.replace("b'station,valid,tmpf\\n", "'")
    temperature = temperature.replace("\\n", "newline")
    temperature = re.sub("[A-Z]+,", "", temperature)
    temperature = re.sub("newline", "', '", temperature)
    temperature = re.sub(
        "('[0-9]{4}-[0-9]{1,2}-[0-9]{2} [0-9]{2}:[0-9]{2},)|(null,)", "'",
        temperature)
    temperature = temperature.replace("'", "")
    temperature = temperature.split(", ")
    temperature.pop()  # Remove last element, which is empty

    # Remove data from dates outside user requested range
    match timeframe:
        case "year":
            remove_year(data_year, date_time, temperature)
        case "single-month":
            remove_year(data_year, date_time, temperature)
            remove_month(data_month, date_time, temperature)
        case "every-month":
            remove_month(data_month, date_time, temperature)
        case "single-day":
            remove_year(data_year, date_time, temperature)
            remove_month(data_month, date_time, temperature)
            remove_day(data_day, date_time, temperature)
        case "every-day":
            remove_month(data_month, date_time, temperature)
            remove_day(data_day, date_time, temperature)
    remove_null(date_time, temperature)

    # Make the database
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS temperatures")
    cur.execute("CREATE TABLE temperatures(surrogate_key int primary key,"
                "date smalldatetime, temperature decimal(7, 2))")
    # Date can not be primary key because daylight saving time
    # causes duplicate records.
    for index, item in enumerate(temperature):
        cur.execute("INSERT INTO temperatures VALUES (?, ?, ?)",
                    (index, date_time[index], temperature[index]))
    con.commit()

    # Print the requested data
    query = "SELECT " + max_or_min + "(temperature) FROM temperatures"
    select = cur.execute(query)
    result = select.fetchone()
    for result_temperature in result:
        if str(result_temperature) == "None":
            print("No data was found.")
        else:
            print("The " + max_or_min + "imum temperature at " +
                  station_id + " for the " + "requested timeframe is " +
                  str(result_temperature) + "°" + unit.upper() + ".")


if __name__ == "__main__":
    main()
