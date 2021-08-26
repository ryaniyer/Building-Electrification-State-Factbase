from Scripts import eia_national
from Scripts import eia_state
from Scripts import epa_nei
from Scripts import tessum
from Scripts import acs_housing

import pandas as pd
import os
import shutil

restart = False
restart_national = False
restart_national_natgas = False
restart_states = False
restart_states_EIA = False
restart_states_air_quality = False
restart_states_infrastructure = False
restart_states_economics = True

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

if(restart):
    folder_refresh('./State Factbook')
    folder_refresh('./State Factbook/National Data')
    folder_refresh('./State Factbook/State-Level Data')

if(restart_national):
    #National Folder Creation:
    folder_refresh('./State Factbook/National Data')
    
    if(restart_national_natgas):
        folder_refresh('./State Factbook/National Data/Natural Gas')
        #AGA Export:
        aga_source = './Static/Natural_Gas/1972-2019 AGA Construction Expenses.xlsx'
        aga_dest = './State Factbook/National Data/Natural Gas/AGA Construction Expenses.xlsx'
        shutil.copy(aga_source, aga_dest)


#State-Level Folder Creation:
for s in state_names:
    sa = us_state_abbrev[s]
    path = './State Factbook/State-Level Data/'+str(s)

    if(restart_states):
        folder_refresh(path)
    
    if(restart_states_EIA):
        #State-Level EIA Data Export
        df_temp = eia_state.return_state_EIA_data(1970,2020,us_state_abbrev[s])
        df_temp.T.to_csv(path+'/'+s+'_EIA_SEDS_Data.csv')

    if(restart_states_air_quality):
        #Make Air Quality Folder:
        folder_refresh(path+'/Air Quality')
        #EPA NEI Data Export:
        df_sector, df_type, df = epa_nei.get_EPA_NEI_AllSectors_dfs(sa)
        with pd.ExcelWriter(path+'/Air Quality/'+s+' EPA Emissions Data.xlsx') as writer:  
            df_sector.to_excel(writer, sheet_name='By Sector')
            df_type.to_excel(writer, sheet_name='By Pollutant')
            df.to_excel(writer, sheet_name='By County')
        #Tessum Data Export:
        df_state, df_cities = tessum.get_state_tessum(sa)
        with pd.ExcelWriter(path+'/Air Quality/'+s+' PM25 Racial Disparities.xlsx') as writer:  
            df_state.to_excel(writer, sheet_name='State-Level')
            df_cities.to_excel(writer, sheet_name='City-Level')

    if(restart_states_infrastructure):
       folder_refresh(path+'/Buildings Infrastructure')
        
        df_infrastructure = acs_housing.get_state_all_data(sa)
        df_rentown, df_yrblt, df_units, df_hf, df_rooms = acs_housing.get_state_subsets(sa)
        df_infrastructure.to_csv(path+'/Buildings Infrastructure/'+sa+' All Buildings Data.csv')
        df_rentown.to_csv(path+'/Buildings Infrastructure/'+sa+' Building Tenure Data.csv')
        df_yrblt.to_csv(path+'/Buildings Infrastructure/'+sa+' Building Vintage Data.csv')
        df_units.to_csv(path+'/Buildings Infrastructure/'+sa+' Building Type Data.csv')
        df_hf.to_csv(path+'/Buildings Infrastructure/'+sa+' Building Heating Fuel Data.csv')
        df_rooms.to_csv(path+'/Buildings Infrastructure/'+sa+' Building Rooms Data.csv')

    #os.mkdir(path+'/Emissions')
    #os.mkdir(path+'/Energy Use')

    if(restart_states_economics):
        try:
            shutil.rmtree(path+'/Energy Economics')
        except:
            None
        os.mkdir(path+'/Energy Economics')

        df_h_income = acs_housing.get_state_income_data(sa)
        df_h_income.to_csv(path+'/Energy Economics/'+sa+' Household Incomes.csv')

    #os.mkdir(path+'/Energy Economics')
    #os.mkdir(path+'/Natural Gas')

    print('Finished loading ', s)
