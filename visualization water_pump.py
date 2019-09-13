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

plot_type = 'Sequential'
# Options: 'Summarize per day of week', 'Sequential', 'Summarize per week'

data = ['RG8170', 'Niveaumeting']
# Options: (1: dataset) 'RG8170', 'RG8150' (2: measure) 'Niveaumeting',
    # 'Debietmeting'
    
#### plot_type: Sequential ###################
    
resample_unit_1 = 'D' 
# Options: 'H', 'M', 'D', '3M' for 3 months etc.

#### plot_type: Summarize per day of week ####

resample_unit_2 = 'H'
# Options: 'H', 'M', 'D', '3M' for 3 months etc.

#### plot_type: Summarize per week ###########


###############################################################################
###############################################################################
###############################################################################

sns.set(rc={'figure.figsize':(40, 18)})

print('Reading data...')

current_dir = os.path.dirname(os.path.abspath(__file__))

data_path = current_dir + \
            '/waterschap-aa-en-maas_sewage_2019/sewer_data/data_pump/' + \
            data[0] + '/' + data[0] + '/' + data[0] + '_overall.csv'

rg8150 = pd.read_csv(data_path, sep=';', decimal=',')
rg8150['TimeStamp'] = pd.to_datetime(rg8150['TimeStamp'], 
      format = "%d-%m-%Y %H:%M:%S")

rg8150 = rg8150.loc[rg8150['Tagname'].str.contains(data[1]),]
rg8150.index = rg8150['TimeStamp']
rg8150 = rg8150[['TimeStamp', 'Value']]

print('Finished. \n')
    
print('Preprocessing data...')

if plot_type == 'Sequential':
    
    rg8150 = rg8150[['Value', 'TimeStamp']].resample(resample_unit_1).mean()

    print('Finished. \n')
    
    rg8150.plot()
    
elif plot_type == 'Summarize per week':
    
     rg8150 = rg8150.groupby(rg8150['TimeStamp'].dt.weekday).mean()
     rg8150.plot()

elif plot_type == 'Summarize per day of week':
    rg8150['weekday'] = rg8150["TimeStamp"].dt.dayofweek
    
    for i in range(7):
        plt.figure()
        df = rg8150[rg8150['weekday']==i]
        df = df.groupby(df.index.hour)['Value'].mean()
        df.plot(lw=2)
        plt.xlabel('hour', fontsize=24)
        plt.ylabel(data[1], fontsize=22)
        plt.rc('xtick',labelsize=14)
        plt.rc('ytick',labelsize=14)
        plt.title('24 hours of ' + data[1] + ' ' + data[0] + ' ' + days[i],
                  size=26)
        plt.savefig('24 hours of ' + data[1] + ' ' + data[0] + ' ' + \
                    days[i] + '.png')
        


        