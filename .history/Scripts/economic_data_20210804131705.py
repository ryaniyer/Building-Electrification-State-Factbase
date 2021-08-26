import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests

start_year = 2000
end_year = 2019
inflation_adjustment_year = 2019
year_range = range(start_year,end_year+1)

api_key = 'c539dd02b98ef2d57482dfe39f7d6980'
my_url = 'http://api.eia.gov/series/?api_key=' + api_key + '&series_id='


#Import FRED CPI Inflation Adjustment Data
fred_prefix = 'https://api.stlouisfed.org/fred/series/observations?series_id='
fred_api = 'd00618cf19b6ee0f138dbd06ad3b89da'
fred_series = 'CPIAUCSL'
fred_url = fred_prefix + fred_series + '&api_key='+ fred_api + '&file_type=json&frequency=a'
r = requests.get(fred_url)
json_data = r.json()

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
    #Estimate DC City Gate using Maryland 
    #(idea from "Who Will Pay For Legacy Utility Costs" methodology)
    if(sa=='DC'):
        tags = ['NG.N3050'+'MD'+'3.A','NG.N3010'+sa+'3.A','NG.N3020'+sa+'3.A',
                'SEDS.ESRCD.'+sa+'.A','SEDS.ESCCD.'+sa+'.A']
    else:
        tags = ['NG.N3050'+sa+'3.A','NG.N3010'+sa+'3.A','NG.N3020'+sa+'3.A',
                'SEDS.ESRCD.'+sa+'.A','SEDS.ESCCD.'+sa+'.A']
    return tags

def return_state_EIA_data(start_year, end_year, sa, tags):
    years = range(start_year, end_year+1)
    final_output = pd.DataFrame(index=years)
    final_output.index.name = 'Year'
    for d in tags:
        try:
            r = requests.get(my_url + d)
        except:
            print('\n\nError requesting the following API Key: ', d,'\n\n')
        json_data = r.json()
        json_data = json_data['series'][0]
        value_name = json_data['name'] + ' (' + json_data['units'] +')'
        json_data['data']
        temp_dict = dict()
        for pair in json_data['data']:
            temp_dict[str(pair[0])] = pair[1]
        temp_col = []
        for year in years:
            temp_val = ''
            if(str(year) in temp_dict.keys()):
                temp_val = temp_dict[str(year)]  
            temp_col.append(temp_val)
        final_output[value_name] = temp_col
    return final_output.T

def get_energy_price_data(sa):
    df = return_state_EIA_data(start_year,end_year,sa,get_tags(sa))
    inf_adj = list(inf.iloc[1,:])
    ia_note = '(Inflation Adjusted to ' + str(inflation_adjustment_year) + ' USD)'
    df.loc['Natural Gas Citygate Price $/Tcf ' + ia_note] = [inf_adj[i] * list(df.iloc[0])[i] for i in range(len(inf_adj))]
    df.loc['Natural Gas Residential Price $/Tcf ' + ia_note] = [inf_adj[i] * list(df.iloc[1])[i] for i in range(len(inf_adj))]
    df.loc['Natural Gas Commercial Price $/Tcf ' + ia_note] = [inf_adj[i] * list(df.iloc[2])[i] for i in range(len(inf_adj))]
    df.loc['Electricity Residential Price $/MMBtu ' + ia_note] = [inf_adj[i] * list(df.iloc[3])[i] for i in range(len(inf_adj))]
    df.loc['Electricity Commercial Price $/MMBtu ' + ia_note] = [inf_adj[i] * list(df.iloc[4])[i] for i in range(len(inf_adj))]
    df.loc['Inflation Adjustment Factor (' + str(inflation_adjustment_year) + ')'] = inf_adj
    return df