"""
telemetrystation-15min.py

This Python program queries the HydroBase web services for
real-time (15 minute) station telemetry data.
The web service results are output to stdout or a file.

Run with -h to display the usage.

See the main program at the end of this file.
"""

import argparse
import dateutil.parser as p
import json
import pprint
import requests
import sys


def build_url(app_data: dict, param: str, page_index: int) -> str:
    """
    Build the URL for querying the HydroBase web services,
    for a single parameter.

    Args:
        app_data (dict): Dictionary of command line input.
        param (str): Single parameter to query.
        page_index (int): Page index, used for multi-page queries.

    Returns:
        URL to use for query.
    """
    # Get needed data, alphabetized
    api_key = get_app_data(app_data, 'API_KEY')
    end_date = get_app_data(app_data, 'END_DATE')
    output_format = get_app_data(app_data, 'OUTPUT_FORMAT')
    page_size = get_app_data(app_data, 'PAGE_SIZE')
    if output_format == 'json':
        # Automatically use pretty print for JSON
        output_format = 'jsonprettyprint'
    station_abbrev = get_app_data(app_data, 'STATION_ABBREV')
    start_date = get_app_data(app_data, 'START_DATE')

    # Base URL
    url = 'https://dwr.state.co.us/Rest/GET/api/v2/telemetrystations/telemetrytimeseriesraw/?abbrev={}'.format(station_abbrev)
    # Append other parts
    # - station ID is required so put first with the question mark
    if output_format != '':
        url = "{}&format={}".format(url, output_format)
    if page_size != '':
        url = "{}&pageSize={}".format(url, page_size)
    if page_index != '':
        url = "{}&pageIndex={}".format(url, page_index)
    if param != '':
        url = "{}&parameter={}".format(url, param)
    if start_date != '':
        # start_date = '%2F'.join(start_date)
        url = "{}&startDate={}".format(url, start_date)
    if end_date != '':
        # end_date = '%2F'.join(end_date)
        url = "{}&endDate={}".format(url, start_date)
    if api_key != '':
        api_key = api_key.replace('/', '%2F')
        url = "{}&apiKey={}".format(url, api_key)
    return url


def check_input(app_data: dict) -> None:
    """
    Check input parameters and exit if not correct.
    """
    # Check the output format
    # - required argument so won't be blank
    output_format = get_app_data(app_data, 'OUTPUT_FORMAT')
    error_count = 0
    if (output_format != 'csv') and (output_format != 'json'):
        print_stderr('Output format ({}) is not valid, must be csv or json.'.format(output_format))
        error_count += 1

    # Append .csv or .json to the output file if not already at the end.
    output_file = get_app_data(app_data, 'OUTPUT_FILE')
    if not output_file.endswith(output_format):
        output_file = output_file + '.' + output_format
        app_data['OUTPUT_FILE'] = output_file

    # Check the format for start and end dates
    # - optional so could be blank
    start_date = get_app_data(app_data, 'START_DATE')
    if start_date is not None and (start_date != ''):
        if not check_date(start_date):
            print_stderr('Start date ({}) is not valid, must be in format: mm/dd/yyyy'.format(start_date))
            error_count += 1
    end_date = get_app_data(app_data, 'END_DATE')
    if end_date is not None and (start_date != ''):
        if not check_date(end_date):
            print_stderr('End date ({}) is not valid, must be in format: mm/dd/yyyy'.format(end_date))
            error_count += 1
    if error_count > 0:
        sys.exit(1)


def check_date(date_string: str) -> bool:
    """
    Determine if the date is an valid format mm/dd/yyyy.

    Args:
        date_string(str):  date string to check.

    Returns:
        bool: True if value, False if invalid.
    """
    parts = date_string.split('/')
    if len(parts) != 3:
        print_stderr('Date input ({}) is invalid.'.format(date_string))
        print_stderr('Dates must use format:  mm/dd/yyyy')
        return False
    return True


