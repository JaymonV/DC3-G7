# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 14:03:43 2019

@author: Jaymon

Required:
    - Place this file at the same level as the data folders 
        waterschap-aa-en-maas_sewage_2019
        waterschap-aa-en-maas_sewage_2019 
    - Make sure merge_files.py is already executed
"""

import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import calendar
days = list(calendar.day_name)

###############################################################################
############################### SETTINGS ######################################
###############################################################################

################# General #####################

data = ['RG1876_flow']
# Options: (1: dataset) 'RG8176_flow', 'RG1882_flow'

###############################################################################
###############################################################################
###############################################################################

sns.set(rc={'figure.figsize':(40, 18)})

print('Reading data...')

current_dir = os.path.dirname(os.path.abspath(__file__))

data_path = current_dir + '\\' + \
            'waterschap-aa-en-maas_sewage_2019_db_pumps\sewer_data_db\data_wwtp_flow' + '\\' + \
            data[0] + '/' + data[0] + '_overall.csv'

df = pd.read_csv(data_path, sep=';', decimal=',')
df['datumBeginMeting'] = pd.to_datetime(df['datumBeginMeting'], 
      format = "%Y-%m-%d %H:%M:%S")

df['hstWaarde'] = pd.to_numeric(df['hstWaarde'])

df.index = df['datumBeginMeting']

print('Finished. \n')

df_1 = df[df['datumBeginMeting'] < pd.to_datetime('2018-06-01')]

df_1_max = df_1[['datumBeginMeting', 'hstWaarde']].resample('4H').max()
df_1_min = df_1[['datumBeginMeting', 'hstWaarde']].resample('4H').min()

df_1 = pd.concat([df_1_max, df_1_min], axis=1)

df_1.columns = ['datetime', 'max', '.', 'min']

df_1.plot(x='datetime', y=['max', 'min'])

# =============================================================================
# 
# ax = df_1_max.plot(x='datumBeginMeting', y='hstWaarde')
# ax = df_1_min.plot(x='datumBeginMeting', y='hstWaarde')
# =============================================================================


# =============================================================================
# elif plot_type == 'Summarize per day of week':
#     rg8150['weekday'] = rg8150["TimeStamp"].dt.dayofweek
#     
#     for i in range(7):
#         plt.figure()
#         df = rg8150[rg8150['weekday']==i]
#         df = df.groupby(df.index.hour)['Value'].mean()
#         df.plot(lw=2)
#         plt.xlabel('hour', fontsize=24)
#         plt.ylabel(data[1], fontsize=22)
#         plt.rc('xtick',labelsize=14)
#         plt.rc('ytick',labelsize=14)
#         plt.title('24 hours of ' + data[1] + ' ' + data[0] + ' ' + days[i],
#                   size=26)
#         plt.savefig('24 hours of ' + data[1] + ' ' + data[0] + ' ' + \
#                     days[i] + '.png')
# =============================================================================
        