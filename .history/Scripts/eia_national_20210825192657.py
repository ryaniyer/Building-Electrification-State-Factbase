import pandas as pd
import requests
import numpy as np
import global_variables as apis

#api_key = 'c539dd02b98ef2d57482dfe39f7d6980'
#my_url = 'http://api.eia.gov/series/?api_key=' + api_key + '&series_id='
api_key = apis.eia_api_key

datasets = []
#US CO2 Emissions by Fuel Source:
emit_fuel_datasets = ['TOTAL.CKTCEUS.A','TOTAL.NNTCEUS.A','TOTAL.PMTCEUS.A']
#CO2 Electric Power Sector Emissions By Source:
electricity_emit_datasets = ['TOTAL.TXEIEUS.A','TOTAL.CLEIEUS.A','TOTAL.NNEIEUS.A','TOTAL.PAEIEUS.A']
#CO2 Emissions from Buildings Sector:
com_sector_datasets = ['TOTAL.TECCEUS.A','TOTAL.ESCCEUS.A','TOTAL.NNCCEUS.A','TOTAL.PMCCEUS.A']
res_sector_datasets = ['TOTAL.TERCEUS.A','TOTAL.ESRCEUS.A','TOTAL.NNRCEUS.A','TOTAL.PARCEUS.A']
us_co2_datasets = emit_fuel_datasets + electricity_emit_datasets + com_sector_datasets + res_sector_datasets
#Natural Gas Use by Sector:
ng_sector_datasets = ['TOTAL.NGTCPUS.A','TOTAL.NGEIPUS.A','TOTAL.NGACPUS.A','TOTAL.NGINPUS.A','TOTAL.NGCCPUS.A','TOTAL.NGRCPUS.A']
#Natural Gas Number of Customers:
ng_customer_datasets = ['NG.NA1501_NUS_8.A']
#Electricity and Gas Prices:
ng_price_datasets = ['NG.N3010US3.A','NG.N3020US3.A','NG.N3050US3.A']
elec_price_datasets = ['ELEC.PRICE.US-RES.A','ELEC.PRICE.US-COM.A']
price_datasets = ng_price_datasets + elec_price_datasets
all_data = us_co2_datasets + price_datasets + ng_sector_datasets + ng_customer_datasets

def return_national_EIA_data(start_year, end_year, datasets):
    start_year = start_year
    end_year = end_year
    years = range(start_year, end_year+1)
    final_output = pd.DataFrame(index=years)
    final_output.index.name = 'Year'

    for d in datasets:
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