import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import global_variables as gvar

start_year = 2000
end_year = 2018
inflation_adjustment_year = 2019
year_range = range(start_year,end_year+1)

#Import FRED CPI Inflation Adjustment Data
fred_prefix = 'https://api.stlouisfed.org/fred/series/observations?series_id='
fred_api = gvar.fred_api_key
fred_series = 'CPIAUCSL'
fred_url = fred_prefix + fred_series + '&api_key='+ fred_api + '&file_type=json&frequency=a'

year_to_cpi = dict()
for o in list(json_data['observations']):
    year = str(o['date'][0:4])
    cpi = o['value']
    year_to_cpi[year] = cpi

#Create a DataFrame with CPIs and Inflation Adjustments
inf = pd.DataFrame(columns=[str(i) for i in year_range])
cpis = [year_to_cpi[str(i)] for i in year_range]
inf.loc[0] = cpis
adjustment_denom = float(inf.loc[0,str(inflation_adjustment_year)])
iafs = [float(cpis[i])/adjustment_denom for i in range(len(year_range))]
inf.loc[1] = iafs

def get_tags(sa):
    return ['NG.N3050'+sa+'3.A','NG.N3010'+sa+'3.A','NG.N3020'+sa+'3.A']

def get_elec_tags(sa):
    return ['SEDS.ESRCD.'+sa+'.A','SEDS.ESCCD.'+sa+'.A']