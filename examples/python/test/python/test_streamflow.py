import filecmp     # For comparing two files to see if they are different
import glob        # Finds all pathnames matching a specified pattern
import os          # Used for miscellaneous operating system inferfaces
import subprocess  # Spawn new processes, connect to their pipes, and get the return code


# Set up the three query arrays for the testing
PARAMETER = ['DISCHRG', 'GAGE_HT', 'AIRTEMP']
START_DATE = ['06/01/2019', '01/01/2015', '01/01/2019']
END_DATE = ['12/01/2019', '01/06/2015', '01/01/2020']
GREEN = '\033[92m'
BLUE = '\033[94m'
FAIL = '\033[91m'
ENDC = '\033[0m'


# Compares all three CSV file tests to the expected results performed earlier
def compare_csv_files():
    # Delete all the files in the results file
    for filename in glob.glob('results/*'):
        os.remove(filename)
    # Set up the results string so the return file is put into the results directory
    results = 'results/data{}.csv'
    expected = ['expected-results/TEST_PLAKERCO_DISCHRG_CSV_06012019_12012019_DATA.csv',
                'expected-results/TEST_PLAKERCO_GAGE_HT_CSV_01012015_01062015_DATA.csv',
                'expected-results/TEST_PLAKERCO_AIRTEMP_CSV_01012019_01012020_DATA.csv']
    # Go through each index in the query arrays above, and run the streamflow program
    # with each of the elements
    for number in range(1, 4):
        subprocess.run(['python3',
                        '../../src/streamflow.py',
                        '--abbrev','PLAKERCO',
                        '--parameter','{}'.format(PARAMETER[number - 1]),
                        '--format','csv',
                        '--startDate','{}'.format(START_DATE[number - 1]),
                        '--endDate','{}'.format(END_DATE[number - 1]),
                        '--output','data'])
        # Try to mv the newly created file with the returned data and move it into the
        # results directory with the number from 1 - 3 for each test performed
        try:
            subprocess.run(['mv', 'data.csv', results.format(number)])
            outcome = filecmp.cmp(expected[number - 1], results.format(number))
            assert outcome
        except FileNotFoundError:
            print('\n  {}Error: File does not exist!{}\n'.format(FAIL, ENDC))
        except AssertionError:
            print('\n  {}Error: The files do not match. Test failed{}\n'.format(FAIL, ENDC))


# Perform the exact same test with the JSON formatted data
def compare_json_files():
    
    results = 'results/data{}.json'
    expected = ['expected-results/TEST_PLAKERCO_DISCHRG_JSON_06012019_12012019_DATA.json',
                'expected-results/TEST_PLAKERCO_GAGE_HT_JSON_01012015_01062015_DATA.json',
                'expected-results/TEST_PLAKERCO_AIRTEMP_JSON_01012019_01012020_DATA.json']

    for number in range(1, 4):
        subprocess.run(['python3',
                        '../../src/streamflow.py',
                        '--abbrev','PLAKERCO',
                        '--parameter','{}'.format(PARAMETER[number - 1]),
                        '--format','json',
                        '--startDate','{}'.format(START_DATE[number - 1]),
                        '--endDate','{}'.format(END_DATE[number - 1]),
                        '--output','data'])
        try:
            subprocess.run(['mv', 'data.json', results.format(number)])
            outcome = filecmp.cmp(expected[number - 1], results.format(number))
            assert outcome
        except FileNotFoundError:
            print('\n  {}Error: File does not exist!{}\n'.format(FAIL, ENDC))
        except AssertionError:
            print('\n  {}Error: The files do not match. Test failed{}\n'.format(FAIL, ENDC))


if __name__ == '__main__':
    print('\n  {}Testing CSV files{}\n'.format(BLUE, ENDC))
    compare_csv_files()

    print('  {}Testing JSON files{}\n'.format(BLUE, ENDC))
    compare_json_files()

    print('  {}All tests passed successfully!{}'.format(GREEN, ENDC))

