var chartLabelList = [];      // X-Axis array for the chart
var chartValueList = [];      // Y-Axis array for the chart
var clusterizeList = [];      // Array for the table rows for clusterize
var input_api_key = '';       // Api Key for increased query limit
var input_abbrev = '';        // StationId needed for query
var input_end_date = '';      // If given, ending date for data queried
var input_include_third_party = ''; // Include third-party data
var input_modified = '';      // Returned date of last modified record
var input_parameter = '';     // Parameter to query (DISCHRG, GAGE_HT, AIRTEMP)
var input_start_date = '';    // Date to start the query
var input_offset = ''         // The time of offset to grab the data for
var html_type = ''            // Which html file is being run (Raw, Day, etc.)
var units = '';               // After query, this populates the table units
var x_axis_label = '';        // The dynamic x-axis label for the graph
var pager = {                 // The pager object that is passed to the
  pageSize: 50000,            // TelemetryTimeSeries function, the automated
  pageIndex: 1                // code generated from the State of Colorado
}


// Dynamically populate the clusterized table header using the parameters and
// units that was returned from the server.
function clusterUnitHeader() {
  // Set the Clusterize table Units Column Header
  document.getElementById('units').innerHTML = 
  `${input_parameter} (${unitsCap})`

  if (html_type == '15min') {
    document.getElementById('date').innerHTML = 'Date/Time';
    x_axis_label = 'Date/Time';
  }
  else  {
    document.getElementById('date').innerHTML = 'Date';
    x_axis_label = 'Date';
  }
}


// The callback function that TelemetryTimeSeriesDay calls to get the info from the
// HydroBase Web Server.
function dataRetrieved(data) {
  // The result array retrieved from the web server, and the number of pages
  let results = data.responseObject.ResultList
  let pageCount = data.responseObject.PageCount;
  let trueDates = [];

  // Variables to correctly format the clusterize table rows
  let tr_td = '<tr><td>';
  let td_td = '</td><td class=\"right\">';
  let td_tr = '</td></tr>';
  
  let test_index = 0;
  // Go through the array of results returned and push the date, measured value, and
  // both into the x-axis label, y-axis label, and clusterize <tr> and <td>
  // respectively, for the 15 minute raw data.
  if (html_type == '15min') {
    for (i = 0; i < results.length; ++i) {

      if (results[i - 1] != undefined) {
        let currentMin = String(results[i].measDateTime).slice(19, 21);
        if (currentMin == '00') currentMin = '60';
        let lastMin = String(results[i - 1].measDateTime).slice(19, 21);

        if (parseInt(currentMin, 10) - parseInt(lastMin, 10) != 15) {
          let tempString = String(results[i - 1].measDateTime)
          .replace(String(results[i - 1].measDateTime).slice(19, 21),
          parseInt(String(results[i - 1].measDateTime).slice(19, 21) + 15));
          let nextDate = new Date(tempString);

          chartLabelList.push(new Date(String(results[i].measDateTime)));
          chartValueList.push('null');
        } else {
          chartLabelList.push(new Date(String(results[i].measDateTime)));
          chartValueList.push(results[i].measValue);
        }
      }
      // Add to the clusterize list for the table rows and columns
      clusterizeList
        .push(tr_td
        .concat(moment(String(results[i].measDateTime))
        .format('YYYY-MM-DD HH:mm'),
        td_td,
        results[i].measValue,
        td_tr));
    }
  }
  // If the HTML file passed is for day data, query the Web Service along with
  // the missing value protection
  else if (html_type == 'day') {
    trueDates = getDates(new Date(String(results[0].measDate)),
    (new Date(String(results[results.length - 1].measDate))));

    for (i = 0; i < trueDates.length; ++i) {
      if (String(results[test_index].measDate) == trueDates[i]) {   
        chartLabelList
        .push(new Date(moment(String(results[test_index].measDate))));
        chartValueList.push(results[test_index].measValue.toFixed(1));
        test_index += 1;
      } else {
        chartLabelList.push(trueDates[i]);
        chartValueList.push('null');
      }
      // Add to the clusterize list for the table rows and columns
      clusterizeList
        .push(tr_td
        .concat(moment((trueDates[i]))
        .format('YYYY-MM-DD'),
        td_td,
        chartValueList[i],
        td_tr));
    }
  }

  pager['pageIndex'] += 1;
  // After updating the pager object's pageIndex, check to see if the actual pageCount
  // is still greater than or equal to it. If it is, there are more pages to get, so
  // go get them recursively. If not, assign our parameter and units and create the output.
  if (pageCount >= pager['pageIndex']) {
    switch (html_type) {
      case "15min":
        TelemetryTimeSeriesRaw.getData(dataRetrieved,
          pager,
          input_api_key,
          input_abbrev,
          input_end_date,
          input_include_third_party,
          input_modified,
          input_parameter,
          input_start_date);
          break;
      case "day":
        TelemetryTimeSeriesDay.getData(dataRetrieved,
          pager,
          input_api_key,
          input_abbrev,
          input_end_date,
          input_include_third_party,
          input_modified,
          input_offset,
          input_parameter,
          input_start_date);
          break;
    }
  } else {
    // For displaying on the graph in regular case and upper case.
    units = data.responseObject.ResultList[0].measUnit;
    unitsCap = units.toUpperCase();
    clusterUnitHeader();
    displayGraph();
  }
}

