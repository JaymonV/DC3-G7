    o# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 10:38:02 2019

@author: Jaymon

Script used for merging the csv files in data folders. Supported:
    - sewer_data
    - wwtp flow

Preparation: (1) unzip the data folders, (2) place this file in the folder for:
  sewer_data      - 'waterschap-aa-en-maas_sewage_2019\sewer_data\' 
  wwtp flow       - 'waterschap-aa-en-maas_sewage_2019_db_pumps\sewer_data_db\
                      data_wwtp_flow'
  data_pump_flow  - 'waterschap-aa-en-maas_sewage_2019_db_pumps\sewer_data_db\
                     data_pump_flow'
  rain_timeseries - 'waterschap-aa-en-maas_sewage_2019\sewer_data'

Output: '..._overall.csv' data file placed in each data folder
"""

# Folders currently supported
folder_names = ['RG8150/RG8150', 'RG8170/RG8170', 'rg8170_99', 
                'rg8170_N99', 'RG8180_L0', 'RG8180_Q0', 
                'RG1876_flow', 'RG1882_flow', '1210FIT201_99',
                '1210FIT301_99', '1210FIT401_94', '1210FIT501_99',
                'rain_timeseries']

import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

# Binary value; set to 1 if the script fails (useful for debug)
script_test = 0

for folder in folder_names:
    
    df = pd.DataFrame()
    
    folder_path = current_dir + '/' + folder
    
    if os.path.exists(folder_path):
        
        script_test = 1
        
        for file in os.listdir(folder_path):
            # Skip the overall files already created, to prevent duplicate
            # data.
            if 'overall' not in file:
                print('merging file: ' + file)
                df_temp = pd.read_csv(folder_path + '/' + file, 
                                      error_bad_lines=False, sep=None)
                df = pd.concat([df, df_temp])

    try:
        df.to_csv(folder_path + '/' + folder + '_overall.csv', 
                  index=False, 
                  sep=';')
    
    except:
        pass

if script_test != 1:
    print('No folder with data found to extract. Check script file location.')
    
else:
    print('Merge succesful.')
