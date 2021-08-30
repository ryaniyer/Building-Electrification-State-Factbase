import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Import NEI Data for GHG and CAP
dfghg = pd.read_csv('../Static/Air_Quality/2017_EPA_NEI_GHG.csv')
dfcap = pd.read_csv('../Static/Air_Quality/2017_EPA_NEI_CAP.csv')

def get_county_cap_data(sa):
    caps = pd.DataFrame(columns=['State','County','Sector','Pollutant','Pollutant Type','Total Emissions','Emissions Unit of Measure'])
    df2 = dfcap[dfcap['state']==sa]
    for c in df2['county'].unique():
        for p in df2['pollutant desc'].unique():
            for s in df2['sector'].unique():
                try:
                    dft2 = df2[(df2['pollutant desc']==p)&(df2['sector']==s)].reset_index(drop=True)
                    caps.loc[len(caps.index)] = [sa, c, s, p, 'CAP', sum(dft2['total emissions']), dft2['emissions uom'][0]]
                except:
                    None
            dft2 = df2[(df2['pollutant desc']==p)].reset_index(drop=True)
            caps.loc[len(caps.index)] = [sa, c, 'All Sectors', p, 'CAP', sum(dft2['total emissions']), dft2['emissions uom'][0]]
    caps = caps.sort_values(by=['County','Sector','Pollutant']).reset_index(drop=True)
    return caps

def get_state_cap_data(sa):
    caps = pd.DataFrame(columns=['State','Sector','Pollutant','Pollutant Type','Total Emissions','Emissions Unit of Measure'])
    df2 = dfcap[dfcap['state']==sa]
    for p in df2['pollutant desc'].unique():
        for s in df2['sector'].unique():
            try:
                dft2 = df2[(df2['pollutant desc']==p)&(df2['sector']==s)].reset_index(drop=True)
                caps.loc[len(caps.index)] = [sa, s, p, 'CAP', sum(dft2['total emissions']), dft2['emissions uom'][0]]
            except:
                None
        dft2 = df2[(df2['pollutant desc']==p)].reset_index(drop=True)
        caps.loc[len(caps.index)] = [sa, 'All Sectors', p, 'CAP', sum(dft2['total emissions']), dft2['emissions uom'][0]]
    caps = caps.sort_values(by=['Sector', 'Pollutant']).reset_index(drop=True)
    return caps

def get_national_cap_data():
    caps = pd.DataFrame(columns=['Sector','Pollutant','Pollutant Type','Total Emissions','Emissions Unit of Measure'])
    df2 = dfcap[~dfcap.state.isnull()].state.unique()
    for p in df2['pollutant desc'].unique():
        for s in df2['sector'].unique():
            try:
                dft2 = df2[(df2['pollutant desc']==p)&(df2['sector']==s)].reset_index(drop=True)
                caps.loc[len(caps.index)] = [s, p,'CAP',  sum(dft2['total emissions']), dft2['emissions uom'][0]]
            except:
                None
        dft2 = df2[(df2['pollutant desc']==p)].reset_index(drop=True)
        caps.loc[len(caps.index)] = ['All Sectors', p,'CAP',  sum(dft2['total emissions']), dft2['emissions uom'][0]]
    caps = caps.sort_values(by=['Sector', 'Pollutant']).reset_index(drop=True)
    return caps

def get_county_ghg_data(sa):
    ghgs = pd.DataFrame(columns=['State','County','Sector','Pollutant','Pollutant Type','Total Emissions','Emissions Unit of Measure'])
    df2 = dfghg[dfghg['state']==sa]
    for c in df2['county'].unique():
        for p in df2['pollutant desc'].unique():
            for s in df2['sector'].unique():
                try:
                    dft2 = df2[(df2['pollutant desc']==p)&(df2['sector']==s)].reset_index(drop=True)
                    ghgs.loc[len(ghgs.index)] = [sa, c, s, p,'GHG',  sum(dft2['total emissions']), dft2['emissions uom'][0]]
                except:
                    None
            dft2 = df2[(df2['pollutant desc']==p)].reset_index(drop=True)
            ghgs.loc[len(ghgs.index)] = [sa, c, 'All Sectors', p,'GHG',  sum(dft2['total emissions']), dft2['emissions uom'][0]]
    ghgs = ghgs.sort_values(by=['County','Sector','Pollutant']).reset_index(drop=True)
    return ghgs

