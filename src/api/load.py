# This file handles the connection to the Ergast API

# We require the status table, the driver table, the races table, circuits table, qualifying table, results table, 
import json, xmltodict, requests
import pandas as pd

# Check if data in cache
def check_cache(filename:str):
    # Try and open the file with the cached API data, return None if it does not exist
    try:
        with open(filename, 'r') as file:
            print(f'Fetched data from cache at {filename}.')
            return json.load(file)
    except(FileNotFoundError, json.JSONDecodeError) as e:
        print(f'File not found: {e}')
        return None

"""
    All functions contain parameter 'update'. When true the API endpoint is fetched whether cached file exists or not
    All functions return a dataframe representation of xml response from API endpoint /endpoint (status, driver, circuits, etc.)
"""
class GetAPIData:
    BASE_URL = 'http://ergast.com/api/f1'

    def get_finish_status(self, update:bool=False):
        status_json = check_cache('src/cache/status.json')

        if status_json == None or update:
            print('Fetching from API...')
            status = requests.get(self.BASE_URL + '/status?limit=137')
            data = status.text
            status_dict = xmltodict.parse(data) # Converting to python dict
            status_json = status_dict['MRData']['StatusTable']['Status'] # Extracting the data we need
            # Write to cache for future calls
            with open('src/cache/status.json', 'w') as file:
                json.dump(status_json, file)
        return pd.DataFrame.from_dict(status_json)

    def get_driver_details(self, update:bool=False):
        drivers_json = check_cache('src/cache/drivers.json')

        if drivers_json == None or update:
            print('Fetching from API...')
            drivers = requests.get(self.BASE_URL + '/drivers?limit=857')
            data = drivers.text
            drivers_dict = xmltodict.parse(data) # Converting to python dict
            drivers_json = drivers_dict['MRData']['DriverTable']['Driver'] # Extracting the data we need
            # Write to cache for future calls
            with open('src/cache/drivers.json', 'w') as file:
                json.dump(drivers_json, file)
        return pd.DataFrame.from_dict(drivers_json)

    def get_results_details(self, update:bool=False):
        results_json = check_cache('src/cache/results.json')

        if results_json == None or update:
            print('Fetching from API...')
            results = requests.get(self.BASE_URL + '/results')
            data = results.text
            results_dict = xmltodict.parse(data) # Converting to python dict
            results_json = results_dict#['MRData']['DriverTable']['Driver'] # Extracting the data we need
            # Write to cache for future calls
            with open('src/cache/results.json', 'w') as file:
                json.dump(results_json, file)
        return pd.DataFrame.from_dict(results_json)

getData = GetAPIData()
getData.get_results_details()
