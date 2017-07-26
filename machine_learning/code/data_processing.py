import csv
import glob
import os.path
import pandas as pd

pop_struct = pd.read_csv('pop_structure.csv')
file1 = pd.read_csv('Sutherland2016.csv')
file2 = pd.read_csv('Rosthern2016.csv')
file3 = pd.read_csv('Nepal2016.csv')
file4 = pd.read_csv('Sutherland2017.csv')
file5 = pd.read_csv('Rosthern2017.csv')

#pop_struct.set_index('Entry',inplace=True)
#sutherland.set_index('Entry',inplace=True)

joined = pd.concat([file1,file2,file4,file5])
print(joined)
joined.to_csv('all_data_canada.csv', index=False)


