# examples/javascript

This folder contains examples of how to link JavaScript (web applications) to
the State of Colorado's HydroBase REST web services.
Whereas other examples such as Python and TSTool focus on command line and desktop software
that automates data processing, the JavaScript examples focus on retrieving data for visualization
in a web browser.

The HydroBase REST web services provide data and also have features to provide
JavaScript API code that can be used to develop web applications.
Consequently, the work necessary to write client-side application code has partly been completed.
Use of the API library helps ensure that application code does not need to be redeveloped and that the API is consistent
with the server-side web services.

See also the JavaScript example on the
[HydroBase REST Web Services website](https://dwr.state.co.us/Rest/GET/Help#TechInfoHelp&#All&#gettingstarted&#jsonxml).

The following sections provide a summary of the project and instructions for getting
started:

* [JavaScript Example Folder Structure](#javascript-example-folder-structure)
* [Example Description](#example-description)
* [Getting Started](#getting-started)
* [JavaScript Example Arguments](#javascript-example-arguments)
* [Running the Example](#running-the-example)
* [Software Design](#software-design)
* [Moving Forward](#moving-forward)

----

## JavaScript Example Folder Structure

The following folder structure is recommended for development, consistent with other OpenCDSS software.

```text
C:\Users\user\                             User's home folder, Windows style.
/c/Users/user/                             User's home folder, Git Bash style.
/cygdrive/C/Users/user/                    User's home folder, Cygwin style.
/home/user/                                User's home folder, Linux style.
  cdss-dev/                                Work done on Colorado Decision Support Systems projects.
    REST-examples/                         REST examples.
      git-repos/                           Git repositories for the REST examples.
        cdss-rest-services-examples/       See below.
```

This repository contains the following files for the JavaScript examples:

```text
cdss-rest-services-examples/               The CDSS REST example repository folder.
  examples/                                The folder for web services examples.
    javascript/                            The folder for JavaScript examples.
      css/                                 The css directory for styling the JavaScript example and third-party packages.
        bootstrap.min.css                  Third-party package (TPP) for styling text font consistent to other CDSS & OWF projects.
        Chart.min.css                      TPP for styling the graph animations and general layout and colors.
        clusterize.css                     TPP for styling the table displaying the data returned, notably the height of the table.
        style.css                          Main style file for the web example, styling where the title, graph, and table are located.
      js/                                  Folder for JavaScript libraries.
        Chart.min.js                       TPP Chart.js library, used for showing data on a graph.
        chartjs-plugin-zoom.min.js         Plugin for chartjs to zoom and pan, and displaying axes dynamically.
        clusterize.min.js                  TPP for easily creating a table to efficiently display large amounts of data.
        hammer.min.js                      Needed along with chartjs zoom plugin, and used for gesture recognition.
        javascript-example.js              The OWF-created file that uses JavaScript to query the HydroBase Web Services.
        moment.min.js                      TPP that deals with dates, times and the formatting of them using moments().
      index-telemetry-station-15min.html   The main html for displaying the raw 15 minute data example on a web page.
      index-telemetry-station-day.html     The main html for displaying the per day example on a web page.
      package-lock.json                    JSON file listing the dependencies for the web page, e.g. the chartjs version.
      README.md                            This README file.
      run-server.sh                        The bash script that uses Python to begin the local web server to run the examples.
```

## Example Description

The State of Colorado's HydroBase web services provide automated JavaScript API code to help with 
querying the web services.  This lessens the burden on web application developers to create code for the same functionality.
The API code provides the function `getData()` that performs an HTTP GET
request and returns the data. These examples use this API code to query data
and additional example code has been developed to display the data using graphs and tables.
The examples therefore illustrate how to use web services to develop a simple data viewing application.

The following JavaScript packages are used in the examples:

**Chart.js Package** - This third party package is a popular graphing
tool for dynamic graphs and provides options for colors, backgrounds,
legends, labels, and graph types.  A graph is created with an object, usually called
config, that is populated with graph options and data, and then provided to the Chart
constructor to paint using the document object model (DOM).  More info can be found on the
[chartjs website](https://www.chartjs.org/). The zoom-plugin was used for zooming and
panning throughout the graph, and unfortunately there is not an overabundance
of documentation for that online. There are a few options, but nothing much
more than their [GitHub Chartjs zoom plugin](https://github.com/chartjs/chartjs-plugin-zoom) page.

**Clusterize.js Package** - This third party package is used for displaying the
table next to the graph. It specializes in displaying large amounts of data
efficiently, so lag isn't noticeable to users. It also has an easy to use
set up for populating a `<table>` component by putting each row (`<tr>`) and
column (`<td>`) in an array that's passed to the Clusterize constructor.
Documentation can be found on the [Clusterize website](https://clusterize.js.org/).

Other important design issues include:

**State API key** - The API key controls access to data and throttles requests.
If necessary the State can be contacted to increase query limits for a specific key.
The [CDSS REST Web Services help page](https://dwr.state.co.us/rest/get/help)
provides instructions for obtaining the API key.

**Paging** - By default, the State of Colorado will return more pages of
information to the user if the amount of data rows exceeds 50,000.
Normally, a user would have to make additional requests to retrieve the
remaining rows. This JavaScript example will take care of that, so that only one
query is sent; If there are multiple pages, they will be subsequently queried,
retrieved, and added to the graph and table to be displayed.

**Missing Values** - By default, the State's Web Services only return non-missing
value rows. For example, if there are 10 missing days for a query of daily data,
there will be no empty rows in the returned data; March 9th data will be
followed by March 20th data. Because of this, the consuming application such as the examples
in this repository need to fill in missing records for display.

**Local Time Zones** - The HydroBase web service return all dates and times in
local time zones.  Consequently, the JavaScript examples 
display all x- and y-labels, legends, and table values in
[ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) compliant local
date and time formats.  Changes due to daylight saving time result in
a one hour data gap in the spring (spring forward) and a redundant hour of data being
thrown away in the fall (fall back).

## Getting Started

JavaScript does not require additional software to be installed to used.
A text editor is required to edit code and a
modern web browser (Microsoft Edge, Google Chrome, Firefox, Safari, etc.) is used to run the program in the browser.
The work done in this repository used Chrome.

A Python http server was used to simulate a deployed environment on `localhost`.
Check if Python is already installed by typing `python --version` in a command prompt window.
Python may not be in the `PATH`.  It may also be found as `py`.
Even though the Python 2 end-of-life was reached on January 1, 2020, version 2 or 3 will start the server.
Python installation instructions can be found at [python.org](https://www.python.org/downloads/).

## JavaScript Example Arguments

The separate html files listed in the Folder Structure are separate
examples for linking JavaScript code to the HydroBase REST Services.
Specify queries are defined as variables and the code can be adapted for other queries
or integrated with user interface elements such as choice lists.

The arguments for each query executed are described in the following sections.

### Telemetry Station 15 Minute Raw and Day Data

The following parameters are used by both the `index-telemetry-station-15min.html` and
`index-telemetry-station-day.html` files:

| **Parameter** | **Description** | **Default** |
| --------- | ----------- | ------- |
| `abbrev`<br>**required** | The telemetry station ID abbreviation, as given by the [Colorado Division of Water Resources](https://water.state.co.us). `ABBREV` **must** be in all caps. The full list can be viewed [here](https://dwr.state.co.us/surfacewater/). | None - must be specified. |
| `parameter`<br>**required** | The parameter to query at the aforementioned telemetry station. `parameter` **must** be in all caps. (e.g. `DISCHRG`, `AIRTEMP`, `GAGE_HT`) | None - must be specified. |
| `includeThirdParty`<br>**required** | Boolean input, so value must be `true` or `false`, indicating whether third-party data should be included (typically `true` to see all available data). | None - must be specified. |
| `api-key` | The API key to allow more daily returned requests from the Web Services than the default amount. Use the [web services help page](https://dwr.state.co.us/rest/get/help) to obtain an api key. | |
| `end-date` | The end date to query from the HydroBase Web Service in the form `mm/dd/yyyy`.  If the end date is given and the start date is not given, the web service will return one month's worth of data before the end date. | |
| `modified` | The date the record was last modified will be returned | |
| `start-date` | The starting date of the data returned in the form `mm/dd/yyyy`. If the start date is given and end date is not given, the web service will return one month's worth of data after the start date. | |

#### Additional constraints for `start_date` and `end_date` include:

* By default, if no starting or ending date is given, the HydroBase web service 
responds with the last month of data.
* If both are given, the web service will return the data for the specified period.

## Running the Example

There are two ways to run each example.
The first method is opening the html file directly in a browser, which is useful for
quickly displaying the page; however, URLs use `file:` rather than `http:` and some browsers may have limitations.
The second method requires running a local Python web server and then accessing the file using localhost.
The second method more closely resembles a web service and is typically used in development.
The following describes running the `index-telemetry-station-15min.html` file:

### Method 1: Opening the html file in a Web Browser

1. Open a browser of choice, in this case Chrome.
2. For Chrome, Firefox, or Safari, press `ctl-o` (control "oh"), and select the html
file on the local file system to open. The page should then display in the browser.
If `ctl-o` worked and the example is shown, stop here.
3. If on Microsoft Edge, another unnamed browser, or the above did not work, the
file's full path on the system can be pasted into the search bar to be shown.
Otherwise, finding the html file in file explorer, right-clicking and opening
with Microsoft Edge will work.

### Method 2: Running the file using a server in localhost

1. Open up a terminal (Linux/macOS terminal, Cygwin, Git Bash, Command Prompt)
2. `cd` into the repository `examples/javascript/` folder.
3. For Linux terminal, Cygwin, and Git Bash, run the server by typing `./run-server.sh`.
4. Once the server is running, open up a browser of choice and open the URL
`http://localhost:8000`. There are multiple html files as described in the
folder structure above, so the browser will show all files where the html
files are located.
5. Click on the index html file to run, and the example will show up.
6. Or, use `http://localhost:8000/index-telemetry-station-15min.html` or `http://localhost:8000/index-telemetry-station-day.html` to directly open a web page.

## Software Design

This section needs to describes the basics of what calls what.
It also needs to clearly explain how the State's code has been incorporated,
for example though a `<script>`

Why do you have unassigned variables in the index.html and then hard-code the values in the javascript-example.js file?
Wouldn't it be better to assign in the index.html so people know what that looks like and they can change the values,
rather than having to go deeper into the code to remove hard-coded values?

## Moving Forward

After an example has been run, there are a few lines of code that need to be
changed in order to use different data than the example, as follows:

1. Open up the index-telemetry-station-15min.html file in a text editor of choice.
2. Note the <!-- --> comment about halfway through the code. These are the
variables that would be passed to the JavaScript from the web page once assigned 
and are the arguments that will be sent to the HydroBase Web Service.
3. Open up the js/javascript-example.js file. At the very bottom is a function 
called retrieveAllData. The first 7 variables here from the html are assigned 
their own in the javascript to be used. By default, to display the example, all 
seven variables are immediately overridden, hard-coded, and in between two
comments so they're easier to find. These need to be deleted in the future when
displaying dynamic data.

This should be all that needs to be done before moving on.
