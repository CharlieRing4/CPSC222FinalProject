import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from datetime import datetime
from statsmodels.stats.proportion import proportions_ztest
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix,ConfusionMatrixDisplay
from sklearn.neighbors import KNeighborsClassifier
import json

def clean_habits(df:pd.DataFrame):
    df['Pushups'] = df['Pushups'].fillna(0)
    df['Miles Ran'] = df['Miles Ran'].fillna(0)
    ind_df = df.set_index('Date')
    return ind_df
    
def clean_and_load_insta():
    times_list = []
    daily_groups = {}

    with open('liked_posts.json','r') as file:
        json_obj = json.load(file)
    
    for item in range(len(json_obj)):
        timestamp = json_obj[item]['timestamp']
        day_name = datetime.fromtimestamp(timestamp).strftime('%m/%d/%y')
        daily_groups.setdefault(day_name, []).append(timestamp)

    counts_dict = {day: len(items) for day, items in daily_groups.items()}

    insta_series = pd.Series(counts_dict,name='Liked Posts')
    df_counts = insta_series.reset_index()
    df_counts.columns = ['Date','Liked Posts']
    return df_counts

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

    weekday_fails = weekday_length-weekday_successes
    weekend_fails = weekend_length-weekend_successes
    weekday_prop = [weekday_successes,weekday_fails]
    weekend_prop = [weekend_successes,weekend_fails]

    return weekday_prop,weekend_prop

def pie_flossing(prop,label):
    plt.figure(layout='constrained',figsize=(12,5))
    plt.pie(x=prop,labels=['Did Floss','Did Not Floss'],colors=['seagreen','indianred'],startangle=45,autopct='%1.1f%%')
    plt.title(f'{label} Flossing Proportion')
    plt.legend()
    plt.show()

def pushups_display(df:pd.DataFrame):
    jan_df = df.iloc[:31]
    feb_df = df.iloc[32:59]
    mar_df = df.iloc[60:90]
    apr_df = df.iloc[91:]

    plt.figure(layout='compressed')
    plt.xlim(0,5)
    plt.ylim(0,30)
    plt.title('Average Pushups Per Day')
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
    # plt.show()


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

def make_insta_graph(merged_df:pd.DataFrame):
    weekly_data = merged_df.resample('W').sum()
    x=np.arange(len(weekly_data))
    width=.4

    plt.figure(layout='constrained',figsize=(9,4))
    plt.bar(x=x,height=weekly_data['Liked Posts'],color='orchid')
    plt.title('Liked Instagram Posts by Week')
    plt.xlabel('Week')
    plt.ylabel('Liked Posts')
    plt.xticks(x,weekly_data.index.strftime('%m-%d-%y'),rotation=45)
    plt.show()

def decision_tree_dotw(merged_df:pd.DataFrame):
    tree = DecisionTreeClassifier()
    y = merged_df['Day of the Week'][:112]
    x = merged_df.drop(['Day of the Week'],axis='columns')
    x=x.drop(['Liked Posts'],axis='columns')
    x=x[:112]

    X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=.25,stratify=y)
    tree.fit(X_train,y_train)

    y_preds = tree.predict(X_test)
    tree_acc = accuracy_score(y_test,y_preds)


    print(f'Accuracy: {tree_acc:.2f}')
    # print(y_preds)
    # print(y_test)

def decision_tree_weekly(merged_df:pd.DataFrame):

    pass

def main():
    running_df = pd.read_csv('activities.csv')
    habits_df = pd.read_csv('habits.csv')
    insta_df = clean_and_load_insta()

    clean_habits_df = clean_habits(habits_df)
    clean_habits_df.index = pd.to_datetime(clean_habits_df.index,format='%m/%d/%y').strftime('%m/%d/%y')

    merged_df = pd.merge(clean_habits_df,insta_df,left_index=True,right_on='Date',how='outer')
    merged_df['Date']= pd.to_datetime(merged_df['Date'],format='%m/%d/%y')
    merged_df.set_index('Date',inplace=True)
    merged_df['is_weekend'] = (merged_df.index.dayofweek >=5).astype(int)
    merged_df['Liked Posts'] = merged_df['Liked Posts'].fillna(0)
    merged_df.to_csv('test.csv')

    # weekday,weekend = flossing_hyp_test(clean_habits_df)
    # pie_flossing(weekday,'Weekdays')
    # pie_flossing(weekend,'Weekends')
    # pushups_display(clean_habits_df)
    # pushups_f_test(clean_habits_df)
    # make_insta_graph(merged_df)

    decision_tree_dotw(merged_df)

    pass

if __name__=='__main__':
    main()