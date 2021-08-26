import pandas as pd

states = pd.read_csv('Static/Air_Quality/Tessum/states_pm_exposure.csv', index_col=0)
cities = pd.read_csv('Static/Air_Quality/Tessum/cities_pm_exposure.csv', index_col=0)

def get_state_tessum(sa):
    print(states.head())
    return states[states.state==sa]