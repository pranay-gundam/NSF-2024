# General Data Packages
import numpy as np
import pandas as pd

# BLS Importing
import requests
import json
import prettytable
import dotenv as env
import os

env.load_dotenv()
BLS_API_KEY = os.getenv('BLS_API_KEY')

# Average Prices
## We build the series ID as AP{seasonal_adjustment}{area_code}{item_code}

# Seasonal Adjustment: S or U
seasonal_adjustment = "S"

## Area Codes Importing
avgp_area_code_file = open('area_codes_avgp.area', 'r')
avgp_area_codes = list(map(lambda x: tuple(x.split("\t")), avgp_area_code_file.read().splitlines()[1:]))
avgp_area_code_file.close()
avgp_area_codes_dict = {code: name for code, name in avgp_area_codes}

## Item Codes Importing
avgp_item_code_file = open('item_codes_avgp.item', 'r')
avgp_item_codes = list(map(lambda x: tuple(x.split("\t")), avgp_item_code_file.read().splitlines()[1:]))
avgp_item_code_file.close()
avgp_item_codes_dict = {code: name for code, name in avgp_item_codes}

"""
headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": ['CUUR0000SA0','SUUR0000SA0'],"startyear":"2011", "endyear":"2014"})
p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/{BLS_API_KEY}', data=data, headers=headers)
json_data = json.loads(p.text)
for series in json_data['Results']['series']:
    x=prettytable.PrettyTable(["series id","year","period","value","footnotes"])
    seriesId = series['seriesID']
    for item in series['data']:
        year = item['year']
        period = item['period']
        value = item['value']
        footnotes=""
        for footnote in item['footnotes']:
            if footnote:
                footnotes = footnotes + footnote['text'] + ','
        if 'M01' <= period <= 'M12':
            x.add_row([seriesId,year,period,value,footnotes[0:-1]])
    output = open(seriesId + '.txt','w')
    output.write (x.get_string())
    output.close()
"""