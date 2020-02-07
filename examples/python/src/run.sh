#!/bin/bash

(set -o igncr) 2>/dev/null && set -o igncr; # this comment is required
# The above line ensures that the script can be run on Cygwin/Linux even with Windows CRNL

# Declaring functions here

checkOperatingSystem()
{
	if [ ! -z "${operatingSystem}" ]; then
		# Have already checked operating system so return
		return
	fi
	operatingSystem="unknown"
	os=`uname | tr [a-z] [A-Z]`
	case "${os}" in
		CYGWIN*)
			operatingSystem="cygwin"
			;;
		LINUX*)
			operatingSystem="linux"
			;;
		MINGW*)
			operatingSystem="mingw"
			;;
		DARWIN*)
			operatingSystem="macos"
			;;
	esac
}

# Entry point for script here

checkOperatingSystem

# Get the absolute path where this script is located
#scriptFolder=`cd $(dirname "$0") && pwd`
# Changes to the directory where the script is located
#cd ${scriptFolder}


# This if else statement determines what OS we're using and uses the correct syntax for running the script
# So far this has only taken this machine into account. For example, we're assuming python3 will work, and
# where the PATH for python will be. This needs to be changed
if [ "${operatingSystem}" = "cygwin" -o "${operatingSystem}" = "linux" -o "${operatingSystem}" = "macos" ]; then
	# Test help message
	# python3 get-streamflow.py

	# Test required parameters
	# python3 get-streamflow.py --stationid PLAKERCO -p DISCHRG -f csv -m 90

	# test output goes to file
	# python3 get-streamflow.py --stationid PLAKERCO -p DISCHRG -f csv --output data.csv

	# Test multiple parameters
	# python3 get-streamflow.py --stationid PLAKERCO -p DISCHRG AIRTEMP -f csv -m 120

	# Test the clarified minutes
	# python3 get-streamflow.py --stationid PLAKERCO -p DISCHRG AIRTEMP -f json -m 120 -o data

	# Test csv data for the entirety of 2019
	# python3 get-streamflow.py -sid PLAKERCO -p AIRTEMP -f csv -sd 01/01/2019 -ed 01/01/2020 -o data

	# Test csv data for 3 months in 2015
	# python3 get-streamflow.py -sid PLAKERCO -p GAGE_HT -f csv -ed 01/01/2019 -o data
	python3 get-streamflow.py -sid PLAKERCO -p AIRTEMP -f csv
elif [ "${operatingSystem}" = "mingw" ]; then
	# For Git Bash
	C:/Program\ Files/Python37/python.exe get-streamflow.py --stationid PLAKERCO -p DISCHRG --output data.csv
fi

# For python 2?
#python get-streamflow.py --stationid PLAKERCO --output data.csv
