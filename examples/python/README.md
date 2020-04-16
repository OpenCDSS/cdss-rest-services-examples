# examples/python

This folder contains an example of how to use a Python program to access the
State of Colorado's HydroBase REST web services.

[Python](https://www.python.org/doc/essays/blurb/) is an interpreted,
object-oriented, high-level programming language with dynamic semantics. Python
can query the web services by running a Python program, using command line
parameters to indicate which data to retrieve.

The following sections provide a summary of the project and instructions for
getting started:

* [Python Example Folder Structure](#python-example-folder-structure)
* [Python Prerequisites](#python-prerequisites)
* [Running the Program](#running-the-program)
* [Available Python Example Arguments](#available-python-example-arguments)
* [Examples](#examples)
* [Testing](#testing)

----

## Python Example Folder Structure

The following folder structure is recommended for development. Top-level folders
should be created as necessary. The following folder structure clearly separates
user files (as per operating system) and development area (`cdss-dev`) folders:

```
C:\Users\user\                             User's home folder, Windows style.
/c/Users/user/                             User's home folder, Git Bash style.
/cygdrive/C/Users/user/                    User's home folder, Cygwin style.
/home/user/                                User's home folder, Linux style.
  cdss-dev/                                Work done on Colorado Decision Support Systems projects.
    REST-examples/                         REST web service examples.
      git-repos/                           Git repositories for the REST web service examples.
        cdss-rest-services-examples/       See below.
```

This repository and the Python example contains the following:

```
cdss-rest-services-examples/               The CDSS web-services example repository folder.
  examples/                                The folder with all CDSS web services examples.
    python/                                Top folder for Python examples.
      src/                                 The source code for the Python example.
        .gitignore                         Git ignore file for ignoring dynamic files.
        telemetrystation-15min.py          Python script that retrieves the HydroBase data.
        telemetrystation-15min.sh          Bash script that runs the Python script.
        telemetrystation-15min.bat         Windows batch file that runs the Python script.
      test/                                The testing folder.
        python/                            Python testing folder.
          expected-results/                The verified result files retrieved earlier that subsequent queries will compare to.
          results/                         A folder with files that new queries will be written to and compared with expected-results/ files.
          test_streamflow.py               The Python example end-to-end testing program.
          test_streamflow.sh               The bash script to run the Python program.
        tstool/                            TSTool testing folder.
          results/                         File containing dynamically created testing files for TSTool.
          TEST_commands.tstool             The testing Command file for TSTool.
        README.md                          The testing folder README.
      .gitignore                           Top-level Git ignore for dynamic files.
      README.md                            This introductory README file.
```

## Example Description

The `telemetrystation-15min.py` Python program example builds a query for the State of Colorado's HydroBase web services.
The Python program can be run with the complementary `telemetrystation-15min.sh` bash
script or Windows `telemetrystation-15min.bat` batchfile,
which auto-detect the installed Python on the system.
Iinstructions to install Python are in the next section).
A table of the available program command line arguments is provided below
and can be printed if the program is run with `-h` option.

Technical considerations include:

**Paging** - By default, web service requests that return more than 50,000 rows
will result in multiple pages being used to split the response.
The Python program handles this by making multiple requests to retrieve the
full dataset and append results to the output.

**Missing Values** - The web services only returns periods where data records are available.
Consequently, a time series may have gaps with no data rows.
This Python example **does not** insert additional missing values.
Other technologies, such as [TSTool](../tstool/README.md), automatically add rows containing missing values.
In the `test/tstool/` folder, TSTool can be used to test for missing values.
Instructions for testing can be found in the [test README.md](test/README.md).
See also the [OpenCDSS TSTool page](https://opencdss.state.co.us/tstool/).

**Local Time Zones** - By default, the HydroBase web services return times
in local Colorado time zone.
Time series will have a one hour gap in the spring and one hour of redundant data values are discarded in the fall
due to daylight saving changes.

----

## Python Prerequisites

The following are prerequisites to creating a Python program to access the web services.
Development used Cygwin and Git Bash,
with testing in these environments and Windows command prompt.

* Install a recent version of Python.  Python Version 3.6 or newer is recommended.
Installation instructions can be found at
[python.org](https://www.python.org/downloads/).

* Install the [requests](https://requests.readthedocs.io/en/master/user/install/) 
module. For example, `python -m pip install requests`.
This package is used for HTTP requests to retrieve the data.

* Install the [dateutil](https://dateutil.readthedocs.io/en/stable/) module. If
installing on Cygwin and `pip` prints a Permission Denied error, try
`sudo pip install python-dateutil`, which will need a system password. If that
does not work, try `pip install python-dateutil --user`. Instead of installing
the module to a system folder that requires root access, this installs it
to the user's home folder.

----
## Running the Program

The example `telemetrystation-15min.py` Python program is a command line program, so open up a shell of choice
(Cygwin, Git Bash, Terminal, Windows Command Prompt, etc.). Change directories to
the `src/` folder.

The program can be run using 3 required arguments and 5 optional arguments, as follows:

### Available Python Example Arguments

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| ==================== | Required parameters | =================================== |
| `--abbrev ABBREV`<br>**required** | The telemetry station ID abbreviation, as used by the [Colorado Division of Water Resources](http://water.state.co.us). `ABBREV` **must** be in all caps. The full list can be viewed on the [DWR streamflow website](https://dwr.state.co.us/surfacewater/). | None - must be specified. |
| `--parameter PARAM_NAME [PARAM_NAME ...]`<br>**required** | One or more parameters to query for the telemetry station, separated by spaces. `PARAM_NAME` **must** be in all caps. (e.g. `DISCHRG`, `AIRTEMP`, `GAGE_HT`) | None - must be specified. |
| `--format data_format`<br>**required** | The output format for the retrieved information, either `csv` or `json`. | None - must be specified. |
| ==================== | Optional parameters | =================================== |
| `--apiKey api_key` | The API key to allow more daily returned rows/requests than the default amounts. An API key can be obtained by creating an account on the [CDSS REST Web Services Website](https://dwr.state.co.us/rest/get/help). | Web service default. |
| `-h`, `--help` | Displays the help message and exits | |
| `--output filename` | Instead of printing the information retrieved to the terminal (default), this specifies that it needs to be written to an output file, name determined by the user. | Print to the standard output (the console). |
| `--pageSize count` | Maximum data records on a page, used for testing. | Web service default. |
| `--startDate start_date` | The starting date of the data returned in the form `mm/dd/yyyy`. If the start date is given and end date is not given, the web service will return one month's worth of data after the start date. | Web service default. |
| `--endDate end_date` | The ending date of the data returned in the form `mm/dd/yyyy`. If the end date is given and the start date is not given, the web service will return one month's worth of data before the end date. | Web service default. |

#### Additional constraints for start_date and end_date include:

* By default, if no starting or ending date is given, the HydroBase web service 
responds with the last month of data.
* If both are given, the web service will return the data for the specified period.

## Examples

Use the `telemetrystation-15min.sh` script or `telemetrystation-15min.bat` batch file
to run the `telemetrystation-15min.py` program along with 
the arguments needed for the query. The program will create CSV
or JSON output containing the data returned from the HydroBase Web Service.
Each file returned contains one time series. This example does
not support multiple time series in one file.
The output file name will automatically be given an extension
`.json` or `.csv` if not specified.
The following example runs a standard query:

### Linux, macOS, Git Bash, Cygwin and Windows Bash Shell

```
./telemetrystation-15min.sh --abbrev PLAKERCO --parameter AIRTEMP --format csv --output data
```

### Windows Command Prompt

```
telemetrystation-15min.bat --abbrev PLAKERCO --parameter AIRTEMP --format csv --output data
```

The program will also write multiple parameters differently depending on format.
Multiple parameters in csv format will be written to the same file. Multiple parameters in
JSON will be written to separate files with names `filename_PARAM.json`.

### Multiple CSV parameters

```
./streamflow.sh --abbrev PLAKERCO --parameter AIRTEMP DISCHRG --format csv --output data
Fetching data for AIRTEMP...
Data successfully received and written to file 'data.csv'

Fetching data for DISCHRG...
Data successfully received and written to file 'data.csv'
```

### Multiple JSON parameters

```
./streamflow.sh --abbrev PLAKERCO --parameter AIRTEMP DISCHRG --format json --output data
Fetching data for AIRTEMP...
Data successfully received and written to file 'data_AIRTEMP.json'

Fetching data for DISCHRG...
Data successfully received and written to file 'data_DISCHRG.json'
```

## Testing

Automated testing has been implemented for the Python example and is described in the
[test folder README](test/README.md).
