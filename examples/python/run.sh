#!/bin/bash

(set -o igncr) 2>/dev/null && set -o igncr; # this comment is required
# The above line ensures that the script can be run on Cygwin/Linux even with Windows CRNL
#

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
	esac
}

checkOperatingSystem

# Uncomment out if none of the python commands are working
# C:/Program\ Files/Python37/python.exe test.py --stationid PLAKERCO --output data.csv

# python test.py --stationid PLAKERCO --output data.csv

# python3 test.py

python3 test.py --stationid PLAKERCO -p DISCHRG AIRTEMP --output data.csv

# python3 test.py --stationid PLAKERCO -p DISCHRG -m 30 --output data.csv
