var labelList = [];  // X-Axis array for the chart
var valueList = [];  // Y-Axis array for the chart

/**
 * Retrieve all the data from the HydroBase Web Services, including multiple pages
 * if necessary, and put them in the above arrays for use with displaying the Graph
**/
function retrieveAllData() {
  var pager = { pageSize: 100, pageIndex: 1 }
  var pageCount = 0;

  // 6bZT/60P7k8HGBCnrQ1Yt18zccP35sun ----------------------------------V
  TelemetryTimeSeriesDay.getData(dataRetrieved, pager, "", "PLAKERCO",
    "6bZT/60P7k8HGBCnrQ1Yt18zccP35sun", false, "", "", "DISCHRG", "");
  function dataRetrieved(data) {

    let results = data.responseObject.ResultList
    pageCount = data.responseObject.PageCount;
    for (let i = 0; i < results.length; ++i) {
      // Right now substring is hard-coded, must change
      labelList.push(String(results[i].measDate).substring(0, 24))
      valueList.push(results[i].measValue)
    }

    pager['pageIndex'] += 1;

    if (pageCount >= pager['pageIndex']) {
      TelemetryTimeSeriesDay.getData(dataRetrieved, pager, "", "PLAKERCO",
        "6bZT/60P7k8HGBCnrQ1Yt18zccP35sun", false, "", "", "DISCHRG", "");
    }
  }
}

// label is currently hard-coded
let config = 
{
  type: 'line',
  data: {
    labels: labelList,
    datasets: [{
      label: `DISCHRG in CFS`,
      borderColor: 'rgb(255, 99, 132)',
      borderWidth: 1,
      fill: false,
      data: valueList
    }]
  },
  options: {scales: {
              xAxes: [{
                ticks: {
                  maxTicksLimit: 8
                }
              }],
            },
            elements: {
              point: {
                radius: 0
              }
            }
          }
}

// Currently trying to get async operations squared up so the chart can be shown
// right when the page is loaded. As of now, it won't show since all the data hasn't
// been obtained by the time the x- and y-axis is displayed on the DOM
function displayGraph() {
  const ctx = document.getElementById('myChart').getContext('2d');
  const myChart = new Chart(ctx, config);
}

/**
 * Display the graph using a Chart from chart.js
**/
// function displayGraph() {
//   let ctx = document.getElementById('myChart').getContext('2d');
//   let myChart = new Chart(ctx, {
//                             type: 'line',
//                             data: {
//                               labels: labelList,
//                               datasets: [{
//                                 label: `DISCHRG in CFS`,
//                                 borderColor: 'rgb(255, 99, 132)',
//                                 borderWidth: 1,
//                                 fill: false,
//                                 data: valueList
//                               }]
//                             },
//                             options: {scales: {
//                                         xAxes: [{
//                                           ticks: {
//                                             maxTicksLimit: 8
//                                           }
//                                         }],
//                                       },
//                                       elements: {
//                                         point: {
//                                           radius: 0
//                                         }
//                                       }
//                                     }
//                           });
// }
