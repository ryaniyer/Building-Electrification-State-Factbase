import pandas as pd

states = pd.read_excel('Static/Air_Quality/Tessum/abf4491_Data_file_S2.xlsx', 0)
cities = pd.read_excel('Static/Air_Quality/Tessum/abf4491_Data_file_S2.xlsx', 1)

state1 = ['' for _ in cities.index]
state2 = ['' for _ in cities.index]
state3 = ['' for _ in cities.index]
for i in cities.index:
    state = cities['urban_area'][i].split(',')[1].split('--')
    state1[i] = (state[0].strip(' '))
    if(len(state)>1):
        state2[i] = (state[1].strip(' '))
    if(len(state)>2):
        state3[i] = (state[2].strip(' '))
cities['State1'] = state1
cities['State2'] = state2
cities['State3'] = state3

#Returns 2 pandas dataframes
#1. For State-Level disparities
#2. For City-Level Disparities
def get_state_tessum(sa):
    df1 = states[states.state==sa].reset_index(drop=True)
    df2 = cities[cities.state==sa].reset_index(drop=True)
    return df1, df2