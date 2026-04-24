import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import datetime as dt
from statsmodels.stats.proportion import proportions_ztest

def clean_habits(df:pd.DataFrame):
    df['Pushups'] = df['Pushups'].fillna(0)
    df['Miles Ran'] = df['Miles Ran'].fillna(0)
    ind_df = df.set_index('Date')
    return ind_df
    

def clean_activities(df:pd.DataFrame):
    # ToDo
    date_df = df['Activity Date']
    date_ser = pd.to_datetime(date_df)
    print(date_ser)

def compute_proportions(df:pd.DataFrame):
    length = len(df)
    total = df['Flossed'].sum()
    return length, total

def flossing_hyp_test(df:pd.DataFrame):
    grouped_by_dotw = df.groupby('Day of the Week')
    weekend_df = pd.concat([grouped_by_dotw.get_group('Friday'),grouped_by_dotw.get_group('Saturday')])
    weekday_df = pd.concat([grouped_by_dotw.get_group('Monday'),grouped_by_dotw.get_group('Tuesday'),grouped_by_dotw.get_group('Wednesday'),grouped_by_dotw.get_group('Thursday'),grouped_by_dotw.get_group('Friday')])
   
    weekend_length, weekend_tot = compute_proportions(weekend_df)
    weekday_length, weekday_tot = compute_proportions(weekday_df)
    


    



def group_by_month(df:pd.DataFrame):
    pass



def main():
    running_df = pd.read_csv('activities.csv')
    habits_df = pd.read_csv('habits.csv')

    # clean_activities(running_df)
    clean_habits_df = clean_habits(habits_df)

    flossing_hyp_test(clean_habits_df)
    print(clean_habits_df.head())

    pass

if __name__=='__main__':
    main()