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

#The states variable is set to work for the 48 continental states + DC
states = ["AL", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
state_names = ["Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia","Florida", "Georgia", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
us_state_abbrev = {'the United States':'US','Alabama': 'AL','Alaska': 'AK','American Samoa': 'AS','Arizona': 'AZ','Arkansas': 'AR','California': 'CA','Colorado': 'CO', 'Connecticut': 'CT','Delaware': 'DE','District of Columbia': 'DC', 'Florida': 'FL','Georgia': 'GA','Guam': 'GU','Hawaii': 'HI', 'Idaho': 'ID','Illinois': 'IL','Indiana': 'IN','Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA', 'Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO', 'Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY','North Carolina': 'NC', 'North Dakota': 'ND','Northern Mariana Islands':'MP','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA','Puerto Rico': 'PR', 'Rhode Island': 'RI','South Carolina': 'SC','South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX','Utah': 'UT', 'Vermont': 'VT','Virgin Islands': 'VI','Virginia': 'VA','Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'}
abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))

#Update with most recent year for which EIA has data:
eia_year = 2020

#Set the following variables tor true for desired restart:
#   Restarts the entire Spreadsheets/States folder
restart_all_states = False
#   Restarts the state-level air quality folder
restart_states_air_quality = False
#   Restarts the state-level infrastructure folder
restart_states_infrastructure = False
#   Restarts the state-level Energy Economics folder
restart_states_economics = False
#   Restarts the state-level Natural Gas folder
restart_states_natgas = False
#   Restarts the state-level CO2 Emissions folder
restart_states_co2 = False
#Restarts the state-level Energy Use Folder
restart_states_energyuse = False
#   Restarts the state-level Equity Folder
restart_states_equity = True
#List of all "restarter" variables
restart_variables = [restart_all_states, restart_states_air_quality, restart_states_infrastructure, restart_states_economics,
                    restart_states_natgas, restart_states_co2, restart_states_energyuse, restart_states_equity]

#Set rerun_all_state_folders to True to completely re-run State-Factbook
rerun_all_state_folders = False
if(rerun_all_state_folders):
    for i in restart_variables:
        i = True

#Deletes a folder given the pathname and replaces it with an empty one
def folder_refresh(pathname):
    try:
        shutil.rmtree(pathname)
    except:
        None
    os.mkdir(pathname)

#Print how long it takes for supporting scripts to load (some require file processing that may take a bit of time)
print('Start-Up Complete. Time Elapsed',round(time.time()-start_time,2), 'seconds')

#Restart the entire State Factbase spreadsheets folder
if(restart_all_states):
    folder_refresh('../State Factbase/Spreadsheets/State-Level Data')
    #Recreate each state-level folder
    for s in state_names:
        sa = us_state_abbrev[s]
        path = '../State Factbase/Spreadsheets/State-Level Data/'+str(s)
        folder_refresh(path)

