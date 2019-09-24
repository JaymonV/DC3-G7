import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

print('importing data...')
df = pd.read_csv(current_dir +  '/full_data.csv')

print('importing finished.')
