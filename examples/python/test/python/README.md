# Python Automated Testing

This directory uses python to test CSV and JSON files retrieved from the HydroBase
Web Service. It calls the get-streamflow.py file (which is in charge of the query)
multiple time with different parameters and compares them to the files in the
expected-results/ directory. 

##### Testing

Testing is as easy as typing `python3 test_get-streamflow.py`

This will let you know if anything goes wrong
