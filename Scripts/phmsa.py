import pandas as pd 
import numpy as np 

def generate_dfs(df):
    mo = df[df['Operator Type']=='Municipal Owned'].reset_index(drop=True)
    io = df[df['Operator Type']=='Investor Owned'].reset_index(drop=True)
    po = df[df['Operator Type']=='Privately Owned'].reset_index(drop=True)
    co = df[df['Operator Type']=='Cooperative'].reset_index(drop=True)
    dfs = [mo,io,po,co,df]
    return dfs

def get_statewide_mileage(sa):
    mmiles = pd.read_csv('../Static/Natural_Gas/PHMSA_Cleaned_Data/PHMSA_Main_Mileage_2020.csv',index_col=0)
    temp_df = mmiles[mmiles.State==sa].reset_index(drop=True)
    dfs = generate_dfs(temp_df)
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
        mt = [int(sum(dfs[i][col])) for col in temp_df.columns[7:]]
        data = tot+sums1+sums2+sums3+mt
        finals.append(data)
    for i in range(5):
        temp_df.loc[len(temp_df.index)] = finals[i]
    temp_df = temp_df.iloc[::-1].reset_index(drop=True)
    temp_df.columns = ['Operator Name', 'Operator ID', 'Operator Type', 'State','Total Main Miles', 'Main Mileage Average Age','Main Miles over 50 Years Old', 'Main Miles Built in Unknown Decade','Pre-1940', '1940-49', '1950-59', '1960-69', '1970-79', '1980-89', '1990-99', '2000-09', '2010-19', '2020-29']
    temp_df.columns = ['Operator Name', 'Operator ID', 'Operator Type', 'State','Total Main Miles', 'Main Mileage Average Age','Main Miles over 50 Years Old', 'Main Miles Built in Unknown Decade',
       'Pre-1940', '1940-49',
       '1950-59', '1960-69',
       '1970-79', '1980-89',
       '1990-99', '2000-09',
       '2010-19', '2020-29']
    return temp_df

def get_statewide_hazleaks(sa):
    hazlks = pd.read_csv('../Static/Natural_Gas/PHMSA_Cleaned_Data/PHMSA_Hazardous_Leaks_2010_2020.csv',index_col=0)
    temp_df = hazlks[hazlks.State==sa].reset_index(drop=True)
    years = temp_df.columns[4:]
    temp_df['Total Hazardous Leaks (2010-2020)'] = [sum(temp_df.iloc[i,4:]) for i in temp_df.index]
    temp_df = temp_df.filter(['Operator ID','Operator Name','Operator Type','State','Total Hazardous Leaks'] + list(years))
    dfs = generate_dfs(temp_df)
    dfnames = ['Municipal Owned','Investor Owned','Privately Owned','Cooperative','Total']
    finals = []
    for i in range(5):
        tot = ['','Statewide Total',dfnames[i],sa]
        hl = [int(sum(dfs[i][col])) for col in temp_df.columns[4:]]
        data = tot + hl
        finals.append(data)
    for i in range(5):
        temp_df.loc[len(temp_df.index)] = finals[i]
    temp_df = temp_df.iloc[::-1].reset_index(drop=True)
    return temp_df

def get_statewide_totleaks(sa):
    hazlks = pd.read_csv('../Static/Natural_Gas/PHMSA_Cleaned_Data/PHMSA_Total_Leaks_2010_2020.csv',index_col=0)
    temp_df = hazlks[hazlks.State==sa].reset_index(drop=True)
    years = temp_df.columns[4:]
    temp_df['Total Leaks (2010-2020)'] = [sum(temp_df.iloc[i,4:]) for i in temp_df.index]
    temp_df = temp_df.filter(['Operator ID','Operator Name','Operator Type','State','Total Leaks'] + list(years))
    dfs = generate_dfs(temp_df)
    dfnames = ['Municipal Owned','Investor Owned','Privately Owned','Cooperative','Total']
    finals = []
    for i in range(5):
        tot = ['','Statewide Total',dfnames[i],sa]
        hl = [int(sum(dfs[i][col])) for col in temp_df.columns[4:]]
        data = tot + hl
        finals.append(data)
    for i in range(5):
        temp_df.loc[len(temp_df.index)] = finals[i]
    temp_df = temp_df.iloc[::-1].reset_index(drop=True)
    return temp_df

def get_statewide_services(sa):
    srvs = pd.read_csv('../Static/Natural_Gas/PHMSA_Cleaned_Data/PHMSA_Services_2020.csv',index_col=0)
    temp_df = srvs[srvs.State==sa].reset_index(drop=True)
    dfs = generate_dfs(temp_df)
    dfnames = ['Municipal Owned','Investor Owned','Privately Owned','Cooperative','Total']
    finals = []
    for i in range(5):
        tot = ['Statewide Total','',dfnames[i],sa]
        sums1 = [int(sum(dfs[i][col])) for col in temp_df.columns[4:]]
        data = tot+sums1
        finals.append(data)
    for i in range(5):
        temp_df.loc[len(temp_df.index)] = finals[i]
    temp_df = temp_df.iloc[::-1].reset_index(drop=True)
    return temp_df


def get_national_mileage():
    mmiles = pd.read_csv('../Static/Natural_Gas/PHMSA_Cleaned_Data/PHMSA_Main_Mileage_2020.csv',index_col=0)
    temp_df = mmiles[mmiles.State!='AK'].reset_index(drop=True)
    dfs = generate_dfs(temp_df)
    dfnames = ['Municipal Owned','Investor Owned','Privately Owned','Cooperative','Total']
    finals = []
    for i in range(5):
        tot = ['Total','',dfnames[i],'Contiguous US']
        sums1 = [sum(dfs[i]['Total Main Miles'])]
        try:
            sums2 = [sum(dfs[i]['Main Mileage Average Age'])/len(dfs[i])]
        except:
            sums2 = [0]
        sums3 = [sum(dfs[i]['Main Miles over 50 Years Old'])]
        mt = [int(sum(dfs[i][col])) for col in temp_df.columns[7:]]
        data = tot+sums1+sums2+sums3+mt
        finals.append(data)
    for i in range(5):
        temp_df.loc[len(temp_df.index)] = finals[i]
    temp_df = temp_df.iloc[::-1].reset_index(drop=True)
    temp_df.columns = ['Operator Name', 'Operator ID', 'Operator Type', 'State','Total Main Miles', 'Main Mileage Average Age','Main Miles over 50 Years Old', 'Main Miles Built in Unknown Decade','Pre-1940', '1940-49', '1950-59', '1960-69', '1970-79', '1980-89', '1990-99', '2000-09', '2010-19', '2020-29']
    temp_df.columns = ['Operator Name', 'Operator ID', 'Operator Type', 'State','Total Main Miles', 'Main Mileage Average Age','Main Miles over 50 Years Old', 'Main Miles Built in Unknown Decade','Pre-1940', '1940-49','1950-59', '1960-69','1970-79', '1980-89','1990-99', '2000-09','2010-19', '2020-29']
    return temp_df