# Get all of the user files in split by month output
import os
from pathlib import Path
from numpy.core.fromnumeric import sort
import pandas as pd
import numpy as np


currentDir = os.getcwd()

def getUserDir(name):
    '''Requires split_by_month_output/'''
    dataDir = os.path.join(currentDir, f'split_by_month_output/{name}')
    parseDir = Path(dataDir).rglob('*.csv')
    all = sorted(parseDir, key=lambda i: os.path.splitext(os.path.basename(i))[0])
    files = [x for x in all]
    return files
    
def dataSetup(all_files):    
    dfs = [pd.read_table(f, sep = ",", names=['Latitude', 'Longitude', 'Zero', 'Altitude', 'Num of Days', 'Date', 'Time']) for f in all_files]
    raw_concat = pd.concat(dfs, ignore_index=True)
    raw_concat = raw_concat.drop(['Num of Days','Zero'], axis=1)
    return raw_concat
    
def dropNAN(raw):
    df = raw
    df = df.replace(0, np.nan)
    df = df.dropna(how='all', axis=0)
    df = df.replace(np.nan, 0)
    return df

def oneMonth(file):
    '''Requires split_by_month_output/'''
    df = pd.read_csv(file, sep = ",", names=['Latitude', 'Longitude', 'Zero', 'Altitude', 'Num of Days', 'Date', 'Time'])
    return dropNAN(df)

def wholeDirectoryToDF(folderDirectory):
    files = getUserDir(folderDirectory)
    raw_data = dataSetup(files)
    return dropNAN(raw_data)