import pandas as pd

states = pd.read_csv('Static/Air_Quality/Tessum/states_pm_exposure.csv', index_col=0)
cities = pd.read_csv('Static/Air_Quality/Tessum/cities_pm_exposure.csv', index_col=0)

def get_state_tessum(sa):
    df1 = states[states.state==sa]
    df2 = cities[cities.state==sa]
    return df1, df2