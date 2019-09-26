""" 

Requires 'full_data.csv' in the same folder as the current Python file. 

"""

########################### SETTINGS ##########################################
import warnings
import time

import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')

import os
import pandas as pd
from statsmodels.tsa.arima_model import ARMA
import matplotlib
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

current_dir = os.path.dirname(os.path.abspath(__file__))

########## DATA IMPORT - ONLY RUN ONCE - LONG RUNNING TIME ####################

print('importing data...')

time_start = time.time()

df = pd.read_csv(current_dir +  '/full_data.csv')

print('importing finished. Time: {}'.format(str(time.time() - time_start)))

pump_stations = list(df['pump_station'].unique())
data_column_names = df.columns

pump_station_choice = input('Select a pump: \n{} \n'
                            .format(', '
                                    .join(str(e) for e in pump_stations)))

df = df[(df['pump_station'] == pump_station_choice)]

measurement_types = list(df['measurement_type'].unique())
measurement_type_choice = input('Select a measurement type: \n {} \n'
                            .format(', '
                                    .join(str(e) for e in measurement_types)))

df = df[(df['measurement_type'] == measurement_type_choice)]

df['measurement_begin'] = pd.to_datetime(df['measurement_begin'])

print('Data filtered. \n \nDate range: {} to {}.'
      .format(str(df['measurement_begin'].min()), 
              str(df['measurement_begin'].max())))

df = df[['measurement_begin', 'measurement_type', 'interval', 'pump_station',
         'value']]

df = df.set_index('measurement_begin')

###############################################################################

time_start = time.time()

y = df['value'].resample('3H').mean()

y = y.fillna(method='ffill')

y.to_csv('Export {} {}.csv'
         .format(pump_station_choice, measurement_type_choice))

# =============================================================================
# print('Fitting model...')
# 
# model = ARMA(y, order=(24, 1))
# 
# print('Part 1 done')
# 
# model_fit = model.fit(disp=0)
# 
# print(model_fit.summary())
# 
# print('Running time: {}'.format(str(time.time() - time_start)))
# =============================================================================
