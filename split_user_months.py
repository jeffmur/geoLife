import pandas as pd
import preprocess as pre 
import heatmap as hp
import glob
from pathlib import Path
import os

# TODO: add header & combine split files

directoryInput = '/home/jeffmur/dev/privamov/data/gps_all_user_month/'
output_dir = Path('/home/jeffmur/dev/privamov/data/user_by_month/')
gps_header = ['ID', 'Date', 'Time', 'Longitude', 'Latitude']

# Make dir if does NOT exist
if(not (os.path.isdir(output_dir))):
    output_dir.mkdir()

all_files = glob.glob(directoryInput+'*')

for path in all_files:
    print(path)
    fileName = hp.parse4Date(path)
    monthDF = pd.read_csv(path, names=gps_header)
    # monthDF.head()

    # Number of Users in Month File
    numOfUsers = len(pd.unique(monthDF['ID']))

    # Group by ID
    grouped = monthDF.groupby(monthDF['ID'])

    # Write each user group to monthFile in sub dir
    for userName, group in grouped:
        user_dir = output_dir / Path(str(userName))

        group = group.reset_index().drop('index', axis=1)

        # Make dir if does NOT exist
        if(not (os.path.isdir(user_dir))):
            user_dir.mkdir()
        #print(name)
        group.to_csv(f'{user_dir}/{fileName}.csv')