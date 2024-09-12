# Data Helpers
from data_helpers import *


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

CPICU_series = [f"CU{sa}{per}{area}{base}{item}" for sa in cpicu_seasonal_adjustment 
                                                 for per in cpicu_periodicity 
                                                 for area in cpicu_area_df['area_code'] 
                                                 for base in cpicu_base 
                                                 for item in cpicu_item_df['item_code']]

# File path
cpicu_file_path = 'CPICU_codes.txt'

# Write the list to a text file
with open(cpicu_file_path, mode='w') as file:
    for series in CPICU_series:
        file.write(series + '\n')


# File path
avgp_file_path = 'AVGP_codes.txt'

# Write the list to a text file
with open(avgp_file_path, mode='w') as file:
    for series in AVGP_series:
        file.write(series + '\n')
