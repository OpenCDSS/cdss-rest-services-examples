# examples/statedmi

This folder contains examples of how to access the State of Colorado's HydroBase REST web services with StateDMI software.
StateDMI is used to process data from HydroBase and other sources into model data files.
Whereas TSTool focuses on time series, StateDMI handles other files such as station files, water rights, and irrigated acreage.

* See the [OpenCDSS StateDMI website](http://opencdss.state.co.us/opencdss/statedmi/)

StateDMI version 5.00.00 and later include limited integration with REST web services,
and such features continue to be enhanced over time.
Because StateDMI is mainly used by modelers that use a local HydroBase database,
StateDMI web service features are not currently used for modeling full basins.
However, web service features will continue to grow in use as StateDMI is used to automate processing data
independent of a local database.

StateDMI implements a datastore design that is similar to TSTool.
Refer to the [TSTool examples](../tstool/README.md) documentation for information about configuring datastores.
