import pandas as pd

states = pd.read_csv('Static/Tessum/states_pm_exposure.csv', index_col=0)
cities = pd.read_csv('Static/Tessum/cities_pm_exposure.csv', index_col=0)

def get_state_tessum(sa):
    return states[states.state==sa]