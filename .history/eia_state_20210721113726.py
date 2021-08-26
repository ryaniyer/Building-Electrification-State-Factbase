import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)
import numpy as np
from datetime import date
import matplotlib.ticker as ticker
from PyPDF2 import PdfFileMerger, PdfFileReader
import scipy.stats
pd.set_option('display.max_columns', None)

api_key = 'c539dd02b98ef2d57482dfe39f7d6980'
my_url = 'http://api.eia.gov/series/?api_key=' + api_key + '&series_id='

def get_data_tags(sa):
    #State-Level CO2 Emissions by Fuel Source:
    emit_fuel_datasets = ['EMISS.CO2-TOTV-TT-CO-' + sa + '.A','EMISS.CO2-TOTV-TT-NG-'+sa+'.A','EMISS.CO2-TOTV-TT-PE-'+sa+'.A']
    #Natural Gas by Sector:
    ng_sector_datasets = ['SEDS.NGRCP.'+sa+'.A','SEDS.NGCCP.'+sa+'.A', 'SEDS.NGICP.'+sa+'.A', 'SEDS.NGEIP.'+sa+'.A']
    #Natural Gas Emissions by Sector:
    ng_sector_emit_datasets = ['EMISS.CO2-TOTV-RC-NG-'+sa+'.A','EMISS.CO2-TOTV-CC-NG-'+sa+'.A','EMISS.CO2-TOTV-IC-NG-'+sa+'.A']
    #State-Level Emissions by Sector:
    emit_sector_datasets = ['EMISS.CO2-TOTV-RC-TO-'+sa+'.A','EMISS.CO2-TOTV-CC-TO-'+sa+'.A', 'EMISS.CO2-TOTV-IC-TO-'+sa+'.A', 'EMISS.CO2-TOTV-TC-TO-'+sa+'.A','EMISS.CO2-TOTV-EC-NG-'+sa+'.A']
    #Population:
    pop_datasets = ['SEDS.TPOPP.'+sa+'.A']
    #Natural Gas Prices 
    ng_price_datasets = ['NG.N3050'+sa+'3.A','NG.N3010'+sa+'3.A','NG.N3020'+sa+'4.A','NG.N3020'+sa+'3.A']
    
    return ng_sector_datasets + emit_fuel_datasets + ng_sector_emit_datasets + emit_sector_datasets + pop_datasets + ng_price_datasets

def return_state_EIA_data(start_year, end_year, sa):
    start_year = start_year
    end_year = end_year
    years = range(start_year, end_year+1)
    final_output = pd.DataFrame(index=years)
    final_output.index.name = 'Year'
    all_data = get_data_tags(sa)
    for d in all_data:
        r = requests.get(my_url + d)
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

    return final_output

if(__name__ == "__main__"):
    None