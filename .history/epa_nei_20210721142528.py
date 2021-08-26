import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Returns 3 pandas dataframes (1. State-level by Sector, 2. State-level by Pollutant, 3. County-Level for All)
def get_EPA_NEI_dfs(sa):
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