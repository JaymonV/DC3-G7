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

print('Reading data...')

current_dir = os.path.dirname(os.path.abspath(__file__))

data_path = current_dir + '\\' + \
            'waterschap-aa-en-maas_sewage_2019_db_pumps\sewer_data_db\data_wwtp_flow' + '\\' + \
            data[0] + '\\' + data[0] + '_overall.csv'

df = pd.read_csv(data_path, sep=';', decimal=',')
df['datumBeginMeting'] = pd.to_datetime(df['datumBeginMeting'], 
      format = "%Y-%m-%d %H:%M:%S")

df['hstWaarde'] = pd.to_numeric(df['hstWaarde'])

print('Finished. \n')

df_1 = df[df['datumBeginMeting'] < pd.to_datetime('2018-06-01')]

df_1['rounded_date'] = df_1['datumBeginMeting'].dt.round('10D')

f, ax = plt.subplots(figsize=(20, 10))

sns.set(rc={'figure.figsize':(20, 9),
            "lines.linewidth": 0.15})

sns.lineplot(x=df_1['rounded_date'], y=df_1['hstWaarde'],
             ci=99.9)

ax.xaxis.set_major_locator(plt.MaxNLocator(8))
ax.set_title('WWTP flow value: 99% confidence interval by 10 days',
             {'fontsize': 22})
ax.set_xlabel('Date', {'fontsize': 16})
ax.set_ylabel('Flow value', {'fontsize': 16})
ax.tick_params(axis='both', which='major', labelsize=14)
