# examples/curl

This folder contains examples of how to link command line `curl` program
to the State of Colorado's HydroBase REST web services.

`curl` is a command line tool that facilitates automating data downloads.
`curl` can be called from the command line, batch files, scripts, etc.
`curl` is also useful to automate monitoring that data are available and to implement basic
automated tests (download file and compare with expected results from previous download).

* [`curl` Documentation](#curl-dcumentation)
* [Install `curl`](#install-curl)
* [Examples](#examples)

----------------------

## `curl` Documentation ##

See the main `curl` documentation:  [https://curl.haxx.se/docs/manual.html](https://curl.haxx.se/docs/manual.html)

## Install `curl` ##

Free and open source versions of `curl` software are available for various operating systems.

* Windows - see [curl for Windows](https://curl.haxx.se/windows/)
* Linux - install the `curl` package using installation tools for the Linux distribution
* Git Bash (used with Git for Windows) - available by default
* Cygwin - install `curl` package

## Examples ##

The following are examples to download data from HydroBase REST web services.
The URLs that are used can be prototyped using the ***Url Generator*** links on the
[HydroBase REST Web Services](https://dwr.state.co.us/rest/get/help) page.

### Real-time (15-minute) Streamflow for a Station ###

The following queries 15-minute streamflow data for recent (default) period for station `PLAKERCO` and saves JSON format to local file `PLAKERCO.json`.
Note that the URL must be quoted on Linux (and is OK to do on Windows) because of special characters in the URL.

```
curl -o "PLAKERCO.json https://dwr.state.co.us/Rest/GET/api/v2/telemetrystations/telemetrytimeseriesraw/?format=jsonprettyprint&abbrev=PLAKERCO&parameter=DISCHRG"
```

The following queries 15-minute streamflow data for recent (default) period for station `PLAKERCO` and saves JSON format to local file `PLAKERCO.csv`.

```
curl -o "PLAKERCO.csv https://dwr.state.co.us/Rest/GET/api/v2/telemetrystations/telemetrytimeseriesraw/?format=csv&abbrev=PLAKERCO&parameter=DISCHRG"
```
