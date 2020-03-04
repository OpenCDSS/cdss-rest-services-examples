#!/bin/bash

(set -o igncr) 2>/dev/null && set -o igncr; # this comment is required
# The above line ensures that the script can be run on Cygwin/Linux even with Windows CRNL

# Declaring functions here
checkOperatingSystem()
{
	if [[ -n "${operatingSystem}" ]]; then
		# Have already checked operating system so return
		return
	fi
	operatingSystem="unknown"
	os=$(uname | tr '[:lower:]' '[:upper:]')
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

determinePythonVersion()
{
	# Version is printed to stderr or stdout so a bit trickier to redirect
	# -see:  https://stackoverflow.com/questions/2342826/how-to-pipe-stderr-and-not-stdout
	# First try the general Python launcher
	pythonVersion=$(py --version 2>&1 | cut -d ' ' -f 2 | cut -d . -f 1)
	usePy="false"

	if [ "${pythonVersion}" != "3" ]; then
		# Did not find the correct py version so try whether python3 is found
		pythonVersion=$(python3 --version 2>&1 | cut -d ' ' -f 2 | cut -d . -f 1)

		if [ ${pythonVersion} != "3" ]; then
		echo Error: get-streamflow.py can only be run using Python Version 3
		echo Please update to the most up-to-date version try again
		exit 1
		fi
	else
		# py was found
		usePy="true"
	fi
}

######## ENTRY POINT FOR SCRIPT HERE ######## 
checkOperatingSystem
determinePythonVersion

# Get the absolute path where this script is located
scriptFolder=$(cd $(dirname "${0}") && pwd)
# Changes to the directory where the script is located
cd ${scriptFolder}

# Determine what OS is being used. Also, "$@" is an element seperated 
# Cygwin, Linux and macOS
if [[ "${operatingSystem}" = "cygwin" ]] || [[ "${operatingSystem}" = "linux" ]] || [[ "${operatingSystem}" = "macos" ]]; then
	# Use py command
	if [[ ${usePy} = "true" ]]; then
		py get-streamflow.py "$@"
	# Use python3 command
	else
		python3 get-streamflow.py "$@"
	fi
# Git Bash
elif [[ "${operatingSystem}" = "mingw" ]]; then
	# Use py command
	if [[ ${usePy} = "true" ]]; then
		py get-streamflow.py "$@"
	# Use the python executable
	else
		# We need to know the absolute path of where python.exe is located
		pythonPath=$(which python)
		# Finally, put quotes around the file path in case a directory has a space in its name
		"${pythonPath}" get-streamflow.py "$@"
	fi
fi
