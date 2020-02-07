"""
This simple Python program reads in a few arguments from command line that a user enters
and queries the HydroBase Web Service Database. Depending on how the user wants the
information to be displayed, it can either be printed to terminal or written to a file
in CSV or JSON format. Run    python3 file_name.py -h    to display help message
"""

import argparse
import json
import pprint
import requests
import sys


# We take in the arguments given, complain if they're incorrect, and assign them
# to global constants, since they won't change during this program
def parse_command_line() -> None:
    parser = argparse.ArgumentParser(description='Querying the HydroBase web services')

    # Add the first two optional arguments, -m and --output
    parser.add_argument('-o', '--output', metavar='filename', default='stdout',
                        help='Write the data obtained to filename instead of stdout')
    parser.add_argument('-m', '--minutes', metavar='<integer>', default=15, type=int,
                        help='an integer to obtain time increments from data in minutes; options are '
                             '30, 60, 90, etc. (15 is default)')
    parser.add_argument('-sd', '--startDate', metavar='start_date', default='',
                        help='The date to start the query in the form mm/dd/yyyy')
    parser.add_argument('-ed', '--endDate', metavar='end_date', default='',
                        help='The date to end the query in the form mm/dd/yyyy')

    # Add an argument group that is required from the user
    required = parser.add_argument_group('required arguments')
    required.add_argument('-sid', '--stationid', metavar='abbrev', help='The station identifier',
                          required=True)
    required.add_argument('-p', '--parameter', nargs='+', metavar='param_name',
                          help='The measured parameter name', required=True)
    required.add_argument('-f', '--format', metavar='data_format',
                          help='format the data is displayed as; options are '
                                'CSV or JSON', required=True)

    # If no arguments are given at all, print help to let user know argument options
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    # The next line is where we actually parse the user's input
    args = parser.parse_args()
    # Create our global variables so we don't pass 5+ parameters to every function
    global STATIONID
    global PARAMETERS
    global MINUTES
    global DATA_FORMAT
    global OUTPUT
    global START_DATE
    global END_DATE

    STATIONID = args.stationid
    PARAMETERS = args.parameter
    MINUTES = args.minutes
    DATA_FORMAT = args.format
    OUTPUT = args.output
    START_DATE = args.startDate
    END_DATE = args.endDate


# The principal method in our program. Given the arguments specified on command line,
# we fetch the data from the HydroBase web service and display it in CSV format. The stationid
# will be static for this program, so if the user needs to look up multiple stations, another
# command will need to be run. There can however be multiple measured parameters given.
def run_batch() -> None:
    # To determine whether we should write the csv headers at the top of the file
    first_page = True

    for param in PARAMETERS:
        print('  Fetching data for {}...'.format(param))

        # Build our url to fit what the user wants to query. We need to query first to see
        # if we get back more than one page from the database
        url = build_url(param, 1)
        response = requests.get(url)

        # Through some means (usually incorrect parameter name) nothing was returned from the database
        if 'zero records from CDSS' in response.text:
            print('\n    parameter error {}: {}'.format(param, response.text))
            print('    {} not used in query\n'.format(param))
            continue

        # Process JSON
        if DATA_FORMAT == 'json':
            process_json(param, response.text)
        # Process CSV
        else:
            process_csv(param, first_page, response.text)
            first_page = False


