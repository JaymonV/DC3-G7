# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 10:38:02 2019

@author: Jaymon

Script used for merging the csv files in data folders. Supported:
    - sewer_data
    - wwtp flow

Preparation: (1) unzip the data folders, (2) place this file in the folder for:
    sewer_data - 'waterschap-aa-en-maas_sewage_2019\sewer_data\' 
    wwtp flow  - 'waterschap-aa-en-maas_sewage_2019_db_pumps\sewer_data_db\
                  data_wwtp_flow'

  (3) Define list of folders (folder names variable) for:
    sewer_data - ['RG8150/RG8150', 'RG8170/RG8170', 'rg8170_99', 
                'rg8170_N99', 'RG8180_L0', 'RG8180_Q0']
    wwtp flow - ['RG1876_flow', 'RG1882_flow']

Output: '..._overall.csv' data file placed in each data folder
"""

folder_names = ['RG8150/RG8150', 'RG8170/RG8170', 'rg8170_99', 
                'rg8170_N99', 'RG8180_L0', 'RG8180_Q0', 
                'RG1876_flow', 'RG1882_flow']

import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

for folder in folder_names:
    
    df = pd.DataFrame()
    
    folder_path = current_dir + '/' + folder
    
    script_test = 0
    
    if os.path.exists(folder_path):
        
        script_test = 1
        
        for file in os.listdir(folder_path):
            if 'overall' not in file:
                print('merging file: ' + file)
                df_temp = pd.read_csv(folder_path + '/' + file, 
                                      error_bad_lines=False, sep=';')
                df = pd.concat([df, df_temp])

    try:
        df.to_csv(folder_path + '/' + folder + '_overall.csv', index=False, sep=';')
    
    except:
        pass

if script_test != 1:
    print('No folder with data found to extract. Check script file location.')
    
else:
    print('Merge succesful.')