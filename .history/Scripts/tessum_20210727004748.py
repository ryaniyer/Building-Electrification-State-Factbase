import pandas as pd
us_state_abbrev = {'the United States':'US','Alabama': 'AL','Alaska': 'AK','American Samoa': 'AS','Arizona': 'AZ','Arkansas': 'AR','California': 'CA','Colorado': 'CO', 'Connecticut': 'CT','Delaware': 'DE','District of Columbia': 'DC', 'Florida': 'FL','Georgia': 'GA','Guam': 'GU','Hawaii': 'HI', 'Idaho': 'ID','Illinois': 'IL','Indiana': 'IN','Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA', 'Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO', 'Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY','North Carolina': 'NC', 'North Dakota': 'ND','Northern Mariana Islands':'MP','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA','Puerto Rico': 'PR', 'Rhode Island': 'RI','South Carolina': 'SC','South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX','Utah': 'UT', 'Vermont': 'VT','Virgin Islands': 'VI','Virginia': 'VA','Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'}
abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))

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
    df1 = states[states.state==abbrev_us_state[sa]].reset_index(drop=True)
    df1 = df1.drop(columns=['lookup'])
    df2 = cities[(cities.State1==sa)|(cities.State2==sa)|(cities.State3==sa)].reset_index(drop=True)
    df2 = df2.drop(columns=['State1','State2','State3'])
    df2['State'] = [sa for _ in df2.index]
    return df1, df2

def get_national_tessum():
    df1 = states.drop(columns='lookup')
    return df1, cities