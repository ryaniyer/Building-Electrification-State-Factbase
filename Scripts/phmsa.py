import pandas as pd 
import numpy as np 

def get_statewide_mileage(sa):
    mmiles = pd.read_csv('../Static/Natural_Gas/PHMSA_Cleaned_Data/PHMSA_Main_Mileage_2020.csv',index_col=0)
    temp_df = mmiles[mmiles.State==sa].reset_index(drop=True)
    mo = temp_df[temp_df['Operator Type']=='Municipal Owned'].reset_index(drop=True)
    io = temp_df[temp_df['Operator Type']=='Investor Owned'].reset_index(drop=True)
    po = temp_df[temp_df['Operator Type']=='Privately Owned'].reset_index(drop=True)
    co = temp_df[temp_df['Operator Type']=='Cooperative'].reset_index(drop=True)
    dfs = [mo,io,po,co,temp_df]
    dfnames = ['Municipal Owned','Investor Owned','Privately Owned','Cooperative','Total']
    finals = []
    for i in range(5):
        tot = ['Statewide Total','',dfnames[i],sa]
        sums1 = [sum(dfs[i]['Total Main Miles'])]
        try:
            sums2 = [sum(dfs[i]['Main Mileage Average Age'])/len(dfs[i])]
        except:
            sums2 = [0]
        sums3 = [sum(dfs[i]['Main Miles over 50 Years Old'])]
        mt = [int(sum(dfs[i][col])) for col in mmiles.columns[7:]]
        data = tot+sums1+sums2+sums3+mt
        finals.append(data)
    for i in range(5):
        temp_df.loc[len(temp_df.index)] = finals[i]
    temp_df = temp_df.iloc[::-1].reset_index(drop=True)
    return temp_df