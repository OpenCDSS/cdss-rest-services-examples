# examples/python

This folder contains examples of how to use Python programs to access the State of Colorado's HydroBase REST web services.


[Python](https://www.python.org/doc/essays/blurb/) is an interpreted, object-oriented, high-level programming language with dynamic semantics. Python can query the web services by running a simple Python program, using command line parameters to indicate which data to retrieve.

----
## Python Prerequisites
The following are prerequisites to creating a Python program to access the web services:

* Install the most up-to-date version of Python. The Python 2 end of life was reached on January 1, 2020 and will not be maintained anymore, even if security issues are found; Because of this, the get-streamflow program used here will not be able to run on Python 2. Python Version 3.6 or newer is strongly recommended. Installation instructions can be found at [python.org](https://www.python.org/downloads/)

* Install the [requests](https://requests.readthedocs.io/en/master/user/install/) 
module. For example, `python -m pip install requests`

----
## Running the Program

This example python program is a command line program, so open up a shell of choice
(Cygwin, Git Bash, Terminal, Windows Command Prompt, etc.). Change directories to the 
`src/` folder.

The program can be run using 3 required arguments and 5 optional arguments, as follows:

### Optional Arguments

Parameter | Description | Default
--------- | ----------- | -------
`--abbrev ABBREV`<br>**required** | The telemetry station ID abbreviation, as given by the [Colorado Division of Water Resources](https://cdnr.us/#/division/DWR). `ABBREV` **must** be in all caps. The full list can be viewed [here](https://dwr.state.co.us/surfacewater/). | None - must be specified.
`--parameter PARAM_NAME [PARAM_NAME ...]`<br>**required** | One or more parameters to query at the aforementioned telemetry station. `PARAM_NAME` **must** be in all caps. (e.g. DISCHRG, AIRTEMP, GAGE\_HT) | None - must be specified.
`--format data_format`<br>**required** | The format for the retrieved information, either `csv` or `json`. | None - must be specified.
 `--end_date end_date` | The ending date of the data returned in the form mm/dd/yyyy. If the end date is given and the start date is not given, the web service will return one month's worth of data before the end date. | Empty
`-h`, `--help` | Displays the help message and exits | Empty
`--output filename` | Instead of printing the information retrieved to the terminal (default), this specifies that it needs to be written to an output file, name determined by the user. | Empty
`--start_date start_date` | The ending date of the data returned in the form mm/dd/yyyy. If the start date is given and end date is not given, the web service will return one month's worth of data after the start date. | Empty

#### Additional constraints for start_date and end_date include:
* By default, if no starting or ending date is given, the HydroBase web service 
responds with the last month of data.
* If both are given, the web service will return the data for the specified period.

----
## Examples

Use the `get-streamflow.sh` script to run the get-streamflow.py program along with 
the arguments needed for the query. Note the output file name given is `data`. The
get-streamflow program will automatically attach the ending `.json` or `.csv` 
depending on the format given.

    get-streamflow.sh --abbrev PLAKERCO --parameter AIRTEMP --format csv --output data

The program will also write multiple parameters differently depending on format.
Multiple parameters in CSV will be written to the same file. Multiple parameters in
JSON will be written to seperate files in the form `filename_PARAM.json`. Examples
as follows:

### Multiple CSV parameters

    get-streamflow.sh --abbrev PLAKERCO --parameter AIRTEMP DISCHRG --format csv --output data
      Fetching data for AIRTEMP...
      Data successfully received and written to file 'data.csv'

      Fetching data for DISCHRG...
      Data successfully received and written to file 'data.csv'

### Multiple JSON parameters

    get-streamflow.sh --abbrev PLAKERCO --parameter AIRTEMP DISCHRG --format json --output data
      Fetching data for AIRTEMP...
      Data successfully received and written to file 'data_AIRTEMP.json'

      Fetching data for DISCHRG...
      Data successfully received and written to file 'data_DISCHRG.json'

----
## Testing

Work in progress