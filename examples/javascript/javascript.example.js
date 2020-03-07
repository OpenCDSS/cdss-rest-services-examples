var labelList = [];      // X-Axis array for the chart
var valueList = [];      // Y-Axis array for the chart
var clusterizeList = []  // Array for the table rows for clusterize
var parameter = '';      // Parameter in query (DISCHRG, AIRTEMP)
var units = '';          // Units in query (cfs, degF)
var pager = {            // The pager object that is passed to the
  pageSize: 40000,       // TelemetryTimeSeriesDay function, the automated
  pageIndex: 1           // code generated from the State of Colorado
}

/**
 * Retrieve all the data from the HydroBase Web Services, including multiple pages
 * if necessary, and put them in the above arrays for use with displaying the Graph
 * and table.
**/
function retrieveAllData() {
  TelemetryTimeSeriesDay.getData(dataRetrieved, pager, '', 'PLAKERCO',
                                    '', false, '', '', 'DISCHRG', '');
}

// The callback function that TelemetryTimeSeriesDay calls to get the info from the
// HydroBase Web Server.
function dataRetrieved(data) {
  // The result array retrieved from the web server, and the number of pages
  let results = data.responseObject.ResultList
  let pageCount = data.responseObject.PageCount;  

  // Variables to format the clusterize table rows correctly
  let tr_td = '<tr><td>';
  let td_td = '</td><td>';
  let td_tr = '</td></tr>';
  
  console.log(typeof moment(String(results[0].measDate)).format());
  var a = moment([2007, 0, 29]);
  var b = moment([2007, 0, 28]);
  console.log(a);   // =1
  
  // Go through the array of results returned and push the date, measured value, and
  // both into the x-axis label, y-axis label, and clusterize <td> respectively.
  for (let i = 0; i < results.length; ++i) {
    // Right now substring is hard-coded, must change    
    labelList.push(new Date(String(results[i].measDate)));
    valueList.push(results[i].measValue);

    if (results[i + 1] != undefined) {
      let day1 = moment(String(results[i].measDate));
      let day2 = moment(String(results[i + 1].measDate));
      let days = day1.diff(day2, 'days');
      if (days > 1) {
        console.log("More than one day");
        
      }
    }
    clusterizeList.push(tr_td.concat(moment(String(results[i].measDate)).format(), td_td,
                                      results[i].measValue, td_tr));
  }

  pager['pageIndex'] += 1;
  // After updating the pager object's pageIndex, check to see if the actual pageCount
  // is still greater than or equal to it. If it is, there are more pages to get, so
  // go get them recursively. If not, assign our parameter and units and create the graph.
  if (pageCount >= pager['pageIndex']) {
    TelemetryTimeSeriesDay.getData(dataRetrieved, pager, '', 'PLAKERCO',
                                      '', false, '', '', 'DISCHRG', '');
  } else {
    parameter = data.responseObject.ResultList[0].parameter;    
    units = data.responseObject.ResultList[0].measUnit.toUpperCase();
    displayGraph();
  }
}

// spanGaps: false     maybe for not filling in the line without values.
function displayGraph() {
  let config = 
    {
      type: 'line',
      data: {
        labels: labelList,
        datasets: [{
          label: `${parameter} in ${units}`,
          borderColor: 'rgb(255, 99, 132)',
          borderWidth: 1,
          fill: false,
          data: valueList,
          lineTension: 0
        }]
      },
      options: { 
        responsive: true,
        title: {
          display: true,
          text: 'JavaScript Example Using the State of Colorado\'s HydroBase Web Services'
        },
        scales: {
          xAxes: [
            {
            distribution: "linear",
            type: 'time',
            time: {
              displayFormats: {
                month: 'MMM YYYY'
              }
            },
            scaleLabel: {
              display: true,
              labelString: 'Date'
            },
            ticks: {
              min: labelList[0],
              max: labelList[labelList.length - 1],
              maxTicksLimit: 10,
              maxRotation: 0
            }
          }
        ],
          yAxes: [
            {
            scaleLabel: {
              display: true,
              labelString: `${parameter} (${units})`
            }
          }
        ],
        },
        elements: {
          point: {
            radius: 1
          }
        },
        plugins: {
          zoom: {
            pan: {
              enabled: true,
              mode: 'x',
              rangeMin: {
                x: labelList[0]
              },
              rangeMax: {
                x: labelList[labelList.length - 1]
              }
            },
            zoom: {
              enabled: true,
              drag: false,
              mode: 'x',
              rangeMin: {
                x: labelList[0]
              },
              rangeMax: {
                x: labelList[labelList.length - 1]
              }
            }
          }
        }
      }
    }

  // Create and display the graph
  const ctx = document.getElementById('myChart').getContext('2d');
  let sal = new Chart(ctx, config);
  
  // Create and display the table
  let clusterTable = new Clusterize({
    rows: clusterizeList,
    scrollId: 'scroll-area',
    contentId: 'content-area'
  });
}