def format_output(lines: list) -> list:
    """
    The data received from the database returns a time format that is verbose.
    This function converts to standard ISO 8601 formats.
    """
    temp1 = []

    meas_date_time = lines[2].split(',')[2] if lines[2].split(',')[2] == 'measDateTime' else ''
    modified = lines[2].split(',')[7] if lines[2].split(',')[7] == 'modified' else ''
    meas_date_time_index = lines[2].split(',').index('measDateTime')
    modified_index = lines[2].split(',').index('modified')

    # Go through each line in the file
    for i, line in enumerate(lines):
        temp2 = []
        # Split the line by commas into a list of strings and go through each element
        for index, elem in enumerate(line.split(',')):
            # The next four slightly convoluted lines check to see if the measDateTime
            # and modified variables have been set (they exist), and if they do,
            # make sure to skip the first 3 lines of the data (they're metadata) and
            # double check that the index in the line of split strings is the
            # same as the original measDateTime and modified columns that are found. Then
            # replace the dates there with ISO 8601 dates with no 'T' in between the
            # date and time, and don't display anything faster than a second, or else
            # it will import weirdly in Excel.
            if meas_date_time != '' and i > 2 and index == meas_date_time_index:
                temp2.append(p.parse(elem).isoformat(sep=' ', timespec='minutes'))
            elif modified != '' and i > 2 and index == modified_index:
                temp2.append(p.parse(elem).isoformat(sep=' ', timespec='minutes'))
            else:
                # The element is not a date so just append to the temp list.
                temp2.append(elem)
        # Now join all the elements in the temp list into a string and append to temp1 list.
        # This way it's being put back the way it was originally, except for the extra date formatting.
        temp1.append(','.join(temp2))
    # Now that the outer for loop is finished, return the new list
    return temp1


def get_app_data(app_data: dict, key: str) -> object or None:
    """
    Get application data value from the application data dictionary.

    Args:
        app_data (dict):  Application data from command line.
        key (str):  Name of application data value.

    Returns:
        Object matching the requested key, or None if no value is defined.
    """
    try:
        value = app_data[key]
        # Value is defined so return it
        return value
    except KeyError:
        # Value is not defined
        return None


def parse_command_line() -> dict:
    """
    Parse the command line arguments, warn if they're incorrect, and assign them
    to global constants, since they won't change during this program.

    Returns:
        A dictionary containing the parsed values.
    """
    parser = argparse.ArgumentParser(description='Query the HydroBase web services for real-time 15-minute telemetry station data.')

    # Optional arguments.
    parser.add_argument('--output', metavar='filename', default='stdout',
                        help='Write the output to the specified file instead of stdout.')
    parser.add_argument('--startDate', metavar='start_date', default='',
                        help='The date to start the query in format:  mm/dd/yyyy')
    parser.add_argument('--endDate', metavar='end_date', default='',
                        help='The date to end the query in format: mm/dd/yyyy')
    parser.add_argument('--pageSize', metavar='page_size', default='',
                        help='The page size for the response, used in testing.')
    parser.add_argument('--apiKey', metavar='api_key', default='',
                        help='The API Key to increase response limit from web services.')

    # Required arguments.
    required = parser.add_argument_group('required arguments')
    required.add_argument('--abbrev', metavar='abbrev', help='The station abbreviation (ABBREV) identifier.',
                          required=True)
    required.add_argument('--parameter', nargs='+', metavar='param_name',
                          help='The measured parameter name(s), separated by spaces if more than one.', required=True)
    required.add_argument('--format', metavar='output_format',
                          help='Format for output: csv or json', required=True)

    # If no arguments are given, print help, and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    # Parse the command line
    args = parser.parse_args()

    # Save arguments in a dictionary and return to the calling code.
    app_data = {}
    app_data['STATION_ABBREV'] = args.abbrev
    # The following is a list
    app_data['PARAMETERS'] = args.parameter
    app_data['OUTPUT_FORMAT'] = args.format
    app_data['OUTPUT_FILE'] = args.output
    app_data['START_DATE'] = args.startDate
    app_data['END_DATE'] = args.endDate
    app_data['API_KEY'] = args.apiKey
    app_data['PAGE_SIZE'] = args.pageSize
    return app_data


