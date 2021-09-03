import time
start_time = time.time()
import eia_national
import eia_state
import epa_nei
import tessum
import acs_housing
import economic_data

import pandas as pd
import os
import shutil

restart_national = False
restart_national_natgas = False
restart_national_air_quality = False

states = ["AL", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
state_names = ["Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia","Florida", "Georgia", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
us_state_abbrev = {'the United States':'US','Alabama': 'AL','Alaska': 'AK','American Samoa': 'AS','Arizona': 'AZ','Arkansas': 'AR','California': 'CA','Colorado': 'CO', 'Connecticut': 'CT','Delaware': 'DE','District of Columbia': 'DC', 'Florida': 'FL','Georgia': 'GA','Guam': 'GU','Hawaii': 'HI', 'Idaho': 'ID','Illinois': 'IL','Indiana': 'IN','Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA', 'Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO', 'Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY','North Carolina': 'NC', 'North Dakota': 'ND','Northern Mariana Islands':'MP','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA','Puerto Rico': 'PR', 'Rhode Island': 'RI','South Carolina': 'SC','South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX','Utah': 'UT', 'Vermont': 'VT','Virgin Islands': 'VI','Virginia': 'VA','Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'}
abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))

def folder_refresh(pathname):
    try:
        shutil.rmtree(pathname)
    except:
        None
    os.mkdir(pathname)


if(restart_national):
    #National Folder Creation:
    folder_refresh('./State Factbase/Spreadsheets/National Data')
    
if(restart_national_natgas):
    folder_refresh('../State Factbase/Spreadsheets/National Data/Natural Gas')
    #AGA Export:
    aga_source = '../Static/Natural_Gas/1972-2019 AGA Construction Expenses.xlsx'
    aga_dest = '../State Factbase/Spreadsheets/National Data/Natural Gas/AGA Construction Expenses.xlsx'
    shutil.copy(aga_source, aga_dest)
    #EIA Form 176 Export:
    import eia176
    df_eia176 = eia176.get_national_metric_totals()
    df_eia176.to_csv('../State Factbase/Spreadsheets/National Data/Natural Gas/EIA Form 176.csv',index=False)
    #PHMSA Export:
    import phmsa 
    df_mmiles = phmsa.get_national_mileage()
    df_mmiles.to_csv('../State Factbase/Spreadsheets/National Data/Natural Gas/PHMSA Main Mileage.csv',index=False)
if(restart_national_air_quality):
    folder_refresh('../State Factbase/Spreadsheets/National Data/Air Quality')
    df_nat_tessum = tessum.get_national_tessum()
    df_nat_tessum.to_csv('../State Factbase/Spreadsheets/National Data/Air Quality/National PM25 Racial Disparities.csv',index=False)
