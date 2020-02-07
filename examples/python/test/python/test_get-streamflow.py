import filecmp
import glob
import os
import subprocess


PARAMETER = ['DISCHRG', 'GAGE_HT', 'AIRTEMP']
START_DATE = ['06/01/2019', '01/01/2015', '01/01/2019']
END_DATE = ['12/01/2019', '01/06/2015', '01/01/2020']


def compare_csv_files():

    for filename in glob.glob('results/*'):
        os.remove(filename)

    results = 'results/data{}.csv'
    expected = ['expected-results/TEST_SID=PLAKERCO_P=DISCHRG_F=CSV_SD=06012019_ED=12012019_O=DATA.txt', \
                'expected-results/TEST_SID=PLAKERCO_P=GAGE_HT_F=CSV_SD=01012015_ED=01062015_O=DATA.txt', \
                'expected-results/TEST_SID=PLAKERCO_P=AIRTEMP_F=CSV_SD=01012019_ED=01012020_O=DATA.txt']

    for number in range(3):
        subprocess.run(['python3',
                        '../../src/get-streamflow.py',
                        '-sid','PLAKERCO',
                        '-p','{}'.format(PARAMETER[number]),
                        '-f','csv',
                        '-sd','{}'.format(START_DATE[number]),
                        '-ed','{}'.format(END_DATE[number]),
                        '-o','data'])
        try:
            subprocess.run(['mv', 'data.csv', results.format(number)])
        except FileNotFoundError:
            print('File does not exist!')

        outcome = filecmp.cmp(expected[number], results.format(number))

        assert outcome


def compare_json_files():
    
    results = 'results/data{}.json'
    expected = ['expected-results/TEST_SID=PLAKERCO_P=DISCHRG_F=JSON_SD=06012019_ED=12012019_O=DATA.json', \
                'expected-results/TEST_SID=PLAKERCO_P=GAGE_HT_F=JSON_SD=01012015_ED=01062015_O=DATA.json', \
                'expected-results/TEST_SID=PLAKERCO_P=AIRTEMP_F=JSON_SD=01012019_ED=01012020_O=DATA.json']

    for number in range(3):
        subprocess.run(['python3',
                        '../../src/get-streamflow.py',
                        '-sid','PLAKERCO',
                        '-p','{}'.format(PARAMETER[number]),
                        '-f','json',
                        '-sd','{}'.format(START_DATE[number]),
                        '-ed','{}'.format(END_DATE[number]),
                        '-o','data'])
        try:
            subprocess.run(['mv', 'data.json', results.format(number)])
        except FileNotFoundError:
            print('File does not exist!')

        outcome = filecmp.cmp(expected[number], results.format(number))

    assert outcome


if __name__ == '__main__':
    print('  Testing CSV files...')
    compare_csv_files()
    
    print('  Testing JSON files...')
    compare_json_files()

    print('  All tests passed successfully!')

