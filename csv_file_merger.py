# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 10:38:02 2019

@author: Jaymon

Script used for merging the csv files in data folders. Supported:
    - sewer_data

Preparation: (1) unzip the data folders, (2) place this file in the folder:
    'waterschap-aa-en-maas_sewage_2019\sewer_data\' 

Output: '..._overall.csv' data file placed in each data folder
"""
folder_names = ['RG8150/RG8150', 'RG8170/RG8170', 'rg8170_99', 
                'rg8170_N99', 'RG8180_L0', 'RG8180_Q0']

import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

for folder in folder_names:
    
    df = pd.DataFrame()
    
    path = current_dir + '/' + folder
    
    for file in os.listdir(path):
        if 'overall' not in file:
            print('merging file: ' + file)
            df_temp = pd.read_csv(path + '/' + file, 
                                  error_bad_lines=False, sep=';')
            df = pd.concat([df, df_temp])
    
    df.to_csv(path + '/' + folder + '_overall.csv', index=False, sep=';')