def get_state_ghg_data(sa):
    ghgs = pd.DataFrame(columns=['State','Sector','Pollutant','Pollutant Type','Total Emissions','Emissions Unit of Measure'])
    df2 = dfghg[dfghg['state']==sa]
    for p in df2['pollutant desc'].unique():
        for s in df2['sector'].unique():
            try:
                dft2 = df2[(df2['pollutant desc']==p)&(df2['sector']==s)].reset_index(drop=True)
                ghgs.loc[len(ghgs.index)] = [sa, s, p, 'GHG', sum(dft2['total emissions']), dft2['emissions uom'][0]]
            except:
                None
        dft2 = df2[(df2['pollutant desc']==p)].reset_index(drop=True)
        ghgs.loc[len(ghgs.index)] = [sa, 'All Sectors', p,'GHG',  sum(dft2['total emissions']), dft2['emissions uom'][0]]
    ghgs = ghgs.sort_values(by=['Sector','Pollutant']).reset_index(drop=True)
    return ghgs

def get_national_ghg_data():
    ghgs = pd.DataFrame(columns=['Sector','Pollutant','Pollutant Type','Total Emissions','Emissions Unit of Measure'])
    df2 = dfghg[~dfghg.state.isnull()].state.unique()
    for p in df2['pollutant desc'].unique():
        for s in df2['sector'].unique():
            try:
                dft2 = df2[(df2['pollutant desc']==p)&(df2['sector']==s)].reset_index(drop=True)
                ghgs.loc[len(ghgs.index)] = [s, p, 'GHG', sum(dft2['total emissions']), dft2['emissions uom'][0]]
            except:
                None
        dft2 = df2[(df2['pollutant desc']==p)].reset_index(drop=True)
        ghgs.loc[len(ghgs.index)] = ['All Sectors', p, 'GHG', sum(dft2['total emissions']), dft2['emissions uom'][0]]
    ghgs = ghgs.sort_values(by=['Sector', 'Pollutant']).reset_index(drop=True)
    return ghgs

def get_county_emissions(sa):
    caps= get_county_cap_data(sa)
    ghgs = get_county_ghg_data(sa)
    dfnew = pd.concat([caps, ghgs], axis=0).sort_values(by=['County','Sector','Pollutant Type','Pollutant'])
    dftots = dfnew[dfnew['Sector']=='All Sectors']
    dfnontots = dfnew[dfnew['Sector']!='All Sectors']
    dfnew = pd.concat([dftots, dfnontots], axis=0).reset_index(drop=True)
    return dfnew

def get_state_emissions(sa):
    caps= get_state_cap_data(sa)
    ghgs = get_state_ghg_data(sa)
    dfnew = pd.concat([caps, ghgs], axis=0).sort_values(by=['Sector','Pollutant Type','Pollutant'])
    dftots = dfnew[dfnew['Sector']=='All Sectors']
    dfnontots = dfnew[dfnew['Sector']!='All Sectors']
    dfnew = pd.concat([dftots, dfnontots], axis=0).reset_index(drop=True)
    return dfnew

def get_national_emissions(sa):
    caps= get_national_cap_data()
    ghgs = get_national_ghg_data()
    dfnew = pd.concat([caps, ghgs], axis=0).sort_values(by=['Sector','Pollutant Type','Pollutant'])
    dftots = dfnew[dfnew['Sector']=='All Sectors']
    dfnontots = dfnew[dfnew['Sector']!='All Sectors']
    dfnew = pd.concat([dftots, dfnontots], axis=0).reset_index(drop=True)
    return dfnew