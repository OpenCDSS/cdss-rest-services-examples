#!/bin/sh

# Run examples from the README.md file

curl -o PLAKERCO.json "https://dwr.state.co.us/Rest/GET/api/v2/telemetrystations/telemetrytimeseriesraw/?format=jsonprettyprint&abbrev=PLAKERCO&parameter=DISCHRG"

if [ $? -ne 0 ]; then
  echo "An error occurred downloading PLAKERCO.json"
fi

curl -o PLAKERCO.csv "https://dwr.state.co.us/Rest/GET/api/v2/telemetrystations/telemetrytimeseriesraw/?format=csv&abbrev=PLAKERCO&parameter=DISCHRG"

if [ $? -ne 0 ]; then
  echo "An error occurred downloading PLAKERCO.csv"
fi
