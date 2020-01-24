"""
This simple Python program reads in a few arguments from command line that a user enters
and queries the HydroBase Web Service Database. Depending on how the user wants the
information to be displayed, it can either be printed to terminal or written to a file
in CSV format. Different arguments include

Required:
    --stationid                    The station abbreviation
    -p, --parameter [paramName...] One or more measured parameter in the data will be fetched

Optional
    --ui                           If specified, run in user interface mode (put on hold indefinitely)
    --output Filename              If specified, data retrieved will be written to file 'Filename'
TODO--datetime Minutes             If specified, this will display the data in 15, 30, 45, or 60 minute
                                   increments (15 is default)
"""

import argparse
import requests
import sys


# We take in the arguments given, complain if they're incorrect, and return a tuple of each
def parse_command_line() -> tuple:
    parser = argparse.ArgumentParser(description='Querying the HydroBase web services')

    # Add the first two optional arguments, --ui and --output
    parser.add_argument('--ui', action='store_true',
                        help='Run user interface rather than using terminal')
    parser.add_argument('-o', '--output', metavar='filename', default='stdout',
                        help='Write the data obtained to filename instead of stdout')
    parser.add_argument('-m', '--minutes', metavar='minutes', default=15,
                        help='obtain time increments from data in minutes; options are '
                             '30, 45, 60, etc. (15 minutes is default)')

    # Add an argument group that is required from the user
    required = parser.add_argument_group('required arguments')
    required.add_argument('--stationid', metavar='abbrev', help='The station identifier',
                          required=True)
    required.add_argument('-p', '--parameter', nargs='+', metavar='paramName',
                          help='The measured parameter name', required=True)

    # If no arguments are given at all, print help to let user know argument options
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # The next line is where we actually parse the user's input
    args = parser.parse_args()

    return args.stationid, args.parameter, args.ui, args.output, args.minutes


# The principal method in our program. Given the arguments specified on command line,
# we fetch the data from the HydroBase web service and display it in CSV format. The stationid
# will be static for this program, so if the user needs to look up multiple stations, another
# command will need to be run. There can however be multiple measured parameters given.
def run_batch(stationid: str, parameters: str, output: str, minutes: str) -> None:

    # 'First' variable to determine whether we should write all lines or all lines minus the first
    first = True

    print('  Fetching data...')
    # Go through each parameter given
    for param in parameters:
        # Build our url to fit what the user wants to query
        url = 'https://dwr.state.co.us/Rest/GET/api/v2/telemetrystations/telemetrytimeseriesraw/' \
              '?format=csv&abbrev={}&parameter={}'.format(stationid, param)
        response = requests.get(url)
        # response.text is a string, so we can split on CRLF
        lines = response.text.split('\r\n')

        # Print straight to terminal and exit if no --output argument was received
        if output == 'stdout':
            print(response.text)
            sys.exit()
        # Through some means (usually incorrect parameter name) nothing was returned from the database
        elif len(response.text) == 67:
            print('    parameter error {}: {}'.format(param, response.text))
        # Otherwise, write everything but the first two indexes to the named file
        else:
            if first:
                write_file(output, lines, 2)
                first = False
            else:
                write_file(output, lines, 3)

    print('  Data received and written to file \'{}\''.format(output))
    # TODO remove lines below when time option has been completed (good until this function)
    if minutes != 15:
        print('  The -m and --minutes option is still a work in progress')


def write_file(output: str, lines: str, index: int) -> None:
    with open(output, 'a') as outputFile:
        for item in lines[index:]:
            outputFile.write(item + '\n')


def run_ui() -> None:
    # This function has been put off indefinitely
    pass


def main() -> None:
    # Use our parse_command_line function above to obtain the arguments received by the user
    stationid, parameters, ui, output, minutes = parse_command_line()

    # Since run_batch is our default, if ui was not specified by the user, run that first
    if not ui:
        run_batch(stationid, parameters, output, minutes)
    else:
        run_ui()


if __name__ == '__main__':
    main()
