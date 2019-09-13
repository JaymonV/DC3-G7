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
sns.set(rc={'figure.figsize':(18, 6)})

print('Reading data...')

current_dir = os.path.dirname(os.path.abspath(__file__))

data_path = current_dir + '/waterschap-aa-en-maas_sewage_2019/sewer_data/data_pump'
data_path_RG8150 = data_path + '/RG8150/RG8150/RG8150_overall.csv'
data_path_RG8170 = data_path + '/RG8170/RG8170/RG8170_overall.csv'

rg8150 = pd.read_csv(data_path_RG8150, sep=';', decimal=',')
rg8150['TimeStamp'] = pd.to_datetime(rg8150['TimeStamp'], 
      format = "%d-%m-%Y %H:%M:%S")

rg8150_niv = rg8150.loc[rg8150['Tagname'].str.contains('Niveaumeting'),]

print('Finished. \n')

print('Preprocessing data...')

rg8150_niv.index = rg8150_niv['TimeStamp']
rg8150_niv = rg8150_niv[['Value', 'TimeStamp']].resample('H').mean()


print('Finished. \n')

rg8150_niv.plot()
