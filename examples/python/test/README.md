# Automated Testing

This directory uses both Python and the internally developed Time Series Tool
(TSTool) to test CSV and JSON files retrieved from the HydroBase Web Service. The
Python testing calls the streamflow.py file (which is in charge of the query)
multiple times with different parameters, puts each output file into the results/
directory, and compares them to the files in the expected-results/ directory. The
TSTool testing
    TODO

## Testing using Python

* `cd` into the python/ directory

* Testing is as easy as typing `./test_streamflow.py` (For Windows Command Prompt,
take off the `./`). The test output will show success or failure.

## Testing using TSTool

* 