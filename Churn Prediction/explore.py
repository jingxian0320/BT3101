# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 17:46:33 2016

@author: Jane
"""

import pandas

training = pandas.read_csv('training_data.csv')
print training.head()
print training['is_churner_inactive'].value_counts()
print training['is_churner_uninstalled'].value_counts()
print training['is_male'].value_counts()

print training.groupby(['is_churner_uninstalled', 'is_male']).size()
print training[['is_churner_uninstalled', 'screen_size']].groupby(['is_churner_uninstalled']).mean()
#print training['screen_size'].value_counts()
#print training['screen_resolution'].value_counts()
#print training['ram_mb'].value_counts()

def box_plot(col_name):
    r1 = training[col_name]
    r2 = training[col_name].loc[training["is_churner_uninstalled"] == 1]
    r3 = training[col_name].loc[training["is_churner_uninstalled"] == 0]
    df = pandas.concat([r1, r2, r3], axis=1)
    df.columns = ['all', 'churner','non-churner']
    df.plot(kind = 'box')
    df.to_csv('presentation_data/'+ col_name+'_data.csv', index = False)
    
def churner_plot(col_name, kind):
    df1 = training.loc[training["is_churner_inactive"] == 1]
    df1 = df1[col_name].value_counts().sort_index()
    df1.plot(kind = kind, color = 'k')
    df2 = training.loc[training["is_churner_inactive"] == 0]
    df2 = df2[col_name].value_counts().sort_index()
    df1.to_csv('presentation_data/'+ col_name+'_churner_count.csv')
    df2.to_csv('presentation_data/'+ col_name+'_non_churner_count.csv')