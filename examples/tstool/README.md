# examples/tstool

This folder contains examples of how to access HydroBase REST web services using TSTool software.

* [Introduction](#introduction)
* [Examples](#examples)
	+ [Download data to a file with `WebGet` command](#download-data-to-a-file-with-webget-command)
	+ [Download data and read into a table](#download-data-and-read-into-a-table)
	+ [Download daily diversion records for a structure](#download-daily-diversion-records-for-a-structure)
	+ [Download monthly diversion records for a structure](#download-monthly-diversion-records-for-a-structure)
	+ [Download annual diversion records for a structure](#download-annual-diversion-records-for-a-structure)

----------------------

## Introduction ##

The CDSS TSTool software can be used to automate processing time series and other data.
TSTool and StateDMI are the main tools used to create CDSS StateCU and StateMod model datasets.
However, TSTool can also be used for general data processing.
TSTool can be run in interactive or batch modes.

* See the [TSTool website](http://opencdss.state.co.us/opencdss/tstool/)

TSTool uses "datastores" to configure data sources including web services.
TSTool version 13 and later is distributed with `HydroBaseWeb` datastore automatically configured,
but with no API key.

If an API key is needed, for example to allow processing large datasets,
see the [REST Web Services Help](https://dwr.state.co.us/Rest/GET/Help#TechInfoHelp&#All&#gettingstarted&#jsonxml)
for information about acquiring an API key.
Once the API key is acquired, it can be added to the
[TSTool datastore configuration file](http://opencdss.state.co.us/tstool/13.02.00dev/doc-user/datastore-ref/ColoradoHydroBaseRest/ColoradoHydroBaseRest/).
**Note that TSTool version 13+ must be run at least one time to ensure that folders and files are initialized for that version,
before updating the datastore configuration file.**

From the TSTool interface, use the ***View / Datastores*** menu to view the list of configured datastores.
Datastores that have configuration issues should be highlighted in yellow.
The `HydroBaseWeb` datastore should be included in the list of datastores.

See the [TSTool ColoradoHydroBaseRest Datastore documentation](http://opencdss.state.co.us/tstool/latest/doc-user/datastore-ref/ColoradoHydroBaseRest/ColoradoHydroBaseRest/)
for information about the datastore, including list of available data.
Additional time series will be enabled as web services and TSTool features are updated.

Considerations when using TSTool with HydroBase web services include:

* **Slower performance than direct database read:**
	+ Web services will be slower than direct database connections.
	This is particularly an issue when interacting with commands that attempt to run in "discovery"
	mode in order to provide lists of time series for command editors.
	TSTool will continue to be updated to improve performande;
	however, for heavy data processing
	it may be necessary to edit command files in a text editor and then run with TSTool.
	+ Running a TSTool command file will re-execute the commands.
	Therefore if any command read HydroBase web services, the time to run will be impacted by the data read.
	It can be beneficial to spit processing into download and command file and separate data processing command file.
	This is more important for large data sets and in cases where API key limits may be exceeded because of
	repeated downloads.
* **Different results** - Using TSTool in some cases will result in data different from basic web service queries.
For example, diversion records processed by TSTool may have additional zeros because of software
logic agreed to with the State of Colorado, consistent with common practices in using diversion records.
Additional filled zero values are flagged and can be viewed in TSTool table and graph views,
and will be output in some formats such as the `DateValue` format.

## Examples ##

The following sections describe specific examples that use TSTool to access HydroBase REST web service data.

### Download data to a file with `WebGet` command ###

The TSTool [`WebGet` command](http://opencdss.state.co.us/tstool/latest/doc-user/command-ref/WebGet/WebGet/),
found in the ***File Handling*** commands, can
be used to retrieve any content available on a website using a URL.
This is useful for bulk download of data.
Because other software will need to process the file, choose a data format that can be processed,
such as comma-separated-value (CSV).

Example files:  [example-webget](example-webget)

### Download data and read into a table ###

If a CSV file has been downloaded, it can be read into a table and used for further processing.
For example, this example:

1. gets the list of active structures in water district 3 and saves to a CSV file
2. read the CSV file into TSTool table
3. copies only the `DITCH` structures into another table (because web services don't allow filtering on structure type)
4. loops over the rows in the table using the TSTool
[`For` command](http://opencdss.state.co.us/tstool/latest/doc-user/command-ref/For/For/) command

This basic logic can be used to iterate through lists of structures, stations, or other data to
automate data download, quality control, etc.

Example files:  [example-table](example-table)

### Download daily diversion records for a structure ###

Daily diversion records are the most detailed diversion record data for a structure.
Diversion records are initially recorded as `WaterClass` records, which indicate details
about the source and destination and use of the data.
Note that web services use the term `WaterClass` for all types of records associated with structures,
including `WaterClass`, `DivTotal`, and other records.
The `WaterClass` records are processed into `DivTotal` records, which record total through a structure,
and `RelTotal`, which indicate total release from a structure, such as storage structures.

Daily diversion records returned from web service contain measurements and user-reported values.
DWR implements a carry-forward algorithm within water years (November to October) that fill missing
values by repeating non-zero measurements.  The DWR approach does NOT fill zero values.
However, TSTool by default fills daily diversion records with additional zeros within irrigation years that
have at least one measurement.  Zeros are filled at the beginning of the irrigation year (before first value)
and by repeating zero values.
TSTool will also optionally set additional zeros for days in irrigation years
when annual diversion comment indicates that water was not taken.
The zero values are flagged.
This approach is consistent with common practice in using diversion records.

To understand `WaterClass` records for a structure of interest,
use the [Water Classes URL Generator](https://dwr.state.co.us/Rest/GET/Help/WaterClassesGenerator) and
query the water classes for the structure, in this case WDID 0301121:
[https://dwr.state.co.us/Rest/GET/api/v2/structures/divrec/waterclasses/?format=jsonprettyprint&wdid=0301121](https://dwr.state.co.us/Rest/GET/api/v2/structures/divrec/waterclasses/?format=jsonprettyprint&wdid=0301121).
The list of available record types (`divrectype` for each water class web service record) indicate which web services can be used to retrieve data.
For example, `divrectype` of `DivTotal` indicates that the `divrecday`, `divrecmonth`, and `divrecyear` web services should be used,
depending on the `availableTimesteps` value in water class list.
TSTool streamlines accessing web services by calling web services as needed and returning data as time series
that can be visualized and processed.

For this example:

1. Read daily `WaterClass` diversion records for the structure WDID, in this case 0301121,
using the
[`ReadColoradoHydroBaseRest` command](http://opencdss.state.co.us/tstool/13.02.00dev/doc-user/command-ref/ReadColoradoHydroBaseRest/ReadColoradoHydroBaseRest/),
which is in the ***Commands / Read Time Series*** menu.
Diversion comments are used to fill additional zeros.
2. Read daily `DivTotal` diversion records for the structure.
Diversion comments are used to fill additional zeros.
3. Read daily `RelTotal` diversion records for the structure.
	* The command generates an error for this example because there are no release time series for this structure.
	* The command can be deleted or commented out to avoid generating an error.
4. Read annual `DivComment` diversion records for the structure.
The time series has zeros in years where water was not taken.
	* To graph in TSTool, use a point graph because values are sparse and
	have zero values.

When the command file is run in TSTool, it is useful to click on the legend text to highlight each time series,
as shown in the following figure.

![tstool-graph](example-divrec-day/tstool-graph.png)

The TSTool table view can be used to view the time series data values and flags.
Use the ***Flags: Superscript*** option near the lower left in the table view.
Note that some zero values have been filled using carry forward from an observed zero value.

**Note also that daily diversion records read from HydroBase database may have more zeros than data read from web services.
This is because the HydroBase `vw_CDSS_DailyAmt` and `vw_CDSS_DailyWC` views often provide
zero values where data may have been missing, due to how the view is created.
These values typically are zero without a flag.
This design approach is being evaluated and in the future HydroBase may be distributed with fewer zero values,
in which case the fill carry forward default algorithm in TSTool should fill many of those zeros,
especially at the start of the irrigation year.**

![tstool-table](example-divrec-day/tstool-table.png)

Example files:  [example-divrec-day](example-divrec-day)

### Download monthly diversion records for a structure ###

Monthly diversion records are derived from daily diversion records and
infrequent monthly diversion record data for a structure.
See the discussion of daily data in the previous section
for more information about `WaterClass` and total time series.

Monthly diversion records returned from web service contain measurements and user-reported values.
Unlike daily diversion records, DWR and TSTool DO NOT implement a carry-forward
algorithm within water years (November to October) for monthly diversion records.
TSTool will optionally set additional zeros for months when annual diversion comment indicates that water was not taken.
The zero values are flagged.

To understand `WaterClass` records for a structure of interest,
use the [Water Classes URL Generator](https://dwr.state.co.us/Rest/GET/Help/WaterClassesGenerator) and
query the water classes for the structure, in this case WDID 0301121:
[https://dwr.state.co.us/Rest/GET/api/v2/structures/divrec/waterclasses/?format=jsonprettyprint&wdid=0301121](https://dwr.state.co.us/Rest/GET/api/v2/structures/divrec/waterclasses/?format=jsonprettyprint&wdid=0301121).
The list of available record types (`divrectype` for each water class web service record) indicate which web services can be used to retrieve data.
For example, `divrectype` of `DivTotal` indicates that the `divrecday`, `divrecmonth`, and `divrecyear` web services should be used,
depending on the `availableTimesteps` value in water class list.
TSTool streamlines accessing web services by calling web services as needed and returning data as time series
that can be visualized and processed.

For this example:

1. Read monthly `WaterClass` diversion records for the structure WDID, in this case 0301121,
using the
[`ReadColoradoHydroBaseRest` command](http://opencdss.state.co.us/tstool/13.02.00dev/doc-user/command-ref/ReadColoradoHydroBaseRest/ReadColoradoHydroBaseRest/),
which is in the ***Commands / Read Time Series*** menu.
Diversion comments are used to fill additional zeros.
2. Read monthly `DivTotal` diversion records for the structure.
Diversion comments are used to fill additional zeros.
3. Read monthly `RelTotal` diversion records for the structure.
	* The command generates an error for this example because there are no release time series for this structure.
	* The command can be deleted or commented out to avoid generating an error.
4. Read annual `DivComment` diversion records for the structure.
The time series has zeros in years where water was not taken.
	* To graph in TSTool, use a point graph because values are sparse and
	have zero values.

When the command file is run in TSTool, it is useful to click on the legend text to highlight each time series,
as shown in the following figure.

![tstool-graph](example-divrec-month/tstool-graph.png)

The TSTool table view can be used to view the time series data values and flags.
Use the ***Flags: Superscript*** option near the lower left in the table view.
Note that some zero values have been filled using carry forward from an observed zero value.

**Note also that monthly diversion records read from HydroBase database may have more zeros than data read from web services.
This is because the HydroBase `vw_CDSS_AnnualAmt` and `vw_CDSS_AnnualWC` views often provide
zero values where data may have been missing, due to how the view is created.
The HydroBase database for CDSS does not include observation code for monthly data,
whereas web services do provide observation code.
This design approach is being evaluated and in the future HydroBase may be distributed with fewer zero values,
in which case some type of fill carry forward for monthly data will need to be implemented in TSTool.**

![tstool-table](example-divrec-month/tstool-table.png)

Example files:  [example-divrec-month](example-divrec-month)

### Download annual diversion records for a structure ###

Annual diversion records are derived from monthly diversion records and
infrequent monthly and annual diversion record data for a structure.
The year is defined as "irrigation year" November 1 to October 31 
and therefore care should be taken when comparing with other year types such as
calendar year or USGS Water Year (October 1 to September 30).
See the discussion of daily data in a previous section
for more information about `WaterClass` and total time series.

Annual diversion records returned from web service contain measurements and user-reported values.
TSTool will optionally set additional zeros for years when annual diversion comment indicates that water was not taken.
The zero values are flagged.

To understand `WaterClass` records for a structure of interest,
use the [Water Classes URL Generator](https://dwr.state.co.us/Rest/GET/Help/WaterClassesGenerator) and
query the water classes for the structure, in this case WDID 0301121:
[https://dwr.state.co.us/Rest/GET/api/v2/structures/divrec/waterclasses/?format=jsonprettyprint&wdid=0301121](https://dwr.state.co.us/Rest/GET/api/v2/structures/divrec/waterclasses/?format=jsonprettyprint&wdid=0301121).
The list of available record types (`divrectype` for each water class web service record) indicate which web services can be used to retrieve data.
For example, `divrectype` of `DivTotal` indicates that the `divrecday`, `divrecmonth`, and `divrecyear` web services should be used,
depending on the `availableTimesteps` value in water class list.
TSTool streamlines accessing web services by calling web services as needed and returning data as time series
that can be visualized and processed.

For this example:

1. Read annual `WaterClass` diversion records for the structure WDID, in this case 0301121,
using the
[`ReadColoradoHydroBaseRest` command](http://opencdss.state.co.us/tstool/13.02.00dev/doc-user/command-ref/ReadColoradoHydroBaseRest/ReadColoradoHydroBaseRest/),
which is in the ***Commands / Read Time Series*** menu.
Diversion comments are used to fill additional zeros.
2. Read annual `DivTotal` diversion records for the structure.
Diversion comments are used to fill additional zeros.
3. Read annual `RelTotal` diversion records for the structure.
	* The command generates an error for this example because there are no release time series for this structure.
	* The command can be deleted or commented out to avoid generating an error.
4. Read annual `DivComment` diversion records for the structure.
The time series has zeros in years where water was not taken.
	* To graph in TSTool, use a point graph because values are sparse and
	have zero values.

When the command file is run in TSTool, it is useful to click on the legend text to highlight each time series,
as shown in the following figure.

![tstool-graph](example-divrec-year/tstool-graph.png)

The TSTool table view can be used to view the time series data values and flags.
Use the ***Flags: Superscript*** option near the lower left in the table view.
Note that some zero values have been filled using carry forward from an observed zero value.

![tstool-table](example-divrec-year/tstool-table.png)

Example files:  [example-divrec-year](example-divrec-year)
