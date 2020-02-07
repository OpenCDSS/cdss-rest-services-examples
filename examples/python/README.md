# examples/python

This folder contains examples of how to link Python to the State of Colorado's HydroBase REST web services.


[Python](https://www.python.org/doc/essays/blurb/) is an interpreted, object-oriented, high-level programming language with dynamic semantics. We can use Python to query the web services by running the simple python program we have and filling out necessary fields to get back what we want. 

----
## Python Prerequisites
Before we begin, there are two items to take into account before going forward:

* Install the most up-to-date version of Python you can. Version 3.6 or newer is recommended. You can find installation instructions at [python.org](https://www.python.org/downloads/)

* Install the [requests](https://requests.readthedocs.io/en/master/user/install/) module

----
## Running the Program

Running this simple python program will take place on the command line, so open up your shell of choice (Cygwin, Git Bash, Terminal, Windows Command Prompt, etc.). The get-streamflow.py file is where the program lives, so once you've changed directories to the file that contains this README, go down one more into src/.

The program takes a total of 3 required arguments and 5 optional arguments. They are as follows:

### Optional Arguments

* `-h`, `--help`

Shows the help message and exits

* `-o filename`, `--output filename`

Instead of printing the information retrieved to the terminal (default), this specifies that it needs to be written to an output file, name determined by the user.

* `-m <integer>`, `--minutes <integer>`

Default data is taken every 15 minutes at each station. If different time intervals is desired, this option pulls from longer increments instead. <integer> **must** be a multiple of 30, e.g. 30, 60 90, etc.

###### Start Date and End Date
By default, if no starting or ending date is given, the Hydrobase web service responds with the last month of data up until the most recent. Format of both start and end dates **must** be in the form mm/dd/yyyy

* `-sd start_date`, `--start_date start_date`
* `-ed end_date`, `-end_date end_date`

A couple more things to keep in mind when using start and end dates:

* If the start date is given and end date is **not** given, the web service will reply with one month's worth of data after the start date

* If the end date is given and the start date is **not** given, the web service will reply with one month's worth of data before the end date.

* If both are given, the web service **will** reply with data in between them, so be careful of enormous data sets.

### Required Arguments

* `-sid ABBREV`, `--stationid ABBREV`

The telemetry station abbreviation, as given by the Colorado Division of Water Resources. The id **must** be in all caps. The full list can be viewed [here](https://dwr.state.co.us/surfacewater/).

* `-p PARAM_NAME [PARAM_NAME ...]`, `--parameter PARAM_NAME [PARAM_NAME ...]`

One or more parameters to query at the aforementioned telemetry station. PARAM\_NAME also **must** be in all caps. (e.g. DISCHRG, AIRTEMP, GAGE\_HT)

* `-f data_format`, `--format data_format`

The format the retrieved information is displayed as. Options are either csv or json.

## Example

`python3 get-streamflow.py -sid PLAKERCO -p AIRTEMP -f csv -o data`