// After all the data has been retrieved, configurate the graph, then display
// it along with the clusterize table.
function displayGraph() {
  // The enormous config object used for creating the Chartjs graph
  let config = 
    {
      type: 'line',                                  // Line graph
      data: {                                        // Define the data for graph
        labels: chartLabelList,                      // X-axis labels
        datasets: [{
          label: `${input_parameter} (${unitsCap})`, // Dataset label
          borderColor: 'rgb(255, 99, 132)',          // Actual color of line graph
          backgroundColor: 'rgba(33, 145, 81, 0)',   // Create the legend outline
          borderWidth: 1,                            // Line width
          spanGaps: false,                           // Don't connect null values
          fill: true,                                // Don't fill beneath
          data: chartValueList,                      // Y-axis values
          lineTension: 0                             // Straight line connect
        }]
      },
      options: { 
        responsive: true,
        title: {
          display: true,
          text: `${input_abbrev}`
        },
        tooltips: {                                  // When hovered over each
          callbacks: {                               // data point, this changes
            title: (tooltipItem, data) => {          // what will be shown
              if (html_type == 'day') {              // The title is the top item
                return moment(data['labels'][tooltipItem[0]['index']])// displayed
              .format('YYYY-MM-DD');                 // while hovering
              } else if (html_type == '15min') {
                return moment(data['labels'][tooltipItem[0]['index']])
              .format('YYYY-MM-DD HH:mm');
              }
            },
            label: (tooltipItem, data) => {
              let datasetLabel = data.datasets[tooltipItem.datasetIndex].label;
              let label = data['datasets'][0]['data'][tooltipItem['index']];
              return datasetLabel + ': ' + Number(label).toFixed(1);
            }
          }
        },
        scales: {
          xAxes: [
            {
            distribution: "linear",
            type: 'time',                            // Use the momentjs TPP to
            time: {                                  // dynamically display the
              displayFormats: {                      // X-axis labels in the
                month: 'MMM YYYY'                    // given format
              }
            },
            scaleLabel: {
              display: true,
              labelString: `${x_axis_label}`
            },
            ticks: {                                 // Maybe setting these help
              min: chartLabelList[0],                // with the graph scrolling
              max: chartLabelList[chartLabelList.length - 1],// speed
              maxTicksLimit: 10,                     // No more than 10 ticks
              maxRotation: 0                         // Don't rotate labels
            }
          }
        ],
          yAxes: [
            {
            scaleLabel: {
              display: true,
              labelString: `${input_parameter} (${unitsCap})`
            }
          }
        ],
        },
        elements: {                                  // Show each element on the
          point: {                                   // graph with a small circle
            radius: 1
          }
        },
        plugins: {                                   // Extra plugin for zooming
          zoom: {                                    // and panning.
            pan: {
              enabled: true,
              mode: 'x',
              rangeMin: {
                x: chartLabelList[0]
              },
              rangeMax: {
                x: chartLabelList[chartLabelList.length - 1]
              }
            },
            zoom: {
              enabled: true,
              drag: false,
              mode: 'x',
              rangeMin: {
                x: chartLabelList[0]
              },
              rangeMax: {
                x: chartLabelList[chartLabelList.length - 1]
              },
              sensitivity: 0.01
            }
          }
        }
      }
    }

  // Create and display the graph
  const chartContext = document.getElementById('myChart').getContext('2d');
  window.onload = new Chart(chartContext, config);
  
  // Create and display the table
  window.onload = new Clusterize({
    rows: clusterizeList,
    scrollId: 'scroll-area',
    contentId: 'content-area'
  });
}