#State-Level Folder Creation:
for s in state_names:
    sa = us_state_abbrev[s]
    path = '../State Factbase/Spreadsheets/State-Level Data/'+str(s)

    if(restart_states_air_quality):
        #Make Air Quality Folder:
        folder_refresh(path+'/Air Quality/')
        #EPA NEI Data Export:
        epa_nei.get_county_emissions(sa).to_csv(path+'/Air Quality/'+s+' EPA NEI County-Level Emissions.csv')
        epa_nei.get_state_emissions(sa).to_csv(path+'/Air Quality/'+s+' EPA NEI State-Level Emissions.csv')
        
        #Tessum Data Export:
        df_state, df_cities = tessum.get_state_tessum(sa)
        df_state.to_csv(path+'/Air Quality/'+s+' Statewide PM25 Racial Disparities.csv')
        df_cities.to_csv(path+'/Air Quality/'+s+' City-Level PM25 Racial Disparities.csv')

    if(restart_states_infrastructure):
        folder_refresh(path+'/Buildings Infrastructure')
        folder_refresh(path+'/Buildings Infrastructure/State-Level')
        folder_refresh(path+'/Buildings Infrastructure/County-Level')
        #Get Statewide ACS Data
        df_infrastructure = acs_housing.get_state_all_data(sa)
        df_rentown, df_yrblt, df_units, df_hf, df_rooms = acs_housing.get_state_subsets(sa)
        temp_path = path+'/Buildings Infrastructure/State-Level/'+abbrev_us_state[sa]
        df_infrastructure.to_csv(temp_path+' All ACS Buildings Data.csv')
        df_rentown.to_csv(temp_path+' Building Tenure.csv')
        df_yrblt.to_csv(temp_path+' Building Vintage.csv')
        df_units.to_csv(temp_path+' Building Type.csv')
        df_hf.to_csv(temp_path+' Building Heating Fuel.csv')
        df_rooms.to_csv(temp_path+' Building Rooms.csv')
        #Get County-Level Data
        df_infrastructure = acs_housing.get_county_all_data(sa)
        df_rentown, df_yrblt, df_units, df_hf, df_rooms = acs_housing.get_county_subsets(sa)
        temp_path = path+'/Buildings Infrastructure/County-Level/' + sa + ' By County'
        df_infrastructure.to_csv(temp_path+' All ACS Buildings Data.csv')
        df_rentown.to_csv(temp_path+' Building Tenure.csv')
        df_yrblt.to_csv(temp_path+' Building Vintage.csv')
        df_units.to_csv(temp_path+' Building Type.csv')
        df_hf.to_csv(temp_path+' Building Heating Fuel.csv')
        df_rooms.to_csv(temp_path+' Building Rooms.csv')

    if(restart_states_co2):
        folder_refresh(path+'/CO2 Emissions')

        df_emit = eia_state.return_state_EIA_data(1980, eia_year, sa, eia_state.get_emit_tags(sa))
        df_emit.T.to_csv(path+'/CO2 Emissions/'+abbrev_us_state[sa]+' EIA CO2 Emissions Data.csv')
    
    if(restart_states_equity):
        if(sa!='AZ'):
            folder_refresh(path+'/Equity')
            dest1 = path+'/Equity/'+sa+' NREL LEAD Detailed.csv'
            dest2 = path+'/Equity/'+sa+' NREL LEAD Summary.csv'
            dest3 = path+'/Equity/'+sa+' NREL LEAD Energy Expenditures by Tract.csv'
            source1 = '../Static/NREL LEAD/States/'+sa+'_LEAD_All_Categories.csv'
            source2 = '../Static/NREL LEAD/States/'+sa+'_LEAD_Summary.csv'
            source3 = '../Static/NREL LEAD/Tracts/Energy Expenditures/'+sa+'_NREL_LEAD_Energy_Expenditures.csv'
            shutil.copy(source1, dest1)
            shutil.copy(source2, dest2)
            shutil.copy(source3, dest3)

    if(restart_states_energyuse):
        folder_refresh(path+'/Energy Use')

        df_use = eia_state.return_state_EIA_data(1980, eia_year, sa, eia_state.get_use_tags(sa))
        df_use.T.to_csv(path+'/Energy Use/'+abbrev_us_state[sa]+' EIA Energy Consumption Data.csv')

    if(restart_states_economics):
        folder_refresh(path+'/Energy Economics')
        
        df_h_income = acs_housing.get_state_income_data(sa)
        df_h_income.to_csv(path+'/Energy Economics/'+sa+' Household Incomes.csv')

        df_nrg_prices = economic_data.get_energy_price_data(sa)
        df_nrg_prices.to_csv(path+'/Energy Economics/'+sa+' Electricity and Natural Gas Prices.csv')

    if(restart_states_natgas):
        folder_refresh(path+'/Natural Gas')

        df_ng = eia_state.return_state_EIA_data(1970, eia_year, sa, eia_state.get_ng_tags(sa))
        df_ng.T.to_csv(path+'/Natural Gas/'+sa+' EIA Natural Gas Data.csv')

    print('Finished loading ', s)