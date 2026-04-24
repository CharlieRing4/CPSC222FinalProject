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
    
    weekend_length, weekend_successes = compute_proportions(weekend_df)
    weekday_length, weekday_successes = compute_proportions(weekday_df)

    successes = [weekend_successes,weekday_successes]
    nobs = [weekend_length,weekday_length]

    tstat, pval = proportions_ztest(successes,nobs)
    print(f'Test Statistic: {tstat:.3f}')
    print(f'PValue: {pval:.3f}')


def pushups_display(df:pd.DataFrame):
    jan_df = df.iloc[:31]
    feb_df = df.iloc[32:59]
    mar_df = df.iloc[60:90]
    apr_df = df.iloc[91:]

    plt.figure(layout='compressed')
    plt.xlim(0,5)
    plt.ylim(0,30)
    plt.title('Average Daily Pushups by Month')
    plt.xticks([1,2,3,4],['January','February','March','April'])

    jan_mean = jan_df['Pushups'].mean()
    feb_mean = feb_df['Pushups'].mean()
    mar_mean = mar_df['Pushups'].mean()
    apr_mean = apr_df['Pushups'].mean()

    heights = [jan_mean,feb_mean,mar_mean,apr_mean]
    x=[1,2,3,4]

    plt.bar(x=x,height=heights,color=['powderblue','c','darkcyan','teal'])
    plt.plot(1,jan_mean,'o',color='black')
    plt.plot(2,feb_mean,'o',color='black')
    plt.plot(3,mar_mean,'o',color='black')
    plt.plot(4,apr_mean,'o',color='black')
        
    for i,val in enumerate(heights):
        plt.annotate(f'{val:.2f}', (x[i],heights[i]),textcoords='offset points', xytext=(0,10), ha='center' )
    plt.show()


def pushups_f_test(df:pd.DataFrame):
    jan_df = df.iloc[:31]
    feb_df = df.iloc[32:59]
    mar_df = df.iloc[60:90]
    apr_df = df.iloc[91:]

    f_stat, pval = stats.f_oneway(jan_df['Pushups'],feb_df['Pushups'],mar_df['Pushups'],apr_df['Pushups'])
    print(f'F Statistic: {f_stat:.3f}')
    print(f'P-Value: {pval:.3f}')


def conf_int(x,mean,lbound,ubound):
    horiz_line_width = .25
    left = x-horiz_line_width/2
    right = x+horiz_line_width/2
    
    plt.grid()
    plt.plot([x,x],[lbound,ubound],color='b')
    plt.plot(x,mean,'ro')
    plt.plot([left,right],[lbound,lbound],color='b')
    plt.plot([left,right],[ubound,ubound],color='b')
    
    plt.show()



def main():
    running_df = pd.read_csv('activities.csv')
    habits_df = pd.read_csv('habits.csv')

    # clean_activities(running_df)
    clean_habits_df = clean_habits(habits_df)

    # flossing_hyp_test(clean_habits_df)
    pushups_display(clean_habits_df)
    pushups_ttest(clean_habits_df)

    pass

if __name__=='__main__':
    main()