def print_remaining(app_data: dict, param: str, page_count: int) -> None:
    """
    Have the first query and determined that the page count is greater than one.
    Since it is, have multiple pages and need to query the rest of the pages for both csv and json.
    print_remaining() prints the pages to stdout, and write_remaining writes the pages to a file.

    Args:
        app_data (dict): Application data from the command line.
        param (str): Parameter being processed.
        page_count (int): Page count being processed.

    Return:
        None
    """
    output_format = get_app_data(app_data, 'OUTPUT_FORMAT')
    for page_index in range(2, page_count + 1):
        print_stderr("Processing results page {}.".format(page_count))
        url = build_url(param, page_index)
        print_stderr("Request: {}".format(url))
        response = requests.get(url)

        if output_format == 'csv':
            lines = response.text.split('\r\n')
            print(*lines[3::], sep='\n')
        elif output_format == 'json':
            json_obj = json.loads(response.text)
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(json_obj["ResultList"])


def print_stderr(s: str) -> None:
    """
    Print a string to stderr.
    Do this for messages so that output can be redirected.

    Args:
        s (str): String to print.

    Returns:
        None
    """
    print(s, file=sys.stderr)


def process_csv(app_data: dict, param: str, first_page: bool, response: str) -> None:
    """
    Append page of results to csv output format.

    Args:
        app_data (dict): Application input from command line.
        param (str):  Parameter being read.
        first_page (bool): Whether the first page is being written.
        response (str):  Query response.

    Returns:
        None
    """
    print_stderr('Creating csv output format.')
    # response.text is a string, so can split on CRLF
    lines = response.split('\r\n')
    # Format the output of the response
    lines = format_output(lines)
    # Determine the amount of pages that the returned data was split into (if any)
    page_count = int(lines[1].split(',')[1])
    print_stderr("Processing results page {}.".format(page_count))
    output_file = get_app_data(app_data, 'OUTPUT_FILE')

    # Print straight to terminal if no --output argument was received
    if output_file == 'stdout':
        # Write the CSV headers
        print(lines[2])
        # Write the rest of the list from the first data index
        print(*lines[3::], sep='\n')
        # If more than one page, print them all
        if page_count > 1:
            print_remaining(app_data, param, page_count)

    # Otherwise, write everything but the first two indexes to the named file
    else:
        # First parameter (and its corresponding pages if any)
        if first_page:
            write_file(app_data, lines[2:], first_page=True, last_page=False)
            if page_count > 1:
                write_remaining(app_data, param, page_count)
        # Second parameter and beyond (and its corresponding pages if any)
        else:
            write_file(app_data, lines[3:], first_page=False, last_page=False)
            if page_count > 1:
                write_remaining(app_data, param, page_count)

        print_stderr('Data successfully received and written to file \'{}\'\n'.format(output_file))


def process_json(app_data: dict, param: str, response: str) -> None:
    """
    Append page of results to JSON output format.

    Args:
        app_data (dict): Application input from command line.
        param (str):  Parameter being read.
        response (str):  Query response.

    Returns:
        None
    """
    # Retrieve the data and put into a JSON object
    print_stderr('Creating json output format.')
    json_obj = json.loads(response)
    page_count = json_obj["PageCount"]
    print_stderr("Processing results page {}.".format(page_count))
    output_file = get_app_data(app_data, 'OUTPUT_FILE')
    parameters = get_app_data(app_data, 'PARAMETERS')
    # Printing to terminal here
    if output_file == 'stdout':
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(json_obj["ResultList"])

        if page_count > 1:
            print_remaining(app_data, param, page_count)
    # Writing to a file here
    else:
        if page_count == 1:
            if len(parameters) > 1:
                output_file = output_file + '_' + param
            write_file(app_data, json_obj["ResultList"], first_page=True, last_page=True)
            print_stderr('Data successfully received and written to file \'{}\'\n'.format(output_file))
        else:
            # If there are multiple parameters given, change the file name to
            # fileName_paramName to differentiate between them and write to separate files
            if len(parameters) > 1:
                output_file = output_file + '_' + param
            write_file(app_data, json_obj["ResultList"], first_page=True, last_page=False)
        if page_count > 1:
            write_remaining(app_data, param, page_count)
            print_stderr('Data successfully received and written to file \'{}\'\n'.format(output_file))


