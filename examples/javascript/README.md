# examples/javascript

This folder contains examples of how to link JavaScript (web applications) to
the State of Colorado's HydroBase REST web services.

The State of Colorado has done preliminary work to automate creation of a
JavaScript API library that provides basic access and visualization of web
services. This API will be evaluated, documented, and made available to streamline
use of the web services and implement automated tests. Use of the API library will
ensure that this code does not have to be redeveloped and that the API is consistent
with the server-side web services.

See also the example on the
[HydroBase REST Web Services website](https://dwr.state.co.us/Rest/GET/Help#TechInfoHelp&#All&#gettingstarted&#jsonxml).

The following sections provide a summary of the project and instructions for getting
started:

* [JavaScript Example Folder Structure](#javascript-example-folder-structure)
* [Example Description](#example-description)
* [Getting Started](#getting-started)
* [JavaScript Example Arguments](#javascript-example-arguments)
* [Running the Example](#running-the-example)
* [Moving Forward](#moving-forward)

----
## JavaScript Example Folder Structure
```text
C:\Users\user\                             User's home folder, Windows style.
/c/Users/user/                             User's home folder, Git Bash style.
/cygdrive/C/Users/user/                    User's home folder, Cygwin style.
/home/user/                                User's home folder, Linux style.
  cdss-dev/                                Work done on Colorado Decision Support Systems projects.
```

This repository and the JavaScript example contains the following:
```text
cdss-rest-services-examples/               The top-level CDSS example repository file.
  examples/                                The directory with all CDSS web services examples.
    javascript/                            Top-level directory for this JavaScript example.
      css/                                 The css directory for styling the JavaScript example and third-party packages.
        bootstrap.min.css                  Third-party package (TPP) for styling text font consistent to other CDSS & OWF projects.
        Chart.min.css                      TPP for styling the graph animations and general layout and colors.
        clusterize.css                     TPP for styling the table displaying the data returned, notably the height of the table.
        style.css                          Main style file for the web example, styling where the title, graph, and table are located.
      js/                                  A JavaScript directory for all JavaScript files used for the example.
        Chart.min.js                       The source code for the TPP Chart.js, used for showing data on a graph.
        chartjs-plugin-zoom.min.js         Plugin for chartjs to zoom and pan, and displaying axes dynamically.
        clusterize.min.js                  TPP for easily creating a table to display large amounts of data effeciently.
        hammer.min.js                      Needed along with chartjs zoom plugin, and used for gesture recognition.
        javascript-example.js              The OWF-created file that uses JavaScript to query the HydroBase Web Services.
        moment.min.js                      TPP that deals with dates, times and the formatting of them using moments().
      index-telemetry-station-15min.html   The main html for displaying the raw 15 minute data example on a web page.
      index-telemetry-station-day.html     The main html for displaying the per day example on a web page.
      TODO
      package-lock.json                    A required json file listing the depenedencies for the web page, e.g. the chartjs version.
      README.md                            This README file.
      run-server.sh                        The bash script that uses python to begin the local server to run the example.
```

## Example Description
The state of Colorado has created its own automated JavaScript code to help with 
the querying. They provide the function `getData()` that performs an HTTP GET
request, and returns back the data. What these examples do is takes that data,
and displays them using graphs and tables so they can easily be put in a web
page by anyone wanting to utlilize it. There are a few principal items to cover
that this example uses or utilizes:

**Chart.js Package** - This third party package is a pretty popular graphing
tool for dynamic graphs with a good amount of options for colors, backgrounds,
legends, labels, and graph types. It is created with an object, usually called
config, that is populated with those options and data, then given to the Chart
constructor to paint onto the DOM. More info can be found
[here](https://www.chartjs.org/). The zoom-plugin was used for zooming and
panning throughout the graph, and unfortunately there is not an overabundance
of documentation for that online. There are a few options, but nothing much
more than their [GitHub](https://github.com/chartjs/chartjs-plugin-zoom) page.

**Clusterize.js Package** - This third party package is used for displaying the
table next to the graph. It specializes in displaying large amounts of data
effeciently, so lag isn't noticable to users. It also has an easy to use
set up for populating a `<table>` component by putting each row (`<tr>`) and
column (`<td>`) in an array that's passed to the Clusterize constructor.
Documentation can be found [here](https://clusterize.js.org/).

**State API key** - The API key allows more daily returned requests from the Web
Services than the default amount. This is useful if planning on making many
requests or trying to request large amounts of data, and is an optional
argument to be added to any request. Go to the CDSS REST Web Services help page
[here](https://dwr.state.co.us/rest/get/help) to create an account to obtain an
api key.

**Paging** - By default, the State of Colorado will return more pages of
information to the user if the amount of data rows it returns exceeds 50,000.
Normally, a user would have to make additional requests to retrieve the
remaining rows. This JavaScript example will take care of that, so that only one
query is sent; If there are multiple pages, they will be subsequently queried,
retrieved, and added to the graph and table to be displayed.

**Missing Values** - By default, the State's Web Services only return non-missing
value rows. For example, if there are 10 missing days for a query of daily data,
there will be no empty rows in the returned data; March 9th data will be
followed by March 20th data. Because of this, the consuming application will need
to handle this feature appropriately. This example folder takes care of the
specific Day and Raw queries that it displays.

----
## Getting Started
What's nice about JavaScript is that unlike other coding languages, it does not
need to be installed to use. All that's really needed is a text editor, and any
modern browser (Microsoft Edge, Google Chrome, Firefox, Safari, etc.).

If wanting to use the default localhost server provided in the javascript
example, Python is used and therefore needs to be installed. Check if Python
is already installed by typing `python --version`. Even though the Python 2
end-of-life was reached on January 1, 2020, version 2 or 3 will start the
server. Installation instructions can be found at
[python.org](https://www.python.org/downloads/).

----
## JavaScript Example Arguments
The separate html files listed in the Folder Structure above are each their own
examples for linking JavaScript code to the HydroBase REST Services. The 
arguments for each one are a little different and are as follows:

### Telemetry Station 15 Minute Raw Data
Parameters for the index-telemetry-station-15min html file:

Parameter | Description | Default
--------- | ----------- | -------
`abbrev`<br>**required** | The telemetry station ID abbreviation, as given by the [Colorado Division of Water Resources](https://cdnr.us/#/division/DWR). `ABBREV` **must** be in all caps. The full list can be viewed [here](https://dwr.state.co.us/surfacewater/). | None - must be specified.
`parameter`<br>**required** | The parameter to query at the aforementioned telemetry station. `parameter` **must** be in all caps. (e.g. `DISCHRG`, `AIRTEMP`, `GAGE_HT`) | None - must be specified.
`includeThirdParty`<br>**required** | Boolean input, so value must be true or false. This asks the question, include third-party data? | None - must be specified.
`api-key` | The API key to allow more daily returned requests from the Web Services than the default amount. Go [here](https://dwr.state.co.us/rest/get/help) to obtain an api key. | Empty
`end-date` | The end date to query from the HydroBase Web Service in the form mm/dd/yyyy.If the end date is given and the start date is not given, the web service will return one month's worth of data before the end date. | Empty
`modified` | The date the record was last modified will be returned | Empty
`start-date` | The starting date of the data returned in the form mm/dd/yyyy. If the start date is given and end date is not given, the web service will return one month's worth of data after the start date. | Empty

#### Additional constraints for start_date and end_date include:
* By default, if no starting or ending date is given, the HydroBase web service 
responds with the last month of data.
* If both are given, the web service will return the data for the specified 
period.

----
## Running the Example
There are multiple html examples, and there are two ways to run each one. The first method is opening the html file in a browser. This is handy when wanting
to display the contents quickly and easily. The second method is a little more 
involved, and runs the file using a server in localhost. It's generally a better 
idea to use this method when actually developing a potential web page, as it
more closely resembles a web service, rather than just changing local files like
in the first method. The following describes running the 
index-telemtry-station-15min.html file:

### Method 1: Opening the html file in Chrome
1. Open a browser of choice.
2. For Chrome, Firefox, or Safari, press ctl-o (control "oh"), and find the html
file on the local file system to open. The page should be displayed in browser.
If ctl-o worked and the example is shown, stop here.
3. If on Microsoft Edge, another unnamed browser, or the above did not work, the
file's full path on the system can be pasted into the search bar to be shown.
Otherwise, finding the html file in file explorer, right-clicking and opening
with Microsoft Edge will work.

### Method 2: Running the file using a server in localhost
1. Open up a terminal (Linux/macOS terminal, Cygwin, Git Bash, Command Prompt)
2. `cd` into the javascript/ directory as described above in the folder
structure. This is the top-level directory for the javascript example.
3. For terminal, Cygwin, and Git Bash, run the server by typing
`./run-server.sh`. For Command Prompt, type `run-server.sh`.
4. Now that the server is running, open up a browser of choice and type
`http://localhost:8000`. There are multiple html files as described in the
folder structure above, so the brower will show all files where the html
files are located.
5. Click on the index html file to run, and the example will show up.

## Moving Forward

After an example has been run, there are a few lines of code that need to be
changed in order to use different data than the example. The following will
describe significant code lines to be used moving forward and the lines that
will need to be removed:

1. Open up the index-telemetry-station-15min.html file in a text editor of choice
(Notepad++, Kate, Atom, Sublime, VS Code, etc.)
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