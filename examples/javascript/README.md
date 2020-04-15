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
    REST-examples/                         REST web service examples.
      git-repos/                           Git repositories for the REST web service examples.
        cdss-rest-services-examples/       See below.
```

This repository contains the following files for the JavaScript examples:

```text
cdss-rest-services-examples/               The CDSS REST web service examples repository folder.
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
        javascript-example.js              Example JavaScript code to query the HydroBase Web Services.
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
Production software tools will need to use one or more web services and
deal with issues such as date/time formatting, missing data, and paging.
The example applications handle these technical issues.

The following JavaScript packages are used in the examples:

**Chart.js** - This third-party package is a popular graphing
tool for dynamic graphs and provides options for colors, backgrounds,
legends, labels, and graph types.  A graph is created with an object, usually called
config, that is populated with graph options and data, and then provided to the Chart
constructor to paint using the document object model (DOM).  More info can be found on the
[chartjs website](https://www.chartjs.org/). The zoom-plugin was used for zooming and
panning throughout the graph, and unfortunately there is not an overabundance
of documentation for that online. There are a few options, but nothing much
more than their [GitHub Chartjs zoom plugin](https://github.com/chartjs/chartjs-plugin-zoom) page.

**Clusterize.js** - This third-party package is used for displaying the
table next to the graph. It specializes in displaying large amounts of data
efficiently, so lag isn't noticeable to users. It also has an easy to use
set up for populating a `<table>` component by putting each row (`<tr>`) and
column (`<td>`) in an array that is passed to the Clusterize constructor.
Documentation can be found on the [Clusterize website](https://clusterize.js.org/).

**Other important design considerations include:**

**State API key** - The API key controls access to data and throttles requests.
If necessary the State can be contacted to increase query limits for a specific key.
The [CDSS REST Web Services help page](https://dwr.state.co.us/rest/get/help)
provides instructions for obtaining the API key.

**Paging** - By default, the State of Colorado's web services will use 1+ pages
of output if the amount of data rows exceeds 50,000.
Normally, calling applications would have to make additional requests to retrieve the
remaining rows.
However, these JavaScript examples handle the paging so that only one query is sent.
If there are multiple pages, they will be queried in sequence,
data retrieved, and added to the graph and table for display.

**Missing Data** - By default, the State's web services only return non-missing
value rows. For example, if there are 10 missing days for a query of daily data,
there will be no empty rows in the returned data (March 9th data will be
followed by March 20th data). Because of this, the consuming application such as the examples
in this repository need to fill in missing records for display so that data gaps are obvious.
It is important that data gaps are filled with "missing data values"
such as null or `NaN`, and **not** automatically assumed to be zeros.

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

The separate html files listed in the [Java Example Folder Structure](#java-example-folder-structure) are separate
examples to illustrate accessing HydroBase REST Services from JavaScript code.
Specify queries are configured with variables and the code can be adapted for other queries
or integrated with user interface elements such as choice lists.

The arguments for each query executed are described in the following sections.

### Telemetry Station 15 Minute Raw and Day Data

The following parameters are used by both the `index-telemetry-station-15min.html` and
`index-telemetry-station-day.html` files:

| **Parameter** | **Description** | **Default** |
| ------------- | --------------- | ----------- |
| `abbrev`<br>**required** | The telemetry station ID abbreviation, as used by the [Colorado Division of Water Resources](https://water.state.co.us). `ABBREV` **must** be in all caps. The full list can be viewed [here](https://dwr.state.co.us/surfacewater/). | None - must be specified. |
| `parameter`<br>**required** | The parameter to query at the aforementioned telemetry station. `parameter` **must** be in all caps. (e.g. `DISCHRG`, `AIRTEMP`, `GAGE_HT`) | None - must be specified. |
| `includeThirdParty`<br>**required** | Boolean input, so value must be `true` or `false`, indicating whether third-party data should be included (typically `true` to see all available data). | None - must be specified. |
| `api-key` | The API key to allow more daily returned requests from the web services than the default amount. Use the [web services help page](https://dwr.state.co.us/rest/get/help) to obtain an api key. | |
| `end-date` | The end date to query from the HydroBase Web Service in the form `mm/dd/yyyy`.  If the end date is given and the start date is not given, the web service will return one month's worth of data before the end date. | |
| `modified` | Used to request data since a date, for example if new data are being queried to add to a local database. | |
| `start-date` | The starting date of the data returned in the form `mm/dd/yyyy`. If the start date is given and end date is not given, the web service will return one month's worth of data after the start date. | |

#### Additional constraints for `start_date` and `end_date` include:

* By default, if no starting or ending date is given, the HydroBase web service 
responds with the last month of data.
* If both are given, the web service will return the data for the specified period.

## Running the Example

There are two ways to run each example.
The first method is opening the html file directly in a browser, which is useful for
quickly displaying the page; however, URLs use `file:` rather than `http:` and some browsers may have limitations.
The second method requires running a local Python web server and then accessing the file using `localhost` for the server name.
The second method more closely resembles how an application would be served from a web server and is typically used in development.
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

There are two example html files in this directory:

1. The `index-telemetry-station-15min.html` file retrieves and displays
15 minute data for a specified period, or the last month by default. 
2. The `index-telemetry-station-day.html` file retrieves and displays
daily data for a specified period, or a year by default.

In both cases, the html and JavaScript code are similar.
Around line 70 is a `<script>` tag that calls a web service URL
with the `?js=1` appended to the end.
This query parameter generates JavaScript code that can be used on in
the client application to read from web services.
This URL would normally download the generated JavaScript file to the users's computer.
However, when used as a `src` attribute for the `<script>` tag, it gives access to the
generated code returned from the web service.
The returned code can be used to query the
web services using the provided function.
The functions that are used, in order, are as follows:

| **Function** | **Description** |
| ------------- | --------------- |
| `detectOS` | Determines what operating system is used. This will create the data display table differently, as Windows and other operating systems have different built-in ways of rendering a table with a side scroll bar. This is done with a `<script>` tag on line 16 for both html files, and is 1 of 2 functions directly called from the html. |
| `retrieveAllData` | Uses a `<script>` tag that starts around line 73 for both example html files. It decides which html file is running and calls the appropriate function that is provided by web services. |
| `getData` | The function provided by web services that retrieves data from HydroBase web service. |
| `dataRetrieved` | The callback function in the `getData` function for retrieving all data from the web service.  This hands off logic from the web-service JataScript code to the application code. |
| `getDates` | A helper function for returning all the dates in between two given dates. This is helpful for checking for correct dates, missing data, and labeling the graph. |
| `clusterUnitHeader` | Dynamically names the table and graph headers/axis names depending on which html file is currently being run. |
| `displayGraph` | Sets up the configuration object for the ChartJS graph, and creates and displays both the graph and Clusterize table. |

## Moving Forward

### Changing Variables

The examples focus on a specific station and data parameter.
In order to adapt the code for other stations and parameters,
a few lines of code need to be changed, as follows:

1. Edit the html file in a text editor of choice.
2. Notice the multiple `<var>` tags around line 50. These are the
variables that are passed to the JavaScript from the web page
and are used as function arguments to call HydroBase web services.

For example, in the index-telemetry-station-15min.html, change the variables to:

```html
<var id="input-api-key" hidden></var>
<var id="input-abbrev" hidden>PLAKERCO</var>
<var id="input-end-date" hidden>03/01/2020</var>
<var id="input-include-third-party" hidden></var>
<var id="input-modified" hidden></var>
<var id="input-parameter" hidden>AIRTEMP</var>
<var id="input-start-date" hidden>02/01/2020</var>
<var id="input-offset" hidden></var>
```

This queries the HydroBase web service using the Telemetry Station from the
South Platte River near Kersey, CO, from the entire month of February, looking for
`AIRTEMP` parameter in degrees Fahrenheit. 

### Embeding into Existing Website

To embed the example (or modified version) in an already existing website:

1. Copy `css/` and `js/` folders into the top level directory of the website.
Alternatively, they can be put anywhere, but then the `src` attributes below would
need to be updated so the path to each file is in the correct place relative to
their location. The last link configures the font and is not completely necessary.
The order of the scripts below matter and should not be changed.

2. In the main html, paste the following lines into the `<head>` tag:
  ```html
  <script type="text/javascript" src="js/javascript-example.js"></script>
  <script type="text/javascript">detectOS();</script>
  <link rel="stylesheet" href="css/clusterize.css">
  <script type="text/javascript" src="js/moment.min.js"></script>
  <script type="text/javascript" src="js/Chart.min.js"></script>
  <script type="text/javascript" src="js/hammer.min.js"></script>
  <script type="text/javascript" src="js/chartjs-plugin-zoom.min.js"></script>
  <script type="text/javascript" src="js/clusterize.min.js"></script>
  <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
  ```

3. All `<var>` tags needed for the query should be used, whether they are hard
coded or from user input.

4. The entire `all-data` `div` should be put wherever it needs to be in the
website. This will display the graph on the left and table on the right, and by
default will take the entire width of the page.
