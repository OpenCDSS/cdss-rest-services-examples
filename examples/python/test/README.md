# Automated Testing

This directory uses both Python and the OpenCDSS TSTool software
to test CSV and JSON files retrieved from the HydroBase web service. The
Python testing calls the `stationtelemetry-15min.py` program to query data
multiple times with different parameters, saves each output file in the `results/`
folder, and compares them to the files in the `expected-results/` directory.
Expected results are visually inspected to confirm accuracy.

The TSTool testing compares TSTool output with Python program output.

## Testing using Python

* From the directory that contains this README file, `cd` into the python/
directory

* Run `./test_telemetrystation-15min.sh` in Cygwin or Git Bash.
The test output will show success or failure.

## Testing using TSTool

TSTool version 12 or higher should be used for testing.

TSTool tests run the Python example from TSTool and converts the output
into a time series. It then queries the HydroBase web services using TSTool features,
which automatically creates time series.
TSTool then compares the two time series to see if they are similar, making sure that two
different software tools produce the same output.
In this example testing uses one time series per CSV file.
Multiple time series in one file has not been tested.

Run TSTool tests as follows:

1. Start TSTool.  A local HydroBase database is not required for testing.
2. Use ***File / Open / Command File*** and open the `examples/python/test/tstool/TEST_commands.tstool` file.
3. Press the ***Run All Commands*** button to run the tests.
If there is a problem, a red X will appear to the left of the command.
Right-click on the command and select
***Show Command Status*** to display details about warnings and failures.