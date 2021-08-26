import pandas as pd

us_state_abbrev = {'US':'US','Alabama': 'AL','Alaska': 'AK','Arizona': 'AZ','Arkansas': 'AR','California': 'CA','Colorado': 'CO', 'Connecticut': 'CT','Delaware': 'DE','District of Columbia': 'DC', 'Florida': 'FL','Georgia': 'GA','Guam': 'GU','Hawaii': 'HI', 'Idaho': 'ID','Illinois': 'IL','Indiana': 'IN','Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA', 'Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO', 'Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY','North Carolina': 'NC', 'North Dakota': 'ND','Northern Mariana Islands':'MP','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA','Puerto Rico': 'PR', 'Rhode Island': 'RI','South Carolina': 'SC','South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX','Utah': 'UT', 'Vermont': 'VT','Virgin Islands': 'VI','Virginia': 'VA','Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'}
abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))

df_state = pd.read_csv('Static/ACS/2010_2019_ACS1_State_Data.csv', index_col=0)
df_county = pd.read_csv('Static/ACS/2010_2019_ACS5_County_Data.csv', index_col=0)


def get_state_df(sa):
    df_temp = df_state[df_state.State == abbrev_us_state[sa]]
    df_temp = df_temp.T
    df_temp.columns = df_temp.T['Year']
    df_temp = df_temp.drop(['State','Year'])
    df_temp.insert(0,'State',[sa for _ in df_temp.index])
    df_temp = df_temp.sort_index().reset_index().rename(columns={"index":"Metric"})
    return df_temp

def get_state_all_data(sa):
    df_temp = get_state_df(sa)
    df_temp = df_temp[~df_temp.Metric.str.contains('Household Income')]
    return df_temp

def get_state_subsets(sa):
    df_temp = get_state_df(sa)
    df_rentown = df_temp[df_temp.Metric.str.contains('wner')|df_temp.Metric.str.contains('enter')]
    df_yrblt = df_temp[df_temp.Metric.str.contains('Year Built')]
    df_units = df_temp[df_temp.Metric.str.contains('Units in Structure')]
    df_hf = df_temp[df_temp.Metric.str.contains('Heating Fuel')]
    df_rooms = df_temp[df_temp.Metric.str.contains('Rooms')]
    return df_rentown, df_yrblt, df_units, df_hf, df_rooms

def get_state_income_data(sa):
    df_temp = get_state_df(sa)
    df_temp = df_temp[df_temp.Metric.str.contains('Household Income')]
    return df_temp

def get_county_df(sa):
    df = df_county[df_county.State == abbrev_us_state[sa]]
    datasets = []
    for i in df.County.unique():
        df_temp = df[df.County==i]
        df_temp = df_temp.T
        df_temp.columns = df_temp.T['Year']
        df_temp = df_temp.drop(['State','County','Year'])
        df_temp.insert(0,'County',[i for _ in df_temp.index])
        df_temp.insert(0,'State',[sa for _ in df_temp.index])
        df_temp = df_temp.sort_index().reset_index().rename(columns={"index":"Metric"})
        datasets.append(df_temp)
    return pd.concat(datasets, axis=0)

def get_county_all_data(sa):
    df_temp = get_county_df(sa)
    df_temp = df_temp[~df_temp.Metric.str.contains('Household Income')]
    return df_temp

def get_county_subsets(sa):
    df_temp = get_county_df(sa)
    df_rentown = df_temp[df_temp.Metric.str.contains('wner')|df_temp.Metric.str.contains('enter')]
    df_yrblt = df_temp[df_temp.Metric.str.contains('Year Built')]
    df_units = df_temp[df_temp.Metric.str.contains('Units in Structure')]
    df_hf = df_temp[df_temp.Metric.str.contains('Heating Fuel')]
    df_rooms = df_temp[df_temp.Metric.str.contains('Rooms')]
    return df_rentown, df_yrblt, df_units, df_hf, df_rooms