// Returns an array of dates between the two dates given
// https://gist.github.com/miguelmota/7905510
function getDates(startDate, endDate) {  
  let dates = [],
      currentDate = startDate,
      addDays = function(days) {
        let date = new Date(this.valueOf());
        date.setDate(date.getDate() + days);
        return date;
      };
  while (currentDate <= endDate) {
    dates.push(currentDate);
    currentDate = addDays.call(currentDate, 1);
  }
  return dates;
};


/* The main and only function that is directly called from the html file. The rest
are called from getData function below and subsequent functions below that. The
arguments from the html are assigned here and passed to the automated source code
from the State of Colorado. NOTE: As of right now, all of these variables are in
between the two comments below in each of the switch cases, and are hard-coded so
as to display the example data. */
function retrieveAllData() {

  input_api_key = document.getElementById("input-api-key");
  input_abbrev = document.getElementById("input-abbrev");
  input_end_date = document.getElementById("input-end-date");
  input_include_third_party =
    document.getElementById("input-include-third-party");
  input_modified = document.getElementById("input-modified");
  input_parameter = document.getElementById("input-parameter");
  input_start_date = document.getElementById("input-start-date");
  input_offset = document.getElementById("input-offset");

  html_type = document.getElementById("html-type").innerHTML;
  
  switch (html_type) {
    case '15min':
      // Below, the arguments are hard-coded for example purposes and can be removed
      input_api_key = '';
      input_abbrev = 'PLAKERCO';
      input_end_date = '';
      input_include_third_party = false;
      input_modified = '';
      input_parameter = 'DISCHRG';
      input_start_date = '';
      // Above, the arguments are hard-coded for example purposes and can be removed
      
      TelemetryTimeSeriesRaw.getData(dataRetrieved,
        pager,
        input_api_key,
        input_abbrev,
        input_end_date,
        input_include_third_party,
        input_modified,
        input_parameter,
        input_start_date);
        break;
    case 'day':
      // Below, the arguments are hard-coded for example purposes and can be removed
      input_api_key = '';
      input_abbrev = 'CHARESCO';
      input_end_date = '';
      input_include_third_party = false;
      input_modified = '';
      input_parameter = 'STORAGE';
      input_start_date = '';
      // Only for TelemetryTimeSeriesDay
      input_offset = '';
      // Above, the arguments are hard-coded for example purposes and can be removed
      
      TelemetryTimeSeriesDay.getData(dataRetrieved,
        pager,
        input_api_key,
        input_abbrev,
        input_end_date,
        input_include_third_party,
        input_modified,
        input_offset,
        input_parameter,
        input_start_date);
        break;
  }

}