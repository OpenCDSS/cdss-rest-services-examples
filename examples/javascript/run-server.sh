#!/bin/sh
(set -o igncr) 2>/dev/null && set -o igncr; # this comment is required

# Run a local web server on port 8000 using the Python version that is found
# - Python 3 typically installs "py" program, which intelligently runs latest Python that is installed
# - However, can't rely on that so also check for python and python3 in PATH.
echo "  View the web application in a browser with http://localhost:8000"
echo "  Kill the web server with CTRL-C"

# Version is printed to stderr or stdout so a bit tricker to redirect
# -see:  https://stackoverflow.com/questions/2342826/how-to-pipe-stderr-and-not-stdout
# First try the general Python launcher
pythonVersion=$(py --version 2>&1 | cut -d ' ' -f 2 | cut -d . -f 1)
usePy="false"

if [[ "${pythonVersion}" != "3" ]] && [[ "${pythonVersion}" != "2" ]]; then
  # Did not find the version so try whether python3 is found
  pythonVersion=$(python3 --version 2>&1 | cut -d ' ' -f 2 | cut -d . -f 1)
  if [[ "${pythonVersion}" != "3" ]]; then
    # Did not find python3 so see if python 2 is available
    pythonVersion=$(python --version 2>&1 | cut -d ' ' -f 2 | cut -d . -f 1)
  fi
else
  # py was found
  usePy="true"
fi

# Now try to run the web server
# - See:  https://gist.github.com/willurd/5720255
if [[ "${pythonVersion}" == "3" ]]; then
  if [[ ${usePy} = "true" ]]; then
    echo "  Using py (Python 3) http server"
    py -m http.server 8000
  else
    echo " Using python3 http server"
    python3 -m http.server 8000
  fi
elif [[ "${pythonVersion}" == "2" ]]; then
  if [[ ${usePy} = "true" ]]; then
    echo "  Using py (Python 2) http server"
    py -m SimpleHTTPServer 8000
  else
    echo "  Using python2 http server"
    python -m SimpleHTTPServer 8000
  fi
else
  echo ""
  echo "Cannot determine whether python or python3 are available to run http server"
  exit 1
fi

exit 0
