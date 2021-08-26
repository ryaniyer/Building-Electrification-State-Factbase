import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import global_variables as gvar

start_year = 2000
end_year = 2018
year_range = range(start_year,end_year+1)

#Import FRED CPI Inflation Adjustment Data
fred_prefix = 'https://api.stlouisfed.org/fred/series/observations?series_id='
fred_api = gvar.fred_api_key
fred_series = 'CPIAUCSL'
fred_url = fred_prefix + fred_series + '&api_key='+ fred_api + '&file_type=json&frequency=a'

