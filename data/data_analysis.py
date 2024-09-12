# General Data Packages
import numpy as np
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

# Average Prices
# We build the series ID as AP{seasonal_adjustment}{area_code}{item_code}

## Seasonal Adjustment: S (seasonally adjusted) or U (unadjusted)
avgp_seasonal_adjustment = ["S", "U"]

## Area-Item Codes Importing
avgp_area_df = area_item_importing('area_codes_avgp.area')
avgp_item_df = area_item_importing('item_codes_avgp.item')

AVGP_series = [f"AP{sa}{area}{item}" for sa in avgp_seasonal_adjustment 
                                     for area in avgp_area_df['area_code'] 
                                     for item in avgp_item_df['item_code']]

# CPI Urban Consumers
# We build the series ID as CU{seasonal_adjustment}{periodicity}{area_code}{base_code}{item_code}

## Seasonal Adjustment: S (seasonally adjusted) or U (unadjusted)
cpicu_seasonal_adjustment = ["S", "U"]

## Periodicity: S (semi-annual) or R (monthly)
cpicu_periodicity = ["R", "S"]

## Base: 1982-1984=100 (S), alternate (A)
cpicu_base = ["S", "A"]

## Area-Item Codes Importing
cpicu_area_df = area_item_importing('area_codes_cpicu.area')
cpicu_item_df = area_item_importing('item_codes_cpicu.item')

print(bls_data_request(['CWSR0000SA111211'], 2010, 2020))
print(bls_data_request(['CUUR0000SA0L1E', 'CWSR0000SA111211'], 2010, 2020))

CPICU_series = [f"CU{sa}{per}{area}{base}{item}" for sa in cpicu_seasonal_adjustment 
                                                 for per in cpicu_periodicity 
                                                 for area in cpicu_area_df['area_code'] 
                                                 for base in cpicu_base 
                                                 for item in cpicu_item_df['item_code']]