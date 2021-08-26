import pandas as pd

states = pd.read_csv('Static/Air_Quality/Tessum/states_pm_exposure.csv', index_col=0)
cities = pd.read_csv('Static/Air_Quality/Tessum/cities_pm_exposure.csv', index_col=0)

#Returns 2 pandas dataframes
#1. For State-Level disparities
#2. For City-Level Disparities
def get_state_tessum(sa):
    df1 = states[states.state==sa].reset_index(drop=True)
    df2 = cities[cities.state==sa].reset_index(drop=True)
    return df1, df2