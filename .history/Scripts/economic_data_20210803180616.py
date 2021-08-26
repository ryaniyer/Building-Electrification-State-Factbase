import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import global_variables as gvar

start_year = 2000
end_year = 2020

fred_prefix = 'https://api.stlouisfed.org/fred/series/observations?series_id='
fred_api = 'd00618cf19b6ee0f138dbd06ad3b89da'
fred_series = 'CPIAUCSL'
fred_url = fred_prefix + fred_series + '&api_key='+ fred_api + '&file_type=json&frequency=a'

