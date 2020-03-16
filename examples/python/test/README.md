# Automated Testing

This directory uses both Python and the internally developed Time Series Tool
(TSTool) to test CSV and JSON files retrieved from the HydroBase Web Service. The
Python testing calls the streamflow.py file (which is in charge of the query)
multiple times with different parameters, puts each output file into the results/
directory, and compares them to the files in the expected-results/ directory.

The TSTool testing 

## Testing using Python

* From the directory that contains this README file, `cd` into the python/
directory

* Testing is as easy as typing `./test_streamflow.sh` (For Windows Command Prompt,
take off the `./`). The test output will show success or failure.

## Testing using TSTool

TSTool tests by running the Python example through TSTool and converts its output
into a time series. It then queries the HydroBase Web Services itself and that by
default turns the data into a time series. After both have been made, TSTool
compares the two time series to see if they are similar, making sure that two
different software tools produce the same output. Keep in mind that this example
and testing will only use one time series per CSV file. Multiple in one file is
not supported.

Although it is recommended that version 12 or higher is installed if wanting to
test with TSTool, it is not absolutely crucial. As long as the version of TSTool
used for testing has all the required commands below, it will be enough. The
directions for testing are as follows:

1. Open TSTool and press cancel when the default window pops up, as a local
database will not be used for the testing. Then click OK to confirm that
HydroBase features will be disabled.
2. Click **File > Open > Command File** and open the TEST_commands.tstool. From
the main Python example directory, this is located in
**test/tstool/TEST_commands.tstool**
3. Click the Run All Commands button below the Commands box where the Commands
showed up. The automated testing will take care of the rest. If there is a problem,
a large red X will appear to the left of the command. Right-clicking and selecting
Show Command Status will display any Warnings or Failures.