def process_json(param: str, response: str) -> None:
    global OUTPUT
    temp = OUTPUT
    # Retrieve the data and put into a JSON object
    json_obj = json.loads(response)
    page_count = json_obj["PageCount"]
    # Printing to terminal here
    if OUTPUT == 'stdout':
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(json_obj["ResultList"][:: MINUTES // 15])

        if page_count > 1:
            print_remaining(param, page_count)
    # Writing to a file here
    else:
        if page_count == 1:
            if len(PARAMETERS) > 1:
                OUTPUT = OUTPUT + '_' + param
            write_file(json_obj["ResultList"], first_page=True, last_page=True)
            print('  Data successfully received and written to file \'{}\'\n'.format(OUTPUT))
            OUTPUT = temp
        else:
            # If there are multiple parameters given, change file name to
            # fileName_paramName to differentiate between them and write to separate files
            if len(PARAMETERS) > 1:
                OUTPUT = OUTPUT + '_' + param
            write_file(json_obj["ResultList"], first_page=True, last_page=False)
        if page_count > 1:
            write_remaining(param, page_count)
            print('  Data successfully received and written to file \'{}\'\n'.format(OUTPUT))
            # Since we changed the file name for the first parameter, revert back to original output
            OUTPUT = temp


def process_csv(param: str, first_page: bool, response: str) -> None:
    # response.text is a string, so we can split on CRLF
    lines = response.split('\r\n')
    # Determine the amount of pages that the returned data was split into (if any)
    page_count = int(lines[1].split(',')[1])

    # Print straight to terminal if no --output argument was received
    if OUTPUT == 'stdout':
        # Write the CSV headers
        print(lines[2])
        # Write the rest of the list from the first data index and go up by amount given,
        # or default if not given
        print(*lines[3:: MINUTES // 15], sep='\n')
        # If more than one page, print them all
        if page_count > 1:
            print_remaining(param, page_count)

    # Otherwise, write everything but the first two indexes to the named file
    else:
        # First parameter (and its corresponding pages if any)
        if first_page:
            write_file(lines, first_page=True, last_page=False)
            if page_count > 1:
                write_remaining(param, page_count)

        # Second parameter and beyond (and its corresponding pages if any)
        else:
            write_file(lines, first_page=False, last_page=False)
            if page_count > 1:
                write_remaining(param, page_count)

        print('  Data successfully received and written to file \'{}\'\n'.format(OUTPUT))


# Build our URL for querying the HydroBase web services
def build_url(param: str, page_index: int) -> str:
    data_format = DATA_FORMAT
    if data_format == 'json':
        data_format = 'jsonprettyprint'

    start_date = ''
    end_date = ''
    # Check if the start and end dates were given. If they were, build the correct URL
    # corrected string to pass to the query
    if START_DATE != '':
        start_date = START_DATE.split('/')
        check_date_list(start_date)
        start_date = '%2F'.join(start_date)
    if END_DATE != '':
        end_date = END_DATE.split('/')
        check_date_list(end_date)
        end_date = '%2F'.join(end_date)

    return 'https://dwr.state.co.us/Rest/GET/api/v2/telemetrystations/telemetrytimeseriesraw/' \
        '?format={}&pageIndex={}&abbrev={}&parameter={}&startDate={}&endDate={}'\
        .format(data_format, page_index, STATIONID, param, start_date, end_date)


def check_date_list(date_list) -> None:
    if len(date_list) > 3:
        print('Date input incorrect. Input must be in the form mm/dd/yyyy')
        print('Use the -h option for argument options and more help')
        sys.exit()


# We have our first query, and determined that the page count is greater than one. Since it is,
# we have multiple pages and need to query the rest of the pages for both CSV or JSON. print_remaining
# prints the pages to stdout, and write_remaining writes the pages to a file
def print_remaining(param: str, page_count: int) -> None:
    for page_index in range(2, page_count + 1):
        url = build_url(param, page_index)
        response = requests.get(url)

        if DATA_FORMAT == 'csv':
            lines = response.text.split('\r\n')
            print(*lines[3:: MINUTES // 15], sep='\n')
        else:
            json_obj = json.loads(response.text)
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(json_obj["ResultList"][:: MINUTES // 15])


def write_remaining(param: str, page_count: int) -> None:
    # Write the rest of the pages to a file
    for page_index in range(2, page_count + 1):
        url = build_url(param, page_index)
        response = requests.get(url)

        if DATA_FORMAT == 'csv':
            lines = response.text.split('\r\n')
            write_file(lines, first_page=False, last_page=False)
        else:
            json_obj = json.loads(response.text)
            if page_index == page_count:
                write_file(json_obj["ResultList"], first_page=False, last_page=True)
            else:
                write_file(json_obj["ResultList"], first_page=False, last_page=False)


# Depending on if we have multiple pages, we write the data to a file
def write_file(lines: list, first_page: bool, last_page: bool) -> None:
    global OUTPUT

    # Add .csv or .json to file if not given to the file name
    if '.csv' not in OUTPUT and '.json' not in OUTPUT:
        OUTPUT = OUTPUT + '.' + DATA_FORMAT

    with open(OUTPUT, 'a') as outputFile:
        # Write CSV
        if DATA_FORMAT == 'csv':
            # Write the CSV headers at the top since we're writing the first page
            if first_page:
                outputFile.write(lines[2] + '\n')
            # Write the rest of the CSV to file
            for item in lines[3:: MINUTES // 15]:
                outputFile.write(item + '\n')
        # Write JSON
        else:
            # Write the beginning of the JSON object on the first page
            if first_page:
                outputFile.write('{ \"ResultList\": [')
            # Get the amount of data lines in the page to determine if we're
            # at the last line
            page_length = len(lines[:: MINUTES // 15])
            index = 0
            for item in lines[:: MINUTES // 15]:
                # If we're on the last line of the page AND the last page, end
                # our list from ResultList (we don't want a comma at the end)
                if index == page_length - 1 and last_page:
                    outputFile.write(json.dumps(item, indent=4) + '\n')
                else:
                    outputFile.write(json.dumps(item, indent=4) + ',\n')
                index = index + 1
            # Double check it's the last page and finish writing our JSON object. After
            # that the file will be closed
            if last_page:
                outputFile.write(']}')


def main() -> None:
    # Use our parse_command_line function above to obtain the arguments received by the user
    parse_command_line()
    # Perform the query to the database with our arguments
    run_batch()


if __name__ == '__main__':
    main()
