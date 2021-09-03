import pandas as pd 
import numpy as np 

df_nat = pd.read_csv('../Static/Natural_Gas/Form 176 Type Items 1997-2019.csv',low_memory=False)
df_nat.columns = [i.replace('<BR>',' ') for i in df_nat.columns]

def get_state_metric_totals(s):
    sa = df_nat[df_nat.State==s]
    sasum = pd.DataFrame(columns=['State','Metric']+[str(i) for i in range(1997,2020)])
    for i in sa.columns[21:]:
        metrics = [0 for _ in range(1997,2020)]
        for yr in range(1997,2020):
            temp_df = sa[sa.Year==yr]
            year_metric = np.nan_to_num(temp_df[i])
            if('Price' in i):
                try:
                    val = sum(year_metric)/np.count_nonzero(year_metric)
                    metrics[yr-1997] = round(val,2)
                except:
                    None
            else:
                metrics[yr-1997] = int(sum(year_metric))
        sasum.loc[len(sasum)] = [s,i] + list(metrics)
    return sasum


def get_national_metric_totals():
    sa = df_nat
    sasum = pd.DataFrame(columns=['Metric']+[str(i) for i in range(1997,2020)])
    for i in sa.columns[21:]:
        metrics = [0 for _ in range(1997,2020)]
        for yr in range(1997,2020):
            temp_df = sa[sa.Year==yr]
            year_metric = np.nan_to_num(temp_df[i])
            if('Price' in i):
                try:
                    val = sum(year_metric)/np.count_nonzero(year_metric)
                    metrics[yr-1997] = round(val,2)
                except:
                    None
            else:
                metrics[yr-1997] = int(sum(year_metric))
        sasum.loc[len(sasum)] = [i] + list(metrics)
    return sasum