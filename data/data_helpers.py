# General Data Packages
import pandas as pd


# BLS Importing
import requests
import json
import dotenv as env
import os

env.load_dotenv()
BLS_API_KEY = os.getenv('BLS_API_KEY')

def area_item_importing(file_name):
    file = open(file_name, 'r')
    codes = list(map(lambda x: tuple(x.split("\t")), file.read().splitlines()))
    file.close()
    return pd.DataFrame(codes[1:], columns=codes[0])


def bls_data_request(series_ids, start_year, end_year):
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": series_ids, 
                       "startyear": start_year, 
                       "endyear": end_year, 
                       "registrationKey" : BLS_API_KEY})
    
    p = requests.post(f'https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_dict = json.loads(p.text)['Results']

    series_dfs = []
    for series in json_dict['series']:
        series_id = series['seriesID']
        years = []
        period_names = []
        values = []
        for item in series['data']:
            years.append(item['year'])
            period_names.append(item['periodName'])
            values.append(item['value'])
        
        series_dfs.append(pd.DataFrame({'Year': years, 'Period': period_names, series_id: values}))

    # Merge the list of DataFrames
    merged_df = pd.concat(series_dfs, ignore_index=True)

    return merged_df
