# nj-transit-cli

## Description

This project creates a Command Line Interface for NJ Transit's rail data.
Given a station stop name, the departure times will be 
displayed per headsign that the stop services.

## How to Use

### Directory Structure

All source files are in the njt/ directory. The njt.py file is the main file.

### Compatability

This program will work for Python 3.9>=

I have not tested this on Linux or Windows, only Mac.

### Set Up

Use pip to install the required packages:
- pandas
- requests

Can run: pip install -r requirements.txt

### Arguments

python3 njt.py <stop_names> -t/--time HH:MM -d/--date YYYY-MM-DD -n/--number X -r/--refresh

stop_names: A list of stop names. 
The departure times will be printed for each given stop name.
Partial names will be excepted if the prefix is unique to a single stop name

-t/--time: Specify a minimum departure time.
Defaults to 00:00 or 12 AM.
Must be in a HH:MM format.
Only times after the given time will be printed.
The word "now" can also be used to get times after the current time.

-d/--date: Specify a trip date.
Defaults to today's date.
The date must be in YYYY-MM-DD format.
The departure times will be printed for the given date. 
The word "tomorrow" can also be used to get the next day's times.

-n/--number: Specify a number of times to print.
Defaults to 10.
Specifies how many departure times will be printed after a minimum time.
If the number of times left to print is less than the number specified here, 
then only that lesser amount of times can be printed.

-r/--requirements: Refreshes the rail data from NJ Transit.
On the first run of the program, this will be done automatically.

## Motivation

I wrote this program because I was annoyed with using the NJ Transit app to quickly get times for a stop.
I live right near a light rail station and always have my terminal open, so I wanted a way
to be able to check the next departure times. I use NJ Transit quite often so this is a very helpful little app.