def run_batch(app_data: dict) -> None:
    """
    The principal function in the program.  Given the arguments specified on command line,
    fetch the data from the HydroBase web service and output in requested format.
    A single stationid can be specified, but multiple parameters can be requested.

    Args:
        app_data(dict): Dictionary of values from the command line.

    Returns:
        None
    """

    # Whether csv headers should be written at the top of output
    first_page = True

    parameters = get_app_data(app_data, 'PARAMETERS')
    for param in parameters:
        print_stderr('Fetching data for parameters {}...'.format(param))

        # Build the URL for requested query.
        # Query first to see if get back more than one page from the database.
        url = build_url(app_data, param, 1)
        headers = {'Accept-Encoding': 'gzip'}
        print_stderr("Request: {}".format(url))
        response = requests.get(url, headers=headers)

        # Through some means (usually incorrect parameter name) nothing was returned from the database
        if 'zero records from CDSS' in response.text:
            print_stderr('\n    parameter error {}: {}'.format(param, response.text))
            print_stderr('    {} not used in query\n'.format(param))
            continue

        output_format = get_app_data(app_data,'OUTPUT_FORMAT')
        if output_format == 'json':
            # Process JSON
            process_json(app_data, param, response.text)
        elif output_format == 'csv':
            # Process CSV
            process_csv(app_data, param, first_page, response.text)
            first_page = False
        else:
            print_stderr('Unknown output format {}'.format(output_fromat))


def write_remaining(app_data: dict, param: str, page_count: int) -> None:
    """
    The data returned has more than one page, so write the rest of the pages to file.

    Args:
        app_data (dict):  Application data from command line.
        param (str):  Data parameter.
        page_count (int):  Page being processed.

    Returns:
        None
    """
    output_format = get_app_data(app_data, 'OUTPUT_FORMAT')
    for page_index in range(2, page_count + 1):
        url = build_url(app_data, param, page_index)
        print_stderr("Request: {}".format(url))
        print_stderr("Request: {}".format(url))
        response = requests.get(url)

        if output_format == 'csv':
            lines = response.text.split('\r\n')
            lines = format_output(lines)
            write_file(app_data, lines[3:], first_page=False, last_page=False)
        elif output_format == 'json':
            json_obj = json.loads(response.text)
            if page_index == page_count:
                write_file(app_data, json_obj["ResultList"], first_page=False, last_page=True)
            else:
                write_file(app_data, json_obj["ResultList"], first_page=False, last_page=False)


def write_file(app_data: dict, lines: list, first_page: bool, last_page: bool) -> None:
    """
    Write the data to a file, appending if necessary.

    Args:
        app_data (dict): Dictionary of application data.
        lines (list): Lines to write to the file.
        first_page (bool): Indicates if writing the first page.
        last_page (bool): Indicates if writing the last page.

    Returns:
        None
    """

    output_file = get_app_data(app_data, 'OUTPUT_FILE')
    output_format = get_app_data(app_data, 'OUTPUT_FORMAT')

    with open(output_file, 'a') as outputFile:
        if output_format == 'csv':
            # Write CSV
            # Write the CSV to file
            for item in lines:
                outputFile.write(item + '\n')
        elif output_format == 'json':
            # Write JSON
            # Write the beginning of the JSON object on the first page
            if first_page:
                outputFile.write('{ \"ResultList\": [')
            # Get the number of data lines in the page to determine if at the last line
            page_length = len(lines)
            index = 0
            for item in lines:
                # If on the last line of the page AND the last page, end
                # the list from ResultList (don't want a comma at the end).
                if index == page_length - 1 and last_page:
                    outputFile.write(json.dumps(item, indent=4) + '\n')
                else:
                    outputFile.write(json.dumps(item, indent=4) + ',\n')
                index = index + 1
            # Double check it's the last page and finish writing the JSON object. After
            # that the file will be closed.
            if last_page:
                outputFile.write(']}')


def main() -> None:
    """
    Main function for the program.
    """

    # Parse the command line
    app_data = parse_command_line()

    # Check command line parameters
    check_input(app_data)

    # Perform the web service request in batch mode
    run_batch(app_data)


if __name__ == '__main__':
    """
    Main entry point for the program.
    """
    # Run the main function.
    main()
