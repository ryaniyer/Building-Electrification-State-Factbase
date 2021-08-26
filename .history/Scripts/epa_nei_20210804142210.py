import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Returns 3 pandas dataframes fo r
# 1. State-level by Sector
# 2. State-level by Pollutant
# 3. County-Level for All Pollutants/Sectors)

df = pd.read_csv('Static/Air_Quality/2017 EPIA NEI GHG All Sectors/2017_EPA_NEI_GHG.csv')

def get_EPA_NEI_AllSectors_dfs(sa):
    df = pd.read_csv('Static/Air_Quality/2017_EPA_NEI_AllSectors/States/'+sa+'_2017_NEI_Cleaned.csv',index_col=0).reset_index(drop=True)
    df = df.drop(columns=['pollutant type(s)'])
    
    finals = []
    for i in df.sector.unique():
        for j in df['pollutant desc'].unique():
            tags = [i,j,sum(df[(df['pollutant desc']==j)&(df.sector==i)]['total emissions']),'TON']
            finals.append(tags)
    df_sector = pd.DataFrame(columns=['Sector','Pollutant Type','Total Emissions','Emissions Unit of Measurement'])
    for i in range(len(finals)):
        df_sector.loc[len(df_sector.index)] = finals[i]
    df_sector = df_sector.iloc[::-1].reset_index(drop=True)
    df_sector = df_sector.sort_values(by=['Sector','Pollutant Type']).reset_index(drop=True)
    finals = []
    for i in df['pollutant desc'].unique():
        for j in df.sector.unique():
            tags = [i,j,sum(df[(df['pollutant desc']==i)&(df.sector==j)]['total emissions']),'TON']
            finals.append(tags)
        tags = [i,'All Buildings Sectors',sum(df[df['pollutant desc']==i]['total emissions']),'TON']
        finals.append(tags)
    df_type = pd.DataFrame(columns=['Pollutant Type','Sector','Total Emissions','Emissions Unit of Measurement'])
    for i in range(len(finals)):
        df_type.loc[len(df_type.index)] = finals[i]
    df_type = df_type.iloc[::-1].reset_index(drop=True)
    df_type = df_type.sort_values(by=['Pollutant Type','Sector']).reset_index(drop=True)
    
    df = df.sort_values(by=['county','sector','pollutant desc']).reset_index(drop=True)
    
    return df_sector, df_type, df

#Returns 3 pandas dataframes from the nonpoint 2017 NEI dataset
# 1. State-level by Sector
# 2. State-level by Pollutant
# 3. County-Level for All Pollutants/Sectors)
def get_EPA_NEI_NonPoint_dfs(sa):
    df = pd.read_csv('Static/Air_Quality/2017_NEI_Cleaned/States/'+sa+'_2017_NEI_Cleaned.csv',index_col=0).reset_index(drop=True)
    df = df.drop(columns=['epa region code','pollutant type(s)','fips state code','tribal name'])
    finals = []
    for i in df.sector.unique():
        for j in df['pollutant desc'].unique():
            tags = [i,j,sum(df[(df['pollutant desc']==j)&(df.sector==i)]['total emissions']),'TON']
            finals.append(tags)
        tags = [i,'All CAP Pollutants',sum(df[df.sector==i]['total emissions']),'TON']
        finals.append(tags)
    df_sector = pd.DataFrame(columns=['Sector','Pollutant Type','Total Emissions','Emissions Unit of Measurement'])
    for i in range(len(finals)):
        df_sector.loc[len(df_sector.index)] = finals[i]
    df_sector = df_sector.iloc[::-1].reset_index(drop=True)
    finals = []
    for i in df['pollutant desc'].unique():
        for j in df.sector.unique():
            tags = [i,j,sum(df[(df['pollutant desc']==j)&(df.sector==i)]['total emissions']),'TON']
            finals.append(tags)
        tags = [i,'All Sectors',sum(df[df.sector==i]['total emissions']),'TON']
        finals.append(tags)
    df_type = pd.DataFrame(columns=['Pollutant Type','Sector','Total Emissions','Emissions Unit of Measurement'])
    for i in range(len(finals)):
        df_type.loc[len(df_type.index)] = finals[i]
    df_type = df_type.iloc[::-1].reset_index(drop=True)
    df = df.sort_values(by=['county','sector','pollutant code']).reset_index(drop=True)

    return df_sector, df_type, df